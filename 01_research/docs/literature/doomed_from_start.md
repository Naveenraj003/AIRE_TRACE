# Doomed from the Start: Early Abort of LLM Agent Episodes via a Recall-Controlled Probe Cascade (July 2026)

**Category:** Failure Warning / Monitoring Systems
**arXiv:** [2607.06503](https://arxiv.org/abs/2607.06503)
**Published:** July 2026
**Ref ID:** [M6]

---

## What the Paper Is

Studies **early failure prediction and inference-time early stopping** using **hidden-state probes** on LLM internal activations — predicting eventual task failure from the **first interaction round**.

### Core Method: Recall-Controlled Abort Cascade
- **Linear probes** on internal LLM activations predict failure from round 1 (much earlier than behavior-only monitoring)
- **Distribution-free calibrated failure detector** at each early interaction round
- **Jointly optimizes per-round recall budgets** across all early stopping gates
- After selection, the cascade is **frozen and certified on independent data** → exact post-selection recall guarantee

### Results (TextCraft + WebShop; Qwen-2.5-7B, Llama-3.2-3B, Qwen3-1.7B)
- Saves **1.5–8.8× more compute** at 90% recall target vs best single-gate baseline
- Achieved recall within **one standard deviation of target** in all 24 configurations
- **60.2% token reduction** on TextCraft, **54.9%** on WebShop at 90% recall
- **Behavior-only monitoring is consistently weaker** → adding behavioral features to hidden-state probes provides no further gain

### Key Finding
> "Behavior-only monitoring is consistently weaker, and adding behavioral features to hidden-state probes provides no further gain."

## What It Solves

- Extreme compute savings through early abort of doomed trajectories
- Provable recall guarantee via post-selection certification
- Shows that hidden-state probes dominate observable behavior for early failure prediction

## What It Lacks

- Requires access to **model internal activations** → not applicable to black-box closed-API models (GPT, Claude, Gemini)
- Only evaluated on TextCraft and WebShop — both simpler than TerminalBench
- Linear probes are limited; complex, multi-step failures may need deeper representations
- The "behavior-only is weaker" finding is a limitation for AIRE-TRACE: our entire approach is behavior-only

## Relevance to AIRE-TRACE

- **Critical challenge**: This paper finds that behavior-only monitoring is consistently weaker than hidden-state probes — a direct challenge to AIRE-TRACE's observable-telemetry-only approach
- AIRE-TRACE's response: (1) black-box applicability is a feature, not a bug; (2) the deterministic verification layer adds precision that hidden-state probes can't provide; (3) our AUROC 0.872 on behavior-only is validated empirically
- The **recall-controlled cascade design** is related to our CUSUM alarm cascade — both use sequential decision-making with bounded recall costs
- Post-selection certification (frozen + tested on independent data) parallels our TEST-set freeze requirement (Rule: never select threshold using TEST data)
- **Important limitation to document in our paper**: we cannot match hidden-state probe performance on models where activations are accessible — must qualify claims for black-box deployment context
- The 90% recall target mirrors our 5% FPR target — different parameterization of the same precision-recall tradeoff

---

## Key Terms
`hidden-state probes` · `recall-controlled cascade` · `early abort` · `distribution-free` · `behavior-only monitoring` · `token savings`
