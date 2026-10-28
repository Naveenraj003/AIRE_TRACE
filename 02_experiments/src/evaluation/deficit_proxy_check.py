"""
Tests whether two proxy signals for failure deficits separate meaningfully.
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
from datasets import load_dataset
import sys
import os

def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes.parquet"
    df_tb = pd.read_parquet(tb_path)
    
    # Load metadata mapping to get category and difficulty
    print("Loading dataset metadata...")
    ds = load_dataset("Contextbench/Tracebench", split="full")
    meta_map = {row["traj_id"]: {"category": row["category"], "difficulty": row["difficulty"]} for row in ds}
    
    # Apply category and difficulty
    df_tb["category"] = df_tb["episode_id"].map(lambda x: meta_map.get(x, {}).get("category", "unknown"))
    df_tb["difficulty"] = df_tb["episode_id"].map(lambda x: meta_map.get(x, {}).get("difficulty", "unknown"))
    
    df_train = df_tb[df_tb["split"] == "train"].copy()
    df_test = df_tb[df_tb["split"] == "test"].copy()
    
    print("Computing TRAIN means...")
    df_train["proxy_a"] = df_train["feat_retry_count"] + df_train["feat_tool_error_count"]
    df_train["proxy_b"] = df_train["feat_repeated_action_last2"]
    
    # Using episode max or mean across all prefixes? We will use mean across all prefixes
    # as a baseline rate for that category/difficulty.
    mean_a = df_train.groupby(["category", "difficulty"])["proxy_a"].mean().to_dict()
    mean_b = df_train.groupby(["category", "difficulty"])["proxy_b"].mean().to_dict()
    
    # Test failed episodes with onset_annotated=True
    fail_test = df_test[(df_test["eventual_outcome"] == 1) & (df_test["onset_annotated"] == True)].copy()
    
    fail_test["onset_col"] = pd.to_numeric(fail_test["annotation_derived_onset_step"], errors="coerce")
    fail_test = fail_test[fail_test["onset_col"].notna()]
    
    # Window immediately before onset (prefix_len <= onset_step)
    at_onset = fail_test[fail_test["prefix_len"] <= fail_test["onset_col"]]
    # Get the latest available prefix that is <= onset
    at_onset = at_onset.sort_values("prefix_len").groupby("episode_id").last().reset_index()
    
    at_onset["proxy_a_raw"] = at_onset["feat_retry_count"] + at_onset["feat_tool_error_count"]
    at_onset["proxy_b_raw"] = at_onset["feat_repeated_action_last2"]
    
    def get_relative(row, proxy_raw, mean_dict):
        cat_diff = (row["category"], row["difficulty"])
        base_mean = mean_dict.get(cat_diff, 0.0)
        return row[proxy_raw] - base_mean
        
    at_onset["proxy_a_rel"] = at_onset.apply(lambda r: get_relative(r, "proxy_a_raw", mean_a), axis=1)
    at_onset["proxy_b_rel"] = at_onset.apply(lambda r: get_relative(r, "proxy_b_raw", mean_b), axis=1)
    
    if len(at_onset) > 0:
        pearson_corr, _ = pearsonr(at_onset["proxy_a_rel"], at_onset["proxy_b_rel"])
        spearman_corr, _ = spearmanr(at_onset["proxy_a_rel"], at_onset["proxy_b_rel"])
        
        # Partial correlation controlling for prefix_len
        # Regress proxy_a_rel on prefix_len
        len_vals = at_onset["prefix_len"].values
        a_vals = at_onset["proxy_a_rel"].values
        b_vals = at_onset["proxy_b_rel"].values
        
        # Simple linear regression: y = beta * x + intercept
        slope_a, intercept_a = np.polyfit(len_vals, a_vals, 1)
        res_a = a_vals - (slope_a * len_vals + intercept_a)
        
        slope_b, intercept_b = np.polyfit(len_vals, b_vals, 1)
        res_b = b_vals - (slope_b * len_vals + intercept_b)
        
        part_pearson, _ = pearsonr(res_a, res_b)
        part_spearman, _ = spearmanr(res_a, res_b)
        
        print(f"Number of analyzed episodes: {len(at_onset)}")
        print(f"Raw Correlation (Pearson): {pearson_corr:.4f} | Partial Correlation: {part_pearson:.4f}")
        print(f"Raw Correlation (Spearman): {spearman_corr:.4f} | Partial Correlation: {part_spearman:.4f}")
    else:
        print("No valid episodes found.")

if __name__ == "__main__":
    main()
