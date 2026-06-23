import subprocess, json, time, os, sys

HUB_URL = os.environ.get("HUB_URL", "http://192.168.20.154:8765")
MACHINE = os.environ.get("MACHINE_NAME", "小p")

# Exponential backoff: 30s → 5min → 10min → 30min → 60min → stop
INTERVALS = [30, 300, 600, 1800, 3600]
fail_count = 0

while True:
    try:
        r = subprocess.run(
            ["curl", "-s", f"{HUB_URL}/poll/{MACHINE}"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0:
            fail_count = 0  # reset on success
            msgs = json.loads(r.stdout)
            if msgs:
                for m in msgs:
                    print(f"[通知] 來自 {m['from_who']}: {m['text']}")
                    subprocess.run(
                        ["curl", "-s", "-X", "POST", f"{HUB_URL}/ack/{m['id']}"],
                        capture_output=True
                    )
        else:
            raise Exception(r.stderr)
    except Exception as e:
        fail_count += 1
        if fail_count >= len(INTERVALS):
            print(f"[停止] 機器 {MACHINE} 持續離線，停止輪詢")
            sys.exit(0)
        interval = INTERVALS[fail_count]
        print(f"[離線] 無法連線（第{fail_count}次），{interval}秒後重試")
        time.sleep(interval)
        continue

    time.sleep(INTERVALS[0])  # normal: 30s