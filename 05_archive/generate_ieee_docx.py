"""
generate_ieee_docx.py
---------------------
Generates the IEEE Conference Word Document (.docx) for AIRE-Trace
strictly following IEEE Conference template specifications.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START

from ieee_docx_helpers import (
    set_page_setup, set_columns, add_title, add_metadata_line, add_author_grid,
    add_abstract, add_keywords, add_heading_1, add_heading_2, add_heading_3,
    add_body, add_bullet_item, add_figure, add_table_header_caption,
    add_table_note, add_custom_table, add_reference_item
)

def build_manuscript():
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # SECTION 0: Full-Width Title & Author Header (1 Column)
    # -------------------------------------------------------------
    sec0 = doc.sections[0]
    set_page_setup(sec0)
    set_columns(sec0, num_cols=1, space_twips=0)
    
    add_title(doc, "AIRE-Trace: A Standardized Prospective Evaluation Protocol for Online Agent-Failure Warning")
    add_metadata_line(doc, "Submitted to: [IEEE CONFERENCE NAME — TO BE SELECTED]")
    add_metadata_line(doc, "Submission Date: [SUBMISSION DATE — TO BE DETERMINED]")
    add_author_grid(doc)
    
    # -------------------------------------------------------------
    # SECTION 1: Two-Column IEEE Body
    # -------------------------------------------------------------
    sec1 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    set_page_setup(sec1)
    set_columns(sec1, num_cols=2, space_twips=360) # 0.25 in gutter
    
    # Abstract & Keywords
    abstract_text = (
        "The increasing deployment of autonomous agentic systems creates demand for mechanisms "
        "that provide prospective warning of task failure from partial execution trajectories, "
        "rather than retrospectively diagnosing failure after it occurs. Prior work on online "
        "agent-failure warning (including PrefixGuard, AgentForesight, and Trajectory Guard) has "
        "demonstrated that prefix-based failure prediction is a viable research direction, but these "
        "methods each use their own datasets, prefix definitions, calibration procedures, and metrics. "
        "Consequently, comparative claims across method families are difficult to interpret.\n\n"
        "This paper presents AIRE-Trace: a standardized, prospective, prefix-only evaluation protocol "
        "for online agent-failure warning that fixes information visibility, failure-target definition, "
        "alert semantics, calibration procedure, false-alarm constraints, lead-time measurement, and "
        "compute accounting. The protocol is applied to representative heuristic (H1--H4), classical "
        "machine-learning (M1), and sequence-model (S1, S2) warning methods on the TerminalBench "
        "trajectory corpus.\n\nThe study population consists of 636 reconstructed episodes -- 19.18% of "
        "3,316 declared source rows -- split task-disjointly into TRAIN (163 episodes), CALIBRATION "
        "(57 episodes), and TEST (416 episodes). Of 317 failed TEST episodes, 257 carried usable "
        "failure-onset annotations sufficient for prospective evaluation. Across seven evaluated models "
        "at checkpoint horizon K=30, Mode A (TerminalBench) AUROC ranged from 0.5074 to 0.6371. "
        "S1 (Random Forest) achieved the highest observed AUROC (0.6371, 95% CI [0.5885, 0.6745]). "
        "Under a 5% false-alarm rate (FAR) constraint, prospective Recall@FAR was near zero across "
        "all evaluated models. Paired episode-cluster bootstrap testing (B=1,000, Holm--Bonferroni "
        "correction) showed S1 had statistically significant AUROC advantages over S2, H2, and H3, "
        "but not over M1, H1, or H4. For AUPRC, S1's advantage was statistically significant only "
        "against S2. Feature ablation identified that removing error and retry signals "
        "(feat_tool_error_count and feat_retry_count) produced the largest observed discrimination "
        "degradation (Delta_AUROC = -0.1069). The overall Pairwise Direction Consistency (PDC) across "
        "21 informative pairs was 0.8294 (coverage 0.881). These findings indicate that available "
        "trajectory-prefix structural features contain limited prospective failure information under "
        "strict operational false-alarm constraints, and that comparative rankings are partially "
        "but not universally stable across metrics."
    )
    add_abstract(doc, abstract_text)
    
    keywords_text = "Agentic systems, failure warning, prospective evaluation, trajectory analysis, standardized benchmarking, online monitoring, calibration, bootstrap inference."
    add_keywords(doc, keywords_text)
    
    # -------------------------------------------------------------
    # I. INTRODUCTION
    # -------------------------------------------------------------
    add_heading_1(doc, "I. Introduction")
    
    add_heading_2(doc, "A. Motivation")
    add_body(doc, "The widespread deployment of autonomous agentic systems has raised new reliability questions that standard outcome benchmarking cannot fully answer. Benchmarks such as AgentBench [1], AgentBoard [2], and GAIA [3] measure whether an agent ultimately succeeds or fails on a task. This final-outcome evaluation is necessary but insufficient for monitoring purposes: by the time the outcome is observed, the agent has already consumed resources and potentially caused unrecoverable side effects.")
    add_body(doc, "Prospective failure warning addresses a different and complementary question: given only the portion of the trajectory observed so far (a prefix), can a monitor produce a timely alert that the episode will likely fail before the outcome is known? This early-warning capability would enable intervention -- pausing the agent, escalating to human review, or switching strategies -- before failure becomes irreversible.")
    
    add_heading_2(doc, "B. Prior Work and the Comparative Gap")
    add_body(doc, "Recent work has shown that prefix-based failure prediction is achievable. PrefixGuard [7] achieves AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its own evaluation protocol, demonstrating that prefix-based monitoring is feasible across multiple benchmarks. Direct numerical comparison with AIRE-Trace results is not appropriate due to differences in prefix representation, feature regime, and calibration protocol. AgentForesight [8] employs a reinforcement-learning-trained 7B online auditor for risk estimation. Trajectory Guard [9] applies real-time sequence anomaly detection to agent trajectories. These methods collectively establish that prospective warning from partial trajectories is a viable line of research with documented discriminative capability.")
    add_body(doc, "However, these methods each use their own datasets, prefix definitions, calibration procedures, evaluation metrics, and operating points. No existing work cross-compares heuristic, classical machine-learning, and sequence-model warning methods under one fixed protocol. Consequently, it is unclear whether reported comparative advantages between method families in individual papers are robust to a common evaluation protocol, or are partially artifacts of differing evaluation conditions.")
    
    add_heading_2(doc, "C. AIRE-Trace Contribution")
    add_body(doc, "AIRE-Trace does not propose a new detector architecture and does not claim that prospective warning itself is novel. Instead, it addresses a different methodological question: given that prospective warning is achievable in principle, how should comparative warning capability be evaluated when methods must operate under a fixed, deployment-relevant false-alarm budget?")
    add_body(doc, "The specific contribution is a standardized, prospective, prefix-only evaluation protocol for online agent-failure warning -- fixing information visibility (pre-onset prefix only), failure-target definition, alert semantics, calibration procedure, false-alarm constraints, lead-time measurement, and compute accounting -- applied to representative warning methods under a common harness.")
    add_body(doc, "The conceptual boundary distinguishing this work from adjacent approaches is clear:")
    add_bullet_item(doc, "**Attribution approaches** (e.g., AgentRx [5], Who&When Pro [6]) ask: where or why did this already-failed run go wrong? They are retrospective and require the full trajectory.")
    add_bullet_item(doc, "**Warning approaches** (e.g., PrefixGuard, AgentForesight) ask: what is the probability of eventual failure, given only the prefix, while the outcome remains unknown? They are prospective.")
    add_bullet_item(doc, "**AIRE-Trace** asks: do comparative performance claims for warning methods remain consistent when those methods are evaluated under identical constraints? It is an evaluation-protocol contribution, not a new warning method.")
    
    add_heading_2(doc, "D. Research Question")
    add_body(doc, "This study investigates: *Do comparative performance claims for online agent-failure warning methods remain consistent when different methods are evaluated under identical information, target, alert, calibration, lead-time, and compute constraints?*")
    
    add_heading_2(doc, "E. Experimental Scope")
    add_body(doc, "The evaluation uses 636 reconstructed episodes split task-disjointly into TRAIN (163), CALIBRATION (57), and TEST (416). Seven baseline methods are evaluated in Mode A using trajectory prefixes up to K=30 steps.")
    
    add_heading_2(doc, "F. Main Empirical Findings")
    add_bullet_item(doc, "Mode A AUROC ranged from 0.5074 (H3) to 0.6371 (S1).")
    add_bullet_item(doc, "S1 achieved the highest observed AUROC but was not universally statistically superior.")
    add_bullet_item(doc, "Under a 5% FAR constraint, prospective Recall@FAR was near zero across all models.")
    add_bullet_item(doc, "Error and retry signals showed the strongest association with discrimination capability (Delta_AUROC = -0.1069 at A4 ablation).")
    add_bullet_item(doc, "PDC = 0.8294 (coverage = 0.881) indicates partially consistent but not universally stable rankings.")
    
    add_heading_2(doc, "G. Contributions Summary")
    add_bullet_item(doc, "1. A standardized, auditable, prospective evaluation protocol for online agent-failure warning enforcing FAR <= 5%, episode-level evaluation semantics, and onset-boundary enforcement.")
    add_bullet_item(doc, "2. An empirical comparison of seven representative warning methods under the common protocol on a reconstructed trajectory corpus.")
    add_bullet_item(doc, "3. A Gate 6 operational analysis distinguishing prospective early-warning recall from post-onset late-detection activity.")
    add_bullet_item(doc, "4. A component-level feature ablation study (A0--A6) identifying the association between structural trace signals and discrimination performance.")
    add_bullet_item(doc, "5. A Pairwise Direction Consistency (PDC) analysis of metric-ranking stability.")
    add_bullet_item(doc, "6. Transparent reporting of provenance-repair limitations and population coverage constraints.")
    
    # -------------------------------------------------------------
    # II. RELATED WORK
    # -------------------------------------------------------------
    add_heading_1(doc, "II. Related Work")
    
    add_heading_2(doc, "A. Agent Outcome Benchmarking")
    add_body(doc, "Outcome benchmarks [1][2][3] establish performance baselines for agent capabilities but do not provide mechanisms for prospective mid-execution monitoring. TRAIL [4] articulates the need for robust evaluation methods for agentic workflow traces, introduces a formal taxonomy of error types, and presents 148 human-annotated traces for trace-debugging evaluation.")
    
    add_heading_2(doc, "B. Retrospective Failure Attribution")
    add_body(doc, "Post-hoc failure attribution methods identify where or why a trajectory went wrong after failure has occurred. AgentRx [5] provides post-hoc localization of critical failure steps. Who&When Pro [6] addresses retrospective attribution using 12,326 trajectories with controlled failure injection. By construction, these approaches require the complete trajectory and ground-truth failure state and cannot produce warnings during execution.")
    add_body(doc, "AgentProcessBench [11] introduces step-level quality evaluation using 1,000 trajectories and 8,509 human-labeled step annotations (ternary: correct/neutral/erroneous). These step-quality labels require the complete trajectory with known outcome and are retrospective by construction.")
    
    add_heading_2(doc, "C. Prospective Agent-Failure Warning")
    add_body(doc, "PrefixGuard [7] demonstrates prefix-based warning monitors, achieving AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its own evaluation protocol with typed-step adapters. Direct numerical comparison with AIRE-Trace results is not appropriate due to differences in prefix representation, feature regime, and calibration protocol; both studies use TerminalBench, but under distinct evaluation conditions. AgentForesight [8] employs an RL-trained 7B-parameter auditor. Trajectory Guard [9] applies real-time sequence anomaly detection.")
    add_body(doc, "These works establish prospective prefix-based warning as a viable research direction, but each operates in isolation. No existing work cross-compares heuristic, classical-ML, sequence-model, and LLM-monitor warning methods under one fixed protocol.")
    add_body(doc, "Advani [10] characterizes false success in LLM agents across 9,876 tau2-Bench and 1,879 AppWorld trajectories, showing that lightweight TF-IDF detectors achieve AUROC 0.83-0.95 for false-success detection while LLM judges fail to exceed AUROC 0.65 on tau2-Bench. This work addresses task-completion monitoring rather than mid-trajectory prospective warning.")
    
    add_heading_2(doc, "D. Evaluation Methodology for Sequential Predictions")
    add_body(doc, "Prefix-level predictions exhibit within-episode dependence because prefixes from the same episode share the outcome label. Episode-cluster bootstrapping is the appropriate procedure when the observational unit is the episode rather than the individual prefix.")
    add_body(doc, "Cameron, Gelbach, and Miller [12] establish the pairs cluster bootstrap as the appropriate inference procedure when observations are dependent within clusters; resampling entire clusters (episodes in our case) rather than individual observations (prefixes) preserves the within-cluster correlation structure.")
    add_body(doc, "Holm [13] introduced the sequentially rejective multiple test procedure for step-down control of the familywise error rate without requiring independence among tests.")
    
    # -------------------------------------------------------------
    # III. PROBLEM FORMULATION
    # -------------------------------------------------------------
    add_heading_1(doc, "III. Problem Formulation")
    
    add_heading_2(doc, "A. Agent Trajectory and Episode")
    add_body(doc, "An agent episode consists of a sequence of events e1, e2, ..., eT produced by an autonomous agent executing a task. Each event contains role information (agent, tool, user, system), action type (message, tool call, tool result), tool names, error indicators, and other structural metadata. The episode has an eventual outcome: eventual_success or eventual_failure.")
    
    add_heading_2(doc, "B. Failure Onset")
    add_body(doc, "For TerminalBench episodes, failure onset is defined by the earliest identified incorrect step: t_onset = min(incorrect_step_ids). If this field is absent or empty, the episode is onset-unannotated and excluded from onset-dependent prospective metrics (Recall@FAR, lead time) while remaining eligible for ranking metrics (AUROC, AUPRC, Brier, ECE).")
    
    add_heading_2(doc, "C. Prefix and Checkpoint")
    add_body(doc, "At checkpoint t in {1, ..., min(Ti, K)}, a monitor accesses only the prefix (e1, ..., et). The checkpoint schedule is outcome-independent and episode-symmetric. An alert at checkpoint t is valid (prospective) if and only if t <= t_onset. An alert at t > t_onset is a late detection; it does not constitute actionable early warning. Late detections are reported separately in the operational analysis and excluded from Recall@FAR.")
    
    add_heading_2(doc, "D. Warning Formulation")
    add_body(doc, "Given a prefix at checkpoint t, a monitor produces a risk score s(e1,...,et) in [0,1]. An alert is raised when s >= tau for a calibrated threshold tau. Episode-level False Alarm Rate (FAR), with denominator equal to successful TEST episodes, is formulated as: FAR = |{i : success(i), exists t: alert raised}| / |{i : success(i)}|.")
    add_body(doc, "The conceptual flow of the overall architecture is illustrated in Fig. 1.")
    add_figure(doc, "figures/ieee/fig1_aire_trace_architecture.png", 1, 
               "AIRE-Trace standardized prospective evaluation pipeline. Trajectories are provenance-audited before episode-level splitting; trainable methods are fitted on TRAIN, operating thresholds are selected on CALIBRATION under the false-alarm constraint, and frozen thresholds are applied to the TEST population for prospective evaluation and operational analysis.", width_inches=3.4)
    
    add_heading_2(doc, "E. Evaluation Modes")
    add_body(doc, "**Mode A -- Prospective-Warning Evaluation:** Conducted on TerminalBench (failure-onset annotations present). Supports AUROC, AUPRC, Brier, ECE, prospective Recall@FAR, lead time, and late-detection analysis. Primary reported mode.")
    add_body(doc, "**Mode B -- Eventual-Outcome Diagnostic:** Conducted on tau2-Bench (no onset annotations). Reports eventual-outcome ranking metrics only (AUROC, AUPRC, Brier, ECE, Raw Recall). Does NOT support prospective Recall@FAR. Mode B metrics must not be compared directly to Mode A metrics.")
    
    # -------------------------------------------------------------
    # IV. DATASET, PROVENANCE, AND STUDY POPULATION
    # -------------------------------------------------------------
    add_heading_1(doc, "IV. Dataset, Provenance, and Study Population")
    
    add_heading_2(doc, "A. Source Corpus")
    add_body(doc, "Primary corpus: Tracebench (Contextbench/Tracebench) -- 3,316 declared source rows, AI agent coding-task trajectory recordings. Secondary corpus (Mode B only): tau2-Bench (sierra-research/tau-bench) -- 1,980 episodes, 115 tasks, outcome-only (no onset annotations).")
    add_body(doc, "Canonical Outcome Mapping (Protocol Rule 10): reward == 1.0 / solved == True maps to eventual_success; reward == 0.0 / solved == False maps to eventual_failure.")
    
    add_heading_2(doc, "B. Provenance-Repair Process")
    add_body(doc, "State transitions applied to 3,316 declared rows (sources: post_recovery_audit.txt, lineage_verification.txt): 636 rows retained (verified_existing) with valid mini.traj.json artifact present; 2,655 rows excluded (structurally_invalid) due to mini.traj.json absent after artifact inspection; 25 rows excluded (missing_artifact_path) due to missing source metadata.")
    add_body(doc, "Recovery investigation: 1,457 previously network-excluded artifacts were successfully downloaded. Upon inspection, 100% were structurally invalid (mini.traj.json absent). Net addition to valid population: 0. Final valid population: 636 episodes (19.18% of 3,316 declared rows). All downstream results are valid for this 636-episode population only.")
    
    add_heading_2(doc, "C. Sanitization")
    add_body(doc, "Terminal event content is replaced with a redaction marker before any feature extraction. Outcome keys are stripped from trace feature inputs (Protocol Rule 6). The provenance and exclusion accounting leading to this subset is detailed in Fig. 2.")
    add_figure(doc, "figures/ieee/fig2_provenance_recovery.png", 2, 
               "Provenance and exclusion accounting for the AIRE-Trace empirical population. The downstream study is restricted to the canonical 636-episode population for which the required trajectory evidence was verified or deterministically reconstructed.", width_inches=3.4)
    
    add_heading_2(doc, "D. Train/Calibration/Test Split")
    add_body(doc, "Splits are assigned strictly at the episode level across three disjoint sets (TRAIN, CALIBRATION, TEST) to prevent prefix-level leakage. Table I summarizes the population accounting.")
    
    add_table_header_caption(doc, "I", "Study Population Accounting")
    t1_headers = ["Quantity", "Count", "Source"]
    t1_rows = [
        ["Declared Tracebench rows", "3,316", "post_recovery_audit.txt"],
        ["Valid reconstructed episodes", "636", "post_recovery_audit.txt"],
        ["Structurally invalid", "2,655", "post_recovery_audit.txt"],
        ["Missing artifact path", "25", "post_recovery_audit.txt"],
        ["Coverage (636/3,316)", "19.18%", "Computed"],
        ["TRAIN episodes", "163", "gate7_ablation.json (A0)"],
        ["CALIBRATION episodes", "57", "gate7_ablation.json (A0)"],
        ["TEST episodes", "416", "primary_k30_results.json"],
        ["TEST: failed episodes", "317", "primary_k30_results.json"],
        ["TEST: successful episodes", "99", "416 - 317"],
        ["TEST: valid annotated failures", "257", "primary_k30_results.json"],
        ["TEST: unannotated failures", "60", "primary_k30_results.json"]
    ]
    add_custom_table(doc, t1_headers, t1_rows, col_widths=[1.6, 0.6, 1.2],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    
    # -------------------------------------------------------------
    # V. AIRE-TRACE EVALUATION PROTOCOL
    # -------------------------------------------------------------
    add_heading_1(doc, "V. AIRE-Trace Evaluation Protocol")
    
    add_heading_2(doc, "A. Feature Set (13 Category-A Features)")
    add_body(doc, "Thirteen category-A structural features computable identically across trajectories were extracted: cumulative step count (feat_steps_so_far), actor roles (agent, tool, user, system), action types (message, tool call, tool result), cumulative tool error count (feat_tool_error_count), consecutive error retry count (feat_retry_count), distinct tools used (feat_unique_tools_used), tool call ratio (feat_tool_call_ratio), and repeated action indicator in the last 2 steps (feat_repeated_action_last2).")
    
    add_heading_2(doc, "B. Checkpoint Policy")
    add_body(doc, "Checkpoints t in {1, ..., min(Ti, K)}, K = 30. The policy is outcome-independent and episode-symmetric. The monitor accesses only events e1,...,et at inference time.")
    
    add_heading_2(doc, "C. Episode-Balanced Weighting")
    add_body(doc, "Weights w_{i,t} = 1 / min(Ti, K) ensure that each episode contributes equally to prefix-level metric computation regardless of trajectory length.")
    
    add_heading_2(doc, "D. Threshold Calibration")
    add_body(doc, "We select tau* = argmax_tau Recall(tau) subject to FAR_calib(tau) <= target_FAR, on CALIBRATION split only. Ties are resolved by lower FAR, then higher threshold. tau* is frozen; the TEST set is never examined before threshold freeze. Target FAR for the primary evaluation is 5% (0.05). Frozen thresholds obtained: H1 = 0.86, H2 = 0.89, H3 = 0.01, H4 = 0.93, M1 = 0.98, S1 = 0.97, S2 = 0.74. For H3, calibration FAR reached 1.000, making its Recall@FAR undefined (NaN) on TEST.")
    
    add_heading_2(doc, "E. Evaluation Metrics")
    add_body(doc, "Metrics include prefix-level ranking (AUROC, AUPRC, Brier Score, ECE) with episode-balanced weights, and episode-level operational metrics (FAR with N=99 denominator, Recall@FAR with N=257 denominator). Prospective prefix evaluation semantics are visualized in Fig. 3.")
    add_figure(doc, "figures/ieee/fig3_prospective_prefix.png", 3, 
               "Prospective prefix evaluation semantics. At each permitted checkpoint, the monitor observes only the trajectory information available up to that point. Alerts at or before the annotated failure onset are prospective detections; alerts after onset are analyzed separately as late detections.", width_inches=3.4)
    
    # -------------------------------------------------------------
    # VI. WARNING METHODS AND IMPLEMENTATION
    # -------------------------------------------------------------
    add_heading_1(doc, "VI. Warning Methods and Implementation")
    
    add_heading_2(doc, "A. Heuristic Monitors (H1--H4) -- Training-Free")
    add_body(doc, "H1 (Tool-Error Rate): Min-max normalized feat_tool_error_count. H2 (Retry-Count): Min-max normalized feat_retry_count. H3 (Repeated-Action): Min-max normalized feat_repeated_action_last2. H4 (Combined Heuristic): Sigmoid of average z-score across error, retry, and repeated action features, parameterized on TRAIN.")
    
    add_heading_2(doc, "B. Classical Machine Learning Monitor (M1)")
    add_body(doc, "M1 (Logistic Regression): scikit-learn LogisticRegression (C=1.0, lbfgs, max_iter=1000, random_state=42) over 13 Category-A features with StandardScaler normalization, fitted on TRAIN with episode-balanced weights.")
    
    add_heading_2(doc, "C. Sequence Monitor S1 -- Random Forest")
    add_body(doc, "S1 (Random Forest): scikit-learn RandomForestClassifier (n_estimators=100, max_depth=6, min_samples_split=5, random_state=42) over 13 features without scaling. (Classified as Sequence S1 by registry conventions).")
    
    add_heading_2(doc, "D. Sequence Monitor S2 -- GRU")
    add_body(doc, "S2 (GRU): PyTorch GRU network (hidden_dim=64, 1 layer, lr=1e-3, epochs=10, batch_size=128, cpu, seed=42) trained with BCEWithLogitsLoss.")
    
    add_heading_2(doc, "E. Placeholder Model L")
    add_body(doc, "Model L (Semantic/LLM Monitor) was registered but not empirically evaluated due to hardware constraints (RTX 2050, 4GB VRAM). Table II summarizes the baseline definitions.")
    
    add_table_header_caption(doc, "II", "Warning Method Definitions")
    t2_headers = ["Model", "Family", "Method", "Key Parameters"]
    t2_rows = [
        ["H1", "Heuristic", "Tool-error rate monitor", "Min-max feat_tool_error_count"],
        ["H2", "Heuristic", "Retry-count monitor", "Min-max feat_retry_count"],
        ["H3", "Heuristic", "Repeated-action monitor", "Min-max feat_repeated_action_last2"],
        ["H4", "Heuristic", "Combined heuristic", "sigmoid(z-score avg, 3 features)"],
        ["M1", "Classical", "Logistic Regression", "C=1.0, lbfgs, StandardScaler, seed=42"],
        ["S1", "Sequence*", "Random Forest", "n_estimators=100, max_depth=6, seed=42"],
        ["S2", "Sequence", "GRU", "hidden_dim=64, 1 layer, epochs=10, seed=42"],
        ["L", "Semantic", "LLM Monitor", "NOT EVALUATED (hardware constraint)"]
    ]
    add_custom_table(doc, t2_headers, t2_rows, col_widths=[0.5, 0.7, 1.1, 1.1],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])
    add_table_note(doc, "*S1 classified Sequence by registry; implemented as Random Forest tabular ensemble.")
    
    # -------------------------------------------------------------
    # VII. EXPERIMENTAL PROTOCOL AND STATISTICAL ANALYSIS
    # -------------------------------------------------------------
    add_heading_1(doc, "VII. Experimental Protocol and Statistical Analysis")
    
    add_heading_2(doc, "A. Experimental Setup")
    add_body(doc, "All experiments used random seed 42. The MasterEvaluator class programmatically enforces prefix-horizon cutoff at K=30, post-onset exclusion from Recall@FAR denominator, episode-balanced weighting, CALIBRATION-only threshold selection, and runtime leakage guards.")
    
    add_heading_2(doc, "B. Bootstrap Confidence Intervals")
    add_body(doc, "Paired episode-cluster bootstrap with B = 1,000 iterations resampled entire episodes with replacement to preserve within-cluster correlation. Prefix-level resampling was strictly prohibited to avoid pseudo-replication.")
    
    add_heading_2(doc, "C. Statistical Hypothesis Testing")
    add_body(doc, "Hypothesis tests evaluated S1 vs. {M1, S2, H1, H2, H3, H4} for AUROC and AUPRC (12 comparisons). Null-centered bootstrap distributions were tested with Holm--Bonferroni step-down correction (alpha = 0.05).")
    
    add_heading_2(doc, "D. Pairwise Direction Consistency (PDC)")
    add_body(doc, "For each model pair across AUROC, AUPRC, Recall@FAR, and ECE, PDC measured the proportion of non-tied comparisons agreeing on the majority direction, paired with coverage.")
    
    add_heading_2(doc, "E. Feature Ablation Design")
    add_body(doc, "Ablation conditions (A0--A6) isolated component contributions: A1 (steps), A2 (roles), A3 (actions), A4 (errors/retries), A5 (tools), A6 (repeated actions).")
    
    # -------------------------------------------------------------
    # VIII. RESULTS
    # -------------------------------------------------------------
    add_heading_1(doc, "VIII. Results")
    
    add_heading_2(doc, "A. Primary Mode A TEST Performance (K=30, target FAR 5%)")
    add_body(doc, "Table III reports Mode A prospective performance on TEST (N=416). S1 achieved the highest AUROC (0.6371), while H3 achieved 0.5074. Under 5% target FAR, Recall@FAR collapsed to near zero for all models.")
    
    add_table_header_caption(doc, "III", "Primary Mode A TEST Performance (K=30, Target FAR 5%)")
    t3_headers = ["Model", "AUROC", "95% CI", "AUPRC", "95% CI", "Recall@FAR", "95% CI", "FAR", "Brier", "ECE", "tau"]
    t3_rows = [
        ["H1", "0.6205", "[0.5799, 0.6513]", "0.8371", "[0.7894, 0.8674]", "0.0000", "[0.0000, 0.0000]", "0.0000", "0.6186", "0.6622", "0.86"],
        ["H2", "0.5752", "[0.5402, 0.6116]", "0.8329", "[0.7799, 0.8702]", "0.0000", "[0.0000, 0.0000]", "0.0000", "0.7034", "0.7223", "0.89"],
        ["H3", "0.5074", "[0.5024, 0.5122]", "0.8702", "[0.8476, 0.8927]", "UNDEF", "(see note)", "1.0000", "0.2885", "0.2885", "0.01"],
        ["H4", "0.6135", "[0.5729, 0.6445]", "0.8346", "[0.7866, 0.8647]", "0.0000", "[0.0000, 0.0000]", "0.0202", "0.2644", "0.2794", "0.93"],
        ["M1", "0.6215", "[0.5630, 0.6629]", "0.8331", "[0.7796, 0.8659]", "0.0078", "[0.0000, 0.0195]", "0.0303", "0.1767", "0.0140", "0.98"],
        ["S1", "0.6371", "[0.5885, 0.6745]", "0.8452", "[0.8020, 0.8761]", "0.0000", "[0.0000, 0.0000]", "0.0404", "0.1746", "0.0124", "0.97"],
        ["S2", "0.5496", "[0.5212, 0.5734]", "0.8129", "[0.7638, 0.8436]", "0.0000", "[0.0000, 0.0000]", "0.0000", "0.2042", "0.1530", "0.74"]
    ]
    add_custom_table(doc, t3_headers, t3_rows, col_widths=[0.35, 0.35, 0.45, 0.35, 0.45, 0.35, 0.45, 0.3, 0.3, 0.3, 0.25],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT] + [WD_ALIGN_PARAGRAPH.RIGHT]*10)
    add_table_note(doc, "Note: H3 Recall@FAR is undefined (NaN) because calibration FAR reached 1.000 -- the 5% constraint was not achievable on CALIBRATION. Level 1 evidence.")
    
    add_body(doc, "**Mode B results (tau2-Bench, NOT comparable to Mode A):** H1 AUROC=0.5000; H2 AUROC=0.5000; H3 AUROC=0.5027; H4 AUROC=0.5027; M1 AUROC=0.5233; S1 AUROC=0.5029; S2 AUROC=0.5300. Mode B metrics evaluate eventual-outcome risk without onset-boundary semantics and must not be pooled with Mode A.")
    
    add_heading_2(doc, "B. Statistical Hypothesis Tests")
    add_body(doc, "Under the paired episode-cluster bootstrap test (B=1000, Holm--Bonferroni correction), S1 demonstrated statistically significant AUROC advantages over S2, H2, and H3 (p_adj = 0.006 each), but was not statistically distinguishable from M1, H1, or H4. For AUPRC, S1 was significantly higher only against S2. Table V and Fig. 4 present the statistical test outcomes.")
    
    add_table_header_caption(doc, "V", "Statistical Tests (S1 vs. Comparators, B=1000, Holm-Bonferroni)")
    t5_headers = ["Comparison", "Metric", "Delta_obs", "p_raw", "p_adj", "Reject H0 (a=0.05)"]
    t5_rows = [
        ["S1 vs M1", "AUROC", "+0.0156", "0.1588", "0.3177", "No"],
        ["S1 vs S2", "AUROC", "+0.0875", "0.0010", "0.0060", "YES"],
        ["S1 vs H1", "AUROC", "+0.0165", "0.1948", "0.3177", "No"],
        ["S1 vs H2", "AUROC", "+0.0619", "0.0010", "0.0060", "YES"],
        ["S1 vs H3", "AUROC", "+0.1297", "0.0010", "0.0060", "YES"],
        ["S1 vs H4", "AUROC", "+0.0236", "0.0559", "0.1678", "No"],
        ["S1 vs M1", "AUPRC", "+0.0121", "0.0849", "0.4246", "No"],
        ["S1 vs S2", "AUPRC", "+0.0323", "0.0020", "0.0120", "YES"],
        ["S1 vs H1", "AUPRC", "+0.0082", "0.2517", "0.4246", "No"],
        ["S1 vs H2", "AUPRC", "+0.0124", "0.1538", "0.4246", "No"],
        ["S1 vs H3", "AUPRC", "-0.0250", "0.0919", "0.4246", "No"],
        ["S1 vs H4", "AUPRC", "+0.0106", "0.1189", "0.4246", "No"]
    ]
    add_custom_table(doc, t5_headers, t5_rows, col_widths=[0.7, 0.5, 0.5, 0.45, 0.45, 0.8],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER])
    
    add_figure(doc, "figures/ieee/fig4_mode_a_auroc.png", 4, 
               "Mode A TEST AUROC for the evaluated warning methods under the K=30 protocol. Error bars denote the corresponding 95% episode-cluster bootstrap confidence intervals.", width_inches=3.4)
    
    add_heading_2(doc, "C. Pairwise Direction Consistency (PDC)")
    add_body(doc, "Across the seven models (21 pairs), the overall PDC was 0.8294 with coverage 0.881 across 21/21 informative pairs. This indicates that while the majority of ranking directions agree, approximately 17% of informative comparisons display metric disagreement.")
    
    add_heading_2(doc, "D. Operating-Point Sensitivity (S1)")
    add_body(doc, "Evaluating S1 across target FAR constraints: at 1% and 5% target FAR (frozen threshold 0.97), TEST FAR was 0.0404 and Recall@FAR was 0.0000. Relaxing target FAR to 10% (threshold 0.93) yielded TEST FAR = 0.1212 and Recall@FAR = 0.0973. This confirms that early warning recall collapses under strict false-alarm budgets.")
    
    add_heading_2(doc, "E. Feature Ablation Results (S1)")
    add_body(doc, "Table VI reports S1 ablation results. Removing error and retry signals (A4) produced the largest degradation (Delta_AUROC = -0.1069). As shown in Fig. 5, error and retry signals are strongly associated with discrimination, though this design does not establish causality.")
    
    add_table_header_caption(doc, "VI", "Feature Ablation Results (S1, Mode A, K=30)")
    t6_headers = ["ID", "Removed Features", "TEST AUROC", "TEST AUPRC", "Delta_AUROC"]
    t6_rows = [
        ["A0", "None (full baseline)", "0.6371", "0.8452", "0.0000"],
        ["A1", "feat_steps_so_far", "0.6357", "0.8450", "-0.0014"],
        ["A2", "4 actor-role features", "0.6335", "0.8422", "-0.0036"],
        ["A3", "3 action-type features", "0.6383", "0.8477", "+0.0012"],
        ["A4", "feat_tool_error_count + feat_retry_count", "0.5302", "0.7820", "-0.1069"],
        ["A5", "feat_unique_tools_used + feat_tool_call_ratio", "0.6360", "0.8479", "-0.0011"],
        ["A6", "feat_repeated_action_last2", "0.6341", "0.8462", "-0.0030"]
    ]
    add_custom_table(doc, t6_headers, t6_rows, col_widths=[0.3, 1.6, 0.5, 0.5, 0.5],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    
    add_figure(doc, "figures/ieee/fig5_a4_ablation.png", 5, 
               "A4 component ablation under the defined evaluation protocol. The observed AUROC change is reported as an empirical association under the ablation design and does not establish causal attribution.", width_inches=3.4)
    
    # -------------------------------------------------------------
    # IX. OPERATIONAL ANALYSIS (GATE 6)
    # -------------------------------------------------------------
    add_heading_1(doc, "IX. Operational Analysis (Gate 6)")
    
    add_heading_2(doc, "A. Gate 6 Operational Summary")
    add_body(doc, "Table IV and Fig. 6 summarize the Gate 6 operational analysis across false alarms (N=99), late-alert-only failure episodes (N=257), and total alert burden (N=416).")
    
    add_table_header_caption(doc, "IV", "Gate 6 Operational Summary")
    t4_headers = ["Model", "FA Ep", "FAR (N=99)", "Late-Only Ep", "% Valid Fails", "Total Alerts", "Mean/Ep"]
    t4_rows = [
        ["H1", "0", "0.0000", "3", "1.17%", "19", "0.046"],
        ["H2", "0", "0.0000", "2", "0.78%", "16", "0.039"],
        ["H3", "99", "1.0000", "51", "19.84%", "8,012", "19.26"],
        ["H4", "2", "0.0202", "8", "3.11%", "119", "0.286"],
        ["M1", "3", "0.0303", "10", "3.89%", "161", "0.387"],
        ["S1", "4", "0.0404", "16", "6.23%", "25", "0.060"],
        ["S2", "0", "0.0000", "10", "3.89%", "107", "0.257"]
    ]
    add_custom_table(doc, t4_headers, t4_rows, col_widths=[0.4, 0.4, 0.6, 0.5, 0.5, 0.5, 0.5],
                     alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    
    add_figure(doc, "figures/ieee/fig6_gate6_operational.png", 6, 
               "Gate 6 operational analysis showing false alarms, late-alert-only episodes, and alert burden under the frozen TEST evaluation.", width_inches=3.4)
    
    add_heading_2(doc, "B. Late Detections")
    add_body(doc, "An alert at t > t_onset is a late detection; it does not constitute actionable early warning. Model H3 generated 3,339 late alerts across TEST; 51 of 257 valid failure episodes (19.84%) received only late alerts. For S1, 16/257 (6.23%) received only late alerts.")
    
    add_heading_2(doc, "C. False Alarms")
    add_body(doc, "H1, H2, and S2 produced 0 false alarms (FAR = 0.0000). H4 produced 2 (0.0202), M1 produced 3 (0.0303), and S1 produced 4 false alarms (FAR = 0.0404), safely within the 5% target budget. In contrast, H3 alerted on 99/99 successful episodes (FAR = 1.0000).")
    
    add_heading_2(doc, "D. Alert Burden")
    add_body(doc, "Across all 416 TEST episodes, S1 generated only 25 total alerts (mean 0.060 per episode, max 2), representing the lowest alert burden among models generating prospective detections. H3 generated 8,012 alerts (mean 19.26 per episode, max 28).")
    
    # -------------------------------------------------------------
    # X. DISCUSSION
    # -------------------------------------------------------------
    add_heading_1(doc, "X. Discussion")
    
    add_heading_2(doc, "A. The Operational Recall Collapse")
    add_body(doc, "The near-zero prospective Recall@FAR across all models demonstrates that while models can separate failures from successes probabilistically over a population, translating weak-to-moderate ranking signals (AUROC 0.50--0.63) into thresholded prospective alerts under strict false-alarm budgets remains unresolved.")
    
    add_heading_2(doc, "B. Selective Superiority of S1")
    add_body(doc, "S1's statistically certified advantages cover only {S2, H2, H3}. Its advantages over M1, H1, and H4 are not statistically significant after Holm correction. S1's superiority is selective rather than universal.")
    
    add_heading_2(doc, "C. Association Between Error Signals and Discrimination")
    add_body(doc, "Ablation condition A4 established a strong association between error/retry signals and discrimination performance (Delta_AUROC = -0.1069). Whether these signals provide early warning or reflect symptoms proximate to failure onset cannot be answered by ablation alone.")
    
    add_heading_2(doc, "D. Prospective Warning vs. Retrospective Diagnosis")
    add_body(doc, "H3's profile (FAR = 1.0000, 19.84% late-alert-only) demonstrates why prospective evaluation must strictly enforce onset boundaries. High alert volume does not equate to actionable early warning.")
    
    # -------------------------------------------------------------
    # XI. LIMITATIONS AND THREATS TO VALIDITY
    # -------------------------------------------------------------
    add_heading_1(doc, "XI. Limitations and Threats to Validity")
    
    add_heading_2(doc, "A. Population Coverage")
    add_body(doc, "The evaluation is restricted to 636 usable reconstructed episodes from 3,316 declared rows (19.18% coverage). The 2,680 excluded rows lacked required trajectory artifacts. Representativeness of the full source corpus is not established; findings must not be generalized beyond this subset.")
    
    add_heading_2(doc, "B. Incomplete Onset Annotation")
    add_body(doc, "60 of 317 TEST failure episodes lacked usable onset annotations, limiting onset-dependent evaluations to 257 valid failures.")
    
    add_heading_2(doc, "C. Provenance Mapping Fragility")
    add_body(doc, "Fallback onset-mapping based on role and content matching may exhibit multi-match ambiguity for identical messages, representing a potential provenance limitation.")
    
    add_heading_2(doc, "D. Model and Evaluation Scope")
    add_body(doc, "Model L was not evaluated due to hardware constraints. Evaluation was restricted to Mode A; Mode B metrics cannot be compared directly.")
    
    # -------------------------------------------------------------
    # XII. REPRODUCIBILITY AND AUDITABILITY
    # -------------------------------------------------------------
    add_heading_1(doc, "XII. Reproducibility and Auditability")
    
    add_heading_2(doc, "A. Protocol Implementation & Determinism")
    add_body(doc, "All experiments used random seed 42. The MasterEvaluator pipeline enforces K=30 horizon, post-onset exclusion, episode-balanced weighting, CALIBRATION-only threshold selection, and runtime leakage guards. All 38 protocol invariant tests in the project test suite pass.")
    
    add_heading_2(doc, "B. Canonical Artifact Inventory")
    add_body(doc, "Key artifacts include: repaired_636_canonical.json (population), primary_k30_results.json (Mode A/B results), baseline_comparison_table.csv (full results with CIs), pdc_summary.json (ranking consistency), gate7_ablation.json (ablation A0--A6), and gate7_statistical_tests.json (hypothesis tests).")
    
    # -------------------------------------------------------------
    # XIII. CONCLUSION
    # -------------------------------------------------------------
    add_heading_1(doc, "XIII. Conclusion")
    add_body(doc, "This study evaluated prospective failure warning from trajectory-prefix information under an explicit separation between pre-onset prediction and post-onset alerting. Across seven evaluated models at K=30, Mode A AUROC ranged from 0.5074 to 0.6371. S1 achieved the highest observed AUROC and demonstrated statistically significant advantages over S2, H2, and H3, but these advantages were selective rather than universal. Under a 5% FAR constraint, prospective Recall@FAR collapsed to near zero across all models. Feature ablation identified error and retry signals as strongly associated with discrimination. Overall, available trajectory-prefix structural features contain limited failure information, and translating that information into reliable early warning under strict operational false-alarm constraints remains challenging.")
    
    # -------------------------------------------------------------
    # ACKNOWLEDGMENT
    # -------------------------------------------------------------
    add_heading_1(doc, "Acknowledgment")
    add_body(doc, "The authors thank the benchmark authors and maintainers of AgentBench, GAIA, TerminalBench, and tau2-Bench for releasing the execution trajectories and evaluation environments that made this study possible.")
    
    # -------------------------------------------------------------
    # REFERENCES
    # -------------------------------------------------------------
    add_heading_1(doc, "References")
    
    refs = [
        (1, 'X. Liu et al., "AgentBench: Evaluating LLMs as Agents," in Proc. Int. Conf. Learn. Representations (ICLR), 2024. arXiv:2308.03688.'),
        (2, 'C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents," in Proc. Advances in Neural Inf. Process. Syst. (NeurIPS), 2024. arXiv:2401.13178.'),
        (3, 'G. Mialon et al., "GAIA: a benchmark for General AI Assistants," in Proc. Int. Conf. Learn. Representations (ICLR), 2024. arXiv:2311.12983.'),
        (4, 'D. Deshpande et al., "TRAIL: Trace Reasoning and Agentic Issue Localization," arXiv preprint arXiv:2505.08638, 2025.'),
        (5, 'S. Barke et al., "AgentRx: Diagnosing AI Agent Failures from Execution Trajectories," arXiv preprint arXiv:2602.02475, 2026.'),
        (6, 'J. Liu et al., "Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?" arXiv preprint arXiv:2607.09996, 2026.'),
        (7, 'X. Huang et al., "PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors," arXiv preprint arXiv:2605.06455, 2026.'),
        (8, 'B. Zhang et al., "AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems," arXiv preprint arXiv:2605.08715, 2026.'),
        (9, 'L. Advani, "Trajectory Guard: A Lightweight, Sequence-Aware Model for Real-Time Anomaly Detection in Agentic AI," arXiv preprint arXiv:2601.00516, 2026.'),
        (10, 'L. Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents," arXiv preprint arXiv:2606.09863, 2026.'),
        (11, 'S. Fan et al., "AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents," arXiv preprint arXiv:2603.14465, 2026.'),
        (12, 'A. C. Cameron, J. B. Gelbach, and D. L. Miller, "Bootstrap-Based Improvements for Inference with Clustered Errors," Rev. Econ. Stat., vol. 90, no. 3, pp. 414-427, 2008.'),
        (13, 'S. Holm, "A Simple Sequentially Rejective Multiple Test Procedure," Scand. J. Stat., vol. 6, no. 2, pp. 65-70, 1979.')
    ]
    
    for num, txt in refs:
        add_reference_item(doc, num, txt)
        
    out_master = "AIRE-Trace_Universal_IEEE_Conference_Master.docx"
    out_copy = "AIRE-Trace_IEEE_Conference_Paper.docx"
    doc.save(out_master)
    doc.save(out_copy)
    print(f"Successfully generated {out_master} and {out_copy}")

if __name__ == "__main__":
    build_manuscript()
