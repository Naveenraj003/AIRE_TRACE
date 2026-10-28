import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Setup
out_dir = Path("figures/ieee")
out_dir.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def save_fig(fig, name):
    fig.savefig(out_dir / f"{name}.svg", format="svg", bbox_inches="tight")
    fig.savefig(out_dir / f"{name}.png", format="png", dpi=300, bbox_inches="tight")
    plt.close(fig)

def generate_fig4():
    print("Generating Figure 4 (Mode A TEST AUROC)")
    df = pd.read_csv("results/baseline_runs/baseline_comparison_table.csv")
    
    # Process CI strings
    df['AUROC_CI_low'] = df['AUROC_95CI'].apply(lambda x: float(x.strip('[]').split(',')[0]))
    df['AUROC_CI_high'] = df['AUROC_95CI'].apply(lambda x: float(x.strip('[]').split(',')[1]))
    df['err_lower'] = df['AUROC'] - df['AUROC_CI_low']
    df['err_upper'] = df['AUROC_CI_high'] - df['AUROC']
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    models = df['method']
    auroc = df['AUROC']
    yerr = [df['err_lower'], df['err_upper']]
    
    ax.bar(models, auroc, yerr=yerr, capsize=5, color='#4c72b0', alpha=0.8, edgecolor='black')
    ax.set_ylim(0.4, 0.75)
    ax.set_ylabel('TEST AUROC (Mode A, K=30)')
    ax.set_title('Mode A TEST AUROC for Evaluated Warning Methods')
    
    # Add text labels
    for i, v in enumerate(auroc):
        ax.text(i, 0.42, f'{v:.4f}', ha='center', va='bottom', color='white', fontweight='bold')
    
    save_fig(fig, "fig4_mode_a_auroc")

def generate_fig5():
    print("Generating Figure 5 (A4 Ablation)")
    with open("reports/gate7_ablation.json") as f:
        data = json.load(f)
        
    df = pd.DataFrame(data)
    # Ensure correct order
    df = df.set_index('ablation_id').loc[['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6']].reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#55a868' if x == 'A0' else '#c44e52' if x == 'A4' else '#dd8452' for x in df['ablation_id']]
    
    ax.bar(df['ablation_id'], df['TEST_AUROC'], color=colors, alpha=0.8, edgecolor='black')
    ax.set_ylim(0.45, 0.65)
    ax.set_ylabel('TEST AUROC')
    ax.set_title('Feature Ablation Results (Mode A, K=30)')
    
    # X labels with description
    labels = [f"{row.ablation_id}\n({row.description})" for _, row in df.iterrows()]
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')
    
    # Annotate Delta
    for i, row in df.iterrows():
        delta = row['TEST_AUROC'] - df.loc[0, 'TEST_AUROC']
        if i == 0:
            txt = "Baseline"
        else:
            txt = f"$\\Delta$={delta:+.4f}"
        ax.text(i, row['TEST_AUROC'] + 0.002, txt, ha='center', va='bottom')
        
    save_fig(fig, "fig5_a4_ablation")

