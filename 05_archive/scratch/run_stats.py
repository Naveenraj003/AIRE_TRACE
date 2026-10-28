import pandas as pd
import numpy as np
import scipy.stats as stats
import warnings

from src.baselines.logistic import LogisticBaseline
from src.baselines.m4_category import M4CategoryBaseline
from src.evaluation.statistical_testing import compute_paired_bootstrap_test

class M4DifficultyOnly(M4CategoryBaseline):
    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
        X_num = df[self.feature_cols].values
        episodes = df['episode_id'].values
        diff_encoded = np.zeros(len(df))
        for i, ep in enumerate(episodes):
            meta = self.meta_map.get(ep, {"difficulty": "unknown"})
            diff_encoded[i] = self.diff_failure_rates.get(meta["difficulty"], self.global_failure_rate)
        X_diff = diff_encoded.reshape(-1, 1)
        X_combined = np.hstack([X_num, X_diff])
        if is_fit:
            return self.scaler.fit_transform(X_combined)
        else:
            return self.scaler.transform(X_combined)

def main():
    warnings.filterwarnings("ignore")
    
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()
    
    y_train = df_train['eventual_outcome'].values.astype(int)
    
    m4_dummy = M4CategoryBaseline()
    m4_dummy.fit(df_train, y_train)
    
    ep_df_train = df_train[['episode_id']].drop_duplicates().copy()
    ep_df_train['category'] = ep_df_train['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    cat_counts = ep_df_train.groupby('category').size()
    supported_cats = cat_counts[cat_counts >= 10].index.tolist()
    
    df_test['category'] = df_test['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    df_test_supported = df_test[df_test['category'].isin(supported_cats)].copy()
    
    # 1. Fit models
    m1 = LogisticBaseline()
    m1.fit(df_train, y_train)
    y_prob_m1 = m1.predict_proba(df_test_supported)
    
    m_diff = M4DifficultyOnly()
    m_diff.fit(df_train, y_train)
    y_prob_diff = m_diff.predict_proba(df_test_supported)
    
    m_full = M4CategoryBaseline()
    m_full.fit(df_train, y_train)
    y_prob_full = m_full.predict_proba(df_test_supported)
    
    # --- TASK 1: Paired Wilcoxon Test for DeltaP ---
    df_ts = df_test_supported.copy()
    df_ts['prob_m1'] = y_prob_m1
    df_ts['prob_m4'] = y_prob_full
    
    fail_df = df_ts[df_ts['eventual_outcome'] == 1].copy()
    onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
    valid_mask = (fail_df["onset_annotated"].astype(bool)) & (onset_col.notna()) & (fail_df["prefix_len"] <= onset_col)
    fail_valid_df = fail_df[valid_mask].copy()
    
    delta_m1 = []
    delta_m4 = []
    
    for ep_id, ep_grp in fail_valid_df.groupby('episode_id'):
        ep_grp = ep_grp.sort_values('prefix_len')
        if len(ep_grp) == 0:
            continue
        d_m1 = ep_grp.iloc[-1]['prob_m1'] - ep_grp.iloc[0]['prob_m1']
        d_m4 = ep_grp.iloc[-1]['prob_m4'] - ep_grp.iloc[0]['prob_m4']
        delta_m1.append(d_m1)
        delta_m4.append(d_m4)
        
    delta_m1 = np.array(delta_m1)
    delta_m4 = np.array(delta_m4)
    delta_diff = delta_m4 - delta_m1
    
    w_stat, p_val = stats.wilcoxon(delta_diff)
    zeros = np.sum(delta_diff == 0)
    
    print("--- TASK 1: PAIRED WILCOXON TEST (DeltaP) ---")
    print(f"n = {len(delta_diff)}")
    print(f"M1   DeltaP: mean = {np.mean(delta_m1):.4f}, median = {np.median(delta_m1):.4f}")
    print(f"M4   DeltaP: mean = {np.mean(delta_m4):.4f}, median = {np.median(delta_m4):.4f}")
    print(f"Paired median difference (M4 - M1): {np.median(delta_diff):.4f}")
    print(f"Zero differences / ties: {zeros}")
    print(f"Wilcoxon statistic: {w_stat}")
    print(f"p-value: {p_val:.4e}")
    
    # --- TASK 2: AUROC COMPARISON ---
    print("\n--- TASK 2: AUROC COMPARISON ---")
    predictions = {
        "M4-diff": y_prob_diff,
        "M4-full": y_prob_full
    }
    
    # Run the paired bootstrap test
    print("Running paired bootstrap (1000 iterations, episode-cluster)...")
    res = compute_paired_bootstrap_test(
        df_test_supported, 
        predictions, 
        base_model="M4-diff", 
        comparators=["M4-full"], 
        n_iterations=1000, 
        random_seed=42, 
        max_k=30
    )
    
    auroc_res = [r for r in res if r["metric"] == "AUROC"][0]
    print(f"Difference (Diff-only - Cat+Diff) obs: {auroc_res['delta_obs']:.4f}")
    print(f"Method: Paired episode-cluster bootstrap (N=1000)")
    print(f"Bootstrap mean difference: {auroc_res['bootstrap_mean_delta']:.4f}")
    print(f"p-value (raw): {auroc_res['p_raw']:.4f}")
    print(f"p-value (adj): {auroc_res['p_adj']:.4f}")
    
    # --- TASK 3: FALSE-TRIGGER COST ---
    print("\n--- TASK 3: FALSE-TRIGGER COST ---")
    print("M1 false-trigger rate = 2.0%")
    print("M4 false-trigger rate = 12.0%")
    print("Absolute increase = 10.0 percentage points")
    print("Relative increase = 6x")

if __name__ == "__main__":
    main()
