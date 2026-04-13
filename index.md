---
title: 知識庫目錄
updated: 2026-04-14
---

# LLM Wiki — 知識庫知識地圖

> **24 筆原始來源 → 22 頁 Wiki → 4 大知識主軸**

---

## 知識主軸一：數位健康能力框架

> 涵蓋 8 個國家/區域、21 份框架文獻，是知識庫目前最大主題。

### 核心概念
- [[digital-health-capability|數位健康能力]] — 定義、四維度模型（技術/方法論/社會/個人）、六大共通能力領域

### 跨國比較
- [[analysis-global-digital-health-capability-frameworks|跨國數位健康能力框架比較分析]] — 21 份文獻、框架比較表、能力等級比較、Scoping Review 發現

### 依區域

| 區域 | Wiki 摘要 | 原始來源數 | 代表性框架 |
|------|----------|-----------|-----------|
| 🇬🇧 英國 | [[summary-frameworks-uk]] | 2 | HEE 6 領域 4 等級框架、NHS AI Capability Framework |
| 🇦🇺 澳洲 | [[summary-frameworks-australia]] | 8 | AU General、AMC 醫師、Nursing、Allied Health、Action Plan、Roadmap、自評工具 |
| 🌍 國際 | [[summary-frameworks-international]] | 9 | EU DigComp 2.2、US HHS AI Plan、Canada、ASEAN、Singapore、UNESCO |
| 📚 學術 | [[summary-scoping-reviews-digital-competence]] | 2 | Brice (59 項能力/13 類別)、Mainz (46 篇研究/衡量缺口) |

### 關鍵機構
- [[hee|Health Education England (HEE)]] — 英國醫療數位能力框架制定者
- [[adha|Australian Digital Health Agency (ADHA)]] — 澳洲數位健康核心推動機構

---

## 知識主軸二：醫療 AI 導入與評估

> 聚焦 AI 工具的臨床評估、驗證標準、導入方法和已知風險。

### 核心概念
- [[ai-clinical-evaluation|AI 臨床評估框架]] — 六大評估維度（效能/安全/倫理/隱私/工作流程/法律）
- [[ai-validation-standards|AI 驗證標準]] — SPIRIT-AI、CONSORT-AI、NICE、CE/UKCA、DCB0129/0160、GDPR/HIPAA
- [[stanford-method|The Stanford Method]] — 基於品質改善（QI）的 AI 導入六步驟
- [[starfield-4cs|Starfield 4Cs]] — 基層醫療四大支柱與 AI 導入定位

### 風險與倫理
- [[coded-bias|Coded Bias（編碼偏見）]] — 資料偏見 → AI 偏見、Buolamwini 臉部辨識研究、Obermeyer 醫療演算法偏見
- [[cognitive-biases-in-ai|AI 互動中的認知偏見]] — Automation bias、Aversion bias、Confirmation bias、Rejection bias、Alert fatigue

### 來源摘要
- [[summary-clinicians-guide-ai-primary-care|Clinician's Guide to AI]] — Steven Lin, JABFM 2022. AI 改變醫療的 10 種方式、3 大限制
- [[summary-physician-ai-handbook|The Physician AI Handbook]] — Bryan Tegomoh, 2026. 19 專科 AI 同儕審查證據

### 關鍵人物
- [[steven-lin|Steven Lin]] — Stanford, 基層醫療 AI 導入先驅
- [[bryan-tegomoh|Bryan Tegomoh]] — The Physician AI Handbook 作者

---

## 知識主軸三：臨床 AI 人才培育

> 從課程設計到培訓路徑，如何培養具備 AI 能力的臨床醫師。

### 核心概念
- [[clinical-ai-training|臨床 AI 人才培育]] — 跨來源綜合比較表：NHS Fellowship vs 美國路徑 vs 自學資源

### 來源摘要
- [[summary-fcai-clinical-ai-curriculum|FCAI Clinical AI Curriculum v3.2]] — NHS 12 個月 Fellowship, 5 大主題, 4 種教學方法, 5 個代表性專案

### 關鍵人物與機構
- [[alexander-deng|Alexander T Deng]] — FCAI Programme Lead
- [[gstt-csc|GSTT Clinical Scientific Computing]] — NHS 臨床 AI Fellowship 教學團隊, Moorfields-DeepMind 合作

---

## 知識主軸四：策略與政策

> 國家級 AI 策略、數位轉型政策、國際趨勢。

### 來源（存於 raw/，已納入分析頁）
- US HHS AI Strategic Plan (2025) — 四大策略目標、七大 AI 應用領域
- AU National Digital Health Capability Action Plan (2020)
- AU National Digital Health Workforce and Education Roadmap (2020)
- Victoria's Digital Health Roadmap 2021-2025
- ASEAN Digital Health Adoption Assessment (2024)
- Canada DHC Market Study

---

## 知識關聯圖

```
                    ┌──────────────────────────┐
                    │   數位健康能力（基礎層）    │
                    │  UK·AU·EU·CA·ASEAN·UNESCO │
                    └─────────┬────────────────┘
                              │ 進階延伸
                    ┌─────────▼────────────────┐
                    │   醫療 AI 能力（專項層）    │
                    │  評估·驗證·偏見·導入方法    │
                    └─────────┬────────────────┘
                              │ 落地實踐
              ┌───────────────┼───────────────┐
    ┌─────────▼─────────┐   ┌▼──────────────┐ ┌▼─────────────┐
    │   人才培育          │   │  策略與政策    │ │  臨床應用     │
    │  FCAI·Stanford·   │   │  HHS·AU·ASEAN │ │  19專科證據   │
    │  ABAIM·AMIA       │   │  Victoria·CA  │ │  (Handbook)  │
    └───────────────────┘   └───────────────┘ └──────────────┘
```

---

## 統計

| 指標 | 數量 |
|------|------|
| 原始來源 | 24 筆（23 papers + 1 article） |
| Wiki 頁面 | 22 頁 |
| — Analyses | 1 |
| — Concepts | 8 |
| — Entities | 6 |
| — Summaries | 7 |
| 涵蓋國家/區域 | 8（UK、Australia、EU、USA、Canada、ASEAN、Singapore、International） |

**最後更新：** 2026-04-14
