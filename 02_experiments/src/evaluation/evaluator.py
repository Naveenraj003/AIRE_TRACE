"""
AIRE-Trace Master Evaluator Module
Executes complete Gate 3 baseline experiment suite across Mode A (TerminalBench TEST)
and Mode B (tau-bench diagnostic). Formats PDC tables and exports baseline run artifacts.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List

from src.baselines.registry import BaselineRegistry
from src.evaluation.thresholding import select_calibration_threshold
from src.evaluation.metrics import compute_all_metrics
from src.evaluation.bootstrap import compute_episode_bootstrap_ci
from src.evaluation.pdc import compute_overall_pdc

class MasterEvaluator:
    def __init__(
        self,
        target_far: float = 0.05,
        bootstrap_iterations: int = 500,
        random_seed: int = 42
    ):
        self.target_far = target_far
        self.bootstrap_iterations = bootstrap_iterations
        self.random_seed = random_seed

    def _prepare_fitted_models(self, df_train: pd.DataFrame, feature_cols_by_model: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """
        Instantiates baseline models and fits them on TRAIN data.
        Internal helper to instantiate and fit baseline models.
        """
        y_train = df_train["eventual_outcome"].values.astype(int)
        feature_cols = [c for c in df_train.columns if c.startswith("feat_")]
        models = BaselineRegistry.get_baseline_models(feature_cols=feature_cols, feature_cols_by_model=feature_cols_by_model)
        
        for m_id, model in models.items():
            if m_id not in ("L", "L_PENDING"):
                model.fit(df_train, y_train)
        
        return models


    def run_evaluation(
        self,
        df_tb: pd.DataFrame,
        df_tau2: pd.DataFrame,
        max_k: int = 30,
        compute_bootstrap: bool = True,
        feature_cols_by_model: Dict[str, List[str]] = None
    ) -> Dict[str, Any]:
        """
        Executes full baseline experiment pipeline for horizon max_k.
        1. Split TerminalBench into TRAIN, CALIBRATION, TEST.
        2. Fit baselines (H1-H4, M1, S1) on TRAIN.
        3. Calibrate thresholds on CALIBRATION (FAR <= target_far).
        4. Evaluate on Mode A (TerminalBench TEST) & Mode B (tau-bench).
        5. Compute 95% CIs via Episode-Cluster Bootstrap.
        6. Compute PDC & Coverage across all baseline pairs.
        """
        # Filter prefixes by max_k horizon
        df_tb_k = df_tb[df_tb["prefix_len"] <= max_k].copy()
        df_tau2_k = df_tau2[df_tau2["prefix_len"] <= max_k].copy()

        df_train = df_tb_k[df_tb_k["split"] == "train"].copy()
        df_calib = df_tb_k[df_tb_k["split"] == "calibration"].copy()
        df_test = df_tb_k[df_tb_k["split"] == "test"].copy()

        y_train = df_train["eventual_outcome"].values.astype(int)
        y_calib = df_calib["eventual_outcome"].values.astype(int)
        y_test = df_test["eventual_outcome"].values.astype(int)

        feature_cols = [c for c in df_train.columns if c.startswith("feat_")]

        # Get and fit baseline models
        models = self._prepare_fitted_models(df_train, feature_cols_by_model=feature_cols_by_model)
        
        mode_a_results = {}
        mode_b_results = {}
        threshold_info = {}
        bootstrap_results = {}
        mode_a_predictions = {}

        print(f"\n--- Running Baseline Experiments for K = {max_k} ---")
        
        for m_id, model in models.items():
            if m_id == "L" or model == "L_PENDING":
                print(f"  [{m_id}] L_PENDING — Semantic / LLM monitor placeholder (skipped).")
                continue

            print(f"  [{m_id}] Evaluating...")

            print(f"  [{m_id}] Calibrating threshold on CALIBRATION ({len(df_calib)} prefixes)...")
            prob_calib = model.predict_proba(df_calib)
            thresh_dict = select_calibration_threshold(df_calib, prob_calib, target_far=self.target_far)
            frozen_thresh = thresh_dict["frozen_threshold"]
            threshold_info[m_id] = thresh_dict

            # Mode A: TerminalBench TEST Evaluation
            print(f"  [{m_id}] Evaluating Mode A (TerminalBench TEST: {len(df_test)} prefixes) at tau = {frozen_thresh}...")
            prob_test = model.predict_proba(df_test)
            mode_a_predictions[m_id] = prob_test
            metrics_test = compute_all_metrics(
                df_test, prob_test, frozen_thresh, max_k=max_k, mode="prospective",
                calibration_far=thresh_dict["calibration_far"], target_far=self.target_far
            )
            mode_a_results[m_id] = metrics_test

            # Bootstrap CIs on TEST
            if compute_bootstrap:
                print(f"  [{m_id}] Running {self.bootstrap_iterations} episode-cluster bootstrap iterations...")
                ci_test = compute_episode_bootstrap_ci(
                    df_test, prob_test, frozen_thresh,
                    n_iterations=self.bootstrap_iterations,
                    random_seed=self.random_seed,
                    max_k=max_k,
                    mode="prospective"
                )
                bootstrap_results[m_id] = ci_test
            else:
                bootstrap_results[m_id] = {}

            # Mode B: tau-bench Evaluation (Evaluation-only diagnostic)
            print(f"  [{m_id}] Evaluating Mode B (tau-bench: {len(df_tau2_k)} prefixes) at tau = {frozen_thresh}...")
            prob_tau2 = model.predict_proba(df_tau2_k)
            metrics_tau2 = compute_all_metrics(df_tau2_k, prob_tau2, frozen_thresh, max_k=max_k, mode="raw")
            mode_b_results[m_id] = metrics_tau2

        # Pairwise Direction Consistency (PDC) on Mode A
        pdc_summary = compute_overall_pdc(mode_a_results)

        return {
            "horizon_k": max_k,
            "target_far": self.target_far,
            "mode_a_terminalbench_test": mode_a_results,
            "mode_b_tau2_bench": mode_b_results,
            "calibrated_thresholds": threshold_info,
            "bootstrap_confidence_intervals": bootstrap_results,
            "pdc_summary": pdc_summary,
            "mode_a_predictions": mode_a_predictions
        }
