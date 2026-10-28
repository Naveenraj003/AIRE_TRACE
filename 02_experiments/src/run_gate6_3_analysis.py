"""
AIRE-Trace Master Gate 6.3 Alert Burden Analysis Runner
Executes alert burden analysis using existing MasterEvaluator infrastructure and exports
standalone Gate 6 artifacts.
"""

from src.evaluation.alert_burden import run_alert_burden_analysis
from src.evaluation.gate6_runner_utils import run_gate6_diagnostic

def main():
    run_gate6_diagnostic(
        diagnostic_name="Alert Burden Analysis",
        analysis_func=run_alert_burden_analysis,
        output_filename="gate6_alert_burden.json",
        max_k=30
    )

if __name__ == "__main__":
    main()
