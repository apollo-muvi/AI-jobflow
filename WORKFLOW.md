# CramAI 開發團隊工作流程 v1.0

> 最後更新：2026-06-22
> 適用範圍：Idea3（主力）、Pi4、Air13 三機協作

---

## 一、角色定義

| 角色 | 代號 | 職責 | 權限 |
|------|------|------|------|
| **創辦人** | @apollo | 產品方向決策、最終批准、客戶溝通 | 所有 |
| **🧠 CEO** | Hermes (on Idea3) | 產品規劃、任務分解、派活、品質把關、資源調度 | Kanban管理、Delegate、確認關卡 |
| **👨‍💻 Coder** | Claude Sonnet 4 | 照 Implementation Plan 寫 code、修 bug | 僅接 CEO 任務 |
| **🤖 Assist Coder** | Gemini 3.1 Flash-Lite | 協助 CEO 寫 code、debug、驗證 bug | 僅接 CEO 任務 |
| **🔍 Reviewer** | o4-mini | Code review、Implementation drift 檢查 | 審查 Coder / Assist Coder 產出 |
| **🧪 QA** | deepseek / Claude | E2E 測試、功能驗證、Deploy、文件手冊 | 測試、出報告 |

### 三機分工

| 機器 | 角色 | 用途 |
|------|------|------|
| **Idea3** (24GB) | 🧠 CEO + 開發除錯 | 主力開發、Kanban、LLM API |
| **小p** (4GB + 512GB SSD) | 🚀 Deployer | 常開不關機、部署CramAI服務、Cloudflare Tunnel、備份、監控 |
| **Air13** (4GB) | 🧪 QA（備用） | 不常用，QA 暫代其 Reviewer 職責 |
| **小a** (Air13) | 🎲 機動支援 | 不常在線，忙時才支援 |

---

## 二、版號規則

### Dev 階段

```
0.1 → 0.2 → 0.3 → ...（每完成一個 task +0.1）
```

- 每次 Coder push 到 main 前，bump VERSION 檔案
- 放在 `~/CramAI/VERSION`，僅含版號數字

### Release 階段（產品交付客戶）

```
1.0 → 1.1 → 1.2 → ...（每個正式版本 +0.1）
```

- 僅 CEO（@apollo 或 CEO Agent）決定何時進 release

### GA（General Availability）

```
1.0GA
```

- 客戶正式交付版
- 在 GitHub 上打 tag：`git tag v1.0GA`

---

## 三、完整開發流程

```
🧠 CEO 開 Kanban Ticket
    │
    ▼
👨‍💻 Coder 接任務 → 實作
    │
    ├─ 修正 3 次內成功? ──→ 🧪 QA 驗證
    │       │                   │
    │       │              ┌────┴────┐
    │       │              │         │
    │       │           ✅ PASS    ❌ FAIL
    │       │              │         │
    │       │              │    ← 回 Coder（計 iteration）
    │       │              │       若 iteration=3 → 停，回報 CEO
    │       │              │
    │       │              ▼
    │       │         🧠 CEO 確認
    │       │              │
    │       │              ▼
    │       │         👨‍💻 Coder git push + tag
    │       │         bump VERSION
    │       │         hermes kanban complete
    │       │
    └── ❌ 第 3 次 iteration 未過
              │
              ▼
         🧠 CEO 向 @apollo 匯報
              │
              ▼
         @apollo 決定：換人 / 換方案 / 擱置
```

### 3-Iteration 終止規則

| Iteration | 狀態 | 行動 |
|:---------:|:----:|------|
| 1 | Coder 送 QA | 正常驗證 |
| 2 | QA 打回第 2 次 | 正常回 Coder |
| 3 | QA 打回第 3 次 | **強制停止**，Coder 不準再修。QA 發 ticket 給 CEO |
| — | CEO 收到停止通知 | 向 @apollo 匯報，由創辦人決定下一步 |

**如何計算 iteration：** 在 Kanban 上看 comment 次數。

```
hermes kanban show t_xxxxx
  ● Coder v1: 送 QA                             ← 1
  ● QA v1: ❌ 原因...
  ● Coder v2: 修正，送 QA                       ← 2
  ● QA v2: ❌ 原因...
  ● Coder v3: 修正，送 QA                       ← 3 ← STOP
  ● QA v3: ❌ 第 3 次未過 → 通報 CEO
```

---

## 四、Kanban 操作規範

### 開票格式

```
hermes kanban create "0.1 — 任務名稱" --body "
## 規格
[需求描述]

## 版號
當前: 0.1 | 目標: 0.2

## 預估工時
Coder: X hrs | QA: Y hrs

## 簽核流程
Coder → QA（出報告）→ CEO確認 → Coder push

## 相關檔案
[檔案路徑]
"
```

### 狀態流轉

