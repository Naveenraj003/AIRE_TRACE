from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from src.api.loaders import get_canonical_audit

router = APIRouter()

@router.get("/audit/summary")
def get_audit_summary():
    audit = get_canonical_audit()
    if not audit:
        raise HTTPException(status_code=503, detail="Artifacts not loaded")
    return audit
