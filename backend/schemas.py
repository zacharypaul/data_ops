from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# Metric schemas
class MetricBase(BaseModel):
    name: str
    value: float
    unit: str

class MetricCreate(MetricBase):
    pass

class Metric(MetricBase):
    id: int
    timestamp: datetime
    
    class Config:
        orm_mode = True

# Alert schemas
class AlertBase(BaseModel):
    title: str
    message: str
    severity: str = Field(..., description="Must be one of: 'critical', 'warning', 'info'")

class AlertCreate(AlertBase):
    pass

class AlertUpdate(BaseModel):
    is_active: bool = False
    resolved_at: Optional[datetime] = None

class Alert(AlertBase):
    id: int
    is_active: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True

# Response schemas
class HealthResponse(BaseModel):
    status: str
    version: str

class MetricsResponse(BaseModel):
    metrics: List[Metric]
    
class AlertsResponse(BaseModel):
    alerts: List[Alert] 