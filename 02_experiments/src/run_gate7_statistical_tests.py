import os
import json
import pandas as pd
from src.evaluation.evaluator import MasterEvaluator
from src.evaluation.statistical_testing import compute_paired_bootstrap_test

def main():
    tb_path = r"p:\AIRE-TRACE\data\processed\manifests\terminalbench_prefixes.parquet"
    tau2_path = r"p:\AIRE-TRACE\data\processed\manifests\tau2_prefixes.parquet"
    
    print("Loading data...")
    df_tb = pd.read_parquet(tb_path)
    df_tau2 = pd.read_parquet(tau2_path)

    print("\n===========================================")
    print("Running G7-D Statistical Testing")
    print("===========================================")
    
    # Instantiate evaluator with default Gate 3 parameters
    evaluator = MasterEvaluator(target_far=0.05, bootstrap_iterations=100, random_seed=42)
    
    # Run evaluation but disable the internal bootstrap to save time,
    # since we are doing the B=1000 paired bootstrap afterwards.
    res = evaluator.run_evaluation(
        df_tb=df_tb,
        df_tau2=df_tau2,
        max_k=30,
        compute_bootstrap=False
    )
    
    # Extract Mode A test set (since that's what MasterEvaluator uses)
    df_tb_k = df_tb[df_tb["prefix_len"] <= 30]
    df_test = df_tb_k[df_tb_k["split"] == "test"].copy()
    
    predictions = res["mode_a_predictions"]
    
    print("\nRunning Paired Episode-Cluster Bootstrap (B=1000)...")
    results = compute_paired_bootstrap_test(
        df_test,
        predictions,
        base_model="S1",
        comparators=["M1", "S2", "H1", "H2", "H3", "H4"],
        n_iterations=1000,
        random_seed=42,
        max_k=30
    )
    
    output_path = r"p:\AIRE-TRACE\reports\gate7_statistical_tests.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSaved Gate 7 Statistical Testing results to: {output_path}")

if __name__ == "__main__":
    main()
