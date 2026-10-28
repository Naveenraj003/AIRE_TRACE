"""
AIRE-Trace Task-Group Aware Splitter Module
Implements deterministic 53/18/18 task-disjoint splitting for TerminalBench.
"""

import random
from typing import List, Dict, Set, Tuple

def make_task_disjoint_split(
    tasks: List[str],
    n_train: int = 53,
    n_calib: int = 18,
    seed: int = 42
) -> Tuple[Set[str], Set[str], Set[str]]:
    """
    Splits unique task names into three disjoint sets: TRAIN, CALIBRATION, TEST.
    Uses deterministic shuffling with fixed seed.
    """
    sorted_unique_tasks = sorted(list(set(tasks)))
    rng = random.Random(seed)
    shuffled_tasks = list(sorted_unique_tasks)
    rng.shuffle(shuffled_tasks)

    train_tasks = set(shuffled_tasks[:n_train])
    calib_tasks = set(shuffled_tasks[n_train:n_train + n_calib])
    test_tasks = set(shuffled_tasks[n_train + n_calib:])

    # Runtime assertion: zero task overlap
    assert len(train_tasks & calib_tasks) == 0, f"Task overlap between Train and Calib: {train_tasks & calib_tasks}"
    assert len(train_tasks & test_tasks) == 0, f"Task overlap between Train and Test: {train_tasks & test_tasks}"
    assert len(calib_tasks & test_tasks) == 0, f"Task overlap between Calib and Test: {calib_tasks & test_tasks}"

    return train_tasks, calib_tasks, test_tasks
