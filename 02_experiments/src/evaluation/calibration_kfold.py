import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
from src.evaluation.evaluator import MasterEvaluator
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall

def run_kfold_calibration():
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()

    # Fit S1 on TRAIN
    evaluator = MasterEvaluator(target_far=0.05, bootstrap_iterations=1, random_seed=42)
    models = evaluator._prepare_fitted_models(df_train)
    m = models['S1']
    feature_cols = [c for c in df_train.columns if c.startswith('feat_')]

    # Get probabilities for CALIBRATION
    X_calib = df_calib[feature_cols].copy()
    probs_calib = m.predict_proba(X_calib) if hasattr(m, 'predict_proba') else m.predict(X_calib)
    y_prob_calib = probs_calib[:, 1] if len(probs_calib.shape) == 2 else probs_calib

    # Get probabilities for TEST
    X_test = df_test[feature_cols].copy()
    probs_test = m.predict_proba(X_test) if hasattr(m, 'predict_proba') else m.predict(X_test)
    y_prob_test = probs_test[:, 1] if len(probs_test.shape) == 2 else probs_test

    # We K-Fold over the episodes in CALIBRATION only.
    # Why only CALIBRATION? To strictly maintain the frozen protocol rule that TRAIN data 
    # is used exclusively for fitting parameters, preventing leakage of fitting data into 
    # the threshold selection step.
    
    unique_calib_episodes = df_calib['episode_id'].unique()
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    
    thresholds = []
    
    for train_idx, test_idx in kf.split(unique_calib_episodes):
        complement_episodes = unique_calib_episodes[train_idx]
        mask = df_calib['episode_id'].isin(complement_episodes)
        df_fold = df_calib[mask].copy()
        y_prob_fold = y_prob_calib[mask]
        
        res = select_calibration_threshold(df_fold, y_prob_fold, target_far=0.05)
        thresholds.append(res['frozen_threshold'])

    mean_threshold = np.mean(thresholds)
    median_threshold = np.median(thresholds)
    
    print("5-Fold Calibration on CALIBRATION split only:")
    print("Why CALIBRATION only: To strictly isolate parameter fitting (TRAIN) from hyperparameter/threshold tuning (CALIBRATION), preventing data leakage in the threshold selection step.")
    print(f"Fold thresholds: {thresholds}")
    print(f"Mean threshold: {mean_threshold:.4f}")
    print(f"Median threshold: {median_threshold:.4f}")
    
    # Report TEST FAR/Recall using median threshold
    test_far, test_recall, _ = compute_episode_far_and_recall(df_test, y_prob_test, median_threshold, mode="prospective")
    print(f"\nTEST Evaluation using Median K-Fold Threshold ({median_threshold:.4f}):")
    print(f"FAR: {test_far:.4f}")
    print(f"Recall: {test_recall:.4f}")

if __name__ == "__main__":
    run_kfold_calibration()
