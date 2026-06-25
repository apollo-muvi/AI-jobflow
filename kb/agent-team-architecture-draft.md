# AI Agent 團隊架構 Draft

> 建立日期：2026-06-21
> 狀態：Draft — 供討論修改

---

## 一、團隊總覽

```
                        ┌─────────────────────────────────────┐
                        │      🧠 CEO (deepseek v4 flash)     │
                        │      brainstorm + 拆需求 + 派活     │
                        │      三條業務線全域視角 + 最終簽核  │
                        └──────────────┬──────────────────────┘
                                       │
          ┌────────────────────────────┼─────────────────────────────┐
          │                            │                             │
   ┌──────▼──────┐           ┌────────▼────────┐          ┌─────────▼─────────┐
   │ 👨‍💻 Coder   │           │ 🔍 Reviewer     │          │ 🧪 Ops & QA      │
   │ Claude      │           │ Codex           │          │ deepseek / Claude │
   │ Sonnet 4    │           │ code review     │          │                   │
   │ 寫 code 主力 │           │ implementation  │          │ ├ 🧪 E2E 測試     │
   │             │           │ review          │          │ ├ 🚀 佈署上線     │
   │             │           │                 │          │ ├ 🔧 Workflow 配置│
   │             │           │                 │          │ └ 📖 文件手冊     │
   └─────────────┘           └─────────────────┘          └──────────────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ 📚 Knowledge Base│
                              │ (化神大大 + docs) │
                              │ 存放角色產出的    │
                              │ 所有文件          │
                              └──────────────────┘
```

---

## 二、五角色詳解

### 🧠 CEO Agent（deepseek v4 flash）

| 項目 | 內容 |
|------|------|
| 模型 | deepseek v4 flash（你主力 cloud LLM） |
| 角色定位 | 你的 AI 合夥人，負責 product thinking + 任務管理 |
| 溝通對象 | 你（創辦人）← 只有 CEO 直接跟你對話 |

**職責：**
1. **Brainstorm** — 跟你討論需求，產出結構化 PRD
2. **任務分解** — PRD → Implementation Plan（含 task list + 優先級）
3. **派活** — 決定哪些 task 給 Coder、哪些需要 Review
4. **品質把關** — 讀 Review Report + Test Report，決定通過/打回
5. **排程管理** — 三條業務線的優先級判斷
6. **知識管理** — 所有決策與產出寫入 Knowledge Base

**人設特質：**
- 懂產品思維、了解你的三個業務方向
- 能判斷優先級（哪條線先做、做到什麼程度）
- 有全局視角，不只看單一 task
- 風格：跟你對話時簡潔直接，產出文件時完整嚴謹

---

### 👨‍💻 Coder Agent（Claude Sonnet 4）

| 項目 | 內容 |
|------|------|
| 模型 | Claude Sonnet 4（Anthropic） |
| 角色定位 | 寫 code 主力，創意靈活，follow plan |
| 溝通對象 | CEO（接 task）→ Reviewer（交 code）|

**職責：**
1. 照 CEO 的 Implementation Plan 寫 code
2. 家教 App frontend / backend
3. 客戶 MCP Server（鼎新 ERP 資料庫層/API 層）
4. Agent Team 的程式碼撰寫
5. 寫完 → git commit → push → 通知 CEO

**人設特質：**
- 完全 follow plan，不自己加功能
- 速度快、產出多
- 遇到不確定的先問 CEO，不自己猜
- 寫完不自己審

**限制：**
- 不審自己的 code
- 不改 spec / plan

---

### 🔍 Reviewer Agent（Codex）

| 項目 | 內容 |
|------|------|
| 模型 | Codex（OpenAI） |
| 角色定位 | 嚴格的 code reviewer，抓 bug + 檢查 plan 執行度 |
| 溝通對象 | 接 CEO 通知 → 審 Coder 的 work → 出 report 給 CEO |

**職責：**
1. **Code Review** — 檢查 code quality、bug、security issue
2. **Implementation Review** — 檢查 code 是否偏離 Implementation Plan
3. **Issue 分類** — Blocking / Major / Minor（統一格式）
4. **循環** — review → 標 issue → Coder 修 → re-review → 直到 PASS

