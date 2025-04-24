from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

import data

router = APIRouter(
    prefix="/api/metrics",
    tags=["metrics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_metrics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: str = None
):
    """
    Retrieve metrics with optional filtering by name.
    """
    if name:
        metrics = data.get_metrics_by_name(name=name)
    else:
        metrics = data.get_metrics(skip=skip, limit=limit)
    
    return {"metrics": metrics}

@router.get("/{metric_id}")
def read_metric(metric_id: str):
    """
    Retrieve a specific metric by ID.
    """
    metric = data.get_metric_by_id(metric_id=metric_id)
    if metric is None:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.post("/", status_code=201)
def create_metric(metric: Dict):
    """
    Create a new metric.
    """
    return data.create_metric(metric) 