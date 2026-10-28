# AIRE-Trace: A Standardized Prospective Evaluation Protocol for Online Agent-Failure Warning

## Abstract

Early detection of task failure in agentic systems requires distinguishing prospective warning signals from information that becomes available only after failure onset. This study evaluates whether trajectory-prefix features can support prospective failure detection under constrained false-alarm rates. Using the reconstructed Tracebench population, we evaluated 636 usable episodes from 3,316 declared source rows in a task-disjoint train/calibration/test protocol. Seven baseline models were evaluated in Mode A using trajectory prefixes up to \(K=30\), with thresholds calibrated on the calibration split and prospective metrics evaluated on the test split.

Across the evaluated models, AUROC ranged from 0.5074 to 0.6371, with the Random Forest model (S1) achieving the highest observed AUROC. However, prospective Recall@FAR remained near zero under a 5% false-alarm constraint. Paired episode-cluster bootstrap testing with 1,000 iterations and Holm-Bonferroni correction showed that S1 had significant AUROC advantages over S2, H2, and H3, while its differences from M1, H1, and H4 were not statistically significant. For AUPRC, S1 was significantly higher only than S2. Feature ablation further showed that removing `tool_error_count` and `retry_count` produced the largest observed degradation in S1 performance, indicating an association between these signals and discrimination performance rather than establishing causality. Post-onset analysis also showed that H3 generated 3,339 late alerts, with 19.84% of valid failure episodes receiving only late alerts.

These results indicate that the evaluated trajectory-prefix features provide limited prospective discrimination, while achieving actionable early warning under strict false-alarm constraints remains challenging. The findings should be interpreted within the 636-episode reconstructed population and should not be generalized to the complete declared source population.

**Keywords:** Agentic Systems, Failure Warning, Standardized Evaluation, Trajectory Analysis, Operational Metrics

## I. Introduction

The increasing deployment of autonomous agentic systems has shifted evaluation priorities from merely measuring final task outcomes to ensuring reliability during execution. While outcome benchmarking (e.g., AgentBench [1], AgentBoard [2], GAIA [3]) establishes whether an agent ultimately succeeds or fails, it does not provide mechanisms for preemptive intervention. Post-hoc failure localization and attribution methods (e.g., AgentRx [5], Who&When Pro [6]) identify where a trajectory went wrong, but their retrospective nature requires the full trajectory and ground-truth failure state by construction.

Conversely, online agent-failure warning methods attempt to predict eventual task failure prospectively, using only the partial trajectory (prefix) available before failure onset. Recent methods, including PrefixGuard [7], AgentForesight [8], and Trajectory Guard [9], address this prospective warning task. However, these methods each use their own datasets, prefix definitions, calibration procedures, and evaluation metrics. Consequently, it remains unclear whether reported comparative claims between different method families (e.g., heuristic, classical machine learning, or sequence models) are robust, or whether they are artifacts of differing evaluation protocols.

Prospective, prefix-based failure warning is therefore not itself a new research direction: PrefixGuard and AgentForesight, in particular, already demonstrate that predicting eventual failure from an unfolding trajectory prefix is a viable and active line of work, with reported predictive performance substantially exceeding the baseline family evaluated in this study. AIRE-Trace does not claim to invent prospective warning, nor does it propose a new detector architecture intended to outperform these systems. Instead, this work addresses a different, complementary methodological question: given that prospective warning is achievable in principle, how should the resulting warning capability be evaluated once it is required to operate under a fixed, deployment-relevant false-alarm budget, rather than being assessed purely on retrospective ranking quality? Prior work has established prospective/prefix-based failure prediction as a research direction; AIRE-Trace addresses a different methodological question concerning how such warning capability should be evaluated under a fixed operational false-alarm constraint.

To address this methodological gap, this study asks: do comparative performance claims for online agent-failure warning methods remain consistent when evaluated under identical information, target, alert, calibration, lead-time, and compute constraints?

