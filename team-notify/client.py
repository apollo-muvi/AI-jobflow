#!/usr/bin/env python3
"""
Client 通知接收端 — 跑在各機器上
每 30 秒輪詢 Hub，有新通知就 print 到 stdout
"""
import os
import sys
import time
import json
import socket
import urllib.request
import urllib.error

HUB_URL = os.environ.get("HUB_URL", "http://localhost:8765")
MACHINE_NAME = os.environ.get("MACHINE_NAME", socket.gethostname())
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "30"))


def log(msg: str):
    """帶時間戳的日誌輸出（到 stderr，不干擾通知輸出）"""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", file=sys.stderr, flush=True)


def poll_notifications() -> list[dict]:
    """向 Hub 輪詢未讀通知"""
    url = f"{HUB_URL}/poll/{MACHINE_NAME}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data if isinstance(data, list) else []
    except urllib.error.HTTPError as e:
        if e.code == 404:
            log(f"⚠️ Hub 無此機器「{MACHINE_NAME}」")
        else:
            log(f"⚠️ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        return []
    except urllib.error.URLError as e:
        log(f"⚠️ 無法連線 Hub ({HUB_URL}): {e.reason}")
        return []
    except (json.JSONDecodeError, ConnectionError, TimeoutError) as e:
        log(f"⚠️ 連線異常: {e}")
        return []


def ack_message(msg_id: int) -> bool:
    """向 Hub 確認已讀"""
    url = f"{HUB_URL}/ack/{msg_id}"
    try:
        req = urllib.request.Request(url, method="POST", data=b"")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.getcode() == 200
    except Exception as e:
        log(f"⚠️ 標記已讀失敗 (msg_id={msg_id}): {e}")
        return False


def main():
    log(f"📡 通知用戶端啟動")
    log(f"   機器名稱: {MACHINE_NAME}")
    log(f"   Hub 位址: {HUB_URL}")
    log(f"   輪詢間隔: {POLL_INTERVAL} 秒")
    log("   — 按 Ctrl+C 停止 —")
    log(f"{'─' * 50}")

    while True:
        try:
            messages = poll_notifications()
            for msg in messages:
                # 輸出到 stdout — Hermes 或其他監控程式可讀取
                print(json.dumps({
                    "type": "notification",
                    "id": msg.get("id"),
                    "from": msg.get("from_who", "?"),
                    "text": msg.get("text", ""),
                    "time": msg.get("created_at", ""),
                }, ensure_ascii=False))
                sys.stdout.flush()

                # 自動標記已讀
                msg_id = msg.get("id")
                if msg_id is not None:
                    ack_message(msg_id)

            if messages:
                log(f"✅ 收到 {len(messages)} 則新通知，已標記已讀")

        except KeyboardInterrupt:
            log("👋 用戶端停止")
            break
        except Exception as e:
            log(f"❌ 未預期錯誤: {e}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()