| 狀態 | 觸發 | 含義 |
|------|------|------|
| `ready` | CEO create 或 promote | 任務就緒，等待 Coder |
| `running` | CEO delegate_task | Coder 正在工作 |
| `blocked` | Coder 完成後 block | 等待 QA 驗證 |
| `blocked` (with comment) | QA 打回 | 回 Coder 重做，iteration +1 |
| `done` | CEO complete | 任務結束 |

### 常用指令

```bash
# 看 board
hermes kanban ls

# 看單一 ticket 完整記錄（含所有 comment + 事件）
hermes kanban show t_xxxxx

# 看 worker log（Coder 的執行記錄）
hermes kanban log t_xxxxx

# 加 comment（追蹤進度用）
hermes kanban comment t_xxxxx "Coder v1: 送 QA"

# 完成任務
hermes kanban complete t_xxxxx
```

---

## 五、QA 測試報告規範

QA 每次驗證後必須產出測試報告，存到 `~/CramAI/tests/`。

### 檔名格式

```
驗證報告_YYYY-MM-DD_ticket-t_xxxxx.md
```

### 報告模板

```markdown
# QA 測試報告

## 基本資訊
- **Ticket:** t_xxxxx
- **版號:** 0.1
- **測試日期:** 2026-06-22
- **測試人員:** QA Agent
- **Iteration:** v1

## 測試目標
[一句話說明這個 ticket 在測什麼]

## 測試方法
1. [步驟 1]
2. [步驟 2]
3. ...

## 測試環境
- Backend: localhost:8000
- LLM: OpenRouter deepseek v4 flash
- Qdrant: localhost:6333
- 知識庫: cram_school_rag_knowledge_base.pdf

## 測試結果

### Case 1: [測試案例名稱]
- **輸入:** [輸入內容]
- **預期:** [預期結果]
- **實際:** [實際結果]
- **判定:** ✅ PASS / ❌ FAIL

### Case 2: ...
...

## 結論
- **判定:** ✅ PASS / ❌ FAIL
- **Iteration 計數:** v1 / v2 / v3
- **備註:** [其他注意事項]
```

---

## 六、Git 操作規範

### 分支策略

```
main ← 只有 CEO 可合併
  └── feat/... ← Coder 開發分支
```

### Push 條件

僅在 QA **PASS** 且 **CEO 確認**後，Coder 才能 push：

```bash
# Coder push 前先 bump 版號
echo "0.2" > ~/CramAI/VERSION

# 修改 backend/app/__init__.py 或 main.py 中的 version

git add -A
git commit -m "0.2 — 修復 LINE Bot 簽章驗證"
git push origin main
git tag v0.2
git push origin v0.2
```

### 不同客戶分支（未來）

```
main
  └── client/zhuoyue    ← 卓越補習班專屬設定
  └── client/mingren     ← 明仁補習班專屬設定
```

---

## 七、安全規則（Credential 管理）

開發與部署流程中，所有 API Key、Token、Secret 必須遵守以下規則：

1. **零硬編碼原則** — 任何 credential 不得直接寫在 .py / .yaml / .json / .toml 原始碼中
2. **強制環境變數** — 所有敏感值必須從 `.env`（開發）或系統環境變數（生產）讀取
3. **．env 隔離** — `.env` 已加入 `.gitignore`，永不被 git 追蹤。新增.env.\* 檔案時務必檢查
4. **密碼掃描** — 每次 commit 前建議執行 `git diff HEAD` 確認無 credential 混入
5. **GitGuardian** — 若 GitGuardian 偵測到外洩，立刻撤銷受影響的 credential 並更新

---

## 八、不同機器協作注意事項

| 機器 | 負責事項 | 注意 |
|------|---------|------|
| **Idea3** (CEO) | 開 ticket、派活、Kanban 管理 | 始終在 idea3 上操作 |
| **Pi4** (Coder/QA) | 接收 delegated task | Pi4 不需登入 Hermes，透過 delegate_task 取得任務 |
| **Air13** (Reviewer/QA) | 接收 delegated task | 同上 |

- Kanban DB 在 idea3 上，所有狀態以 idea3 為準
- delegated task 時在 context 標註 `ticket:t_xxxxx`
- 測試報告統一存到 idea3 的 `~/CramAI/tests/`

---

## 九、緊急中斷規則

如果開發過程中發生以下情況，Coder/QA 必須立即暫停並通知 CEO：

1. **同 bug 修復 3 次未過** → 強制停止，CEO 匯報 @apollo
2. **發現重大安全漏洞** → 立即通報
3. **客戶需求變更** → 暫停當前工作，等 CEO 重新規劃
4. **任何需要決策的模糊點** → 停，問 CEO，不自己猜

---

*本文件由 🧠 CEO Agent 建立，如有修改需求請告知。*