instead of proposing another failure detector, this work contributes a standardized, prospective, prefix-only evaluation protocol for online agent-failure warning. By fixing the information visibility, failure-target definition, alert semantics, calibration procedure, and false-alarm constraints, we evaluate representative heuristic, classical-ML, and sequence-based methods under a common harness. Full prospective evaluation is performed on TerminalBench, which provides the necessary failure-onset annotations. A secondary diagnostic capability, τ²-Bench, is provided as protocol context for assessing external-transfer consistency, but Mode B is explicitly outside the scope of the reported prospective study.

## II. Methodology

### A. Research Question and Evaluation Principle

The primary objective of this evaluation protocol is to determine whether comparative conclusions across different agent-failure warning methods remain stable under identical constraints. Rather than evaluating the internal optimization of each method, the protocol standardizes the evaluation conditions: every method receives the same partial information and is scored on common accuracy, calibration, and operational metrics.

### B. Datasets and Evaluation Modes

The protocol defines two distinct evaluation modes based on dataset capabilities:

**Mode A (Prospective-warning evaluation):** Conducted exclusively on TerminalBench, which provides step-level failure-onset annotations (`incorrect_stages`). This mode evaluates genuine early warning by restricting inputs to pre-onset and onset prefixes. It supports AUROC, AUPRC, calibration metrics, prospective Recall@FAR, and lead time.

**Mode B (Eventual-outcome diagnostic):** Conducted on τ²-Bench, which lacks onset annotations. This secondary mode validates representation transfer and eventual-outcome risk calibration over partial trajectories using the same checkpoint policy as Mode A, without onset-based exclusion. Mode B represents protocol capability and context only, and does not form part of the reported experimental evidence. Mode B does not support prospective Recall@FAR or lead time.

### C. Canonical Trace Processing

To ensure cross-dataset feature compatibility, we define a canonical target by mapping each benchmark's native success/failure determination (e.g., TerminalBench's reward criterion and τ²-Bench's task-completion reward) into unified `eventual_success` and `eventual_failure` outcomes. All outcome-bearing content and terminal markers are subsequently sanitized from the event stream prior to feature computation to prevent terminal-event leakage.

### D. Prospective Prefix Construction

Checkpoints are evaluated according to an outcome-independent, episode-symmetric schedule using the first 30 valid steps by absolute index (\(K=30\)). At checkpoint \(t\), a monitor accesses only steps 1...\(t\). An alert at \(t\) is valid if and only if \(t \le t_{onset}\), yielding a lead time of \(t_{onset} - t\). Alerts occurring after \(t_{onset}\) are recorded as late detections and excluded from prospective warning metrics.

### E. Baseline Methods

We evaluate three mandatory method families, strictly bounded to the frozen model set {H1, H2, H3, H4, M1, S1, S2}:

- **Heuristic monitor (H):** Training-free, rule-based methods utilizing retry counts, tool-error rates, and latency trends.
- **Classical ML (M):** Baseline machine learning models over engineered features.
- **Sequence monitor (S):** Sequence models processing the feature time series.

### F. Train/Calibration/Test Protocol

Splitting is performed at the episode level across three disjoint sets (TRAIN, CALIBRATION, TEST) to prevent prefix-level leakage. TerminalBench serves as the sole training and calibration source. For model fitting (M and S) and threshold calibration (H, M, S), failed episodes contribute prefixes only up to failure onset (\(t \le t_{onset}\)), ensuring the models learn prospective risk rather than retrospective collapse.

### G. Threshold Calibration and Recall@FAR

Thresholds are calibrated exclusively on the CALIBRATION split. For a given target False Alarm Rate (FAR), we select the threshold that maximizes calibration-set recall while satisfying calibration FAR \(\le\) target FAR. Ties are broken by lower FAR, then higher threshold. The selected threshold is frozen and applied unchanged to the TEST split.

### H. Evaluation Metrics

Prefix-level ranking metrics (AUROC, AUPRC, Brier, ECE) utilize episode-balanced prefix weighting (each prefix weighted \(1/n_i\)), ensuring each episode contributes equally regardless of trajectory length. Operational metrics, including FAR and Recall@FAR, are measured at the episode level. An episode is classified as a false alarm if it eventually succeeds but receives at least one alert.

