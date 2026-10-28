import pandas as pd
import numpy as np
from src.baselines.m4_category import M4CategoryBaseline
from src.evaluation.thresholding import compute_episode_far_and_recall
from src.evaluation.metrics import compute_all_metrics
import warnings

def main():
    warnings.filterwarnings("ignore")
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_tb_k = df_tb[df_tb['prefix_len'] <= 30].copy()
    
    df_train = df_tb_k[df_tb_k['split'] == 'train'].copy()
    df_calib = df_tb_k[df_tb_k['split'] == 'calibration'].copy()
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()

    y_train = df_train['eventual_outcome'].values.astype(int)

    m4 = M4CategoryBaseline()
    m4.fit(df_train, y_train)

    train_cats = set([m4.meta_map.get(ep, {}).get("category", "unknown") for ep in df_train['episode_id'].unique()])
    
    ep_df_train = df_train[['episode_id']].drop_duplicates().copy()
    ep_df_train['category'] = ep_df_train['episode_id'].apply(lambda ep: m4.meta_map.get(ep, {}).get("category", "unknown"))
    ep_df_train['difficulty'] = ep_df_train['episode_id'].apply(lambda ep: m4.meta_map.get(ep, {}).get("difficulty", "unknown"))
    
    cat_counts = ep_df_train.groupby('category').size()
    diff_counts = ep_df_train.groupby('difficulty').size()
    
    print("--- TRAIN Category Episode Counts ---")
    print(cat_counts.to_string())
    print("\n--- TRAIN Difficulty Episode Counts ---")
    print(diff_counts.to_string())
    
    frozen_threshold = 0.93
    
    df_test['category'] = df_test['episode_id'].apply(lambda ep: m4.meta_map.get(ep, {}).get("category", "unknown"))
    df_test_seen = df_test[df_test['category'].isin(train_cats)].copy()
    df_test_novel = df_test[~df_test['category'].isin(train_cats)].copy()
    
    def evaluate_subset(df_sub, name):
        num_episodes = df_sub['episode_id'].nunique()
        if num_episodes == 0:
            print(f"\nSubset {name}: 0 episodes")
            return
            
        y_prob = m4.predict_proba(df_sub)
        
        try:
            metrics = compute_all_metrics(df_sub, y_prob, frozen_threshold, mode="prospective")
            auroc = metrics.get('AUROC', np.nan)
        except Exception:
            auroc = np.nan
            
        try:
            far, recall, _ = compute_episode_far_and_recall(df_sub, y_prob, frozen_threshold, mode="prospective")
        except Exception:
            far, recall = np.nan, np.nan
            
        print(f"\nSubset {name} ({num_episodes} episodes):")
        if pd.isna(auroc):
            print("AUROC: NaN (likely 0 failures in subset)")
        else:
            print(f"AUROC: {auroc:.4f}")
        print(f"Recall_at_FAR (thr={frozen_threshold}): {recall:.4f}")

    evaluate_subset(df_test_seen, "test_seen")
    evaluate_subset(df_test_novel, "test_novel")

if __name__ == "__main__":
    main()
