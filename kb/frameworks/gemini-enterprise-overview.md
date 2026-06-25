# Gemini Enterprise 參考資料

> 收集日期：2026-06-21
> 來源：使用者口述整理
> 用途：作為未來方案比較的對照組

---

## 版本定位

Google Workspace Business 版本的 Gemini Enterprise（非 Vertex AI 路線）。

---

## 三大核心功能

### 1. 代理平台與開發工具 (Agent Platform)

| 功能 | 說明 |
|------|------|
| Agent Designer | 無程式碼（No-Code）拖放設計器，員工用自然語言建立自訂代理 |
| Agent Development Kit (ADK) | 專業開發者工具包，支援複雜邏輯、Skills、CI/CD 整合 |

### 2. 數據連接與 Agentic RAG

| 功能 | 說明 |
|------|------|
| 多代理協同 | Orchestrator + Planner + Sufficient Context Agent |
| Agentic RAG | 不是單次搜尋，而是跨多數據源（Google Workspace、M365、Jira、Salesforce）的多步驟循環式研究 |
| 數據連接器 | 專用 Data Connectors 打破數據孤島 |

#### 關鍵角色對照

| Gemini | 對應 | 說明 |
|--------|------|------|
| Orchestrator | 🧠 CEO | 統籌、分配任務 |
| Planner | 🧠 CEO | 拆 PRD → Implementation Plan |
| Sufficient Context Agent | 🧪 Ops & QA | 驗證是否夠好可上線 |
| Workers | 👨‍💻 Coder + 🔍 Reviewer | 執行 + 審查 |

### 3. 預建企業級代理

| 代理 | 用途 |
|------|------|
| NotebookLM Enterprise | 企業內部知識庫理解與筆記工具 |
| Deep Research | 商業課題深度市場研究 |
| Gemini Code Assist Standard | 開發者 AI 編碼輔助（自動化測試、分析、重構） |

---

## 對比我們的方案

| 維度 | Gemini Enterprise | 我們的方案 |
|------|------------------|-----------|
| 部署 | Google Cloud | 私有化（客戶環境 / 客戶選擇的雲端）|
| 資料 | 送 Google | 不外流 |
| 模型 | Gemini 系列 | Qwen3 / Llama / DeepSeek |
| 平台鎖定 | 綁 Google Workspace | 無平台鎖定 |
| No-Code builder | Agent Designer | 可透過 Dify / n8n 達成類似效果 |
| 專業開發 | ADK | Hermes Skills + MCP |
| 預建代理 | NotebookLM / Deep Research | 視客戶需求客製 |

---

## 商業機會

我們的定位：**私有的 Gemini Enterprise 替代方案**

客戶不想把資料送 Google → 我們的私有化方案就是最佳選項。