### I. Statistical Comparison

Confidence intervals and statistical significance are derived using a paired episode-cluster bootstrap procedure with B=1000 iterations. Multiple-comparison correction is applied using the Holm-Bonferroni method (\(\alpha=0.05\)). Ranking stability across metrics is assessed via the Pairwise Direction Consistency (PDC) statistic, which computes the proportion of informative metrics agreeing on the pairwise winner. Across the seven evaluated models (21 pairs), the overall PDC was 0.8294, with coverage 0.881 across 21/21 informative pairs.

### J. Ablation and Late-Detection Analysis

Component-level feature ablations isolate the association between structural trace components (e.g., error and retry signals) and discrimination capability. Concurrently, post-onset late detections are reported separately from prospective recall to distinguish retrospective diagnostic activity from actionable early warning.

## III. Results

### A. Dataset and Evaluation Population

The evaluation was conducted on a reconstructed dataset consisting of 636 usable episodes, representing 19.18% of the 3,316 declared source rows from the Tracebench corpus. The TEST split comprised 416 episodes, of which 317 resulted in task failure. To evaluate prospective early warning capabilities, 60 of these failure episodes were excluded from onset-dependent metrics (e.g., Recall@FAR) because they lacked usable onset annotations, yielding 257 valid failure episodes.

### B. Baseline Prospective Discrimination

We evaluated the prospective discrimination capabilities of the models using Mode A (TerminalBench TEST) with a maximum prefix horizon of \(K=30\). The evaluated prospective trajectory-prefix features produced AUROC values ranging from 0.5074 to 0.6371 across the seven evaluated models. The Random Forest model (S1) achieved the highest observed AUROC (0.6371), while H3 achieved an AUROC close to chance (0.5074).

Under a 5% target False Alarm Rate (FAR) constraint calibrated on the CALIBRATION split, prospective early-warning recall was near zero across all models. For instance, S1 and M1 produced Recall@FAR(5%) values of 0.0000 and 0.0078, respectively. Model H3 produced an undefined (NaN) Recall@FAR because its calibration FAR reached 1.0000, placing it entirely outside the intended operational regime.

### C. Statistical Comparison

To robustly compare discrimination performance, we utilized a paired episode-cluster bootstrap procedure (B=1000) with Holm-Bonferroni correction (\(\alpha=0.05\)) to account for multiple comparisons across the predefined hypothesis family. Under this strict non-parametric protocol, S1 demonstrated a selective statistical advantage. Specifically, S1 achieved statistically significant AUROC advantages over S2, H2, and H3 (\(p_{adj} \le 0.05\)). However, AUROC differences between S1 and M1, H1, or H4 were not statistically significant after Holm correction.

For AUPRC, S1's advantage was statistically significant only against S2. Furthermore, H3 achieved a directionally higher AUPRC point estimate than S1 (\(\Delta_{obs} = -0.0250\) for S1 \(-\) H3), though this difference was not statistically significant.

### D. Operating-Point Sensitivity

We examined S1's sensitivity across multiple target FAR constraints (1%, 5%, and 10%). Strict FAR constraints severely restricted the model's ability to generate valid prospective alerts. At target FARs of 1% and 5% (frozen threshold 0.97), S1 produced a TEST FAR of 0.0404 and a Recall@FAR of 0.0000. Relaxing the target FAR to 10% (frozen threshold 0.93) yielded a TEST FAR of 0.1212 and a Recall@FAR of 0.0973. This establishes that under strict operational false alarm constraints (FAR \(\le\) 5%), early warning recall essentially collapses in the evaluated setting.

### E. Feature Ablation

To examine the association of individual trace-feature groups with S1's discrimination capability, we conducted a component-level feature ablation study. The full baseline model (A0) achieved an AUROC of 0.6371 and an AUPRC of 0.8452. Removing the error and retry signals (`tool_error_count` and `retry_count`, denoted as condition A4) produced the largest observed degradation, yielding an AUROC of 0.5302 (\(\Delta\) AUROC = \(-0.1069\)) and an AUPRC of 0.7820. This result indicates that the error and retry signals are strongly associated with the observed discrimination performance of S1, although the ablation does not by itself establish a causal relationship.

