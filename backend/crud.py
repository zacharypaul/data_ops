from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

import models
import schemas

# Metrics CRUD operations
def get_metrics(db: Session, skip: int = 0, limit: int = 100) -> List[models.Metric]:
    return db.query(models.Metric).offset(skip).limit(limit).all()

def get_metric_by_id(db: Session, metric_id: int) -> Optional[models.Metric]:
    return db.query(models.Metric).filter(models.Metric.id == metric_id).first()

def get_metrics_by_name(db: Session, name: str) -> List[models.Metric]:
    return db.query(models.Metric).filter(models.Metric.name == name).all()

def create_metric(db: Session, metric: schemas.MetricCreate) -> models.Metric:
    db_metric = models.Metric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

# Alerts CRUD operations
def get_alerts(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[models.Alert]:
    query = db.query(models.Alert)
    
    if active_only:
        query = query.filter(models.Alert.is_active == True)
    
    return query.offset(skip).limit(limit).all()

def get_alert_by_id(db: Session, alert_id: int) -> Optional[models.Alert]:
    return db.query(models.Alert).filter(models.Alert.id == alert_id).first()

def create_alert(db: Session, alert: schemas.AlertCreate) -> models.Alert:
    db_alert = models.Alert(**alert.dict(), is_active=True)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def update_alert(db: Session, alert_id: int, alert_update: schemas.AlertUpdate) -> Optional[models.Alert]:
    db_alert = get_alert_by_id(db, alert_id)
    
    if not db_alert:
        return None
    
    update_data = alert_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_alert, key, value)
    
    if alert_update.is_active is False and not db_alert.resolved_at:
        db_alert.resolved_at = datetime.now()
    
    db.commit()
    db.refresh(db_alert)
    return db_alert 