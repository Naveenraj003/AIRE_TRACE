import pandas as pd
import numpy as np
from src.baselines.m3_taskid import M3TaskidBaseline
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall
from src.evaluation.metrics import compute_all_metrics

def main():
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()

    y_train = df_train['eventual_outcome'].values.astype(int)

    m3 = M3TaskidBaseline()
    m3.fit(df_train, y_train)

    y_prob_calib = m3.predict_proba(df_calib)
    res = select_calibration_threshold(df_calib, y_prob_calib, target_far=0.05)
    frozen_threshold = res['frozen_threshold']

    y_prob_test = m3.predict_proba(df_test)
    mode_a_metrics = compute_all_metrics(df_test, y_prob_test, frozen_threshold, mode="prospective")
    
    test_far, test_recall, _ = compute_episode_far_and_recall(df_test, y_prob_test, frozen_threshold, mode="prospective")

    print(f"M3 TEST AUROC: {mode_a_metrics['AUROC']:.4f}")
    print(f"M3 TEST Recall_at_FAR (thr={frozen_threshold}): {test_recall:.4f}")

if __name__ == "__main__":
    main()
