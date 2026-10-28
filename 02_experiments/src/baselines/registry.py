"""
AIRE-Trace Baseline Registry
Central interface for loading, instantiating, and accessing baseline model families.
"""

from typing import Dict, Any, List
from src.baselines.heuristics import HeuristicMonitor, CombinedHeuristicMonitor
from src.baselines.logistic import LogisticBaseline
from src.baselines.random_forest import RandomForestBaseline
from src.baselines.sequence import SequenceBaseline

class BaselineRegistry:
    @staticmethod
    def get_baseline_models(feature_cols: List[str] = None, feature_cols_by_model: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """Instantiates all baseline models (H1, H2, H3, H4, M1, S1, S2) and L_PENDING placeholder."""
        if feature_cols_by_model is None:
            feature_cols_by_model = {}

        def get_cols(m_id: str) -> List[str]:
            return feature_cols_by_model.get(m_id, feature_cols)

        models = {
            "H1": HeuristicMonitor(model_id="H1", target_feature="feat_tool_error_count"),
            "H2": HeuristicMonitor(model_id="H2", target_feature="feat_retry_count"),
            "H3": HeuristicMonitor(model_id="H3", target_feature="feat_repeated_action_last2"),
            "H4": CombinedHeuristicMonitor(model_id="H4"),
            "M1": LogisticBaseline(model_id="M1", feature_cols=get_cols("M1")),
            "S1": RandomForestBaseline(model_id="S1", feature_cols=get_cols("S1")),
            "S2": SequenceBaseline(model_id="S2", feature_cols=get_cols("S2")),
            "L": "L_PENDING" # Placeholder for Semantic / LLM monitor
        }
        return models
