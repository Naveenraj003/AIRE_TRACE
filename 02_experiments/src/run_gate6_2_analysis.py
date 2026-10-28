"""
AIRE-Trace Master Gate 6.2 False Alarms Analysis Runner
Executes false alarms analysis using existing MasterEvaluator infrastructure and exports
standalone Gate 6 artifacts.
"""

from src.evaluation.false_alarms import run_false_alarms_analysis
from src.evaluation.gate6_runner_utils import run_gate6_diagnostic

def main():
    run_gate6_diagnostic(
        diagnostic_name="False Alarms Analysis",
        analysis_func=run_false_alarms_analysis,
        output_filename="gate6_false_alarms.json",
        max_k=30
    )

if __name__ == "__main__":
    main()