def generate_fig6():
    print("Generating Figure 6 (Operational Analysis)")
    with open("results/baseline_runs/gate6_false_alarms.json") as f:
        fa_data = json.load(f)['false_alarms']
    with open("results/baseline_runs/gate6_late_detections.json") as f:
        ld_data = json.load(f)['late_detections']
    with open("results/baseline_runs/gate6_alert_burden.json") as f:
        burden_data = json.load(f)['alert_burden']
        
    models = ['H1', 'H2', 'H3', 'H4', 'M1', 'S1', 'S2']
    fa_rates = [fa_data[m]['false_alarm_rate'] for m in models]
    late_only_pct = [ld_data[m]['pct_failed_episodes_with_only_late_alerts'] / 100.0 for m in models]
    mean_burden = [burden_data[m]['mean_alerts_per_episode'] for m in models]
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Panel 1: False Alarm Rate
    ax1.bar(models, fa_rates, color='#4c72b0', edgecolor='black')
    ax1.axhline(0.05, color='r', linestyle='--', label='5% Target')
    ax1.set_title('False Alarm Rate\n(Successful Episodes)')
    ax1.set_ylabel('FAR')
    ax1.legend()
    # Log scale if H3 is 1.0 and others are near 0 to make it readable
    
    # Panel 2: Late-Only Alerts
    ax2.bar(models, late_only_pct, color='#c44e52', edgecolor='black')
    ax2.set_title('Late-Alert-Only Rate\n(Valid Failure Episodes)')
    ax2.set_ylabel('Proportion')
    
    # Panel 3: Mean Alert Burden
    ax3.bar(models, mean_burden, color='#55a868', edgecolor='black')
    ax3.set_title('Mean Alert Burden\n(All TEST Episodes)')
    ax3.set_ylabel('Alerts per Episode')
    ax3.set_yscale('log') # Since H3 is very high
    
    plt.tight_layout()
    save_fig(fig, "fig6_gate6_operational")

