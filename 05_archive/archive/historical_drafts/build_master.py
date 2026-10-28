import re
import pypandoc
from markdown_pdf import MarkdownPdf, Section
import os

def get_verified_references():
    return """[1] X. Liu et al., "AgentBench: Evaluating LLMs as Agents," in Proc. ICLR, 2024. arXiv:2308.03688.
[2] C. Ma et al., "AgentBoard: An Analytical Evaluation Board of Multi-turn LLM Agents," in Proc. NeurIPS, 2024. arXiv:2401.13178.
[3] G. Mialon et al., "GAIA: a benchmark for General AI Assistants," in Proc. ICLR, 2024. arXiv:2311.12983.
[4] D. Deshpande et al., "TRAIL: Trace Reasoning and Agentic Issue Localization," arXiv preprint arXiv:2505.08638, 2025.
[5] S. Barke et al., "AgentRx: Diagnosing AI Agent Failures from Execution Trajectories," arXiv preprint arXiv:2602.02475, 2026.
[6] J. Liu et al., "Who&When Pro: Can LLMs Really Attribute Failures in AI Agents?" arXiv preprint arXiv:2607.09996, 2026.
[7] X. Huang et al., "PrefixGuard: From LLM-Agent Traces to Online Failure-Warning Monitors," arXiv preprint arXiv:2605.06455, 2026.
[8] B. Zhang et al., "AgentForesight: Online Auditing for Early Failure Prediction in Multi-Agent Systems," arXiv preprint arXiv:2605.08715, 2026.
[9] L. Advani, "Trajectory Guard: A Lightweight, Sequence-Aware Model for Real-Time Anomaly Detection in Agentic AI," arXiv preprint arXiv:2601.00516, 2026.
[10] L. Advani, "From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents," arXiv preprint arXiv:2606.09863, 2026.
[11] S. Fan et al., "AgentProcessBench: Diagnosing Step-Level Process Quality in Tool-Using Agents," arXiv preprint arXiv:2603.14465, 2026.
[12] A. C. Cameron, J. B. Gelbach, and D. L. Miller, "Bootstrap-Based Improvements for Inference with Clustered Errors," Rev. Econ. Stat., vol. 90, no. 3, pp. 414-427, 2008.
[13] S. Holm, "A Simple Sequentially Rejective Multiple Test Procedure," Scand. J. Stat., vol. 6, no. 2, pp. 65-70, 1979."""

def replace_exact(text, old, new, name):
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{name}: expected exactly 1 occurrence, found {count}")
    return text.replace(old, new)

