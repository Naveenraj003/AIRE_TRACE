import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from src.evaluation.metrics import (
    compute_sample_weights,
    compute_weighted_auroc,
    compute_weighted_auprc,
)

def compute_paired_bootstrap_test(
    df_prefixes: pd.DataFrame,
    predictions: Dict[str, np.ndarray],
    base_model: str = "S1",
    comparators: List[str] = None,
    n_iterations: int = 1000,
    random_seed: int = 42,
    max_k: int = 30,
    metrics: Optional[List[str]] = None,
    thresholds: Optional[Dict[str, float]] = None,
    mode: str = "prospective"
) -> List[Dict[str, Any]]:
    """
    Executes paired episode-cluster bootstrap difference testing.
    Base model and comparators are evaluated on the exact same episode resamples.
    Supports AUROC, AUPRC, and Recall_at_FAR.
    Uses the null-centered difference distribution to compute the two-sided empirical p-value.
    Applies Holm-Bonferroni correction.
    """
    if comparators is None:
        comparators = ["M1", "S2", "H1", "H2", "H3", "H4"]

    if metrics is None:
        metrics = ["AUROC", "AUPRC"]

    all_models = [base_model] + comparators

    run_auc = any(m in ["AUROC", "AUPRC"] for m in metrics)
    run_recall = "Recall_at_FAR" in metrics

    if run_recall:
        if thresholds is None:
            raise ValueError("thresholds dict mapping model name to float threshold must be provided for Recall_at_FAR.")
        for m in all_models:
            if m not in thresholds:
                raise ValueError(f"Missing threshold for model '{m}' in thresholds dict.")
        if mode not in ["prospective", "raw"]:
            raise ValueError(f"Unsupported mode: {mode}. Must be 'prospective' or 'raw'.")

    rng = np.random.RandomState(random_seed)
    
    unique_episodes, ep_inverse = np.unique(df_prefixes["episode_id"].values, return_inverse=True)
    n_episodes = len(unique_episodes)
    
    # Pre-group row indices per episode integer ID
    ep_row_indices = [np.where(ep_inverse == i)[0] for i in range(n_episodes)]
    
    y_true_all = df_prefixes["eventual_outcome"].values.astype(int)
    
    # Observed differences & metrics tracking
    obs_diff = {m: {} for m in metrics}
    bootstrap_diffs = {m: {c: [] for c in comparators} for m in metrics}

    # Setup for AUROC / AUPRC
    if run_auc:
        weights_all = compute_sample_weights(df_prefixes, max_k=max_k)
        base_prob = predictions[base_model]
        if "AUROC" in metrics:
            base_auroc = compute_weighted_auroc(y_true_all, base_prob, weights_all)
        if "AUPRC" in metrics:
            base_auprc = compute_weighted_auprc(y_true_all, base_prob, weights_all)
        
        for c in comparators:
            c_prob = predictions[c]
            if "AUROC" in metrics:
                c_auroc = compute_weighted_auroc(y_true_all, c_prob, weights_all)
                obs_diff["AUROC"][c] = base_auroc - c_auroc
            if "AUPRC" in metrics:
                c_auprc = compute_weighted_auprc(y_true_all, c_prob, weights_all)
                obs_diff["AUPRC"][c] = base_auprc - c_auprc

    # Setup for Recall_at_FAR
    if run_recall:
        bootstrap_fars = {m: [] for m in all_models}
        
        ep_is_succ = np.zeros(n_episodes, dtype=bool)
        ep_is_valid_fail = np.zeros(n_episodes, dtype=bool)
        ep_succ_alert = {m: np.zeros(n_episodes, dtype=bool) for m in all_models}
        ep_fail_alert = {m: np.zeros(n_episodes, dtype=bool) for m in all_models}

        has_prefix_len = "prefix_len" in df_prefixes.columns
        prefix_len_vals = df_prefixes["prefix_len"].values if has_prefix_len else None
        
        if mode == "prospective":
            onset_col = pd.to_numeric(df_prefixes.get("annotation_derived_onset_step", pd.Series(np.nan, index=df_prefixes.index)), errors="coerce").values
            onset_annot = df_prefixes.get("onset_annotated", pd.Series(False, index=df_prefixes.index)).astype(bool).values

        for i in range(n_episodes):
            rows = ep_row_indices[i]
            if has_prefix_len:
                k_mask = prefix_len_vals[rows] <= max_k
                rows_k = rows[k_mask]
            else:
                rows_k = rows

            if len(rows_k) == 0:
                continue

            outcome = y_true_all[rows[0]]
            if outcome == 0:
                ep_is_succ[i] = True
                for m in all_models:
                    max_p = np.max(predictions[m][rows_k])
                    ep_succ_alert[m][i] = bool(max_p >= thresholds[m])
            elif outcome == 1:
                if mode == "prospective":
                    annot = onset_annot[rows[0]]
                    o_step = onset_col[rows[0]]
                    if annot and not np.isnan(o_step):
                        ep_is_valid_fail[i] = True
                        if has_prefix_len:
                            prosp_mask = (prefix_len_vals[rows_k] <= o_step)
                            prosp_rows = rows_k[prosp_mask]
                        else:
                            prosp_rows = rows_k
                        for m in all_models:
                            max_p = np.max(predictions[m][prosp_rows]) if len(prosp_rows) > 0 else -np.inf
                            ep_fail_alert[m][i] = bool(max_p >= thresholds[m])
                elif mode == "raw":
                    ep_is_valid_fail[i] = True
                    for m in all_models:
                        max_p = np.max(predictions[m][rows_k])
                        ep_fail_alert[m][i] = bool(max_p >= thresholds[m])

        n_succ_obs = np.sum(ep_is_succ)
        n_fail_obs = np.sum(ep_is_valid_fail)

        obs_fars = {
            m: (float(np.sum(ep_succ_alert[m]) / n_succ_obs) if n_succ_obs > 0 else 0.0)
            for m in all_models
        }
        obs_recalls = {
            m: (float(np.sum(ep_fail_alert[m]) / n_fail_obs) if n_fail_obs > 0 else 0.0)
            for m in all_models
        }
        for c in comparators:
            obs_diff["Recall_at_FAR"][c] = obs_recalls[base_model] - obs_recalls[c]

    # Paired Bootstrap Loop
    for b in range(n_iterations):
        # Sample episodes once per iteration (shared across all models and metrics)
        sampled_ep_ids = rng.choice(n_episodes, size=n_episodes, replace=True)
        
        if run_auc:
            sampled_row_indices = np.concatenate([ep_row_indices[i] for i in sampled_ep_ids])
            y_true_sub = y_true_all[sampled_row_indices]
            weights_sub = weights_all[sampled_row_indices]
            
            # Base model metrics
            b_prob_sub = base_prob[sampled_row_indices]
            b_auroc = compute_weighted_auroc(y_true_sub, b_prob_sub, weights_sub) if "AUROC" in metrics else None
            b_auprc = compute_weighted_auprc(y_true_sub, b_prob_sub, weights_sub) if "AUPRC" in metrics else None
            
            # Comparator metrics
            for c in comparators:
                c_prob_sub = predictions[c][sampled_row_indices]
                if "AUROC" in metrics:
                    c_auroc = compute_weighted_auroc(y_true_sub, c_prob_sub, weights_sub)
                    bootstrap_diffs["AUROC"][c].append(b_auroc - c_auroc)
                if "AUPRC" in metrics:
                    c_auprc = compute_weighted_auprc(y_true_sub, c_prob_sub, weights_sub)
                    bootstrap_diffs["AUPRC"][c].append(b_auprc - c_auprc)

        if run_recall:
            b_n_fail = np.sum(ep_is_valid_fail[sampled_ep_ids])
            b_n_succ = np.sum(ep_is_succ[sampled_ep_ids])

            base_rec_b = (
                float(np.sum(ep_fail_alert[base_model][sampled_ep_ids]) / b_n_fail)
                if b_n_fail > 0 else 0.0
            )
            base_far_b = (
                float(np.sum(ep_succ_alert[base_model][sampled_ep_ids]) / b_n_succ)
                if b_n_succ > 0 else 0.0
            )
            bootstrap_fars[base_model].append(base_far_b)

            for c in comparators:
                comp_rec_b = (
                    float(np.sum(ep_fail_alert[c][sampled_ep_ids]) / b_n_fail)
                    if b_n_fail > 0 else 0.0
                )
                comp_far_b = (
                    float(np.sum(ep_succ_alert[c][sampled_ep_ids]) / b_n_succ)
                    if b_n_succ > 0 else 0.0
                )
                bootstrap_fars[c].append(comp_far_b)
                bootstrap_diffs["Recall_at_FAR"][c].append(base_rec_b - comp_rec_b)

    results = []
    alpha = 0.05
    k_tests = len(comparators)
    
    for metric in metrics:
        raw_p_values = {}
        # Calculate raw p-values
        for c in comparators:
            delta_obs = obs_diff[metric][c]
            delta_b_star = np.array(bootstrap_diffs[metric][c])
            delta_b_0 = delta_b_star - delta_obs
            
            # P-value = (1 + sum(|Delta_b_0| >= |Delta_obs|)) / (B + 1)
            count_extreme = np.sum(np.abs(delta_b_0) >= np.abs(delta_obs))
            p_raw = float((1 + count_extreme) / (n_iterations + 1))
            raw_p_values[c] = p_raw
            
        # Holm-Bonferroni correction
        # Sort by p_raw ascending
        sorted_comparators = sorted(raw_p_values.keys(), key=lambda x: raw_p_values[x])
        adj_p_values = {}
        prev_adj = 0.0
        
        for i, c in enumerate(sorted_comparators):
            p_raw = raw_p_values[c]
            multiplier = k_tests - i
            p_adj_candidate = p_raw * multiplier
            
            # Ensure monotonicity and cap at 1.0
            p_adj = min(1.0, max(prev_adj, p_adj_candidate))
            adj_p_values[c] = p_adj
            prev_adj = p_adj
            
        # Format results
        for c in comparators:
            delta_obs = obs_diff[metric][c]
            delta_b_star = np.array(bootstrap_diffs[metric][c])
            p_raw = raw_p_values[c]
            p_adj = adj_p_values[c]
            
            res = {
                "comparison": f"{base_model} vs {c}",
                "metric": metric,
                "delta_obs": round(float(delta_obs), 4),
                "bootstrap_mean_delta": round(float(np.mean(delta_b_star)), 4),
                "p_raw": float(p_raw),
                "p_adj": float(p_adj),
                "alpha": alpha,
                "reject_H0": bool(p_adj <= alpha)
            }
            if metric == "Recall_at_FAR":
                ci_lower = float(np.percentile(delta_b_star, 2.5))
                ci_upper = float(np.percentile(delta_b_star, 97.5))
                res["ci_lower_95"] = round(ci_lower, 4)
                res["ci_upper_95"] = round(ci_upper, 4)
                res["diagnostics"] = {
                    "base_obs_far": round(float(obs_fars[base_model]), 4),
                    "comp_obs_far": round(float(obs_fars[c]), 4),
                    "base_obs_recall": round(float(obs_recalls[base_model]), 4),
                    "comp_obs_recall": round(float(obs_recalls[c]), 4),
                    "base_bootstrap_far_mean": round(float(np.mean(bootstrap_fars[base_model])), 4),
                    "comp_bootstrap_far_mean": round(float(np.mean(bootstrap_fars[c])), 4),
                    "base_bootstrap_far_ci_95": [
                        round(float(np.percentile(bootstrap_fars[base_model], 2.5)), 4),
                        round(float(np.percentile(bootstrap_fars[base_model], 97.5)), 4),
                    ],
                    "comp_bootstrap_far_ci_95": [
                        round(float(np.percentile(bootstrap_fars[c], 2.5)), 4),
                        round(float(np.percentile(bootstrap_fars[c], 97.5)), 4),
                    ],
                    "base_bootstrap_fars": [round(float(x), 4) for x in bootstrap_fars[base_model]],
                    "comp_bootstrap_fars": [round(float(x), 4) for x in bootstrap_fars[c]],
                }
            results.append(res)
            
    return results
