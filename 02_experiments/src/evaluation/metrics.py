"""
AIRE-Trace Evaluation Metrics Module
Implements weighted AUROC, AUPRC, Brier Score, Expected Calibration Error (ECE),
and Episode-level Recall @ FAR <= 5% with episode-balanced sample weights w_{i,t} = 1 / min(T_i, K).
"""

import numpy as np
import pandas as pd
from typing import Dict, Any
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc, brier_score_loss
from src.evaluation.thresholding import compute_episode_far_and_recall

def compute_sample_weights(df_prefixes: pd.DataFrame, max_k: int = 30) -> np.ndarray:
    """Computes episode-balanced sample weight w_{i,t} = 1 / min(T_i, K)."""
    weights = 1.0 / np.minimum(df_prefixes["total_steps"].values, max_k)
    return weights.astype(float)


def compute_weighted_auroc(y_true: np.ndarray, y_prob: np.ndarray, sample_weight: np.ndarray) -> float:
    """Computes sample-weighted Area Under ROC Curve."""
    if len(np.unique(y_true)) < 2:
        return 0.5
    try:
        val = roc_auc_score(y_true, y_prob, sample_weight=sample_weight)
        return float(val)
    except Exception:
        return 0.5


def compute_weighted_auprc(y_true: np.ndarray, y_prob: np.ndarray, sample_weight: np.ndarray) -> float:
    """Computes sample-weighted Area Under Precision-Recall Curve."""
    if len(np.unique(y_true)) < 2:
        return 0.0
    try:
        precision, recall, _ = precision_recall_curve(y_true, y_prob, sample_weight=sample_weight)
        val = auc(recall, precision)
        return float(val)
    except Exception:
        return 0.0


def compute_weighted_brier(y_true: np.ndarray, y_prob: np.ndarray, sample_weight: np.ndarray) -> float:
    """Computes sample-weighted Brier Score."""
    try:
        val = brier_score_loss(y_true, y_prob, sample_weight=sample_weight)
        return float(val)
    except Exception:
        return float(np.mean((y_prob - y_true) ** 2))


def compute_weighted_ece(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    sample_weight: np.ndarray,
    n_bins: int = 10
) -> float:
    """
    Computes sample-weighted Expected Calibration Error (ECE).
    Partition predictions into n_bins uniform probability bins in [0, 1].
    ECE = sum_{b=1}^{n_bins} (weight_b / sum_weights) * |acc_b - conf_b|
    """
    bin_boundaries = np.linspace(0.0, 1.0, n_bins + 1)
    total_weight = np.sum(sample_weight)
    if total_weight < 1e-9:
        return 0.0

    ece = 0.0
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        if i == n_bins - 1:
            in_bin = (y_prob >= bin_lower) & (y_prob <= bin_upper)
        else:
            in_bin = (y_prob >= bin_lower) & (y_prob < bin_upper)

        bin_weight = np.sum(sample_weight[in_bin])
        if bin_weight > 0:
            avg_acc = np.average(y_true[in_bin], weights=sample_weight[in_bin])
            avg_conf = np.average(y_prob[in_bin], weights=sample_weight[in_bin])
            ece += (bin_weight / total_weight) * abs(avg_acc - avg_conf)

    return float(ece)


def compute_all_metrics(
    df_prefixes: pd.DataFrame,
    y_prob: np.ndarray,
    threshold: float,
    max_k: int = 30,
    mode: str = "prospective",
    calibration_far: float = 0.0,
    target_far: float = 0.05
) -> Dict[str, float]:
    """Computes full primary metric suite respecting episode sample weighting."""
    if mode not in ["prospective", "raw"]:
        raise ValueError(f"Invalid mode '{mode}'. Must be 'prospective' or 'raw'.")
        
    y_true = df_prefixes["eventual_outcome"].values.astype(int)
    weights = compute_sample_weights(df_prefixes, max_k=max_k)

    auroc = compute_weighted_auroc(y_true, y_prob, weights)
    auprc = compute_weighted_auprc(y_true, y_prob, weights)
    brier = compute_weighted_brier(y_true, y_prob, weights)
    ece = compute_weighted_ece(y_true, y_prob, weights)

    far, recall, exclusion_stats = compute_episode_far_and_recall(
        df_prefixes, y_prob, threshold, mode=mode
    )

    results = {
        "AUROC": round(auroc, 4),
        "AUPRC": round(auprc, 4),
        "Brier": round(brier, 4),
        "ECE": round(ece, 4)
    }

    results["FAR"] = round(far, 4)
    if mode == "prospective":
        if calibration_far > target_far + 1e-6:
            results["Recall_at_FAR"] = np.nan
        else:
            results["Recall_at_FAR"] = round(recall, 4)
            
        if exclusion_stats:
            results["Exclusion_Stats"] = exclusion_stats
    elif mode == "raw":
        results["Raw_Recall"] = round(recall, 4)

    return results
