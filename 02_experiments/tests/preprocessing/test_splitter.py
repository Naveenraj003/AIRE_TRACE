import pytest
from src.preprocessing.splitter import make_task_disjoint_split

def test_task_disjoint_split():
    tasks = [f"task_{i}" for i in range(89)]
    train_tasks, calib_tasks, test_tasks = make_task_disjoint_split(tasks, n_train=53, n_calib=18, seed=42)

    assert len(train_tasks) == 53
    assert len(calib_tasks) == 18
    assert len(test_tasks) == 18

    assert len(train_tasks & calib_tasks) == 0
    assert len(train_tasks & test_tasks) == 0
    assert len(calib_tasks & test_tasks) == 0