### F. Late Detections

Finally, we analyzed post-onset (late) alerting behavior separately from prospective early-warning metrics. Model H3 generated 3,339 late alerts across the TEST split. Notably, 51 of the 257 valid failure episodes (19.84%) received only late alerts from H3, a proportion that substantially exceeds the corresponding proportions for all other evaluated models (e.g., 6.23% for S1 and 3.89% for M1). These results indicate that H3's high alert volume was accompanied by a substantially higher proportion of failure episodes receiving only late alerts.

## IV. Discussion

Our evaluation reveals a fundamental gap between the relative risk-ranking capabilities of trajectory-prefix models and their operational utility for early warning. While the baseline models demonstrate weak-to-moderate ability to discriminate eventual failure in the evaluated subset (AUROC 0.50–0.63), this capability is currently insufficient to support strict operational deployment constraints.

### A. The Collapse of Operational Recall

The most critical operational finding is the collapse of prospective early-warning recall under the evaluated False Alarm Rate (FAR) constraints. When restricted to a FAR \(\le\) 5%, prospective recall fell to near zero across all evaluated models. This indicates that while the models can separate failures from successes probabilistically over a population, they did not achieve substantial prospective recall while satisfying the evaluated strict false-alarm constraint.

### B. Selective Superiority of Non-Linear Modeling

The Random Forest model (S1) demonstrated statistically significant AUROC advantages over specific baselines (S2, H2, and H3) and a significant AUPRC advantage over S2 under the paired episode-cluster bootstrap test. However, S1 was not universally superior; its advantages over models such as M1, H1, or H4 were not statistically significant after multiple-testing correction. This selective superiority suggests that while non-linear combination of prefix features provides some benefit over simple sequence models or specific heuristics, the ceiling for prospective discrimination using only pre-onset structural features remains low.

### C. The Association with Explicit Failure Symptoms

The feature ablation study demonstrated that removing error and retry signals produced the largest observed degradation in S1's performance. This association indicates that these explicit error and retry signals contribute substantially to the observed discrimination performance, while the ablation alone does not establish whether they reflect early predictive information or information proximate to failure onset.

### D. The Distinction Between Activity and Utility

Finally, the post-onset alerting behavior of model H3 underscores the critical methodological necessity of distinguishing between prospective early warning and retrospective diagnosis. H3 generated an excessive volume of alerts, but nearly 20% of its valid failure detections were exclusively late (post-onset). These observations illustrate why evaluations of prospective failure prediction must enforce the onset boundary and distinguish post-onset diagnostic activity from prospective warning capability. The results demonstrate that high alert volume does not equate to effective prospective detection.

## V. Reproducibility Statement and Limitations

### A. Reproducibility Statement

The complete evaluation protocol, including all dataset generation scripts, canonical schema mappings, feature extractors, model configurations, and bootstrap statistical routines, is preserved in the frozen project repository. To ensure strict adherence to the prospective warning constraints, all reported operational metrics and significance tests are deterministic outputs of the automated `MasterEvaluator` pipeline, which programmatically enforces the prefix horizon and post-onset exclusion boundaries.

### B. Dataset Coverage and Representativeness

The primary limitation of this study is the size and provenance of the evaluated population. The evaluation was conducted on 636 usable reconstructed episodes from 3,316 declared source rows, corresponding to 19.18% of the declared source population. The majority of excluded rows were structurally invalid because the required trajectory artifact was unavailable or incomplete. Although the retained population was independently reconciled with the task-disjoint train, calibration, and test splits, its representativeness of the full source population has not been established. Accordingly, the reported performance should not be interpreted as generalizing to the complete 3,316-row population.

### C. Incomplete Onset Annotation

Prospective early-warning evaluation additionally depends on the availability of a usable failure-onset boundary. Of the 317 failure episodes in the TEST split, 60 lacked usable onset annotations and were therefore excluded from onset-dependent metrics such as Recall@FAR. The resulting prospective recall estimates are consequently based on 257 valid failure episodes rather than all TEST failures. This annotation constraint limits the population on which operational early-warning behavior can be assessed.

