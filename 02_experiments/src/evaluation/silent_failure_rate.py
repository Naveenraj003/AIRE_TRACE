"""
Rule-based classification of failure modes into immediate_error, persistent_struggle, silent, and other.
"""
import pandas as pd

def classify_episodes(df_group, checkpoint_dict):
    """
    df_group: dataframe containing prefixes for the episodes to classify.
    checkpoint_dict: dict mapping episode_id to its checkpoint step.
    """
    buckets = {"immediate_error": 0, "persistent_struggle": 0, "silent": 0, "other": 0}
    total = len(checkpoint_dict)
    
    for ep_id, cp_step in checkpoint_dict.items():
        # Get all prefixes up to the checkpoint
        ep_df = df_group[(df_group["episode_id"] == ep_id) & (df_group["prefix_len"] <= cp_step)]
        
        if len(ep_df) == 0:
            buckets["other"] += 1
            continue
            
        # Get latest prefix
        latest = ep_df.sort_values("prefix_len").iloc[-1]
        
        total_errors = latest["feat_tool_error_count"]
        window_length = latest["prefix_len"]
        max_repeated = ep_df["feat_repeated_action_last2"].max()
        
        if total_errors == 0 and max_repeated == 0:
            buckets["silent"] += 1
        elif total_errors >= 2:
            buckets["persistent_struggle"] += 1
        elif total_errors > 0 and window_length <= 2:
            buckets["immediate_error"] += 1
        else:
            buckets["other"] += 1
            
    return buckets, total

def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes.parquet"
    df_tb = pd.read_parquet(tb_path)
    
    df_test = df_tb[df_tb["split"] == "test"].copy()
    
    # 1. Failed episodes with onset_annotated=True
    fail_test = df_test[(df_test["eventual_outcome"] == 1) & (df_test["onset_annotated"] == True)].copy()
    fail_test["onset_col"] = pd.to_numeric(fail_test["annotation_derived_onset_step"], errors="coerce")
    fail_test = fail_test[fail_test["onset_col"].notna()]
    
    fail_checkpoint_dict = {}
    for ep_id, group in fail_test.groupby("episode_id"):
        onset = group["onset_col"].iloc[0]
        fail_checkpoint_dict[ep_id] = onset
        
    fail_buckets, fail_total = classify_episodes(fail_test, fail_checkpoint_dict)
    
    # 2. Successful TEST episodes
    succ_test = df_test[df_test["eventual_outcome"] == 0].copy()
    
    succ_checkpoint_dict = {}
    for ep_id, group in succ_test.groupby("episode_id"):
        # For successful episodes, equivalent checkpoint is the final step
        final_step = group["total_steps"].iloc[0]
        succ_checkpoint_dict[ep_id] = final_step
        
    succ_buckets, succ_total = classify_episodes(succ_test, succ_checkpoint_dict)
    
    def print_results(name, buckets, total):
        print(f"\n--- {name} (Total: {total}) ---")
        for k, v in buckets.items():
            pct = (v / total) * 100 if total > 0 else 0
            print(f"{k}: {v} ({pct:.1f}%)")
            
    print_results("Failed TEST Episodes (at onset)", fail_buckets, fail_total)
    print_results("Successful TEST Episodes (at end)", succ_buckets, succ_total)

if __name__ == "__main__":
    main()
