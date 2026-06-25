# TeamAI 開發日誌

> CramAI — 補習班 AI 客服 SaaS
> 每日不定期更新，記錄開發進度、待辦事項、已知問題

---

## 2026-06-24

### 本日進展（延續）

| 項目 | 狀態 | 說明 |
|------|:----:|------|
| Hub client.py ACK 迴圈 bug | ✅ 已修 | 防止 CEO 機器自我回覆形成 ∞ 迴圈 |
| 團隊架構圖更新 | ✅ | drawio 版本，含 創辦人→CEO→Coder/小陳/Reviewer/QA→小p Deployer |
| 小p正式指定為 Deployer | ✅ | 角色: Docker build + CI/CD + Cloudflare Tunnel + 監控備份 + Deployment Checklist |
| OpsQA-prompt.md 更新 | ✅ | 移除佈署上線職責（改小p負責） |
| WORKFLOW.md 更新 | ✅ | 新增小p Deployer 角色列，移除 Air13 QA 備用職 |
| Agent Team skill 更新 | ✅ | ai-agent-team-architecture 加入 小陳/小p/Deployer |
| 小陳 Demo bugs 修復 | ✅ | branch: fix/clear-mobile-upload (commit 7c4912c) |
| 清除對話按鈕 | ✅ | 小陳實作，上傳文件後 Q&A 區出現 🗑️ 按鈕 |
| 手機上傳修復 | ✅ | upload-zone 改 `<label>` 包裹，iOS Safari 可觸發檔案選擇 |
| client.py 修復部署 | ✅ | CEO client 重啟 (PID 70421) |
| 小p 正式任務 #001 | ⏳ 進行中 | QA 驗證 + Deploy（限 30 分鐘逐條回報） |

### ⚙️ 團隊架構（更新）

```
                 👑 創辦人 @apollo
                        │
                   🧠 CEO (deepseek v4 flash)
                   brainstorm + 拆需求 + 派活
                  ┌──────┬──────┬──────┐
                  │      │      │      │
          👨‍💻 Coder  🔍 Reviewer  🧪 QA/Ops
          Claude     o4-mini     deepseek/Claude
          Sonnet 4   code review E2E測試+文件
              │
          🤖 小陳
          (Assist Coder, Gemini 3.1 FL)
          寫code/debug/驗證
                  │
              🚀 小p (Pi4) — Deployer
              Docker build + CI/CD + Tunnel
              Deployment Checklist + 監控備份
```

### 角色對照表

| 角色 | 模型/機器 | 職責 |
|------|----------|------|
| 🧠 CEO | deepseek v4 flash (idea3) | Brainstorm + 拆任務 + 派活 + 最終簽核 |
| 👨‍💻 Coder | Claude Sonnet 4 | 照 Implementation Plan 寫 code |
| 🤖 小陳 (Assist Coder) | Gemini 3.1 Flash-Lite | 協助寫 code、debug、驗證 bug |
| 🔍 Reviewer | o4-mini | Code review、Implementation drift 檢查 |
| 🧪 QA/Ops | deepseek/Claude (delegate_task) | E2E 測試、Test Report、文件手冊 |
| 🚀 小p | Pi4 (4GB + 512GB SSD) | Docker build + 部署、CI/CD、Tunnel、監控 |

### 目前待完成

| 優先 | 項目 | 負責 | 狀態 |
|:----:|------|:----:|:----:|
| 🔴 1 | 小p 執行 QA 驗證 + Deploy (Demo bugs) | 小p | ⏳ 限30分 |
| 🟡 2 | Demo 頁面 mobile 上傳驗證 | QA/小p | ⏳ |
| 🟡 3 | 建立正式 QA 員工（非小p暫代） | CEO | 📋 待安排 |
| 🟢 4 | client.py Pi4 端更新（同步修復） | 小p | ⏳ 等上線 |

---

## 2026-06-23

### 團隊基礎建設
- ✅ 群組 TeamAI (chat_id: -5333195749) 環境確認
- ✅ 小p (Pi4 @Rain425bot) gateway 重啟恢復回應
- ✅ 發現 idea3 與 Pi4 共用 bot token 導致的 polling conflict
- ✅ 跨機協作流程實際驗證
- ✅ 建立 docs/小p-任務.md 任務看板
- ✅ 建立 GitHub Issue #1 (小p 工作說明)

### 前端修復
- ✅ API prefix /api/v1/ → /api/ 統一
- ✅ Gmail reply 中文寄件者修復 (Invalid To header)

---

## 2026-06-22

- ✅ Credential 安全修復 (LINE Secret/Token 移至 .env)
- ✅ 驗證報告完成 (security fix)
- ✅ RAG 文件防重複索引機制
- ✅ LINE QR Code 更新

---

## 2026-06-21

- ✅ 專案架構討論與定案
- ✅ 四角色 Agent Team 團隊架構設計 (CEO/Coder/Reviewer/OpsQA)
- ✅ PRD 建立 (補習班 AI 客服 SaaS)
- ✅ Implementation Plan 建立 (9 tasks, 5 phases)
- ❌ 嘗試 RAG end-to-end 測試，因 API key 寫入問題中斷

---

## 2026-06-20

- ✅ 專案目錄 ~/CramAI/ 建立
- ✅ Docker Compose 設定 (Qdrant + Backend + Frontend)
- ✅ Phase 1 Foundation 程式碼完成
  - 資料模型 (Tenant/Conversation/Document)
  - RAG Engine (Qdrant + OpenRouter)
  - 文件解析器 (PDF/DOCX/TXT)
  - 文件上傳 API
- ✅ 16 個 Python 檔案語法檢查通過
- ✅ Qdrant 容器啟動成功

---