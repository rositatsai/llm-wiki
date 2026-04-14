---
title: AI 互動中的認知偏見
type: concept
created: 2026-04-14
updated: 2026-04-14
sources:
  - raw/papers/fcai-clinical-ai-curriculum-v3.2.md
tags:
  - 臨床安全
  - AI導入
---

# AI 互動中的認知偏見

## 定義

人類與 AI 技術互動時，認知偏見會影響對 AI 輸出的接受、拒絕和解讀方式，進而影響臨床決策品質和病患安全。

## 主要偏見類型

| 偏見 | 說明 | 臨床風險 |
|------|------|---------|
| **Automation Bias（自動化偏見）** | 過度信賴 AI 輸出，忽略自身判斷 | 接受 AI 的錯誤建議而未批判性評估 |
| **Aversion Bias（厭惡偏見）** | 因不信任而系統性拒絕 AI 建議 | 浪費 AI 帶來的正確輔助價值 |
| **Confirmation Bias（確認偏見）** | 傾向接受與既有信念一致的 AI 輸出 | 選擇性採用 AI 結果，忽略矛盾資訊 |
| **Rejection Bias（拒絕偏見）** | 當 AI 輸出與預期不符時傾向拒絕 | 忽略可能正確的非預期發現 |
| **Alert Fatigue（警報疲勞）** | 大量警報導致對所有警報的敏感度下降 | 忽略真正重要的 AI 警示 |

## AI 失敗模式 vs 人類錯誤

AI 失敗模式與人類臨床推理錯誤本質不同：
- **Outlier detection failure** — AI 無法辨識訓練分佈外的異常案例
- **Adversarial attacks** — 細微的輸入擾動導致 AI 輸出大幅改變

理解這些差異對於設計安全的人機協作工作流程至關重要。

## 緩解策略

- 使用者訓練：理解 AI 的能力和限制
- 工作流程設計：保留人類最終決策權
- AI 可解釋性（Explainability）：使 AI 推理過程透明化
- 定期效能監測：偵測人機互動模式異常

## 相關頁面
- [[summary-fcai-clinical-ai-curriculum|FCAI Curriculum 摘要]]
- [[ai-clinical-evaluation|AI 臨床評估框架]]
- [[coded-bias|Coded Bias]]
