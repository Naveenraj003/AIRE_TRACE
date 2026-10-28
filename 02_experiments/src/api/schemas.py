from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class EpisodeMetadata(BaseModel):
    episode_id: str
    task_id: str
    eventual_outcome: int
    split: str
    dataset_id: str
    dataset_version: str
    
class PredictionRow(BaseModel):
    prefix_len: int
    probability: float

class ModelPredictions(BaseModel):
    threshold: float
    predictions: List[PredictionRow]

class EpisodePredictionsResponse(BaseModel):
    episode_id: str
    horizon_k: int
    models: Dict[str, ModelPredictions]

class AlertResponse(BaseModel):
    model: str
    first_alert_prefix: Optional[int]
    alerted: bool
    threshold: float
