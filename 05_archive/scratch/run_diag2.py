import pandas as pd
import numpy as np
from src.baselines.m2_semantic import M2SemanticBaseline

def main():
    # 1. Duplicate check in the instructions parquet
    df_inst = pd.read_parquet('results/research_extension/episode_task_instructions.parquet')
    dup_count = df_inst['episode_id'].duplicated().sum()
    print(f"episode_task_instructions.parquet episode_id duplicates: {dup_count}")

    # 2. Check length before and after merge in fit()
    df_tb = pd.read_parquet('data/processed/manifests/terminalbench_prefixes.parquet')
    df_train = df_tb[(df_tb['split'] == 'train') & (df_tb['prefix_len'] <= 30)].copy()

    len_before = len(df_train)
    m2 = M2SemanticBaseline()
    
    # We must fit m2 first
    y_train = df_train['eventual_outcome'].values.astype(int)
    m2.fit(df_train, y_train)
    
    merged = df_train.merge(m2.instructions_df, on='episode_id', how='left')
    len_after = len(merged)
    print(f"len(df_train) before merge: {len_before}")
    print(f"len(df_train) after merge: {len_after}")
    print("-" * 50)

    # 3. Group the 591 duplicate t=1 episodes by task_id
    df_t1 = df_tb[df_tb['prefix_len'] == 1].copy()
    X_t1 = m2.extract_raw_features_for_duplicate_check(df_t1)
    
    # We need to map the duplicates.
    df_X = pd.DataFrame(X_t1)
    # Find all rows that have at least one exact duplicate
    is_duplicate = df_X.duplicated(keep=False).values
    dup_episodes = df_t1.iloc[is_duplicate].copy()
    
    # User requested: "groupby('task_id').size() — what fraction of those duplicate groups share the same task_id 
    # (expected, same task/different agent) versus span different task_ids (a real information gap)?"
    
    # To answer this, we should group by the identical feature vectors themselves, and check how many unique task_ids each group contains.
    dup_episodes['feature_group_id'] = df_X.iloc[is_duplicate].apply(lambda row: hash(tuple(row)), axis=1).values
    
    group_task_counts = dup_episodes.groupby('feature_group_id')['task_id'].nunique()
    
    single_task_groups = group_task_counts[group_task_counts == 1]
    multi_task_groups = group_task_counts[group_task_counts > 1]
    
    print(f"Total t=1 episodes with duplicates: {len(dup_episodes)} (which form {len(group_task_counts)} unique feature-vector groups)")
    print(f"Number of these feature groups that contain exactly 1 task_id (expected): {len(single_task_groups)}")
    print(f"Number of these feature groups that span MULTIPLE task_ids (information gap): {len(multi_task_groups)}")

if __name__ == "__main__":
    main()
