# LLM Wiki — 知識庫維護規範

你是這個知識庫的維護者。這套系統基於 Andrej Karpathy 的 LLM Wiki 模式，
透過 LLM 持續維護一組結構化、互相連結的 Markdown 筆記，取代傳統 RAG 的即時檢索模式。

---

## 架構

```
llm-wiki/
├── CLAUDE.md      ← 本檔案：維護規範與工作流程
├── index.md       ← 知識庫目錄（依分類組織）
├── log.md         ← 操作紀錄（僅追加）
├── raw/           ← 原始資料（只進不改）
│   ├── articles/  ← 網頁文章、新聞
│   ├── papers/    ← 學術論文
│   ├── notes/     ← 個人筆記
│   └── data/      ← 資料檔案
└── wiki/          ← LLM 維護的知識頁面
    ├── entities/  ← 人物、組織、產品
    ├── concepts/  ← 概念、技術、方法論
    ├── summaries/ ← 來源摘要
    └── analyses/  ← 綜合分析、比較
```

---

## 三層分工

| 層級 | 擁有者 | 說明 |
|------|--------|------|
| **raw/** | 人類 | 原始資料，不可修改。人類負責蒐集與策展 |
| **wiki/** | LLM | LLM 產生並維護的知識頁面。建立、更新、交叉引用全由 LLM 負責 |
| **CLAUDE.md** | 人類 + LLM | 系統規範。人類設定方向，LLM 可建議調整 |

**核心原則：人類負責策展來源、指定方向、提出問題。LLM 負責其餘所有整理工作。**

---

## Wiki 頁面格式

每個 wiki 頁面使用以下前置資料格式：

```markdown
---
title: 頁面標題
type: entity | concept | summary | analysis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/articles/來源檔名.md
tags:
  - 標籤1
  - 標籤2
---

# 頁面標題

正文內容...

## 相關頁面
- [[相關頁面1]]
- [[相關頁面2]]
```

---

## 四大操作

### 1. Ingest（收錄）

當新的原始資料加入 `raw/` 時：

1. 讀取完整原始資料
2. 在 `wiki/summaries/` 建立該來源的摘要頁
3. 掃描現有 wiki 頁面，更新所有相關頁面（通常 5–15 頁）
4. 若發現新的實體或概念，建立對應頁面於 `wiki/entities/` 或 `wiki/concepts/`
5. 維護所有頁面的交叉引用 `[[連結]]`
6. 更新 `index.md`
7. 在 `log.md` 記錄本次操作

**觸發指令：** `ingest raw/articles/檔名.md`

### 2. Query（查詢）

針對知識庫提問：

1. 搜尋相關 wiki 頁面
2. 綜合多頁資訊產生回答
3. 若回答具有長期價值，將其存為新的 wiki 頁面（`wiki/analyses/`）
4. 在 `log.md` 記錄本次查詢

**觸發指令：** `query 你的問題`

### 3. Lint（健檢）

定期審核知識庫品質：

1. 找出互相矛盾的資訊
2. 找出孤立頁面（無任何連結指向）
3. 找出缺漏的交叉引用
4. 找出過時或需要更新的內容
5. 產出健檢報告並建議修正
6. 在 `log.md` 記錄本次健檢

**觸發指令：** `lint`

### 4. Clip（快速擷取）

搭配 Obsidian Web Clipper 或手動貼上 URL：

1. 抓取網頁內容
2. 存入 `raw/articles/`
3. 自動執行 Ingest 流程

**觸發指令：** `clip https://example.com/article`

---

## 命名慣例

- 檔名使用 kebab-case：`transformer-architecture.md`
- 摘要頁加前綴：`summary-來源名.md`
- 分析頁加前綴：`analysis-主題.md`
- 日期格式：`YYYY-MM-DD`

---

## 交叉引用規則

- 使用 `[[頁面名稱]]` 格式（Obsidian 相容）
- 每個頁面底部列出「相關頁面」區塊
- 新增或更新頁面時，同步更新所有被引用頁面的反向連結

---

## 語言規則

- 所有 wiki 頁面預設使用**繁體中文**
- 專有名詞、技術術語、人名、組織名保留英文
- 來源摘要保留原文語言的關鍵引述
