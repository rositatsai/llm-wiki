---
title: AI 臨床評估框架
type: concept
created: 2026-04-14
updated: 2026-04-14
sources:
  - raw/articles/physician-ai-handbook.md
  - raw/papers/clinicians-guide-ai-primary-care-lead-healthcare-ai.md
  - raw/papers/fcai-clinical-ai-curriculum-v3.2.md
tags:
  - AI評估
  - 臨床導入
  - 同儕審查
  - 醫療品質
---

# AI 臨床評估框架

## 定義

在醫療機構採用 AI 工具前，以系統性方法評估其安全性、有效性、合規性與實務可行性的框架。

## 核心原則

- **證據驅動：** 以同儕審查文獻為基礎，非廠商行銷資料
- **真實環境驗證：** 已發表的驗證研究表現 ≠ 真實臨床環境表現
- **持續監測：** AI 模型可能因資料漂移（data drift）而退化

## 評估維度

1. **臨床效能** — 敏感度、特異度、AUC 等指標在真實環境的表現
2. **安全與風險** — 失敗模式、錯誤類型、後備機制
3. **倫理與公平** — 偏見檢測、健康公平影響
4. **隱私合規** — HIPAA、台灣個資法等法規要求
5. **工作流程適配** — 與現有臨床流程的整合程度
6. **法律責任** — AI 錯誤時的責任歸屬

## 來源

- [[summary-physician-ai-handbook|The Physician AI Handbook]] — Part III: Implementation 提供完整評估框架
- [[summary-clinicians-guide-ai-primary-care|Clinician's Guide to AI]] — 討論 Nongeneralizability、Calibration Drift，並提出 [[stanford-method|The Stanford Method]] 作為 QI 導入框架
- [[summary-fcai-clinical-ai-curriculum|FCAI Curriculum]] — Validation & Evaluation 主題涵蓋 SPIRIT-AI、CONSORT-AI、部署後監測、偏見審核方法論

## 相關頁面
- [[summary-physician-ai-handbook|The Physician AI Handbook 摘要]]
- [[summary-clinicians-guide-ai-primary-care|Clinician's Guide to AI 摘要]]
- [[summary-fcai-clinical-ai-curriculum|FCAI Curriculum 摘要]]
- [[coded-bias|Coded Bias]]
- [[stanford-method|The Stanford Method]]
- [[cognitive-biases-in-ai|AI 互動中的認知偏見]]
- [[ai-validation-standards|AI 驗證標準]]
