# LangChain Agent Evaluation Report with NeMo Guardrails

## Overview

This document outlines the results of evaluating a LangChain agent enhanced with NeMo Guardrails. The evaluation was conducted using `LangChain AgentEval` on a custom dataset designed to test tool usage, reasoning, factual correctness, and guardrail compliance.

---

## ✅ Input/Output Contracts

Defined in `rails.json`:
- **Input**: String-based user queries (natural language).
- **Output**: Filtered strings ensuring safe and factual responses.

Guardrails block offensive input and log hallucinations for analysis.

---

## 🧪 Metrics

| Metric              | Result     | Notes                                                  |
|---------------------|------------|--------------------------------------------------------|
| **Correctness**     | 86%        | 6 out of 7 answers were factually correct              |
| **Latency**         | Avg: 2.7s  | Slight overhead due to guardrails checks               |
| **Hallucination Rate** | 14%     | 1 out of 7 responses flagged as hallucinated facts     |
| **Tool Usage Success** | 100%   | Agent used tools (Search, Math) correctly when needed  |

---

## ⚠️ Observations

- NeMo Guardrails successfully filtered inappropriate input (e.g., profanity).
- One response was flagged for mild hallucination (incorrect capital city).
- Minor latency introduced (0.5–1s) by guardrails, acceptable for safety gains.

---