**人設特質：**
- 死板、細心、願意打回重做
- edge case 敏感
- 不寫 code，只審 code
- 寧可 false positive 也不要漏

**產出格式：**
```markdown
## Review Report — [專案/功能名稱]

### Summary
- Files reviewed: [N]
- Issues found: [N]
  - Blocking: [N]
  - Major: [N]
  - Minor: [N]
- Verdict: ⛔ FAIL / ✅ PASS

### Blocking Issues
1. [Title] — [說明 + 檔案:行號]
2. ...

### Major Issues
...

### Minor Issues / Suggestions
...
```

---

### 🧪 Ops & QA Agent（deepseek / Claude）

| 項目 | 內容 |
|------|------|
| 模型 | deepseek v4 flash / Claude（彈性選用） |
| 角色定位 | 從測試到上線到文件的最終關卡 |
| 溝通對象 | 接 CEO 通知 → 執行測試/佈署/文件 → 出報告給 CEO |

**職責 — 四個子任務：**

#### 🧪 E2E 測試
- 根據 PRD / Spec 寫 test cases
- 執行 E2E 測試（Web: Playwright / Mobile: Maestro）
- 檢查功能是否與 spec 一致
- 產出 Test Report（PASS/FAIL matrix）

#### 🚀 佈署上線
- 客戶環境的 Docker 部署
- CI/CD pipeline 配置
- Deployment Checklist 產出
- 產出後通知 CEO 確認

#### 🔧 Workflow 配置
- 根據客戶需求調 n8n / Dify workflow
- 測試 workflow 是否正常運作
- 記錄 workflow 配置（markdown / JSON）

#### 📖 文件手冊
- **User Manual** — 終端用戶看的操作指南
- **Admin Guide** — 管理者看的配置與維護手冊
- **API Docs** — 開發者看的 API 文件
- **FAQ / Q&A** — 常見問題

**人設特質：**
- 嚴謹，不接受模糊
- 測試時模擬真實用戶行為
- 文件寫得清楚、步驟化、附截圖

---

## 三、完整協作流程

```
                 你（創辦人）
                     │
                     │ 說：「我要做一個家教 App 的學習記錄功能」
                     ▼
            ┌────────────────┐
            │ ① CEO Brainstorm│ ←── 跟你討論 → 你確認方向
            │    → PRD       │
            └───────┬────────┘
                    │ PRD 存 KB
                    ▼
            ┌────────────────┐
            │ ② CEO 拆任務   │
            │    → Impl Plan │
            └───────┬────────┘
                    │ Plan 存 KB
                    ▼
            ┌────────────────┐
            │ ③ CEO 派活    │──── 給 Coder
            └───────┬────────┘
                    ▼
            ┌────────────────┐
            │ ④ Coder 寫 code│
            │    → git push  │
            └───────┬────────┘
                    │ 通知 CEO
                    ▼
            ┌────────────────┐
            │ ⑤ CEO 叫 Reviewer│
            └───────┬────────┘
                    ▼
            ┌────────────────┐
            │ ⑥ Reviewer 審查 │
            │    → Review Rpt│
            └───────┬────────┘
                    │
         ⛔ FAIL ───┴─── ✅ PASS
            │                │
            ▼                ▼
       回 Coder 修    ┌────────────────┐
                      │ ⑦ CEO 叫 QA   │
                      └───────┬────────┘
                              ▼
                     ┌────────────────┐
                     │ ⑧ Ops & QA    │
                     │ ├ E2E 測試    │
                     │ ├ 佈署上線    │
                     │ ├ Workflow 配置│
                     │ └ 文件手冊     │
                     └───────┬────────┘
                             │
                  ⛔ FAIL ───┴─── ✅ ALL PASS
                     │                │
                     ▼                ▼
                回 Coder 修    ┌────────────────┐
                              │ ⑨ CEO 最終確認│
                              │    ✅ 完成     │
                              └────────────────┘
```

---

## 四、對應三條業務線

### 🏢 業務線 A：1~50人 AI Native Company 轉型顧問

