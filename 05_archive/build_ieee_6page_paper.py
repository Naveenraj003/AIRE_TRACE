"""
build_ieee_6page_paper.py
-------------------------
Compiles the AIRE-Trace IEEE Conference Paper strictly formatted to be UNDER 6 PAGES,
incorporating all 6 clean 300-DPI figures, all 6 tables, all 13 verified references,
and preserving all scientific invariants.
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
    add_abstract, add_keywords, add_h1, add_h2, add_h3, add_p, add_bullet,
    add_fig, add_tbl_header, add_tbl, add_ref
)

def build_paper():
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # SECTION 0: Full-Width Title & Author Header (1 Column)
    # -------------------------------------------------------------
    sec0 = doc.sections[0]
    set_page_setup(sec0)
    set_columns(sec0, num_cols=1, space_twips=0)
    
    add_title(doc, "AIRE-Trace: A Standardized Prospective Evaluation Protocol for Online Agent-Failure Warning")
    add_metadata_line(doc, "Submitted to: [IEEE CONFERENCE NAME — TO BE SELECTED]  |  Submission Date: [SUBMISSION DATE — TO BE DETERMINED]")
    add_author_grid(doc)
    
    # -------------------------------------------------------------
    # SECTION 1: Two-Column IEEE Body
    # -------------------------------------------------------------
    sec1 = doc.add_section(WD_SECTION_START.CONTINUOUS)
    set_page_setup(sec1)
    set_columns(sec1, num_cols=2, space_twips=360) # 0.25 in gutter
    
    # Abstract
    abstract_text = (
        "Early detection of task failure in autonomous agentic systems requires distinguishing prospective "
        "warning signals from information available only post-failure onset. This study introduces AIRE-Trace: "
        "a standardized, prospective, prefix-only evaluation protocol for online agent-failure warning that fixes "
        "information visibility, failure-target definition, alert semantics, calibration under false-alarm constraints, "
        "and compute accounting. Using the reconstructed Tracebench population, we evaluated 636 usable episodes "
        "(19.18% of 3,316 declared source rows) in a task-disjoint train/calibration/test protocol across seven baseline "
        "models (H1–H4, M1, S1, S2) up to checkpoint horizon K=30. Across evaluated models, Mode A AUROC ranged from "
        "0.5074 to 0.6371, with Random Forest (S1) achieving the highest observed AUROC (0.6371, 95% CI [0.5885, 0.6745]). "
        "However, prospective Recall@FAR collapsed to near zero across all models under a strict 5% false-alarm rate (FAR) "
        "constraint. Paired episode-cluster bootstrap testing (B=1,000, Holm–Bonferroni correction) showed S1 had "
        "statistically significant AUROC advantages over S2, H2, and H3, while differences from M1, H1, and H4 were not "
        "statistically significant. Component-level ablation established that removing error and retry signals (A4) "
        "produced the largest observed degradation (Delta_AUROC = -0.1069), indicating an empirical association rather than "
        "causality. Post-onset analysis revealed that heuristic H3 produced 3,339 late alerts, with 19.84% of valid failure "
        "episodes receiving exclusively late alerts. These findings demonstrate that current trajectory-prefix structural "
        "features offer limited prospective discrimination under strict operational false-alarm budgets, underscoring the "
        "critical necessity of enforcing the failure-onset boundary in agent-reliability evaluation."
    )
    add_abstract(doc, abstract_text)
    
    keywords_text = "Agentic systems, failure warning, prospective evaluation, trajectory analysis, standardized benchmarking, online monitoring, calibration, bootstrap inference."
    add_keywords(doc, keywords_text)
    
    # -------------------------------------------------------------
    # I. INTRODUCTION
    # -------------------------------------------------------------
    add_h1(doc, "I. Introduction")
    add_p(doc, "The deployment of autonomous agentic systems in complex software and decision-making environments requires rigorous runtime reliability guarantees. While final-outcome benchmarks such as AgentBench [1], AgentBoard [2], and GAIA [3] assess whether an agent successfully finishes a task, they offer no mid-execution visibility. Post-hoc failure localization and attribution frameworks (e.g., TRAIL [4], AgentRx [5], Who&When Pro [6], AgentProcessBench [11]) diagnose root causes retrospectively, requiring the completed trajectory and ground-truth failure outcome by construction.")
    add_p(doc, "Conversely, online agent-failure warning methods seek to predict eventual task failure prospectively from partial trajectory prefixes before failure onset. Recent systems, including PrefixGuard [7], AgentForesight [8], and Trajectory Guard [9], demonstrate that predicting failure from partial traces is achievable. For instance, PrefixGuard [7] reports AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its own evaluation protocol. However, these methods each employ distinct prefix representations, dataset splits, calibration rules, and metric regimes. Consequently, reported comparative advantages between heuristic, classical machine-learning, and sequence models remain unverified under a common, deployment-relevant false-alarm budget.")
    add_p(doc, "AIRE-Trace addresses this methodological gap. Rather than proposing a new detector architecture, this work establishes a standardized, prospective, prefix-only evaluation protocol for online agent-failure warning. By fixing information visibility, failure-target mapping, alert semantics, calibration under false-alarm constraints, lead-time measurement, and compute accounting, we evaluate representative warning methods under a unified experimental harness.")
    
    # Fig 1
    add_fig(doc, "figures/ieee/fig1_aire_trace_architecture.png", 1, 
            "AIRE-Trace standardized prospective evaluation pipeline. Trajectories undergo provenance auditing before task-disjoint splitting. Baselines fit on TRAIN, calibration selects operating thresholds under the FAR constraint, and frozen thresholds are applied to TEST.")
    
    # -------------------------------------------------------------
    # II. METHODOLOGY & PROTOCOL
    # -------------------------------------------------------------
    add_h1(doc, "II. Methodology & Protocol")
    
    add_h2(doc, "A. Evaluation Principle & Modes")
    add_p(doc, "The protocol standardizes evaluation conditions so that every method receives identical prefix observations and is scored on unified ranking, calibration, and operational metrics. Two evaluation modes are defined:")
    add_bullet(doc, "**Mode A (Prospective Warning):** Evaluated on TerminalBench, which provides step-level failure-onset annotations (min(incorrect_step_ids)). Checkpoints are restricted to pre-onset and onset steps (t <= t_onset). Supports AUROC, AUPRC, Brier score, ECE, prospective Recall@FAR, and lead time. This is the primary reported mode.")
    add_bullet(doc, "**Mode B (Eventual-Outcome Diagnostic):** Evaluated on tau2-Bench [10], which lacks onset annotations. Evaluates eventual-outcome risk without onset-based exclusion. Mode B represents protocol context only and is not comparable to Mode A.")
    
    add_h2(doc, "B. Canonical Trace Processing & Sanitization")
    add_p(doc, "To ensure cross-benchmark compatibility, native task success/failure outcomes are mapped into canonical eventual_success and eventual_failure labels (Protocol Rule 10). Crucially, all terminal markers and outcome-bearing event content are sanitized prior to feature extraction to prevent leakage (Protocol Rule 6).")
    
    # Fig 2
    add_fig(doc, "figures/ieee/fig2_provenance_recovery.png", 2, 
            "Provenance and exclusion accounting. Of 3,316 declared rows, 636 episodes were verified with valid mini.traj.json artifacts; 2,680 rows were excluded due to missing trajectory files or metadata.")
    
    add_h2(doc, "C. Prospective Prefix Construction & Evaluation Semantics")
    add_p(doc, "At checkpoint t in {1, ..., min(Ti, K)} with K=30, the monitor accesses only events e1, ..., et. An alert raised at t is prospective (valid early warning) if and only if t <= t_onset. Alerts occurring at t > t_onset are recorded as late detections and excluded from prospective recall metrics.")
    
    # Fig 3
    add_fig(doc, "figures/ieee/fig3_prospective_prefix.png", 3, 
            "Prospective prefix evaluation semantics. At checkpoint t, future events are unobserved. Alerts at or before onset constitute prospective warning; alerts after onset are analyzed separately as late detections.")
    
    add_h2(doc, "D. Baseline Methods & Threshold Calibration")
    add_p(doc, "We evaluate three representative method families across seven baseline models: Heuristic (H1: Tool Error Rate, H2: Retry Count, H3: Repeated Action, H4: Combined Heuristic), Classical ML (M1: Logistic Regression with StandardScaler), and Sequence (S1: Random Forest tabular ensemble, S2: PyTorch GRU network). Model L (LLM monitor) was registered but remains unevaluated due to hardware constraints. Operating thresholds tau* are calibrated strictly on CALIBRATION to satisfy FAR_calib(tau) <= 5%, then frozen for TEST evaluation.")
    
    # Table II
    add_tbl_header(doc, "I", "Warning Method Definitions & Frozen Thresholds")
    t2_h = ["Model", "Family", "Core Method", "tau* (Calib)"]
    t2_d = [
        ["H1", "Heuristic", "Min-max normalized tool error count", "0.86"],
        ["H2", "Heuristic", "Min-max normalized retry count", "0.89"],
        ["H3", "Heuristic", "Min-max repeated action indicator", "0.01*"],
        ["H4", "Heuristic", "Sigmoid of average z-scores (3 feats)", "0.93"],
        ["M1", "Classical", "Logistic Regression (C=1.0, lbfgs)", "0.98"],
        ["S1", "Sequence", "Random Forest (n=100, depth=6)", "0.97"],
        ["S2", "Sequence", "PyTorch GRU (dim=64, 1 layer)", "0.74"]
    ]
    add_tbl(doc, t2_h, t2_d, col_widths=[0.6, 0.9, 1.4, 0.6],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT])
    add_p(doc, "*Note: H3 calibration FAR reached 1.000; its Recall@FAR is undefined on TEST.", indent=False)
    
    add_h2(doc, "E. Statistical Inference Protocol")
    add_p(doc, "Prefix-level predictions exhibit intra-episode dependence. Following Cameron, Gelbach, and Miller [12], we employ a paired episode-cluster bootstrap procedure with B=1,000 iterations. Resampling is performed strictly at the episode level. Multiple-comparison hypothesis testing for S1 vs. all comparators is adjusted via the Holm–Bonferroni step-down procedure [13] at alpha=0.05. Pairwise Direction Consistency (PDC) evaluates ranking stability across metrics.")
    
    # -------------------------------------------------------------
    # III. RESULTS
    # -------------------------------------------------------------
    add_h1(doc, "III. Results")
    
    add_h2(doc, "A. Study Population Accounting")
    add_p(doc, "From 3,316 declared source rows, 636 canonical episodes were reconstructed. The task-disjoint partition assigned 163 episodes to TRAIN, 57 to CALIBRATION, and 416 to TEST (317 failures, 99 successes). Of the 317 TEST failures, 257 had valid failure-onset annotations; 60 unannotated failures were excluded from onset-dependent metrics.")
    
    # Table I
    add_tbl_header(doc, "II", "Study Population Accounting")
    t1_h = ["Population Subset", "Episodes", "Evaluation Role"]
    t1_d = [
        ["Declared Tracebench Rows", "3,316", "Initial source corpus"],
        ["Structurally Excluded", "2,680", "Missing mini.traj.json / metadata"],
        ["Canonical Reconstructed", "636", "Retained empirical population"],
        ["TRAIN Split", "163", "Model fitting (M1, S1, S2)"],
        ["CALIBRATION Split", "57", "Threshold selection (FAR <= 5%)"],
        ["TEST Split (Total)", "416", "Ranking metrics evaluation"],
        ["TEST Failures (Annotated)", "257", "Recall@FAR & late detection denom"],
        ["TEST Successes (FAR denom)", "99", "False alarm rate denominator"]
    ]
    add_tbl(doc, t1_h, t1_d, col_widths=[1.5, 0.6, 1.4],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.LEFT])
    
    add_h2(doc, "B. Baseline Prospective Discrimination")
    add_p(doc, "Table III summarizes Mode A performance on TEST (K=30). Discrimination was weak-to-moderate, with AUROC ranging from 0.5074 (H3) to 0.6371 (S1). Under the 5% FAR constraint, prospective Recall@FAR collapsed to near zero for all models (S1: 0.0000, M1: 0.0078). S1 achieved TEST FAR of 0.0404, remaining within budget.")
    
    # Table III
    add_tbl_header(doc, "III", "Primary Mode A TEST Performance (K=30, FAR Target 5%)")
    t3_h = ["Model", "AUROC [95% CI]", "AUPRC [95% CI]", "Recall@FAR", "FAR", "Brier", "ECE"]
    t3_d = [
        ["H1", "0.6205 [0.58, 0.65]", "0.8371 [0.79, 0.87]", "0.0000", "0.0000", "0.6186", "0.6622"],
        ["H2", "0.5752 [0.54, 0.61]", "0.8329 [0.78, 0.87]", "0.0000", "0.0000", "0.7034", "0.7223"],
        ["H3", "0.5074 [0.50, 0.51]", "0.8702 [0.85, 0.89]", "UNDEF", "1.0000", "0.2885", "0.2885"],
        ["H4", "0.6135 [0.57, 0.64]", "0.8346 [0.79, 0.86]", "0.0000", "0.0202", "0.2644", "0.2794"],
        ["M1", "0.6215 [0.56, 0.66]", "0.8331 [0.78, 0.87]", "0.0078", "0.0303", "0.1767", "0.0140"],
        ["S1", "0.6371 [0.59, 0.67]", "0.8452 [0.80, 0.88]", "0.0000", "0.0404", "0.1746", "0.0124"],
        ["S2", "0.5496 [0.52, 0.57]", "0.8129 [0.76, 0.84]", "0.0000", "0.0000", "0.2042", "0.1530"]
    ]
    add_tbl(doc, t3_h, t3_d, col_widths=[0.4, 0.9, 0.9, 0.5, 0.35, 0.35, 0.35],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    
    add_h2(doc, "C. Statistical Hypothesis Tests")
    add_p(doc, "Paired bootstrap testing (Table IV & Fig. 4) revealed that S1's AUROC advantage was statistically significant against S2, H2, and H3 (p_adj = 0.006 each), but was not distinguishable from M1 (p_adj = 0.318), H1 (p_adj = 0.318), or H4 (p_adj = 0.168). For AUPRC, S1 was significantly higher only against S2 (p_adj = 0.012). S1's superiority is selective rather than universal.")
    
    # Table IV (formerly V)
    add_tbl_header(doc, "IV", "Statistical Tests (S1 vs. Comparators, B=1000, Holm-Bonferroni)")
    t4_h = ["Comparison", "Metric", "Delta_obs", "p_raw", "p_adj", "Reject H0?"]
    t4_d = [
        ["S1 vs M1", "AUROC", "+0.0156", "0.1588", "0.3177", "No"],
        ["S1 vs S2", "AUROC", "+0.0875", "0.0010", "0.0060", "YES"],
        ["S1 vs H1", "AUROC", "+0.0165", "0.1948", "0.3177", "No"],
        ["S1 vs H2", "AUROC", "+0.0619", "0.0010", "0.0060", "YES"],
        ["S1 vs H3", "AUROC", "+0.1297", "0.0010", "0.0060", "YES"],
        ["S1 vs H4", "AUROC", "+0.0236", "0.0559", "0.1678", "No"],
        ["S1 vs S2", "AUPRC", "+0.0323", "0.0020", "0.0120", "YES"],
        ["S1 vs M1/H1-H4", "AUPRC", "Various", ">0.08", ">0.42", "No"]
    ]
    add_tbl(doc, t4_h, t4_d, col_widths=[0.8, 0.5, 0.5, 0.45, 0.45, 0.8],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.CENTER])
    
    # Fig 4
    add_fig(doc, "figures/ieee/fig4_mode_a_auroc.png", 4, 
            "Mode A TEST AUROC for evaluated warning methods (K=30) with 95% episode-cluster bootstrap confidence intervals.")
    
    add_h2(doc, "D. Operating-Point Sensitivity & Ranking Stability")
    add_p(doc, "Evaluating S1 across target FARs: at 1% and 5% target FAR (threshold 0.97), TEST FAR was 0.0404 and Recall@FAR was 0.0000. Relaxing target FAR to 10% (threshold 0.93) yielded TEST FAR = 0.1212 and Recall@FAR = 0.0973. Overall PDC across 21 informative pairs was 0.8294 (coverage 0.881), indicating partially consistent ranking directions across metrics.")
    
    add_h2(doc, "E. Feature Ablation Results")
    add_p(doc, "Ablation of S1 (Table V & Fig. 5) showed that removing tool error and retry counts (A4) produced the largest degradation (Delta_AUROC = -0.1069). Other groups (steps, roles, actions, tools) caused negligible change (|Delta| <= 0.0036). This establishes an empirical association between error signals and discrimination, but does not establish causality.")
    
    # Table V (formerly VI)
    add_tbl_header(doc, "V", "S1 Feature Ablation Results (Mode A, K=30)")
    t5_h = ["ID", "Removed Feature Group", "AUROC", "AUPRC", "Delta_AUROC"]
    t5_d = [
        ["A0", "None (full 13 features)", "0.6371", "0.8452", "0.0000"],
        ["A1", "feat_steps_so_far", "0.6357", "0.8450", "-0.0014"],
        ["A2", "4 actor-role features", "0.6335", "0.8422", "-0.0036"],
        ["A3", "3 action-type features", "0.6383", "0.8477", "+0.0012"],
        ["A4", "tool_error_count + retry_count", "0.5302", "0.7820", "-0.1069"],
        ["A5", "unique_tools + call_ratio", "0.6360", "0.8479", "-0.0011"],
        ["A6", "repeated_action_last2", "0.6341", "0.8462", "-0.0030"]
    ]
    add_tbl(doc, t5_h, t5_d, col_widths=[0.35, 1.6, 0.45, 0.45, 0.55],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    
    # Fig 5
    add_fig(doc, "figures/ieee/fig5_a4_ablation.png", 5, 
            "S1 feature ablation (A0–A6). Removal of error and retry features (A4) causes severe degradation.")
    
    add_h2(doc, "F. Operational Analysis & Late Detections")
    add_p(doc, "Table VI and Fig. 6 summarize Gate 6 operational behavior. Heuristic H3 fired 8,012 alerts (mean 19.26/episode), reaching 100% false alarms (99/99 successes) and generating exclusively late alerts for 19.84% of valid failure episodes (mean lateness 9.15 steps). In contrast, S1 generated only 25 total alerts (mean 0.060/episode, max 2) with 4 false alarms (4.04%) and 16 late-only episodes (6.23%).")
    
    # Table VI (formerly IV)
    add_tbl_header(doc, "VI", "Gate 6 Operational Analysis Summary")
    t6_h = ["Model", "FA Ep", "FAR", "Late-Only", "% Valid", "Total Alerts", "Mean/Ep"]
    t6_d = [
        ["H1", "0", "0.0000", "3", "1.17%", "19", "0.046"],
        ["H2", "0", "0.0000", "2", "0.78%", "16", "0.039"],
        ["H3", "99", "1.0000", "51", "19.84%", "8,012", "19.26"],
        ["H4", "2", "0.0202", "8", "3.11%", "119", "0.286"],
        ["M1", "3", "0.0303", "10", "3.89%", "161", "0.387"],
        ["S1", "4", "0.0404", "16", "6.23%", "25", "0.060"],
        ["S2", "0", "0.0000", "10", "3.89%", "107", "0.257"]
    ]
    add_tbl(doc, t6_h, t6_d, col_widths=[0.4, 0.4, 0.5, 0.5, 0.5, 0.55, 0.55],
            alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
    
    # Fig 6
    add_fig(doc, "figures/ieee/fig6_gate6_operational.png", 6, 
            "Gate 6 operational analysis panels: (a) False alarm rate on successful episodes; (b) Late-alert-only fraction on valid failures; (c) Alert burden per episode.")
    
    # -------------------------------------------------------------
    # IV. DISCUSSION & THREATS TO VALIDITY
    # -------------------------------------------------------------
    add_h1(doc, "IV. Discussion & Threats to Validity")
    add_p(doc, "**The Operational Recall Collapse:** The near-zero prospective Recall@FAR indicates that while tabular models can statistically discriminate eventual outcomes over a population (AUROC ~0.64), the signal is too diffuse to trigger pre-onset alerts for individual episodes under strict false-alarm budgets without violating FAR constraints.")
    add_p(doc, "**Activity vs. Prospective Warning:** Model H3 illustrates the peril of evaluating without onset boundaries. Despite generating over 8,000 alerts, nearly 20% of its failure alerts occurred post-onset, and 100% of successful episodes received false alarms. This reflects uncalibrated post-hoc diagnostic activity rather than actionable warning.")
    add_p(doc, "**Threats to Validity:** (1) *Population Coverage:* The 636 usable episodes represent 19.18% of 3,316 declared rows; unobserved rows may differ systematically. (2) *Onset Annotations:* 60 failure episodes lacked annotations and were excluded from recall metrics. (3) *Provenance Fragility:* Content-based fallback matching in the repair pipeline may introduce multi-match ambiguity. (4) *Model Scope:* Model L remains unevaluated, and Mode B metrics cannot be compared to Mode A.")
    
    # -------------------------------------------------------------
    # V. CONCLUSION & REPRODUCIBILITY
    # -------------------------------------------------------------
    add_h1(doc, "V. Conclusion & Reproducibility")
    add_p(doc, "AIRE-Trace establishes a standardized, leakage-free prospective evaluation harness for online agent-failure warning. Across seven evaluated baselines, prefix structural features provide limited prospective discrimination, and early warning recall collapses under strict false-alarm budgets. All evaluation code, canonical datasets, test suites (38 passing unit tests), and bootstrap routines are preserved deterministically with random seed 42 in the project repository.")
    
    # Acknowledgment
    add_h1(doc, "Acknowledgment")
    add_p(doc, "The authors thank the benchmark authors of AgentBench, GAIA, TerminalBench, and tau2-Bench for releasing the execution trajectories and evaluation environments that enabled this standardized study.")
    
    # References
    add_h1(doc, "References")
    refs = [
        (1, 'X. Liu et al., "AgentBench: Evaluating LLMs as Agents," in Proc. ICLR, 2024. arXiv:2308.03688.'),
        (2, 'C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents," in Proc. NeurIPS, 2024. arXiv:2401.13178.'),
        (3, 'G. Mialon et al., "GAIA: a benchmark for General AI Assistants," in Proc. ICLR, 2024. arXiv:2311.12983.'),
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
        add_ref(doc, num, txt)
        
    out_path = "AIRE-Trace_Universal_IEEE_Conference_Master.docx"
    doc.save(out_path)
    doc.save("AIRE-Trace_IEEE_Conference_Paper.docx")
    print("Paper built successfully.")

if __name__ == "__main__":
    build_paper()
