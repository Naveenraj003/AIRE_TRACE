"""
Compute point-biserial correlations of Category-A features against eventual_outcome at K=1, 15, 30.
"""
import pandas as pd
import numpy as np
from scipy.stats import pointbiserialr

def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes_new.parquet"
    df_tb = pd.read_parquet(tb_path)
    df_train = df_tb[df_tb["split"] == "train"].copy()
    
    feature_cols = [c for c in df_train.columns if c.startswith("feat_")]
    
    results = {}
    checkpoints = [1, 15, 30]
    
    for k in checkpoints:
        # Get prefixes up to K, take the last one for each episode
        df_k = df_train[df_train["prefix_len"] <= k]
        df_k_latest = df_k.sort_values("prefix_len").groupby("episode_id").last().reset_index()
        
        y = df_k_latest["eventual_outcome"].values
        
        results[k] = {}
        for feat in feature_cols:
            x = df_k_latest[feat].values
            # If feature is constant, correlation is undefined (nan)
            if np.std(x) == 0:
                corr = 0.0
            else:
                corr, _ = pointbiserialr(x, y)
            results[k][feat] = corr
            
    # Rank by K=30 absolute correlation
    ranked_features = sorted(feature_cols, key=lambda f: abs(results[30].get(f, 0)), reverse=True)
    
    print("Feature Correlations with eventual_outcome (Point-Biserial)\n")
    print(f"{'Feature':<30} | {'K=1':<8} | {'K=15':<8} | {'K=30':<8}")
    print("-" * 65)
    for feat in ranked_features:
        c1 = results[1][feat]
        c15 = results[15][feat]
        c30 = results[30][feat]
        print(f"{feat:<30} | {c1:>8.4f} | {c15:>8.4f} | {c30:>8.4f}")
        
    print("\n--- Sign Flips Between Checkpoints ---")
    flips_found = False
    for feat in feature_cols:
        c1 = results[1][feat]
        c15 = results[15][feat]
        c30 = results[30][feat]
        
        # Only consider a flip if both correlations have magnitude > 0.01 to avoid noise flips
        s1 = np.sign(c1) if abs(c1) > 0.01 else 0
        s15 = np.sign(c15) if abs(c15) > 0.01 else 0
        s30 = np.sign(c30) if abs(c30) > 0.01 else 0
        
        signs = [s for s in [s1, s15, s30] if s != 0]
        if len(set(signs)) > 1:
            print(f"Sign flip detected for {feat}: K=1 ({c1:.4f}) -> K=15 ({c15:.4f}) -> K=30 ({c30:.4f})")
            flips_found = True
            
    if not flips_found:
        print("No significant sign flips detected.")
        
    print("\n--- Deep Dive: Error & Retry Counts ---")
    for feat in ["feat_tool_error_count", "feat_retry_count"]:
        if feat in results[30]:
            c1 = results[1][feat]
            c15 = results[15][feat]
            c30 = results[30][feat]
            print(f"{feat}:")
            print(f"  K=1  : {c1:.4f}")
            print(f"  K=15 : {c15:.4f}")
            print(f"  K=30 : {c30:.4f}")

if __name__ == "__main__":
    main()
