import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

# Setup output directory
out_dir = Path("figures/patent")
out_dir.mkdir(parents=True, exist_ok=True)

# Common Patent Styling
# Clean black and white / grayscale, sans-serif font, white background, no decorative styling
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = 'black'
plt.rcParams['axes.linewidth'] = 1.2
plt.rcParams['svg.fonttype'] = 'none'

def add_box(ax, xy, width, height, text, ref_num=None, boxstyle="round,pad=0.3", linestyle="-", fill="white", fontsize=9.5, fontweight="normal"):
    x, y = xy
    box = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle=boxstyle,
        facecolor=fill,
        edgecolor="black",
        linewidth=1.2,
        linestyle=linestyle
    )
    ax.add_patch(box)
    
    # Label formatting
    full_text = text
    if ref_num:
        full_text = f"{text}\n({ref_num})"
        
    ax.text(
        x + width / 2.0, y + height / 2.0, full_text,
        ha="center", va="center",
        fontsize=fontsize, fontweight=fontweight,
        color="black", wrap=True
    )
    return box

def add_arrow(ax, start, end, text=None, text_offset=(0, 0), linestyle="-", rad=0.0):
    connectionstyle = f"arc3,rad={rad}" if rad != 0.0 else "arc3"
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            color="black",
            linewidth=1.2,
            linestyle=linestyle,
            mutation_scale=14,
            shrinkA=0, shrinkB=0,
            connectionstyle=connectionstyle
        )
    )
    if text:
        mid_x = (start[0] + end[0]) / 2.0 + text_offset[0]
        mid_y = (start[1] + end[1]) / 2.0 + text_offset[1]
        ax.text(mid_x, mid_y, text, ha="center", va="center", fontsize=8.5, backgroundcolor="white")