### D. Provenance Reconstruction Fragility

The provenance-repair pipeline contains a fallback onset-mapping mechanism that matches messages using role and content when timestamp information is unavailable. Source inspection identified a structural fragility in this fallback: structurally identical messages can produce multiple matches, while the current logic does not explicitly flag such ambiguity. The number of episodes affected by this condition has not yet been quantified against the reconstructed dataset. Therefore, this issue is treated as a potential provenance limitation rather than as a measured source of error in the reported results.

### E. Model and Evaluation Scope

The present evaluation is restricted to the implemented baseline models and the evaluated Mode A prospective-warning setting. The semantic/LLM monitor (L) remains unimplemented, and therefore no conclusions can be drawn about its prospective performance. Similarly, Mode B (τ²-Bench) is not used here to support prospective Recall@FAR claims, because it does not provide the same onset-boundary semantics required for that metric.

### F. Statistical and Interpretive Scope

The statistical comparisons were based on 257 valid TEST failure episodes using a paired episode-cluster bootstrap with 1,000 iterations and Holm-Bonferroni correction. The resulting significance findings should therefore be interpreted within the evaluated population and predefined comparison framework rather than as evidence of universal model superiority. In particular, S1's statistically significant advantages were selective rather than universal, and the feature-ablation results establish associations between feature groups and observed performance rather than causal relationships.

## VI. Conclusion

This study evaluated prospective failure detection from trajectory-prefix information under an explicit separation between pre-onset prediction and post-onset alerting. Across the evaluated baseline models, discrimination was limited, with AUROC values ranging from 0.5074 to 0.6371. S1 achieved the highest observed AUROC and demonstrated statistically significant advantages over S2, H2, and H3 under the predefined paired episode-cluster bootstrap protocol, but these advantages were selective rather than universal.

The results also reveal an important distinction between statistical discrimination and operational early-warning utility. Under a target FAR of 5%, prospective Recall@FAR was near zero across the evaluated models. Relaxing the S1 target FAR to 10% increased Recall@FAR to 0.0973, illustrating the sensitivity of operational performance to the false-alarm constraint. The feature-ablation results further indicate that error and retry signals are strongly associated with the observed discrimination performance of S1, although the ablation design does not establish a causal relationship.

Separately analyzing post-onset alerts showed that H3 produced substantially more late-alert activity than the other evaluated models, with 19.84% of valid failure episodes receiving only late alerts. This reinforces the importance of enforcing the onset boundary when evaluating agent failure prediction; retrospective diagnostic activity should not be conflated with prospective warning capability.

Overall, the findings support a cautious conclusion: the evaluated trajectory-prefix features contain limited information about eventual task failure, but translating that information into reliable early warning under strict false-alarm constraints remains unresolved. Future work should address the limited reconstructed population, incomplete onset annotations, provenance-mapping robustness, and broader model and benchmark coverage before stronger claims about generalization or operational deployment can be made.

## References

[1] X. Liu et al., "AgentBench: Evaluating LLMs as Agents," arXiv preprint arXiv:2308.03688, 2023. 
[2] "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents," arXiv preprint, 2024. 
[3] "GAIA: a benchmark for General AI Assistants," arXiv preprint, 2023. 
[4] "TRAIL: A diagnostic taxonomy for evaluating agent failures," arXiv preprint, 2024. 
[5] "AgentRx: Post-hoc localization of critical failure steps," arXiv preprint arXiv:2602.02475, 2026. 
[6] "Who&When Pro: Retrospective attribution of agent trajectories," arXiv preprint arXiv:2607.09996, 2026. 
[7] "PrefixGuard: Prospective warning monitors," arXiv preprint arXiv:2605.06455, 2026. 
[8] "AgentForesight: Online auditing of agent risk," arXiv preprint arXiv:2605.08715, 2026. 
[9] "Trajectory Guard: Real-time sequence anomaly detection," arXiv preprint arXiv:2601.00516, 2026.
