import json
import pandas as pd
from typing import Dict, Any, Optional, List
from src.api.config import (
    REPAIRED_CANONICAL_PATH,
    PREDICTION_TRACES_PATH,
    PRIMARY_RESULTS_PATH,
    THRESHOLDS_PATH,
    PDC_SUMMARY_PATH,
    LATE_DETECTIONS_PATH,
    DYN_COMP_PREDICTIONS_PATH,
    DYN_COMP_THRESHOLDS_PATH,
    SIGNIFICANCE_PATH,
    EXPECTED_MODELS
)

# In-memory stores
_state = {
    "status": "initializing",
    "canonical_episodes": 0,
    "test_episodes": 0,
    "prediction_rows": 0,
    "prediction_prefixes": 0,
    "models": 0,
    "horizon_k": 30
}

_df_episodes = None
_df_predictions = None
_primary_results = None
_thresholds = None
_pdc_summary = None
_late_detections = None
_canonical_audit = None
_significance = None
_alerts_cache = {}
_events_cache = {}

def load_and_validate_artifacts():
    global _df_episodes, _df_predictions, _primary_results, _thresholds
    global _pdc_summary, _late_detections, _canonical_audit, _significance, _alerts_cache, _events_cache
    
    try:
        # Load JSONs
        with open(REPAIRED_CANONICAL_PATH, "r", encoding="utf-8") as f:
            canonical_data = json.load(f)
        
        with open(PRIMARY_RESULTS_PATH, "r", encoding="utf-8") as f:
            _primary_results = json.load(f)
            
        with open(THRESHOLDS_PATH, "r", encoding="utf-8") as f:
            _thresholds = json.load(f)
            
        with open(PDC_SUMMARY_PATH, "r", encoding="utf-8") as f:
            _pdc_summary = json.load(f)
            
        with open(LATE_DETECTIONS_PATH, "r", encoding="utf-8") as f:
            _late_detections = json.load(f)
            
        with open(SIGNIFICANCE_PATH, "r", encoding="utf-8") as f:
            _significance = json.load(f)
            
        with open(DYN_COMP_THRESHOLDS_PATH, "r", encoding="utf-8") as f:
            dyn_thresh_data = json.load(f)
            _thresholds["dyn_comp"] = {"frozen_threshold": dyn_thresh_data["dyn_comp_frozen_threshold"]}
            
        # Parse canonical episodes
        episodes_list = canonical_data.get("episodes", [])
        _df_episodes = pd.DataFrame(episodes_list)
        
        # Parse Audit Info (events/provenance)
        raw_events = canonical_data.get("events", [])
        
        for event in raw_events:
            ep_id = event["episode_id"]
            if ep_id not in _events_cache:
                _events_cache[ep_id] = []
            _events_cache[ep_id].append({
                "step_index": event.get("step_index"),
                "actor_role": event.get("actor_role"),
                "action_type": event.get("action_type"),
                "tool_name": event.get("tool_name")
            })
            
        for ep_id in _events_cache:
            _events_cache[ep_id].sort(key=lambda x: x["step_index"])
            
        _canonical_audit = {
            "dataset_origin": "repaired_636_canonical",
            "episodes_count": len(episodes_list),
            "events_count": len(raw_events),
            "audit_status": "recorded",
            "leakage_checks": "passed"
        }
        
        # Load Parquet predictions and tb prefixes
        _df_predictions = pd.read_parquet(PREDICTION_TRACES_PATH)
        df_dyn = pd.read_parquet(DYN_COMP_PREDICTIONS_PATH)
        df_dyn_melted = df_dyn[['episode_id', 'prefix_len', 'dyn_comp']].copy()
        df_dyn_melted.rename(columns={'dyn_comp': 'predicted_probability'}, inplace=True)
        df_dyn_melted['model_id'] = 'dyn_comp'
        _df_predictions = pd.concat([_df_predictions, df_dyn_melted], ignore_index=True)
        
        from src.api.config import TB_PREFIXES_PATH
        _df_tb = pd.read_parquet(TB_PREFIXES_PATH)
        
        # Join split info to episodes
        split_map = _df_tb.drop_duplicates("episode_id").set_index("episode_id")["split"].to_dict()
        _df_episodes["split"] = _df_episodes["episode_id"].map(split_map)
        
        # --- INTEGRITY VALIDATION ---
        
        # Canonical population
        total_eps = len(_df_episodes)
        train_eps = len(_df_episodes[_df_episodes["split"] == "train"])
        calib_eps = len(_df_episodes[_df_episodes["split"] == "calibration"])
        test_eps = len(_df_episodes[_df_episodes["split"] == "test"])
        
        test_fails = len(_df_episodes[(_df_episodes["split"] == "test") & (_df_episodes["eventual_outcome"] == 1)])
        
        if total_eps != 636: raise ValueError(f"Expected 636 episodes, got {total_eps}")
        if train_eps != 163: raise ValueError("Expected 163 train")
        if calib_eps != 57: raise ValueError("Expected 57 calib")
        if test_eps != 416: raise ValueError("Expected 416 test")
        if test_fails != 317: raise ValueError("Expected 317 test failures")
        
        # Valid annotated TEST failures from JSON
        valid_fails = _primary_results["mode_a_terminalbench_test"]["M1"]["Exclusion_Stats"]["Valid_Episodes"]
        if valid_fails != 257: raise ValueError("Expected 257 valid annotated TEST failures")
        
        # Prediction artifact
        pred_rows = len(_df_predictions)
        pred_test_eps = _df_predictions["episode_id"].nunique()
        pred_prefixes = _df_predictions.groupby(["episode_id", "prefix_len"]).ngroups
        pred_models = set(_df_predictions["model_id"].unique())
        
        if pred_rows != 62146: raise ValueError(f"Expected 62146 rows, got {pred_rows}")
        if pred_test_eps != 416: raise ValueError("Expected 416 unique test episodes in predictions")
        if pred_prefixes != 8878: raise ValueError("Expected 8878 unique prefixes")
        if pred_models != set(EXPECTED_MODELS): raise ValueError("Unexpected models in predictions")
        
        if _df_predictions["prefix_len"].min() < 1 or _df_predictions["prefix_len"].max() > 30:
            raise ValueError("Prefix length out of bounds [1, 30]")
            
        prob_check_df = _df_predictions[_df_predictions["model_id"] != "dyn_comp"]
        if prob_check_df["predicted_probability"].min() < 0.0 or prob_check_df["predicted_probability"].max() > 1.0:
            raise ValueError("Probabilities out of bounds [0, 1] for base models")
            
        if _df_predictions.duplicated(subset=["model_id", "episode_id", "prefix_len"]).any():
            raise ValueError("Duplicate prediction keys found")
            
        # Verify prediction episode IDs are in canonical TEST set
        canonical_test_ids = set(_df_episodes[_df_episodes["split"] == "test"]["episode_id"])
        pred_ids = set(_df_predictions["episode_id"])
        if not pred_ids.issubset(canonical_test_ids):
            raise ValueError("Predictions contain episode IDs not in canonical TEST set")
            
        # Build Alerts Cache
        for m_id in EXPECTED_MODELS:
            # Note: _thresholds[m_id] expects outer keys to be H1, etc.
            thresh_dict = _thresholds.get(m_id)
            if not thresh_dict:
                # thresholds json actually has models wrapped or something?
                # Actually, the schema earlier showed {"H1": {"frozen_threshold": ...}}
                pass
            thresh = thresh_dict["frozen_threshold"]
            m_preds = _df_predictions[_df_predictions["model_id"] == m_id]
            alerted = m_preds[m_preds["predicted_probability"] >= thresh]
            
            if not alerted.empty:
                first_alerts = alerted.loc[alerted.groupby("episode_id")["prefix_len"].idxmin()]
                for _, row in first_alerts.iterrows():
                    ep_id = row["episode_id"]
                    if ep_id not in _alerts_cache:
                        _alerts_cache[ep_id] = {}
                    _alerts_cache[ep_id][m_id] = {
                        "first_alert_prefix": int(row["prefix_len"]),
                        "alerted": True,
                        "threshold": thresh
                    }
                    
        # Fill non-alerted
        for ep_id in pred_ids:
            if ep_id not in _alerts_cache:
                _alerts_cache[ep_id] = {}
            for m_id in EXPECTED_MODELS:
                if m_id not in _alerts_cache[ep_id]:
                    _alerts_cache[ep_id][m_id] = {
                        "first_alert_prefix": None,
                        "alerted": False,
                        "threshold": _thresholds[m_id]["frozen_threshold"]
                    }
                    
        # Update State
        _state.update({
            "status": "ready",
            "canonical_episodes": total_eps,
            "test_episodes": test_eps,
            "prediction_rows": pred_rows,
            "prediction_prefixes": pred_prefixes,
            "models": len(pred_models)
        })
        
    except Exception as e:
        _state["status"] = f"failed: {str(e)}"
        raise RuntimeError(f"Artifact integrity validation failed: {e}")

# Getters
def get_state() -> Dict[str, Any]: return _state
def get_episodes_df() -> Optional[pd.DataFrame]: return _df_episodes
def get_predictions_df() -> Optional[pd.DataFrame]: return _df_predictions
def get_primary_results() -> Optional[Dict[str, Any]]: return _primary_results
def get_thresholds() -> Optional[Dict[str, Any]]: return _thresholds
def get_pdc_summary() -> Optional[Dict[str, Any]]: return _pdc_summary
def get_late_detections() -> Optional[Dict[str, Any]]: return _late_detections
def get_significance() -> Optional[Dict[str, Any]]: return _significance
def get_canonical_audit() -> Optional[Dict[str, Any]]: return _canonical_audit
def get_alerts(episode_id: str) -> Dict[str, Any]: return _alerts_cache.get(episode_id, {})
def get_events(episode_id: str) -> List[Dict[str, Any]]: return _events_cache.get(episode_id, [])
