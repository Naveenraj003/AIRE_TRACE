import os
import json
import yaml
import pandas as pd
from datasets import load_dataset
from src.preprocessing.terminalbench import normalize_tracebench_as_terminalbench

def main():
    config_path = r"p:\Projects\AIRE-TRACE\configs\data.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    tb_cfg = cfg["datasets"]["terminalbench"]
    print(f"Loading {tb_cfg['hf_repo']} (split: {tb_cfg['split']})...")
    tb_ds = load_dataset(tb_cfg["hf_repo"], split=tb_cfg["split"])
    
    records = []
    
    print("Extracting instructions...")
    for idx, row in enumerate(tb_ds):
        if idx % 100 == 0:
            print(f"Processed {idx} rows...")
        res = normalize_tracebench_as_terminalbench(row, tb_cfg["commit_sha"])
        if res is None or res[0] is None:
            continue
        ep, _ = res
        records.append({
            "episode_id": ep.episode_id,
            "task_instruction": ep.task_instruction
        })
        
    df = pd.DataFrame(records)
    out_dir = r"p:\Projects\AIRE-TRACE\results\research_extension"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "episode_task_instructions.parquet")
    df.to_parquet(out_path, index=False)
    print(f"Saved {len(df)} records to {out_path}")

if __name__ == "__main__":
    main()
