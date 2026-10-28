import os
import json
import pandas as pd
from src.evaluation.evaluator import MasterEvaluator

def main():
    tb_path = r"p:\AIRE-TRACE\data\processed\manifests\terminalbench_prefixes.parquet"
    tau2_path = r"p:\AIRE-TRACE\data\processed\manifests\tau2_prefixes.parquet"
    
    print("Loading data...")
    df_tb = pd.read_parquet(tb_path)
    df_tau2 = pd.read_parquet(tau2_path)

    far_targets = [0.01, 0.05, 0.10]
    results = []

    for far in far_targets:
        print(f"\n===========================================")
        print(f"Running G7-B FAR Sensitivity: Target FAR = {far}")
        print(f"===========================================")
        
        # Instantiate evaluator with specific target_far
        evaluator = MasterEvaluator(target_far=far, bootstrap_iterations=100, random_seed=42)
        
        res = evaluator.run_evaluation(
            df_tb=df_tb,
            df_tau2=df_tau2,
            max_k=30,
            compute_bootstrap=False  # Not strictly necessary for basic sensitivity, but can enable if needed.
                                     # Wait, prompt says: "Preserve the existing episode-level semantics."
                                     # I will leave compute_bootstrap=False for speed unless CIs are specifically requested for FAR.
                                     # Prompt didn't explicitly ask for CIs in G7-B outputs list, but let's run it just in case.
        )
        
        for m_id, metrics in res["mode_a_terminalbench_test"].items():
            calib = res["calibrated_thresholds"][m_id]
            # pdc exists in res["pdc_summary"] if we need it
            
            record = {
                "model_id": m_id,
                "target_FAR": far,
                "calibration_threshold": calib["frozen_threshold"],
                "calibration_FAR": calib["calibration_far"],
                "TEST_FAR": metrics["FAR"],
                "TEST_Recall_at_FAR": metrics.get("Recall_at_FAR", None),
                "TEST_AUROC": metrics["AUROC"],
                "TEST_AUPRC": metrics["AUPRC"],
                "Brier": metrics["Brier"],
                "ECE": metrics["ECE"]
            }
            results.append(record)

        # Add PDC summary for this FAR target
        results.append({
            "target_FAR": far,
            "pdc_summary": res["pdc_summary"]
        })

    output_path = r"p:\AIRE-TRACE\reports\gate7_far_sensitivity.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved Gate 7 FAR Sensitivity results to: {output_path}")

if __name__ == "__main__":
    main()