# ==============================================================================
# FIGURE 1: SYSTEM ARCHITECTURE
# Clean layout: upper branch (static), lower branch (dynamic), right-side vertical column (decomposition, comparison, threshold)
# Zero line crossings, perfectly aligned boxes
# ==============================================================================
def generate_fig1():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 118)
    ax.set_ylim(0, 75)
    ax.axis('off')
    
    # Outer System Boundary (100)
    sys_rect = patches.Rectangle(
        (19, 3), 82, 66,
        fill=False, edgecolor="black", linewidth=1.5, linestyle="--"
    )
    ax.add_patch(sys_rect)
    ax.text(21, 66.5, "100 — Prospective Failure Warning System", fontsize=10.5, fontweight="bold")
    
    # Input 102 (outside/entering system)
    add_box(ax, (2, 32.5), 14, 10, "Partial Trajectory\nInput", "102", boxstyle="square,pad=0.2", fontsize=9, fontweight="bold")
    
    # Split arrows into 104 (upper) and 108 (lower)
    add_arrow(ax, (16, 37.5), (22, 53))
    add_arrow(ax, (16, 37.5), (22, 22))
    
    # Upper branch: Static task difficulty
    # 104: Task Characteristics Input
    add_box(ax, (22, 47.5), 15, 11, "Task\nCharacteristics\nInput", "104", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (37, 53), (42, 53))
    
    # 106: Static Task-Difficulty Model
    add_box(ax, (42, 47.5), 17, 11, "Static Task-Difficulty\nModel", "106", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (59, 53), (64, 53))
    
    # 112: Static Failure Risk Value (P_static)
    add_box(ax, (64, 47.5), 15, 11, "Static Failure\nRisk Value\n(P_static)", "112", boxstyle="round,pad=0.2", fontsize=8.5)
    
    # Lower branch: Dynamic trajectory features
    # 108: Trajectory Execution Features Input
    add_box(ax, (22, 16.5), 15, 11, "Trajectory\nExecution Features\nInput", "108", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (37, 22), (42, 22))
    
    # 110: Dynamic Trajectory Risk Model
    add_box(ax, (42, 16.5), 17, 11, "Dynamic Trajectory\nRisk Model", "110", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (59, 22), (64, 22))
    
    # 114: Dynamic Failure Risk Value (P_dynamic)
    add_box(ax, (64, 16.5), 15, 11, "Dynamic Failure\nRisk Value\n(P_dynamic)", "114", boxstyle="round,pad=0.2", fontsize=8.5)
    
    # Right-hand processing column: Perfectly aligned at x=83, width 16
    # 116: Risk Decomposition Module (Centered vertically at y=33)
    add_arrow(ax, (79, 53), (83, 39))
    add_arrow(ax, (79, 22), (83, 35))
    
    add_box(ax, (83, 31), 16, 12, "Risk Decomposition\nModule\n[ R_t = P_dynamic\n - P_static ]", "116", boxstyle="square,pad=0.2", fontsize=8.5)
    
    # 118: Threshold Comparison Module placed directly below 116
    add_box(ax, (83, 16), 16, 10, "Threshold\nComparison\nModule\n[ R_t >= tau* ]", "118", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (91, 31), (91, 26))
    
    # 120: Calibrated Decision Threshold Storage (tau*) placed directly below 118, feeding straight UP
    add_box(ax, (83, 5), 16, 7.5, "Calibrated Decision\nThreshold Storage\n(tau*)", "120", boxstyle="round,pad=0.2", linestyle=":", fontsize=8)
    add_arrow(ax, (91, 12.5), (91, 16), linestyle=":")
    
    # Prospective Failure Warning Output 122 (exiting system at right of 118)
    add_arrow(ax, (99, 21), (103, 21))
    add_box(ax, (103, 16), 13, 10, "Prospective\nFailure Warning\nOutput", "122", boxstyle="round,pad=0.2", fontsize=8.5, fontweight="bold")
    
    # Caption at bottom
    fig.text(0.5, 0.015, "FIG. 1: Block diagram of a computer-implemented system for prospective failure warning in autonomous agents via trajectory risk decomposition.", ha="center", fontsize=9.5, fontweight="bold")
    
    plt.tight_layout()
    fig.savefig(out_dir / "patent_fig1_system_architecture.svg", format="svg", bbox_inches="tight")
    fig.savefig(out_dir / "patent_fig1_system_architecture.png", format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved patent_fig1_system_architecture")

# ==============================================================================
# FIGURE 2: PROSPECTIVE FAILURE-WARNING METHOD
# Clean vertical flow, loopback routed cleanly through checkpoint node with wide margins
# ==============================================================================
def generate_fig2():
    fig, ax = plt.subplots(figsize=(9, 10.5), dpi=300)
    ax.set_xlim(0, 112)
    ax.set_ylim(0, 105)
    ax.axis('off')
    
    # 200: Receive partial trajectory
    add_box(ax, (20, 94), 52, 7.5, "Receive partial trajectory up to checkpoint t", "200", boxstyle="round,pad=0.3", fontweight="bold", fontsize=9)
    add_arrow(ax, (46, 94), (46, 86))
    
    # 202: Determine task characteristics and trajectory execution features
    add_box(ax, (12, 78.5), 68, 7.5, "Determine task characteristics and trajectory execution features", "202", boxstyle="square,pad=0.2", fontsize=9)
    
    # Split into parallel paths
    add_arrow(ax, (28, 78.5), (28, 69))
    add_arrow(ax, (64, 78.5), (64, 69))
    
    # 204: Compute static failure probability (left)
    add_box(ax, (10, 61.5), 36, 7.5, "Compute static failure probability\n(P_static)", "204", boxstyle="square,pad=0.2", fontsize=8.5)
    
    # 206: Compute dynamic failure probability (right)
    add_box(ax, (48, 61.5), 36, 7.5, "Compute dynamic failure probability\n(P_dynamic)", "206", boxstyle="square,pad=0.2", fontsize=8.5)
    
    # Merge into 208
    add_arrow(ax, (28, 61.5), (38, 51.5))
    add_arrow(ax, (66, 61.5), (54, 51.5))
    
    # 208: Compute residual risk
    add_box(ax, (15, 44), 62, 7.5, "Compute trajectory-dependent residual risk\n(R_t = P_dynamic - P_static)", "208", boxstyle="square,pad=0.2", fontsize=8.5)
    add_arrow(ax, (46, 44), (46, 36.5))
    
    # 210: Decision Diamond (Compare residual risk with calibrated threshold)
    diamond = patches.Polygon(
        [[46, 36.5], [69, 28.5], [46, 20.5], [23, 28.5]],
        closed=True, facecolor="white", edgecolor="black", linewidth=1.2
    )
    ax.add_patch(diamond)
    ax.text(46, 28.5, "Compare residual risk\nwith calibrated threshold\n(R_t >= tau* ?)\n(210)", ha="center", va="center", fontsize=8.5)
    
    # Decision branches
    # YES branch -> 212 (Downward)
    add_arrow(ax, (46, 20.5), (46, 12), text="YES", text_offset=(3.5, 0))
    add_box(ax, (20, 4.5), 52, 7.5, "Generate prospective failure warning", "212", boxstyle="round,pad=0.3", fontweight="bold", fontsize=9)
    
    # NO branch -> 214 (To the right)
    add_arrow(ax, (69, 28.5), (76, 28.5), text="NO", text_offset=(0, 2.5))
    add_box(ax, (76, 23.5), 17, 10, "Proceed without\nwarning and advance\nto checkpoint t+1\n(214)", boxstyle="square,pad=0.2", fontsize=8)
    
    # Continuation loop: Route cleanly through Subsequent Checkpoint node
    # From right of 214 (x=93) to loop channel (x=98)
    ax.plot([93, 98], [28.5, 28.5], color="black", linewidth=1.2, linestyle="--")
    ax.plot([98, 98], [28.5, 57], color="black", linewidth=1.2, linestyle="--")
    
    # Node for subsequent checkpoint (t+1), centered at x=98 with ample canvas margin
    add_box(ax, (91, 57), 14, 8, "Subsequent\nCheckpoint\n(t+1)", boxstyle="square,pad=0.2", linestyle=":", fontsize=8)
    
    # Continuation from subsequent checkpoint (top at y=65) to 200
    ax.plot([98, 98], [65, 97.75], color="black", linewidth=1.2, linestyle="--")
    ax.plot([98, 72], [97.75, 97.75], color="black", linewidth=1.2, linestyle="--")
    ax.annotate("", xy=(72, 97.75), xytext=(75, 97.75),
                arrowprops=dict(arrowstyle="-|>", color="black", linewidth=1.2, mutation_scale=12))

    # Caption at bottom
    fig.text(0.5, 0.01, "FIG. 2: Flowchart of a computer-implemented method for prospective failure warning from a partially observed agent trajectory.", ha="center", fontsize=9.5, fontweight="bold")
    
    plt.tight_layout()
    fig.savefig(out_dir / "patent_fig2_prospective_warning_flow.svg", format="svg", bbox_inches="tight")
    fig.savefig(out_dir / "patent_fig2_prospective_warning_flow.png", format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved patent_fig2_prospective_warning_flow")

# ==============================================================================
# FIGURE 3: THRESHOLD CALIBRATION
# Clean vertical stack, ample margin for FROZEN box on right
# ==============================================================================
def generate_fig3():
    fig, ax = plt.subplots(figsize=(8.5, 10.5), dpi=300)
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 105)
    ax.axis('off')
    
    # Centered slightly to the left (x_start = 12, width = 66)
    # Leaves x=78 to 105 open for the FROZEN indicator
    steps = [
        ("Ingest calibration trajectory dataset", "300", 94),
        ("Compute static and dynamic failure probabilities\non calibration prefixes", "302", 81),
        ("Derive residual risk values for calibration prefixes\n(R_calib = P_dynamic - P_static)", "304", 68),
        ("Aggregate episode-level maximum residual risks\n(success episodes and prospective failure episodes)", "306", 55),
        ("Evaluate candidate decision thresholds\n(sweep tau across residual risk distribution)", "308", 42),
        ("Determine false-alarm rates on\nsuccessful calibration episodes", "310", 29),
        ("Select threshold maximizing failure recall\nsubject to predetermined FAR constraint\n(e.g., FAR <= target_far)", "312", 15),
        ("Freeze and store decision threshold tau*\n(fixed for prospective warning)", "314", 2)
    ]
    
    for i, (text, ref, y) in enumerate(steps):
        is_terminal = (i == 0 or i == len(steps) - 1)
        boxstyle = "round,pad=0.3" if is_terminal else "square,pad=0.2"
        fontweight = "bold" if is_terminal else "normal"
        add_box(ax, (12, y), 66, 8.5, text, ref, boxstyle=boxstyle, fontweight=fontweight, fontsize=8.5)
        if i < len(steps) - 1:
            next_y = steps[i+1][2]
            add_arrow(ax, (45, y), (45, next_y + 8.5))
            
    # Visual lock / frozen indicator beside step 314 (x=81 to 99, completely inside canvas)
    add_arrow(ax, (78, 6.25), (83, 6.25), linestyle=":")
    lock_rect = patches.FancyBboxPatch(
        (83, 2.5), 18, 7.5, boxstyle="round,pad=0.3", facecolor="#f8f8f8", edgecolor="black", linewidth=1.2, linestyle=":"
    )
    ax.add_patch(lock_rect)
    ax.text(92, 6.25, "FROZEN\n[Fixed Storage]", ha="center", va="center", fontsize=8, fontweight="bold")

    fig.text(0.5, 0.005, "FIG. 3: Flowchart of a method for decision threshold calibration under a false-alarm constraint.", ha="center", fontsize=9.5, fontweight="bold")
    
    plt.tight_layout()
    fig.savefig(out_dir / "patent_fig3_threshold_calibration.svg", format="svg", bbox_inches="tight")
    fig.savefig(out_dir / "patent_fig3_threshold_calibration.png", format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved patent_fig3_threshold_calibration")

# ==============================================================================
# FIGURE 4: RISK DECOMPOSITION GRAPH
# Stacked panels, zero overlap between annotations, curves, and legends
# ==============================================================================
def generate_fig4():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8.5), sharex=True, dpi=300)
    
    # Synthetic conceptual trajectory steps (K=30 horizon)
    t = np.linspace(1, 30, 200)
    
    # Panel 1: Composite Failure Probabilities
    # Static task difficulty risk: constant baseline level for a given task (0.35)
    p_static = np.full_like(t, 0.35)
    
    # Dynamic trajectory risk curve: starts near prior, rises as execution anomaly unfolds
    p_dynamic = 0.35 + 0.55 / (1.0 + np.exp(-0.35 * (t - 15)))
    
    # Panel 1 plotting
    ax1.plot(t, p_static, 'k--', linewidth=1.6, label='406 — Static Task-Difficulty Failure Risk (P_static)')
    ax1.plot(t, p_dynamic, 'k-', linewidth=2.0, label='408 — Dynamic Trajectory Failure Risk Curve (P_dynamic(t))')
    
    # Clean double-ended arrow showing residual gap at step t=22
    t_annot = 22.0
    idx_annot = np.argmin(np.abs(t - t_annot))
    y_stat = p_static[idx_annot]
    y_dyn = p_dynamic[idx_annot]
    
    ax1.annotate(
        "", xy=(t_annot, y_dyn), xytext=(t_annot, y_stat),
        arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.5)
    )
    # Boxed text offset to the right in open space (x=22.5 to 29.5)
    ax1.text(
        t_annot + 0.6, (y_stat + y_dyn) / 2.0,
        "Residual Difference\n[ R_t = P_dynamic(t) - P_static ]\n(410)",
        ha="left", va="center", fontsize=8,
        bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="black", linewidth=0.8)
    )
    
    ax1.set_ylabel("Failure Risk Axis\n(Probability)\n(404)", fontsize=9.5, fontweight="bold")
    ax1.set_ylim(0.0, 1.05)
    ax1.legend(loc="upper left", frameon=True, edgecolor="black", fontsize=8.5)
    ax1.set_title("Panel A: Failure Risk Decomposition into Static and Dynamic Components", fontsize=10, pad=6)
    ax1.grid(True, linestyle=":", alpha=0.6)
    
    # Panel 2: Isolated Residual Risk vs Decision Threshold
    r_t = p_dynamic - p_static
    tau_star = 0.32 # calibrated threshold
    
    ax2.plot(t, r_t, 'k-', linewidth=2.2, label='410 — Trajectory-Dependent Residual Risk (R_t = P_dynamic - P_static)')
    ax2.axhline(tau_star, color='black', linestyle=':', linewidth=1.8, label='412 — Calibrated Decision Threshold (tau*)')
    
    # Find trigger point where R_t >= tau*
    cross_idx = np.where(r_t >= tau_star)[0][0]
    t_trigger = t[cross_idx]
    r_trigger = r_t[cross_idx]
    
    # Shading under residual curve where R_t >= tau*
    ax2.fill_between(t[cross_idx:], r_t[cross_idx:], tau_star, color='gray', alpha=0.25, label="Prospective Warning Active Region")
    
    # Mark trigger point 414
    ax2.plot(t_trigger, r_trigger, 'ko', markersize=8, fillstyle='full')
    
    # Place trigger annotation in open lower-right / center area, completely clear of the top-left legend
    ax2.annotate(
        f"414 — Prospective Warning Trigger Point\n[ R_t >= tau* at t = {t_trigger:.1f} ]\n(Warning Emitted Without Outcome Knowledge)",
        xy=(t_trigger, r_trigger), xytext=(t_trigger + 3.5, r_trigger - 0.16),
        arrowprops=dict(arrowstyle="->", color="black", linewidth=1.2),
        ha="left", va="center", fontsize=8, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="black", linewidth=1.0)
    )
    
    ax2.set_xlabel("Execution Prefix Step Axis (t)\n(402)", fontsize=9.5, fontweight="bold")
    ax2.set_ylabel("Trajectory-Dependent\nResidual Risk Axis\n(404)", fontsize=9.5, fontweight="bold")
    ax2.set_ylim(-0.05, 0.65)
    # Legend at upper left, completely away from the trigger point annotation
    ax2.legend(loc="upper left", frameon=True, edgecolor="black", fontsize=8.5)
    ax2.set_title("Panel B: Threshold Comparison on Trajectory-Dependent Residual Risk", fontsize=10, pad=6)
    ax2.grid(True, linestyle=":", alpha=0.6)
    
    fig.suptitle("400 — Graphical Representation of Trajectory-Dependent Risk Decomposition", fontsize=11, fontweight="bold", y=0.98)
    fig.text(0.5, 0.01, "FIG. 4: Graphical representation of trajectory-dependent risk decomposition across execution prefixes.", ha="center", fontsize=9.5, fontweight="bold")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.96])
    fig.savefig(out_dir / "patent_fig4_risk_decomposition.svg", format="svg", bbox_inches="tight")
    fig.savefig(out_dir / "patent_fig4_risk_decomposition.png", format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved patent_fig4_risk_decomposition")

if __name__ == "__main__":
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    
    # Mirror to figures/ directory
    import shutil
    target_dir = Path("figures")
    for f in out_dir.glob("patent_fig*.*"):
        shutil.copy(f, target_dir / f.name)
        
    print("All patent figures generated and mirrored successfully with perfect alignment.")

