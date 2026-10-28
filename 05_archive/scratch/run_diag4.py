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
    df_test = df_tb_k[df_tb_k['split'] == 'test'].copy()

    y_train = df_train['eventual_outcome'].values.astype(int)

    m4 = M4CategoryBaseline()
    m4.fit(df_train, y_train)

    ep_df_train = df_train[['episode_id']].drop_duplicates().copy()
    ep_df_train['category'] = ep_df_train['episode_id'].apply(lambda ep: m4.meta_map.get(ep, {}).get("category", "unknown"))
    
    cat_counts = ep_df_train.groupby('category').size()
    supported_cats = cat_counts[cat_counts >= 10].index.tolist()
    train_count_per_supported_category = cat_counts[supported_cats].to_dict()
    
    frozen_threshold = 0.93
    
    df_test['category'] = df_test['episode_id'].apply(lambda ep: m4.meta_map.get(ep, {}).get("category", "unknown"))
    
    df_test_supported = df_test[df_test['category'].isin(supported_cats)].copy()
    df_test_excluded = df_test[~df_test['category'].isin(supported_cats)].copy()
    
    test_supported_episode_count = df_test_supported['episode_id'].nunique()
    test_excluded_episode_count = df_test_excluded['episode_id'].nunique()
    
    y_prob = m4.predict_proba(df_test_supported)
    
    metrics = compute_all_metrics(df_test_supported, y_prob, frozen_threshold, mode="prospective")
    test_supported_AUROC = metrics.get('AUROC', np.nan)
    
    _, test_supported_Recall_at_FAR, _ = compute_episode_far_and_recall(df_test_supported, y_prob, frozen_threshold, mode="prospective")
    
    print(f"supported_categories = {supported_cats}")
    print(f"train_count_per_supported_category = {train_count_per_supported_category}\n")
    print(f"test_supported_episode_count = {test_supported_episode_count}")
    print(f"test_supported_AUROC = {test_supported_AUROC:.4f}")
    print(f"test_supported_Recall_at_FAR = {test_supported_Recall_at_FAR:.4f}\n")
    print(f"frozen_M4_threshold = {frozen_threshold}\n")
    print(f"excluded_TEST_episode_count = {test_excluded_episode_count}")

if __name__ == "__main__":
    main()
