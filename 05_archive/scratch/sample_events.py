import pandas as pd
import random
from datasets import load_dataset
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
from src.preprocessing.terminalbench import normalize_tracebench_as_terminalbench

def main():
    tb_path = "p:/Projects/AIRE-TRACE/data/processed/manifests/terminalbench_prefixes.parquet"
    df_tb = pd.read_parquet(tb_path)
    
    df_test = df_tb[df_tb["split"] == "test"].copy()
    fail_test = df_test[(df_test["eventual_outcome"] == 1) & (df_test["onset_annotated"] == True)].copy()
    
    fail_test["onset_col"] = pd.to_numeric(fail_test["annotation_derived_onset_step"], errors="coerce")
    fail_test = fail_test[fail_test["onset_col"].notna()]
    
    unique_episodes = fail_test["episode_id"].unique().tolist()
    random.seed(42)
    sample_eps = random.sample(unique_episodes, 15)
    
    ds = load_dataset("Contextbench/Tracebench", split="full")
    ds_dict = {str(row["traj_id"]): row for row in ds}
    
    for ep_id in sample_eps:
        row = ds_dict.get(ep_id)
        if not row:
            continue
            
        print(f"\n=====================================")
        print(f"Episode: {ep_id}")
        
        onset_step = fail_test[fail_test["episode_id"] == ep_id]["onset_col"].iloc[0]
        print(f"Onset Step: {onset_step}")
        
        ep_record, events = normalize_tracebench_as_terminalbench(row, "dummy_sha")
        
        if not events:
            print("  No events parsed.")
            continue
            
        for ev in events:
            if ev.step_index <= onset_step:
                print(f"  Step {ev.step_index} | Actor: {ev.actor_role} | Action: {ev.action_type} | Tool: {ev.tool_name} | Err: {ev.is_error}")
                
if __name__ == "__main__":
    main()
