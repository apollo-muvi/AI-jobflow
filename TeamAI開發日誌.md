# TeamAI 開發日誌

> CramAI — 補習班 AI 客服 SaaS
> 每日不定期更新，記錄開發進度、待辦事項、已知問題

---

## 2026-06-24

### 專案基本盤

| 項目 | 內容 |
|------|------|
| Repo | github.com/apollo-muvi/cram_service |
| 本機路徑 | ~/CramAI/ |
| Branch | **main** (Qdrant), **pinecone** (Pinecone Serverless) |
| Domain | cramai.rain0425.com |
| 最新 commit | `e5accaf` fix: API prefix /api/v1/ → /api/ |
| GitHub Issues | 1 個 open (#1 小p 工作說明) |

---

### ✅ 已完成 (v0.7)

**Phase 1 — Foundation**
- FastAPI 後端骨架 + 資料模型 (Tenant/Conversation/Document)
- RAG Engine (Qdrant + OpenRouter Qwen3 Embedding)
- 文件解析 (PDF/DOCX/TXT/MD)
- Docker Compose (Qdrant + Backend + Frontend)

**Phase 2 — LINE Bot**
- webhook_line.py — LINE Messaging API 整合
- 簽章驗證、自動回覆

**Phase 3 — Email**
- gmail_service.py — Gmail API 輪詢 + Plus Addressing
- RAG 自動回覆郵件
- 中文寄件者修復

**Phase 4 — Admin Dashboard**
- React + Vite + TypeScript 前端
- Demo 頁面 (檔案上傳 + Q&A 測試)
- 對話紀錄、FAQ 管理、Settings 面板
- Loading spinner、auto-scroll、.md 上傳支援

**QA 驗證**
- ✅ Credential 硬編碼安全修復 (2026-06-22)
- ✅ UX 優化驗證：spinner + auto-scroll (2026-06-23)
- ✅ Gmail reply 中文寄件者修復驗證 (2026-06-23)
- ✅ RAG 基本測試：PDF 上傳 + 問答回覆 (2026-06-22)
- ✅ API prefix 標準化 (/api/v1/ → /api/)
- ✅ 產品使用手冊 v0.7

---

### ⏳ 待完成 / 已知問題

| # | 項目 | 狀態 | 說明 |
|---|------|:----:|------|
| 1 | **.env API key 失效** | ❌ 卡住 | OPENROUTER_API_KEY 被系統 redaction 遮罩，需重寫有效 key |
| 2 | **Backend 未啟動** | ❌ | Docker backend container not running (port 8000) |
| 3 | **Frontend 未啟動** | ❌ | Docker frontend container not running (port 3000) |
| 4 | **RAG end-to-end 驗證** | ❌ 未完成 | 6/21 跑到一半因 API key 中斷，從未真正驗證完整 pipeline |
| 5 | **cramai.rain0425.com 運作確認** | ❌ 未驗證 | 需小p確認 Cloudflare Tunnel + 服務是否正常 |
| 6 | **GitHub Issue #1** | 📄 待回覆 | 小p 工作說明，尚未回覆「確認理解」 |
| 7 | **小p 自動 pull 機制** | ⏳ 待辦 | crontab 定時 pull pinecone branch + 重啟 |

---

### 小p 任務看板

| 狀態 | 任務 | 說明 |
|:----:|------|------|
| 🔄 進行中 | 讀取 WORKFLOW.md | 到 AI-jobflow repo 讀完整流程，理解後回覆 CEO |
| ⏳ 待辦 | 確認 cramai.rain0425.com 運作 | 確保服務正常運行 |
| ⏳ 待辦 | 設定自動 pull 機制 | crontab 定時 pull + 重啟 |

---

### 技術細節

#### 運行中服務
| 服務 | 狀態 | Port |
|------|:----:|:----:|
| Qdrant (向量庫) | ✅ 運行中 | 6333 |
| Backend (FastAPI) | ❌ 未啟動 | 8000 |
| Frontend (React) | ❌ 未啟動 | 3000 |

#### .env 現狀
- OPENROUTER_API_KEY=*** (被遮罩，長度/可用性不明)
- GEMINI_API_KEY=*** (小陳 Gemini，被遮罩)
- GOOGLE_API_KEY=*** (被遮罩)

#### 主要障礙
唯一瓶頸：**寫入有效的 OpenRouter API key** → 啟動 backend/frontend → 執行 RAG end-to-end 驗證 → 確認 cramai.rain0425.com 上線。API key 解決前，其他項目均無法推進。

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