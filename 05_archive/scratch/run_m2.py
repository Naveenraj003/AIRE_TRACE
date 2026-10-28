import pandas as pd
import numpy as np
from src.baselines.m2_semantic import M2SemanticBaseline
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall
from src.evaluation.metrics import compute_all_metrics

def main():
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()

    y_train = df_train['eventual_outcome'].values.astype(int)

    m2 = M2SemanticBaseline()
    m2.fit(df_train, y_train)

    y_prob_calib = m2.predict_proba(df_calib)
    res = select_calibration_threshold(df_calib, y_prob_calib, target_far=0.05)
    frozen_threshold = res['frozen_threshold']

    y_prob_test = m2.predict_proba(df_test)
    mode_a_metrics = compute_all_metrics(df_test, y_prob_test, frozen_threshold, mode="prospective")
    
    test_far, test_recall, _ = compute_episode_far_and_recall(df_test, y_prob_test, frozen_threshold, mode="prospective")

    print(f"M2 TEST AUROC: {mode_a_metrics['AUROC']:.4f}")
    print(f"M2 TEST Recall_at_FAR (thr={frozen_threshold}): {test_recall:.4f}")
    
    df_t1 = df_tb[df_tb['prefix_len'] == 1].copy()
    X_t1 = m2.extract_raw_features_for_duplicate_check(df_t1)
    
    df_X = pd.DataFrame(X_t1)
    duplicates = df_X.duplicated(keep=False)
    num_episodes_with_duplicates = duplicates.sum()
    
    print(f"\nM2 full feature space t=1 duplicate-vector check:")
    print(f"Total episodes at t=1: {len(df_t1)}")
    print(f"Episodes with identical t=1 features (including text TF-IDF): {num_episodes_with_duplicates}")

if __name__ == "__main__":
    main()
