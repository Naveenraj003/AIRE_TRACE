import json
from datasets import load_dataset

ds = load_dataset("yoonholee/terminalbench-trajectories", split="train", streaming=True)
for row in ds:
    print(json.dumps(list(row.keys()), indent=2))
    print(row.get("task_name"))
    print(row.get("difficulty"))
    
    break
