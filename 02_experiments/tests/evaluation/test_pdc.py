import pytest
from src.evaluation.pdc import compute_pdc_between_methods, compute_overall_pdc

def test_pdc_tie_handling():
    # 2 Wins, 2 Losses -> 2-2 tie -> PDC = 0.50, Coverage = 1.0
    mA = {"AUROC": 0.8, "AUPRC": 0.7, "Recall_at_FAR": 0.3, "ECE": 0.15}
    mB = {"AUROC": 0.7, "AUPRC": 0.6, "Recall_at_FAR": 0.4, "ECE": 0.05} # mB has higher recall and lower ECE (better ECE)
    
    res = compute_pdc_between_methods(mA, mB)
    assert res["wins"] == 2
    assert res["losses"] == 2
    assert res["pdc"] == 0.50
    assert res["coverage"] == 1.0

def test_pdc_overall():
    results = {
        "H1": {"AUROC": 0.6, "AUPRC": 0.5, "Recall_at_FAR": 0.2, "ECE": 0.2},
        "M1": {"AUROC": 0.7, "AUPRC": 0.6, "Recall_at_FAR": 0.4, "ECE": 0.1},
        "S1": {"AUROC": 0.8, "AUPRC": 0.7, "Recall_at_FAR": 0.5, "ECE": 0.08}
    }
    pdc_res = compute_overall_pdc(results)
    assert pdc_res["overall_pdc"] == 1.0 # Strict superiority hierarchy S1 > M1 > H1
    assert pdc_res["overall_pdc_coverage"] == 1.0