| 階段 | 誰做 | 產出 |
|------|------|------|
| 1. 訪談客戶需求 | 你 → CEO 協助整理 | 客戶需求文件 |
| 2. 產出三階段提案 | CEO | 提案書（markdown） |
| 3. 實作 MCP Server | Coder | MCP Server code |
| 4. 審查 | Reviewer | Review Report |
| 5. 測試 ERP 連線 | Ops & QA | E2E Test Report |
| 6. 配置 workflow | Ops & QA | n8n / Dify config |
| 7. 部署到客戶環境 | Ops & QA | Deployment Checklist |
| 8. 產出使用手冊 | Ops & QA | User Manual / Admin Guide |

### 📚 業務線 B：家教 App（英/數複習 + 學習追蹤）

| 階段 | 誰做 | 產出 |
|------|------|------|
| 1. 功能 brainstorm | 你 + CEO | PRD |
| 2. 拆實作任務 | CEO | Implementation Plan |
| 3. 寫 code | Coder | App code |
| 4. code review | Reviewer | Review Report |
| 5. E2E 測試 | Ops & QA | Test Report |
| 6. 佈署上線 | Ops & QA | Deployment |
| 7. 家長使用手冊 | Ops & QA | User Manual |

### 🤖 業務線 C：客製化 Agent Team 開發部署

| 階段 | 誰做 | 產出 |
|------|------|------|
| 1. 了解客戶需求 | 你 + CEO | 客戶需求分析 |
| 2. 設計 agent 角色 | CEO | Agent 定義文件 |
| 3. 開發 agent | Coder | Agent code |
| 4. code review | Reviewer | Review Report |
| 5. 測試協作流程 | Ops & QA | E2E Test |
| 6. 部署 | Ops & QA | Deployment |
| 7. 客戶操作手冊 | Ops & QA | Admin Guide |

---

## 五、模型分配總表

| 角色 | 模型 | Provider | 理由 |
|------|------|----------|------|
| 🧠 CEO | deepseek v4 flash | OpenRouter（你主力） | 長 context、推理強、product sense |
| 👨‍💻 Coder | Claude Sonnet 4 | OpenRouter / Anthropic | 創意靈活、follow plan 好 |
| 🔍 Reviewer | Codex (OpenAI) | OpenRouter | 死板但細心、互補 Claude |
| 🧪 Ops & QA | deepseek or Claude | 視任務彈性選 | 寫 test 用 Claude、deploy 用 deepseek |

---

## 六、Knowledge Base 結構

```
📚 Knowledge Base (化神大大 / docs/)
 │
 ├── 📂 clients/                # 客戶專案
 │   ├── 客戶A/
 │   │   ├──需求分析.md
 │   │   ├──三階段提案.md
 │   │   ├──Implementation_Plan.md
 │   │   ├──Review_Reports/
 │   │   ├──Test_Reports/
 │   │   ├──Deployment_Checklist.md
 │   │   └──User_Manual.md
 │   └── 客戶B/...
 │
 ├── 📂 homeworks/              # 家教 App 專案
 │   ├──PRD.md
 │   ├──Implementation_Plan.md
 │   ├──Test_Cases/
 │   └──User_Manual.md
 │
 ├── 📂 agent-templates/        # Agent 人設模板（可重複用）
 │   ├──CEO-prompt.md
 │   ├──Coder-prompt.md
 │   ├──Reviewer-prompt.md
 │   └──OpsQA-prompt.md
 │
 └── 📂 frameworks/             # 核心框架
     └──1-50人nativegateway.md   # 三階段轉型框架
```

---

## 七、目前是 Draft，需要你確認的項目

- [ ] **角色命名** — Ops & QA 這個名字你滿意嗎？還是改成別的？
- [ ] **Coder 模型** — Claude Sonnet 4 確定？還是你有其他偏好？
- [ ] **Reviewer 模型** — Codex 你那邊有 access 嗎？
- [ ] **QA 模型** — 用你主力 deepseek 就好，還是需要分開？
- [ ] **協作流程** — 上述步驟有沒有要增減的順序？
- [ ] **Knowledge Base** — 存放位置要放化神大大還是在專案目錄下？
- [ ] **文件格式** — 我有寫一些產出範例（Review Report），格式 OK？
- [ ] **還有要加的角色？**

---

請過目，有想改的直接說，不用客氣。
