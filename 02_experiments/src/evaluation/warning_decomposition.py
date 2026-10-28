"""
Decomposes M1 warning scores into static and dynamic components.
"""
import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import sys
import os

# Ensure src can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.baselines.m4_category import M4CategoryBaseline
from src.baselines.logistic import LogisticBaseline

def custom_select_calibration_threshold(df_calib, y_prob_calib, target_far=0.05):
    df_tmp = df_calib[["episode_id", "eventual_outcome", "onset_annotated", "annotation_derived_onset_step", "prefix_len"]].copy()
    df_tmp["prob"] = y_prob_calib
    
    ep_all = df_tmp.groupby("episode_id").agg(
        outcome=("eventual_outcome", "first"),
        max_prob=("prob", "max")
    )
    succ_probs = ep_all[ep_all["outcome"] == 0]["max_prob"].values
    n_succ = len(succ_probs)
    
    fail_df = df_tmp[df_tmp["eventual_outcome"] == 1]
    onset_col = pd.to_numeric(fail_df["annotation_derived_onset_step"], errors="coerce")
    valid_episodes = fail_df[(fail_df["onset_annotated"].astype(bool)) & (onset_col.notna())]["episode_id"].unique()
    n_fail = len(valid_episodes)
    
    valid_mask = (
        (fail_df["onset_annotated"].astype(bool)) & 
        (onset_col.notna()) & 
        (fail_df["prefix_len"] <= onset_col)
    )
    fail_valid_df = fail_df[valid_mask]
    if len(fail_valid_df) == 0:
        return {"frozen_threshold": 0.5, "calibration_far": 1.0, "calibration_recall": 0.0}
    fail_probs = fail_valid_df.groupby("episode_id")["prob"].max().values
    
    # Use a dynamic range for candidate thresholds
    min_p, max_p = y_prob_calib.min(), y_prob_calib.max()
    # Add a bit of margin
    candidate_thresholds = np.linspace(min_p - 0.01, max_p + 0.01, 500)
    
    best_tau = 0.5
    best_recall = -1.0
    best_far = 1.0
    
    for tau in candidate_thresholds:
        far = float(np.sum(succ_probs >= tau) / n_succ) if n_succ > 0 else 0.0
        recall = float(np.sum(fail_probs >= tau) / n_fail) if n_fail > 0 else 0.0
        
        if far <= target_far:
            if recall > best_recall or (recall == best_recall and far < best_far):
                best_tau = float(tau)
                best_recall = recall
                best_far = far
                
    return {"frozen_threshold": best_tau, "calibration_far": best_far, "calibration_recall": best_recall}


