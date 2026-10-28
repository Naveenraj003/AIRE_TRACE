"""
AIRE-Trace Pairwise Direction Consistency (PDC) Module
Calculates ranking consistency and coverage across method pairs and evaluation metrics.
Respects 2-2 tie = 0.50 rule, informative-pair filtering, and explicit coverage reporting.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple

def evaluate_pairwise_metric(
    metric_name: str,
    val_a: float,
    val_b: float,
    tol: float = 1e-4
) -> int:
    """
    Compares metric values for method A vs method B.
    Returns +1 if Method A outperforms Method B, -1 if Method B outperforms Method A, 0 if tied.
    Note: For ECE, lower is better. For AUROC, AUPRC, Recall, higher is better.
    """
    if abs(val_a - val_b) <= tol:
        return 0 # Tie

    lower_is_better = (metric_name.upper() in ["ECE", "BRIER", "FAR"])
    
    if lower_is_better:
        return 1 if val_a < val_b else -1
    else:
        return 1 if val_a > val_b else -1


def compute_pdc_between_methods(
    method_a_metrics: Dict[str, float],
    method_b_metrics: Dict[str, float],
    metrics_to_compare: List[str] = None
) -> Dict[str, Any]:
    """
    Computes PDC and Coverage for a single pair of methods (Method A vs Method B).
    PDC = max(W, L) / (W + L) for informative pairs (W + L > 0).
    Coverage = (W + L) / total_metrics.
    If W == 2 and L == 2, PDC = 0.50.
    """
    if metrics_to_compare is None:
        metrics_to_compare = ["AUROC", "AUPRC", "Recall_at_FAR", "ECE"]

    wins, losses, ties = 0, 0, 0
    metric_results = {}

    for m in metrics_to_compare:
        va = method_a_metrics.get(m, 0.0)
        vb = method_b_metrics.get(m, 0.0)
        res = evaluate_pairwise_metric(m, va, vb)
        
        if res == 1:
            wins += 1
            metric_results[m] = "WIN (A > B)"
        elif res == -1:
            losses += 1
            metric_results[m] = "LOSS (A < B)"
        else:
            ties += 1
            metric_results[m] = "TIE (A == B)"

    informative_total = wins + losses
    total_metrics = len(metrics_to_compare)

    if informative_total == 0:
        pdc_val = None # All tied
        coverage = 0.0
    else:
        coverage = float(informative_total / total_metrics)
        if wins == 2 and losses == 2:
            pdc_val = 0.50
        else:
            pdc_val = float(max(wins, losses) / informative_total)

    return {
        "wins": wins,
        "losses": losses,
        "ties": ties,
        "informative_total": informative_total,
        "pdc": round(pdc_val, 4) if pdc_val is not None else None,
        "coverage": round(coverage, 4),
        "metric_comparisons": metric_results
    }


def compute_overall_pdc(
    results_by_method: Dict[str, Dict[str, float]],
    metrics_to_compare: List[str] = None
) -> Dict[str, Any]:
    """
    Computes full pairwise PDC matrix and overall average PDC & coverage across all method pairs.
    """
    methods = list(results_by_method.keys())
    pair_records = []
    pdc_values = []
    coverage_values = []

    for i in range(len(methods)):
        for j in range(i + 1, len(methods)):
            ma = methods[i]
            mb = methods[j]
            pair_res = compute_pdc_between_methods(
                results_by_method[ma],
                results_by_method[mb],
                metrics_to_compare
            )
            
            rec = {
                "pair": f"{ma} vs {mb}",
                "method_a": ma,
                "method_b": mb,
                "wins": pair_res["wins"],
                "losses": pair_res["losses"],
                "ties": pair_res["ties"],
                "pdc": pair_res["pdc"],
                "coverage": pair_res["coverage"],
                "metric_comparisons": pair_res["metric_comparisons"]
            }
            pair_records.append(rec)
            
            if pair_res["pdc"] is not None:
                pdc_values.append(pair_res["pdc"])
                coverage_values.append(pair_res["coverage"])

    mean_pdc = float(np.mean(pdc_values)) if len(pdc_values) > 0 else 0.0
    mean_coverage = float(np.mean(coverage_values)) if len(coverage_values) > 0 else 0.0

    return {
        "overall_pdc": round(mean_pdc, 4),
        "overall_pdc_coverage": round(mean_coverage, 4),
        "total_pairs": len(pair_records),
        "informative_pairs": len(pdc_values),
        "pairwise_details": pair_records
    }
