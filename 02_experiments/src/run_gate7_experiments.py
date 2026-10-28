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
    
    # Calculate episode counts (at max_k=30)
    df_tb_k = df_tb[df_tb["prefix_len"] <= 30]
    train_eps = df_tb_k[df_tb_k["split"] == "train"]["episode_id"].nunique()
    calib_eps = df_tb_k[df_tb_k["split"] == "calibration"]["episode_id"].nunique()
    test_eps = df_tb_k[df_tb_k["split"] == "test"]["episode_id"].nunique()

    # The 13 canonical baseline features
    all_features = [
        "feat_steps_so_far",
        "feat_actor_role_agent",
        "feat_actor_role_tool",
        "feat_actor_role_user",
        "feat_actor_role_system",
        "feat_action_type_message",
        "feat_action_type_tool_call",
        "feat_action_type_tool_result",
        "feat_tool_error_count",
        "feat_retry_count",
        "feat_unique_tools_used",
        "feat_tool_call_ratio",
        "feat_repeated_action_last2"
    ]

    ablation_groups = [
        {
            "id": "A0",
            "desc": "Full baseline",
            "remove": []
        },
        {
            "id": "A1",
            "desc": "No progression",
            "remove": ["feat_steps_so_far"]
        },
        {
            "id": "A2",
            "desc": "No actor-role composition",
            "remove": [
                "feat_actor_role_agent",
                "feat_actor_role_tool",
                "feat_actor_role_user",
                "feat_actor_role_system"
            ]
        },
        {
            "id": "A3",
            "desc": "No action-type composition",
            "remove": [
                "feat_action_type_message",
                "feat_action_type_tool_call",
                "feat_action_type_tool_result"
            ]
        },
        {
            "id": "A4",
            "desc": "No error/retry signals",
            "remove": [
                "feat_tool_error_count",
                "feat_retry_count"
            ]
        },
        {
            "id": "A5",
            "desc": "No tool-usage statistics",
            "remove": [
                "feat_unique_tools_used",
                "feat_tool_call_ratio"
            ]
        },
        {
            "id": "A6",
            "desc": "No immediate repetition signal",
            "remove": ["feat_repeated_action_last2"]
        }
    ]

    results = []

    for group in ablation_groups:
        print(f"\n===========================================")
        print(f"Running G7-C Ablation: {group['id']} - {group['desc']}")
        print(f"===========================================")
        
        retained_features = [f for f in all_features if f not in group["remove"]]
        
        feature_cols_by_model = {
            "S1": retained_features
        }

        # Initialize standard evaluator exactly as Gate 3
        evaluator = MasterEvaluator(target_far=0.05, bootstrap_iterations=100, random_seed=42)
        
        res = evaluator.run_evaluation(
            df_tb=df_tb,
            df_tau2=df_tau2,
            max_k=30,
            compute_bootstrap=True,
            feature_cols_by_model=feature_cols_by_model
        )

        s1_metrics = res["mode_a_terminalbench_test"]["S1"]
        s1_calib = res["calibrated_thresholds"]["S1"]
        s1_ci = res["bootstrap_confidence_intervals"]["S1"]
        s1_exclusion = s1_metrics["Exclusion_Stats"]

        record = {
            "ablation_id": group["id"],
            "description": group["desc"],
            "retained_features": retained_features,
            "removed_features": group["remove"],
            "seed": 42,
            "train_episodes": train_eps,
            "calibration_episodes": calib_eps,
            "test_episodes": test_eps,
            "calibration_threshold": s1_calib["frozen_threshold"],
            "calibration_FAR": s1_calib["calibration_far"],
            "calibration_Recall": s1_calib.get("calibration_recall", None),
            "TEST_AUROC": s1_metrics["AUROC"],
            "TEST_AUPRC": s1_metrics["AUPRC"],
            "TEST_Recall_at_FAR": s1_metrics.get("Recall_at_FAR", None),
            "TEST_FAR": s1_metrics["FAR"],
            "Brier": s1_metrics["Brier"],
            "ECE": s1_metrics["ECE"],
            "bootstrap_CIs": s1_ci,
            "exclusion_counts": s1_exclusion,
            "dataset": "TerminalBench (Mode A)",
            "disclaimer": "This is a Gate 7 ablation and does not replace the frozen primary S1 result."
        }
        
        results.append(record)

    output_path = r"p:\AIRE-TRACE\reports\gate7_ablation.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved Gate 7 Ablation results to: {output_path}")

if __name__ == "__main__":
    main()