def main():
    with open("AIRE-Trace_Master_IEEE_Manuscript.md", "r", encoding="utf-8") as f:
        md = f.read()

    # 1. Metadata Block
    metadata_block = """---
VENUE_NAME: [TO BE SELECTED]
PAGE_LIMIT: [TO BE DETERMINED]
PAPER_SIZE: US LETTER BASELINE
REVIEW_MODE: [TO BE DETERMINED]
AUTHOR_BLOCK: [TO BE COMPLETED]
SUBMISSION_DATE: [TO BE DETERMINED]
---

"""
    
    # 2. Author Block format
    author_block_original = """**[AUTHOR 1 NAME]**
[DEPARTMENT]
[INSTITUTION]
[CITY, COUNTRY]
[EMAIL]

**[AUTHOR 2 NAME]** (if applicable)
[DEPARTMENT]
[INSTITUTION]
[CITY, COUNTRY]
[EMAIL]"""

    author_block_new = """**[AUTHOR 1 NAME]**
[AUTHOR 1 DEPARTMENT]
[AUTHOR 1 INSTITUTION]
[CITY, COUNTRY]
[AUTHOR 1 EMAIL]

**[AUTHOR 2 NAME]** (if applicable)
[AUTHOR 2 DEPARTMENT]
[AUTHOR 2 INSTITUTION]
[CITY, COUNTRY]
[AUTHOR 2 EMAIL]"""
    
    md = replace_exact(md, author_block_original, author_block_new, "Author Block Replacement")
    md = replace_exact(md, "*Submitted to: [IEEE VENUE / CONFERENCE NAME]*", "*Submitted to: [IEEE CONFERENCE NAME — TO BE SELECTED]*", "Venue Placeholder")
    md = replace_exact(md, "*Submission Date: [SUBMISSION DATE]*", "*Submission Date: [SUBMISSION DATE — TO BE DETERMINED]*", "Date Placeholder")

    # 3. Fix PrefixGuard Claim
    pg_old = "PrefixGuard [7] demonstrates prefix-based warning monitors across multiple benchmarks, reporting substantially higher prospective performance than the baseline family evaluated in this study."
    pg_new = "PrefixGuard [7] achieves AUPRC of 0.900 on WebArena and 0.557 on TerminalBench under its own evaluation protocol, demonstrating that prefix-based monitoring is feasible across multiple benchmarks. Direct numerical comparison with AIRE-Trace results is not appropriate due to differences in prefix representation, feature regime, and calibration protocol."
    md = replace_exact(md, pg_old, pg_new, "PrefixGuard Claim Fix")

    # 4. Update References Section
    ref_marker_start = "## References"
    ref_idx = md.find(ref_marker_start)
    if ref_idx == -1:
        raise RuntimeError("References section not found in manuscript")
    md = md[:ref_idx + len(ref_marker_start)] + "\n\n" + get_verified_references() + "\n"

    # 5. Insert Figures & References gracefully
    
    # Fig 1 - Architecture
    target_1 = "### D. Warning Formulation"
    insert_1 = "The conceptual flow of the overall architecture is illustrated in Fig. 1.\n\n![Fig. 1. AIRE-Trace standardized prospective evaluation pipeline. Trajectories are provenance-audited before episode-level splitting; trainable methods are fitted on TRAIN, operating thresholds are selected on CALIBRATION under the false-alarm constraint, and frozen thresholds are applied to the TEST population for prospective evaluation and operational analysis.](figures/ieee/fig1_aire_trace_architecture.png)\n\n"
    md = replace_exact(md, target_1, insert_1 + target_1, "Figure 1 Insertion")

    # Fig 2 - Provenance
    target_2 = "### C. Sanitization"
    insert_2 = "The provenance and exclusion accounting leading to this subset is detailed in Fig. 2.\n\n![Fig. 2. Provenance and exclusion accounting for the AIRE-Trace empirical population. The downstream study is restricted to the canonical 636-episode population for which the required trajectory evidence was verified or deterministically reconstructed.](figures/ieee/fig2_provenance_recovery.png)\n\n"
    md = replace_exact(md, target_2, insert_2 + target_2, "Figure 2 Insertion")

    # Fig 3 - Prospective Prefix
    target_3 = "An alert at t > t_onset is a late detection; it does not constitute actionable early warning."
    insert_3 = " These prospective evaluation semantics are visualized in Fig. 3.\n\n![Fig. 3. Prospective prefix evaluation semantics. At each permitted checkpoint, the monitor observes only the trajectory information available up to that point. Alerts at or before the annotated failure onset are prospective detections; alerts after onset are analyzed separately as late detections.](figures/ieee/fig3_prospective_prefix.png)\n\n"
    md = replace_exact(md, target_3, target_3 + insert_3, "Figure 3 Insertion")

    # Fig 4 - AUROC Mode A
    target_4 = "### D. TABLE V -- Statistical Tests"
    insert_4 = "The performance results are visually summarized in Fig. 4.\n\n![Fig. 4. Mode A TEST AUROC for the evaluated warning methods under the K=30 protocol. Error bars denote the corresponding 95% episode-cluster bootstrap confidence intervals.](figures/ieee/fig4_mode_a_auroc.png)\n\n"
    md = replace_exact(md, target_4, insert_4 + target_4, "Figure 4 Insertion")

    # Fig 5 - Ablation
    target_5 = "A4 produced the largest observed degradation (Delta_AUROC = -0.1069)."
    insert_5 = "As shown in Fig. 5, "
    md = replace_exact(md, target_5, insert_5 + target_5.lower(), "Figure 5 text ref")
    
    target_5_img = "establish causality.\n\n---\n\n## IX. Operational Analysis"
    insert_5_img = "establish causality.\n\n![Fig. 5. A4 component ablation under the defined evaluation protocol. The observed AUROC change is reported as an empirical association under the ablation design and does not establish causal attribution.](figures/ieee/fig5_a4_ablation.png)\n\n---\n\n## IX. Operational Analysis"
    md = replace_exact(md, target_5_img, insert_5_img, "Figure 5 image insertion")

    # Fig 6 - Operational
    target_6 = "### B. Late Detections"
    insert_6 = "These operational findings, highlighting false alarms, late-alert-only episodes, and alert burden, are visualized in Fig. 6.\n\n![Fig. 6. Gate 6 operational analysis showing false alarms, late-alert-only episodes, and alert burden under the frozen TEST evaluation.](figures/ieee/fig6_gate6_operational.png)\n\n"
    md = replace_exact(md, target_6, insert_6 + target_6, "Figure 6 Insertion")

    md_final = metadata_block + md
    with open("AIRE-Trace_Universal_Master_temp.md", "w", encoding="utf-8") as f:
        f.write(md_final)
    
    # Render DOCX and TEX via pypandoc
    extra_args = ['--standalone']
    pypandoc.convert_file("AIRE-Trace_Universal_Master_temp.md", 'docx', outputfile="AIRE-Trace_Universal_IEEE_Conference_Master.docx")
    pypandoc.convert_file("AIRE-Trace_Universal_Master_temp.md", 'latex', outputfile="AIRE-Trace_Universal_IEEE_Conference_Master.tex", extra_args=extra_args)
    
    # Render PDF via markdown_pdf
    pdf = MarkdownPdf(toc_level=0)
    pdf.add_section(Section(md_final))
    pdf.save("AIRE-Trace_Universal_IEEE_Conference_Master.pdf")
    print("Files generated successfully.")

if __name__ == "__main__":
    main()