def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes.parquet"
    df_tb = pd.read_parquet(tb_path)
    
    # Filter for K=30
    df_tb = df_tb[df_tb["prefix_len"] <= 30].copy()
    
    df_train = df_tb[df_tb["split"] == "train"].copy()
    df_calib = df_tb[df_tb["split"] == "calibration"].copy()
    df_test = df_tb[df_tb["split"] == "test"].copy()
    
    y_train = df_train["eventual_outcome"].values.astype(int)
    feature_cols = [c for c in df_train.columns if c.startswith("feat_")]
    
    # M4-category-only
    print("Training static component (M4-category-only)...")
    m4_static = M4CategoryBaseline(model_id="M4_static", feature_cols=[])
    m4_static.fit(df_train, y_train)
    
    # M1
    print("Training M1...")
    m1 = LogisticBaseline(model_id="M1", feature_cols=feature_cols)
    m1.fit(df_train, y_train)

    print("Training full M4...")
    m4 = M4CategoryBaseline(model_id="M4", feature_cols=feature_cols)
    m4.fit(df_train, y_train)
    
    # Predict on CALIB and TEST
    prob_m4_static_calib = m4_static.predict_proba(df_calib)
    prob_m1_calib = m1.predict_proba(df_calib)
    dyn_comp_calib = prob_m1_calib - prob_m4_static_calib
    
    prob_m4_static_test = m4_static.predict_proba(df_test)
    prob_m1_test = m1.predict_proba(df_test)
    dyn_comp_test = prob_m1_test - prob_m4_static_test

    prob_m4_test = m4.predict_proba(df_test)
    prob_m4_calib = m4.predict_proba(df_calib)
    
    # 1. Correlation on TEST failing episodes
    fail_test = df_test[df_test["eventual_outcome"] == 1].copy()
    fail_test["time_to_failure"] = fail_test["total_steps"] - fail_test["prefix_len"]
    
    fail_prob_m4_static = m4_static.predict_proba(fail_test)
    fail_prob_m1 = m1.predict_proba(fail_test)
    fail_test["dyn_comp"] = fail_prob_m1 - fail_prob_m4_static
    
    pearson_corr, _ = pearsonr(fail_test["dyn_comp"], fail_test["time_to_failure"])
    spearman_corr, _ = spearmanr(fail_test["dyn_comp"], fail_test["time_to_failure"])
    print(f"Correlation (Pearson): {pearson_corr:.4f}")
    print(f"Correlation (Spearman): {spearman_corr:.4f}")
    
    # 2. Re-thresholding
    from src.evaluation.thresholding import select_calibration_threshold
    
    dyn_thresh_info = custom_select_calibration_threshold(df_calib, dyn_comp_calib)
    m1_thresh_info = select_calibration_threshold(df_calib, prob_m1_calib)
    m4_thresh_info = select_calibration_threshold(df_calib, prob_m4_calib)
    
    from src.evaluation.thresholding import compute_episode_far_and_recall
    
    dyn_far, dyn_recall, _ = compute_episode_far_and_recall(df_test, dyn_comp_test, dyn_thresh_info["frozen_threshold"], mode="prospective")
    m1_far, m1_recall, _ = compute_episode_far_and_recall(df_test, prob_m1_test, m1_thresh_info["frozen_threshold"], mode="prospective")
    m4_far, m4_recall, _ = compute_episode_far_and_recall(df_test, prob_m4_test, m4_thresh_info["frozen_threshold"], mode="prospective")
    
    print(f"Recall@FAR (Dyn Comp): Recall={dyn_recall:.4f}, FAR={dyn_far:.4f}, Thresh={dyn_thresh_info['frozen_threshold']:.4f}")
    print(f"Recall@FAR (M1): Recall={m1_recall:.4f}, FAR={m1_far:.4f}")
    print(f"Recall@FAR (M4): Recall={m4_recall:.4f}, FAR={m4_far:.4f}")

    # --- Persist TEST predictions for downstream bootstrap analysis ---
    # All values below are computed from TRAIN-fit models applied to TEST prefixes.
    # The dyn_comp threshold was selected from CALIBRATION only; no TEST data was used.
    import json
    import os

    out_dir = "results/baseline_runs"
    os.makedirs(out_dir, exist_ok=True)

    pred_df = df_test[["episode_id", "prefix_len", "total_steps", "eventual_outcome",
                        "onset_annotated", "annotation_derived_onset_step"]].copy()
    pred_df["prob_m1"]       = prob_m1_test
    pred_df["prob_m4_static"] = prob_m4_static_test
    pred_df["dyn_comp"]      = dyn_comp_test

    parquet_path = os.path.join(out_dir, "dyn_comp_predictions_k30.parquet")
    pred_df.to_parquet(parquet_path, index=False)
    print(f"\nSaved dyn_comp predictions ({len(pred_df)} rows, "
          f"{pred_df['episode_id'].nunique()} episodes) -> {parquet_path}")

    thresh_path = os.path.join(out_dir, "dyn_comp_threshold_k30.json")
    thresh_record = {
        "dyn_comp_frozen_threshold": dyn_thresh_info["frozen_threshold"],
        "dyn_comp_calibration_far":  dyn_thresh_info["calibration_far"],
        "dyn_comp_calibration_recall": dyn_thresh_info["calibration_recall"],
        "m1_frozen_threshold": m1_thresh_info["frozen_threshold"],
        "m1_calibration_far":  m1_thresh_info["calibration_far"],
        "m1_calibration_recall": m1_thresh_info["calibration_recall"],
        "horizon_k": 30,
        "target_far": 0.05,
        "note": "Threshold selected from CALIBRATION split only. No TEST data used."
    }
    with open(thresh_path, "w") as f:
        json.dump(thresh_record, f, indent=2)
    print(f"Saved dyn_comp threshold info -> {thresh_path}")


if __name__ == "__main__":
    main()

