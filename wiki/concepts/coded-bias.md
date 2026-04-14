---
title: Coded Bias（編碼偏見）
type: concept
created: 2026-04-14
updated: 2026-04-14
sources:
  - raw/papers/clinicians-guide-ai-primary-care-lead-healthcare-ai.md
tags:
  - AI倫理
  - 健康公平
---

# Coded Bias（編碼偏見）

## 定義

自動化系統並非天生中立——它們反映創造者的優先順序、偏好和偏見。如果訓練資料有偏見，AI 產出也會有偏見。

## 關鍵證據

- **臉部辨識偏見（2018）：** Buolamwini & Gebru 研究發現商用臉部辨識工具對男性表現優於女性，對淺膚色優於深膚色。2020 年 George Floyd 事件後，IBM、Microsoft、Amazon 宣布停止向執法機構銷售臉部辨識軟體。
- **醫療預測模型偏見：** 部分模型對富裕白人男性病患更準確，因訓練資料來自該族群。EHR 資料中弱勢族群的不平等就醫紀錄，導致模型低估其風險（Obermeyer et al., *Science* 2019）。
- **自殺風險預測偏見：** 部分模型存在種族/族裔表現差異（Coley et al., *JAMA Psychiatry* 2021）。

## 緩解策略

- 在預測模型中加入**社會決定因素資料**（鄰里、環境、生活方式、語言、交通、收入、社會支持、教育）
- 建立**健康公平諮詢委員會**審核和校正偏見
- **種族正義需要演算法正義**（Dr. Joy Buolamwini, Algorithmic Justice League）

## 相關頁面
- [[ai-clinical-evaluation|AI 臨床評估框架]]
- [[cognitive-biases-in-ai|AI 互動中的認知偏見]]
- [[ai-validation-standards|AI 驗證標準]]
- [[summary-clinicians-guide-ai-primary-care|Clinician's Guide to AI 摘要]]
- [[summary-physician-ai-handbook|The Physician AI Handbook 摘要]]
- [[summary-fcai-clinical-ai-curriculum|FCAI Curriculum 摘要]]
