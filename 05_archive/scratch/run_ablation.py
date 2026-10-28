import pandas as pd
import numpy as np
from src.baselines.logistic import LogisticBaseline
from src.baselines.m4_category import M4CategoryBaseline
from src.evaluation.thresholding import select_calibration_threshold, compute_episode_far_and_recall
from src.evaluation.metrics import compute_all_metrics
import warnings

class M4CategoryOnly(M4CategoryBaseline):
    def _extract_features(self, df: pd.DataFrame, is_fit: bool) -> np.ndarray:
        if self.feature_cols is None:
            self.feature_cols = [c for c in df.columns if str(c).startswith("feat_")]
        X_num = df[self.feature_cols].values
        episodes = df['episode_id'].values
        cat_encoded = np.zeros(len(df))
        for i, ep in enumerate(episodes):
            meta = self.meta_map.get(ep, {"category": "unknown"})
            cat_encoded[i] = self.cat_failure_rates.get(meta["category"], self.global_failure_rate)
        X_cat = cat_encoded.reshape(-1, 1)
        X_combined = np.hstack([X_num, X_cat])
        if is_fit:
            return self.scaler.fit_transform(X_combined)
        else:
            return self.scaler.transform(X_combined)

def main():
    warnings.filterwarnings("ignore")
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()
    
    y_train = df_train['eventual_outcome'].values.astype(int)
    
    # 1. Identify supported categories
    m4_dummy = M4CategoryBaseline()
    m4_dummy.fit(df_train, y_train)
    
    ep_df_train = df_train[['episode_id']].drop_duplicates().copy()
    ep_df_train['category'] = ep_df_train['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    cat_counts = ep_df_train.groupby('category').size()
    supported_cats = cat_counts[cat_counts >= 10].index.tolist()
    
    df_test['category'] = df_test['episode_id'].apply(lambda ep: m4_dummy.meta_map.get(ep, {}).get("category", "unknown"))
    df_test_supported = df_test[df_test['category'].isin(supported_cats)].copy()
    
    print(f"Running ablation on {df_test_supported['episode_id'].nunique()} supported TEST episodes (categories: {supported_cats})")
    
    # Evaluation function
    def evaluate_model(name, model):
        model.fit(df_train, y_train)
        y_prob_calib = model.predict_proba(df_calib)
        res = select_calibration_threshold(df_calib, y_prob_calib, target_far=0.05)
        thr = res['frozen_threshold']
        
        y_prob_test = model.predict_proba(df_test_supported)
        metrics = compute_all_metrics(df_test_supported, y_prob_test, thr, mode="prospective")
        auroc = metrics.get('AUROC', np.nan)
        _, recall, _ = compute_episode_far_and_recall(df_test_supported, y_prob_test, thr, mode="prospective")
        
        print(f"| {name:<35} | {auroc:.4f} | {recall:.4f} | {thr:.2f} |")
    
    print("-" * 75)
    print(f"| {'Model / Ablation Variant':<35} | {'AUROC':<6} | {'Recall':<6} | {'Thr':<4} |")
    print("-" * 75)
    
    # 2. Run ablation
    evaluate_model("1. History-only (M1)", LogisticBaseline())
    evaluate_model("2. Category-conditioned (M4-cat)", M4CategoryOnly())
    evaluate_model("3. Cat+Diff-conditioned (M4-full)", M4CategoryBaseline())
    print("-" * 75)

if __name__ == "__main__":
    main()
