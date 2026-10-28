from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from src.api.loaders import get_episodes_df
from src.api.schemas import EpisodeMetadata
import pandas as pd

router = APIRouter()

@router.get("/episodes", response_model=List[EpisodeMetadata])
def list_episodes():
    df = get_episodes_df()
    if df is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    test_eps = df[df["split"] == "test"]
    
    records = test_eps.to_dict(orient="records")
    return records

@router.get("/episodes/{episode_id}", response_model=EpisodeMetadata)
def get_episode(episode_id: str):
    df = get_episodes_df()
    if df is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    ep = df[(df["episode_id"] == episode_id) & (df["split"] == "test")]
    if ep.empty:
        raise HTTPException(status_code=404, detail="Episode not found or not in canonical TEST set")
        
    return ep.iloc[0].to_dict()

@router.get("/episodes/{episode_id}/events")
def get_episode_events(episode_id: str):
    df = get_episodes_df()
    if df is None:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
        
    ep = df[(df["episode_id"] == episode_id) & (df["split"] == "test")]
    if ep.empty:
        raise HTTPException(status_code=404, detail="Episode not found or not in canonical TEST set")
        
    from src.api.loaders import get_events
    events = get_events(episode_id)
    return events