def generate_conceptual_svgs():
    print("Generating Conceptual SVGs (Figures 1-3)")
    # Fig 1: Architecture
    fig1_svg = """<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white"/>
    <g font-family="sans-serif" font-size="14" text-anchor="middle">
        <!-- Nodes -->
        <rect x="50" y="50" width="150" height="40" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
        <text x="125" y="75">Trajectory/Data</text>

        <rect x="250" y="50" width="200" height="40" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
        <text x="350" y="75">Provenance/Recovery</text>
        
        <rect x="500" y="50" width="250" height="40" fill="#fff9c4" stroke="#fbc02d" stroke-width="2"/>
        <text x="625" y="75">Canonical Study Population</text>

        <rect x="350" y="150" width="150" height="40" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
        <text x="425" y="175">TRAIN</text>

        <rect x="150" y="250" width="150" height="40" fill="#f3e5f5" stroke="#7b1fa2" stroke-width="2"/>
        <text x="225" y="275">CALIBRATION</text>

        <rect x="550" y="250" width="150" height="40" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
        <text x="625" y="275">TEST</text>
        
        <!-- Arrows -->
        <path d="M 200 70 L 250 70" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 450 70 L 500 70" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <path d="M 625 90 L 625 120 L 425 120 L 425 150" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 625 90 L 625 120 L 225 120 L 225 250" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <path d="M 625 90 L 625 250" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>

        <!-- Details -->
        <text x="425" y="210" font-size="12">Train Models</text>
        <path d="M 425 215 L 425 250 L 300 250" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <text x="225" y="315" font-size="12">Select Threshold (FAR constraint)</text>
        <path d="M 300 270 L 550 270" stroke="black" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrow)"/>
        <text x="425" y="265" font-size="12">Frozen Threshold</text>
        
        <rect x="425" y="320" width="200" height="40" fill="#eceff1" stroke="#455a64" stroke-width="2"/>
        <text x="525" y="345">Gate 6 &amp; Auditable Results</text>
        <path d="M 625 290 L 625 320" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
    </defs>
    </svg>"""
    with open(out_dir / "fig1_aire_trace_architecture.svg", "w") as f:
        f.write(fig1_svg)

    # Fig 2: Provenance
    fig2_svg = """<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white"/>
    <g font-family="sans-serif" font-size="14" text-anchor="middle">
        <rect x="200" y="20" width="200" height="50" fill="#eeeeee" stroke="black" stroke-width="2"/>
        <text x="300" y="45" font-weight="bold">3,316 declared rows</text>
        
        <path d="M 300 70 L 300 120" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        
        <!-- Exclusions -->
        <path d="M 300 95 L 450 95 L 450 120" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="350" y="120" width="200" height="80" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
        <text x="450" y="145" font-weight="bold">2,680 excluded</text>
        <text x="450" y="165" font-size="12">2,655 structurally invalid</text>
        <text x="450" y="185" font-size="12">25 missing artifact path/metadata</text>
        
        <!-- Recovered -->
        <rect x="150" y="120" width="180" height="60" fill="#e8f5e9" stroke="#388e3c" stroke-width="2"/>
        <text x="240" y="145" font-weight="bold">636 valid/recovered</text>
        <text x="240" y="165" font-size="12">episodes</text>
        
        <path d="M 240 180 L 240 220" stroke="black" stroke-width="2" marker-end="url(#arrow)"/>
        <rect x="100" y="220" width="280" height="40" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
        <text x="240" y="245">Downstream Empirical Analysis</text>
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
    </defs>
    </svg>"""
    with open(out_dir / "fig2_provenance_recovery.svg", "w") as f:
        f.write(fig2_svg)

    # Fig 3: Prospective prefix evaluation
    fig3_svg = """<svg width="700" height="350" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="white"/>
    <g font-family="sans-serif" font-size="14">
        <!-- Time Axis -->
        <line x1="50" y1="150" x2="650" y2="150" stroke="black" stroke-width="3" marker-end="url(#arrow)"/>
        <text x="650" y="170" text-anchor="end">Time (steps)</text>
        
        <!-- Events -->
        <circle cx="100" cy="150" r="5" fill="black"/>
        <circle cx="150" cy="150" r="5" fill="black"/>
        <circle cx="200" cy="150" r="5" fill="black"/>
        <circle cx="250" cy="150" r="5" fill="black"/>
        
        <text x="250" y="130" text-anchor="middle" fill="#0288d1">Checkpoint t</text>
        <line x1="250" y1="135" x2="250" y2="165" stroke="#0288d1" stroke-width="2" stroke-dasharray="4,4"/>
        
        <!-- Future events masked -->
        <rect x="250" y="120" width="380" height="60" fill="gray" opacity="0.2"/>
        <text x="440" y="145" text-anchor="middle" font-style="italic">Future Events Unavailable</text>
        
        <!-- Failure Onset -->
        <line x1="450" y1="110" x2="450" y2="190" stroke="red" stroke-width="3"/>
        <text x="450" y="100" text-anchor="middle" fill="red" font-weight="bold">Failure Onset</text>
        
        <!-- Box for Prospective evaluation -->
        <rect x="80" y="200" width="200" height="80" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
        <text x="180" y="225" text-anchor="middle" font-weight="bold">Prospective Alert</text>
        <text x="180" y="245" text-anchor="middle" font-size="12">Alert &lt;= Onset</text>
        <text x="180" y="265" text-anchor="middle" font-size="12">(Valid Early Warning)</text>
        <path d="M 250 170 L 180 200" stroke="#0288d1" stroke-width="2" marker-end="url(#arrow)"/>
        
        <!-- Box for Late detection -->
        <rect x="420" y="200" width="200" height="80" fill="#ffebee" stroke="#d32f2f" stroke-width="2"/>
        <text x="520" y="225" text-anchor="middle" font-weight="bold">Late Detection</text>
        <text x="520" y="245" text-anchor="middle" font-size="12">Alert &gt; Onset</text>
        <text x="520" y="265" text-anchor="middle" font-size="12">(Post-failure Diagnosis)</text>
        <path d="M 520 170 L 520 200" stroke="#d32f2f" stroke-width="2" stroke-dasharray="4,4" marker-end="url(#arrow)"/>
        
        <!-- Prefix span -->
        <path d="M 100 170 Q 175 190 250 170" stroke="black" stroke-width="1.5" fill="none"/>
        <text x="175" y="195" text-anchor="middle" font-size="12">Prefix</text>
    </g>
    <defs>
        <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth">
            <path d="M0,0 L0,6 L9,3 z" fill="black"/>
        </marker>
    </defs>
    </svg>"""
    with open(out_dir / "fig3_prospective_prefix.svg", "w") as f:
        f.write(fig3_svg)

if __name__ == "__main__":
    generate_fig4()
    generate_fig5()
    generate_fig6()
    generate_conceptual_svgs()
    print("Done")
