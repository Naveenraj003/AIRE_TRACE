"""
AIRE-Trace Master Gate 6 Late Detections Analysis Runner
Executes late detection analysis using existing MasterEvaluator infrastructure and exports
standalone Gate 6 artifacts.
"""

from src.evaluation.late_detections import run_late_detections_analysis
from src.evaluation.gate6_runner_utils import run_gate6_diagnostic

def main():
    run_gate6_diagnostic(
        diagnostic_name="Late Detections Analysis",
        analysis_func=run_late_detections_analysis,
        output_filename="gate6_late_detections.json",
        max_k=30
    )

if __name__ == "__main__":
    main()
