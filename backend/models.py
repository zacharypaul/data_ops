from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, default=func.now())
    
    def __repr__(self):
        return f"<Metric(name='{self.name}', value={self.value}, unit='{self.unit}')>"

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(Text)
    severity = Column(String)  # "critical", "warning", "info"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<Alert(title='{self.title}', severity='{self.severity}', active={self.is_active})>" 