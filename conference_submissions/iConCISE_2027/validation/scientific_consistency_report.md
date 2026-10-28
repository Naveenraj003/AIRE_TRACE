# Scientific Consistency Report

## Audit of Claims vs. Source Artifacts
- **dyn_comp threshold:** Reported as 0.552167546011228. Source `main.tex` lists frozen threshold as `0.5522`. Status: Consistent (rounded appropriately).
- **M1 threshold:** Reported as 0.98. Source `main.tex` lists `0.98`. Status: Consistent.
- **dyn_comp Recall@FAR / FAR:** Reported 0.1167 / 0.0404. Source lists `0.1167` / `0.0404`. Status: Consistent.
- **M1 Recall@FAR / FAR:** Reported 0.0078 / 0.0303. Source lists `0.0078` / `0.0303`. Status: Consistent.
- **Difference in Recall@FAR:** +0.1089. Source lists `+0.1089`. Status: Consistent.
- **95% Confidence Interval:** [0.0706, 0.1496]. Source lists `[0.0706, 0.1496]`. Status: Consistent.
- **Adjusted p-value:** $9.999 \times 10^{-5}$. Source lists exactly this. Status: Consistent.
- **Baseline AUROC range:** 0.5074–0.6371. Source lists 0.5074 (H3) to 0.6371 (S1). Status: Consistent.
- **S1 Random Forest AUROC:** 0.6371. Source matches. Label is correct (Sequence tier, but tabular ensemble Random Forest implementation explicitly stated). Status: Consistent.
- **M1 Logistic Regression AUROC:** 0.6215. Source matches. Status: Consistent.
- **dyn_comp AUROC:** 0.3593. Source matches. Distinction correctly explained that subtracting the static baseline prior can push AUROC < 0.5 while still acting as a valid threshold anomaly detector. Status: Consistent.
- **Ablation (error + retry):** $\Delta$AUROC = −0.1069. Source matches. Status: Consistent.
- **PDC:** 0.8294 with 21/21 pairs. Source matches. Status: Consistent.
- **Limitations:** 19.18% retention, missing onset annotations (60 episodes), untested LLM monitor (L), limited domain generalization all accurately retained in Section XI of the manuscript. Status: Consistent.

## Findings
No scientific inconsistencies were discovered in the manuscript source files. Values exactly match the required canonical measurements.
