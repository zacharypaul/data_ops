from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

import data

router = APIRouter(
    prefix="/api/alerts",
    tags=["alerts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def read_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    active_only: bool = False
):
    """
    Retrieve alerts with optional filtering for active alerts only.
    """
    alerts = data.get_alerts(skip=skip, limit=limit, active_only=active_only)
    return {"alerts": alerts}

@router.get("/{alert_id}")
def read_alert(alert_id: str):
    """
    Retrieve a specific alert by ID.
    """
    alert = data.get_alert_by_id(alert_id=alert_id)
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.post("/", status_code=201)
def create_alert(alert: Dict):
    """
    Create a new alert.
    """
    return data.create_alert(alert)

@router.patch("/{alert_id}")
def update_alert(alert_id: str, alert_update: Dict):
    """
    Update an alert (e.g., to mark it as resolved).
    """
    updated_alert = data.update_alert(alert_id=alert_id, update_data=alert_update)
    if updated_alert is None:
        raise HTTPException(status_code=404, detail="Alert not found")
    return updated_alert 