"""
generate_clean_ieee_figures.py
------------------------------
Generates all 6 publication-grade, 300-DPI figures for AIRE-Trace
using matplotlib with Times New Roman font and clean, sleek styling.
Includes Trajectory Risk Decomposition in Fig 1.
Zero black-triangle artifacts.
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

out_dir = Path("figures/ieee")
out_dir.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif', 'Times']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.size'] = 9
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['xtick.labelsize'] = 8.5
plt.rcParams['ytick.labelsize'] = 8.5

def save_fig(fig, name):
    target_dirs = [
        Path("04_ieee_publication/overleaf/figures"),
        Path("04_ieee_publication/AIRE-Trace_IEEE/figures"),
        Path("04_ieee_publication/AIRE-Trace_IEEE/figures/ieee"),
        Path("figures/ieee")
    ]
    for d in target_dirs:
        d.mkdir(parents=True, exist_ok=True)
        fig.savefig(d / f"{name}.png", format="png", dpi=300, bbox_inches="tight")
        if "ieee" in str(d):
            fig.savefig(d / f"{name}.svg", format="svg", bbox_inches="tight")
    plt.close(fig)

def generate_fig1():
    """Fig 1: AIRE-Trace Architecture & Pipeline including Risk Decomposition"""
    fig, ax = plt.subplots(figsize=(6.8, 3.2), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    c_blue_fill = '#EBF3FA'
    c_blue_edge = '#2A6F97'
    c_green_fill = '#EAF5EA'
    c_green_edge = '#2D6A4F'
    c_purple_fill = '#F3EBF6'
    c_purple_edge = '#6A0572'
    c_red_fill = '#FDF0ED'
    c_red_edge = '#BA181B'
    c_gray_fill = '#F4F5F7'
    c_gray_edge = '#495057'
    
    # TOP ROW: 3 equal boxes
    # Box 1: [2.5, 28.5], w=26, center = 15.5
    # Box 2: [36.5, 62.5], w=26, center = 49.5
    # Box 3: [70.5, 96.5], w=26, center = 83.5
    y_top = 70
    h_top = 22
    
    # Box 1: Agent Execution Trajectories
    b1 = patches.FancyBboxPatch((2.5, y_top), 26, h_top, boxstyle="round,pad=1.2,rounding_size=2",
                                facecolor=c_blue_fill, edgecolor=c_blue_edge, linewidth=1.5)
    ax.add_patch(b1)
    ax.text(15.5, 83.5, "Agent Execution\nTrajectories", ha='center', va='center', fontsize=9, fontweight='bold', color='#012A4A')
    ax.text(15.5, 75, "3,316 declared rows", ha='center', va='center', fontsize=7.5, style='italic', color='#333333')
    
    # Box 2: Provenance Audit & Reconstruction
    b2 = patches.FancyBboxPatch((36.5, y_top), 26, h_top, boxstyle="round,pad=1.2,rounding_size=2",
                                facecolor=c_blue_fill, edgecolor=c_blue_edge, linewidth=1.5)
    ax.add_patch(b2)
    ax.text(49.5, 83.5, "Provenance Audit\n& Reconstruction", ha='center', va='center', fontsize=9, fontweight='bold', color='#012A4A')
    ax.text(49.5, 75, "636 verified episodes", ha='center', va='center', fontsize=7.5, style='italic', color='#333333')
    
    # Box 3: Task-Disjoint Episode Splitting
    b3 = patches.FancyBboxPatch((70.5, y_top), 26, h_top, boxstyle="round,pad=1.2,rounding_size=2",
                                facecolor=c_gray_fill, edgecolor=c_gray_edge, linewidth=1.5)
    ax.add_patch(b3)
    ax.text(83.5, 83.5, "Task-Disjoint\nEpisode Splitting", ha='center', va='center', fontsize=9, fontweight='bold', color='#212529')
    ax.text(83.5, 75, "TRAIN / CALIB / TEST", ha='center', va='center', fontsize=7.5, style='italic', color='#333333')
    
    # Top horizontal arrows
    ax.annotate('', xy=(35.5, 81), xytext=(29.5, 81),
                arrowprops=dict(arrowstyle="-|>", color=c_blue_edge, lw=1.5, mutation_scale=12))
    ax.annotate('', xy=(69.5, 81), xytext=(63.5, 81),
                arrowprops=dict(arrowstyle="-|>", color=c_blue_edge, lw=1.5, mutation_scale=12))
    
    # BOTTOM ROW: TRAIN, CALIBRATION, TEST
    # Train: [2.5, 26.5], w = 24, center = 14.5
    # Calib: [32.0, 60.5], w = 28.5, center = 46.25
    # Test:  [74.0, 98.0], w = 24, center = 86.0
    y_bot = 12
    h_bot = 26
    
    # TRAIN
    b_train = patches.FancyBboxPatch((2.5, y_bot), 24, h_bot, boxstyle="round,pad=1.2,rounding_size=2",
                                     facecolor=c_green_fill, edgecolor=c_green_edge, linewidth=1.5)
    ax.add_patch(b_train)
    ax.text(14.5, 30.5, "TRAIN (N=163)", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_green_edge)
    ax.text(14.5, 21.0, "Risk Decomposition\n($P_{\\mathrm{dyn}} - P_{\\mathrm{static}}$)", ha='center', va='center', fontsize=7.2, color='#222222')
    
    # CALIBRATION
    b_calib = patches.FancyBboxPatch((32.0, y_bot), 28.5, h_bot, boxstyle="round,pad=1.2,rounding_size=2",
                                     facecolor=c_purple_fill, edgecolor=c_purple_edge, linewidth=1.5)
    ax.add_patch(b_calib)
    ax.text(46.25, 30.5, "CALIBRATION (N=57)", ha='center', va='center', fontsize=8.2, fontweight='bold', color=c_purple_edge)
    ax.text(46.25, 21.0, "Threshold Selection\n(FAR $\\leq$ 5% constraint)", ha='center', va='center', fontsize=7.0, color='#222222')
    
    # TEST
    b_test = patches.FancyBboxPatch((74.0, y_bot), 24, h_bot, boxstyle="round,pad=1.2,rounding_size=2",
                                    facecolor=c_red_fill, edgecolor=c_red_edge, linewidth=1.5)
    ax.add_patch(b_test)
    ax.text(86.0, 30.5, "TEST (N=416)", ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_red_edge)
    ax.text(86.0, 21.0, "Prospective Warning\n($B=10,000$ Bootstrap)", ha='center', va='center', fontsize=7.2, color='#222222')
    
    # DISTRIBUTION BUS from Box 3 to Bottom Row
    y_bus = 53
    ax.plot([83.5, 83.5], [69, y_bus], color=c_gray_edge, lw=1.3)
    ax.plot([14.5, 86.0], [y_bus, y_bus], color=c_gray_edge, lw=1.3)
    
    # Downward arrows from bus into each box
    ax.annotate('', xy=(14.5, 39.5), xytext=(14.5, y_bus),
                arrowprops=dict(arrowstyle="-|>", color=c_gray_edge, lw=1.3, mutation_scale=10))
    ax.annotate('', xy=(46.25, 39.5), xytext=(46.25, y_bus),
                arrowprops=dict(arrowstyle="-|>", color=c_gray_edge, lw=1.3, mutation_scale=10))
    ax.annotate('', xy=(86.0, 39.5), xytext=(86.0, y_bus),
                arrowprops=dict(arrowstyle="-|>", color=c_gray_edge, lw=1.3, mutation_scale=10))
    
    # Bottom horizontal workflow arrows
    # TRAIN -> CALIBRATION
    ax.annotate('', xy=(31.0, 25), xytext=(27.5, 25),
                arrowprops=dict(arrowstyle="-|>", color=c_green_edge, lw=1.3, mutation_scale=10))
    
    # CALIBRATION -> TEST
    # Calib right boundary (with pad=1.2): 60.5 + 1.2 = 61.7
    # Test left boundary (with pad=1.2): 74.0 - 1.2 = 72.8
    # Gap is from 61.7 to 72.8 (width = 11.1 units). Center = 67.25
    ax.annotate('', xy=(72.5, 23), xytext=(62.0, 23),
                arrowprops=dict(arrowstyle="-|>", color=c_purple_edge, lw=1.4, ls='--', mutation_scale=10))
    ax.text(67.25, 28, "Frozen $\\tau^*$", ha='center', va='center', fontsize=7.0, fontweight='bold', color=c_purple_edge)
    
    save_fig(fig, "fig1_aire_trace_architecture")
    print("Fig 1 regenerated with risk decomposition.")

def generate_fig2():
    fig, ax = plt.subplots(figsize=(6.0, 2.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    b_top = patches.FancyBboxPatch((28, 74), 44, 22, boxstyle="round,pad=1.5,rounding_size=2",
                                   facecolor='#F0F4F8', edgecolor='#334E68', linewidth=1.5)
    ax.add_patch(b_top)
    ax.text(50, 87, "Declared Source Population", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#102A43')
    ax.text(50, 79, "3,316 declared Tracebench rows", ha='center', va='center', fontsize=8, color='#334E68')
    
    b_ret = patches.FancyBboxPatch((4, 14), 43, 42, boxstyle="round,pad=1.5,rounding_size=2",
                                   facecolor='#F0F9F5', edgecolor='#2B8A3E', linewidth=1.5)
    ax.add_patch(b_ret)
    ax.text(25.5, 48, "Retained Population (636)", ha='center', va='center', fontsize=9, fontweight='bold', color='#2B8A3E')
    ax.text(25.5, 33, "• 636 canonical episodes (19.18%)\n• Verified trajectory evidence\n• Task-disjoint split:\n  TRAIN (163), CALIB (57), TEST (416)", 
            ha='center', va='center', fontsize=7.5, color='#1B4332')
    
    b_excl = patches.FancyBboxPatch((53, 14), 43, 42, boxstyle="round,pad=1.5,rounding_size=2",
                                    facecolor='#FDF2F2', edgecolor='#BA181B', linewidth=1.5)
    ax.add_patch(b_excl)
    ax.text(74.5, 48, "Excluded Rows (2,680)", ha='center', va='center', fontsize=9, fontweight='bold', color='#9B111E')
    ax.text(74.5, 33, "• 2,655 structurally invalid\n  (missing mini.traj.json)\n• 25 missing artifact metadata\n• Network recovery: 0 valid added", 
            ha='center', va='center', fontsize=7.5, color='#4A0E17')
    
    ax.annotate('', xy=(25.5, 57), xytext=(40, 73),
                arrowprops=dict(arrowstyle="-|>", color='#2B8A3E', lw=1.5, mutation_scale=12))
    ax.annotate('', xy=(74.5, 57), xytext=(60, 73),
                arrowprops=dict(arrowstyle="-|>", color='#BA181B', lw=1.5, mutation_scale=12))
    
    save_fig(fig, "fig2_provenance_recovery")
    print("Fig 2 regenerated.")

def generate_fig3():
    fig, ax = plt.subplots(figsize=(6.5, 2.6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    ax.plot([10, 90], [60, 60], color='#2B2D42', lw=2.2)
    ax.annotate('', xy=(92, 60), xytext=(89, 60),
                arrowprops=dict(arrowstyle="-|>", color='#2B2D42', lw=2.2, mutation_scale=12))
    ax.text(93, 60, "Time (Steps)", ha='left', va='center', fontsize=8, fontweight='bold', color='#2B2D42')
    
    steps = [15, 22, 29, 36, 43]
    for s in steps:
        ax.plot(s, 60, 'o', color='#1D3557', markersize=5)
    
    chk = 43
    ax.plot([chk, chk], [48, 72], color='#0288D1', lw=1.8, ls='--')
    ax.text(chk, 76, "Checkpoint $t$", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#0288D1')
    
    ax.plot([15, 15, chk, chk], [53, 50, 50, 53], color='#1D3557', lw=1.2)
    ax.text((15 + chk)/2, 44, "Observed Prefix ($e_1, \\dots, e_t$)", ha='center', va='top', fontsize=7.5, color='#1D3557')
    
    rect_mask = patches.Rectangle((chk, 54), 45, 12, facecolor='#E5E5E5', alpha=0.6, edgecolor='#999999', ls=':')
    ax.add_patch(rect_mask)
    ax.text(chk + 22.5, 60, "Future Events Unavailable", ha='center', va='center', fontsize=7.5, style='italic', color='#555555')
    
    t_onset = 65
    ax.plot([t_onset, t_onset], [48, 72], color='#D90429', lw=2.2)
    ax.text(t_onset, 76, "Failure Onset ($t_{\\mathrm{onset}}$)", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#D90429')
    
    b_early = patches.FancyBboxPatch((16, 12), 26, 18, boxstyle="round,pad=1,rounding_size=1.5",
                                     facecolor='#E8F5E9', edgecolor='#2A9D8F', lw=1.2)
    ax.add_patch(b_early)
    ax.text(29, 21, "Prospective Alert Window\n($t \\leq t_{\\mathrm{onset}}$: Early Warning)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1B4332')
    
    b_late = patches.FancyBboxPatch((60, 12), 26, 18, boxstyle="round,pad=1.5,rounding_size=1.5",
                                    facecolor='#FFEBEE', edgecolor='#D90429', lw=1.2)
    ax.add_patch(b_late)
    ax.text(73, 21, "Late Detection Window\n($t > t_{\\mathrm{onset}}$: Post-Onset)", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#9B111E')
    
    save_fig(fig, "fig3_prospective_prefix")
    print("Fig 3 regenerated.")

def generate_fig4():
    df = pd.read_csv("results/baseline_runs/baseline_comparison_table.csv")
    df['AUROC_CI_low'] = df['AUROC_95CI'].apply(lambda x: float(x.strip('[]').split(',')[0]))
    df['AUROC_CI_high'] = df['AUROC_95CI'].apply(lambda x: float(x.strip('[]').split(',')[1]))
    df['err_lower'] = df['AUROC'] - df['AUROC_CI_low']
    df['err_upper'] = df['AUROC_CI_high'] - df['AUROC']
    
    fig, ax = plt.subplots(figsize=(5.5, 3.0), dpi=300)
    models = df['method']
    auroc = df['AUROC']
    yerr = [df['err_lower'], df['err_upper']]
    
    colors = ['#2B5C8F' if m != 'S1' else '#1E7E34' for m in models]
    bars = ax.bar(models, auroc, yerr=yerr, capsize=4, color=colors, alpha=0.85, edgecolor='black', linewidth=0.8)
    ax.set_ylim(0.45, 0.72)
    ax.set_ylabel('TEST AUROC (Mode A, K=30)', fontweight='bold')
    ax.set_title('Mode A TEST AUROC with 95% Bootstrap CIs', fontweight='bold')
    ax.axhline(0.5, color='gray', linestyle=':', label='Chance (0.50)')
    
    for i, v in enumerate(auroc):
        ax.text(i, v + yerr[1].iloc[i] + 0.008, f'{v:.4f}', ha='center', va='bottom', fontsize=8)
        
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    save_fig(fig, "fig4_mode_a_auroc")
    print("Fig 4 regenerated.")

def generate_fig5():
    with open("reports/gate7_ablation.json") as f:
        data = json.load(f)
    df = pd.DataFrame(data).set_index('ablation_id').loc[['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']].reset_index()
    
    fig, ax = plt.subplots(figsize=(5.8, 3.0), dpi=300)
    colors = ['#1E7E34' if x == 'A0' else '#BA181B' if x == 'A4' else '#4682B4' for x in df['ablation_id']]
    
    bars = ax.bar(df['ablation_id'], df['TEST_AUROC'], color=colors, alpha=0.85, edgecolor='black', linewidth=0.8)
    ax.set_ylim(0.48, 0.68)
    ax.set_ylabel('TEST AUROC', fontweight='bold')
    ax.set_title('S1 Feature Ablation (A0–A6, K=30)', fontweight='bold')
    
    short_labels = [
        "A0 (Full)", "A1 (-steps)", "A2 (-roles)", "A3 (-actions)",
        "A4 (-errors)", "A5 (-tools)", "A6 (-repeat)"
    ]
    ax.set_xticks(range(len(short_labels)))
    ax.set_xticklabels(short_labels, rotation=25, ha='right')
    
    for i, row in df.iterrows():
        delta = row['TEST_AUROC'] - df.loc[0, 'TEST_AUROC']
        txt = "Baseline" if i == 0 else f"$\\Delta$={delta:+.4f}"
        ax.text(i, row['TEST_AUROC'] + 0.005, txt, ha='center', va='bottom', fontsize=7.5)
        
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    save_fig(fig, "fig5_a4_ablation")
    print("Fig 5 regenerated.")

def generate_fig6():
    with open("results/baseline_runs/gate6_false_alarms.json") as f:
        fa_data = json.load(f)['false_alarms']
    with open("results/baseline_runs/gate6_late_detections.json") as f:
        ld_data = json.load(f)['late_detections']
    with open("results/baseline_runs/gate6_alert_burden.json") as f:
        burden_data = json.load(f)['alert_burden']
        
    models = ['H1', 'H2', 'H3', 'H4', 'M1', 'S1', 'S2']
    fa_rates = [fa_data[m]['false_alarm_rate'] for m in models]
    late_only_pct = [ld_data[m]['pct_failed_episodes_with_only_late_alerts'] for m in models]
    mean_burden = [burden_data[m]['mean_alerts_per_episode'] for m in models]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(7.2, 2.5), dpi=300)
    
    ax1.bar(models, fa_rates, color='#2B5C8F', edgecolor='black', linewidth=0.7)
    ax1.axhline(0.05, color='r', linestyle='--', label='5% Target', lw=1.2)
    ax1.set_title('(a) False Alarm Rate', fontsize=8.5, fontweight='bold')
    ax1.set_ylabel('FAR (N=99)', fontsize=8)
    ax1.set_ylim(0, 1.05)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    
    ax2.bar(models, late_only_pct, color='#BA181B', edgecolor='black', linewidth=0.7)
    ax2.set_title('(b) Late-Alert Only %', fontsize=8.5, fontweight='bold')
    ax2.set_ylabel('% Valid Failures (N=257)', fontsize=8)
    ax2.set_ylim(0, 25)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)
    
    ax3.bar(models, mean_burden, color='#1E7E34', edgecolor='black', linewidth=0.7)
    ax3.set_title('(c) Alert Burden (log)', fontsize=8.5, fontweight='bold')
    ax3.set_ylabel('Alerts/Episode', fontsize=8)
    ax3.set_yscale('log')
    ax3.grid(axis='y', linestyle='--', alpha=0.4)
    
    plt.tight_layout()
    save_fig(fig, "fig6_gate6_operational")
    print("Fig 6 regenerated.")

if __name__ == "__main__":
    generate_fig1()
    generate_fig2()
    generate_fig3()
    generate_fig4()
    generate_fig5()
    generate_fig6()
    print("All 6 figures regenerated successfully.")
