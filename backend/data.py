from datetime import datetime
from typing import Dict, List, Optional
import uuid

# In-memory data storage
metrics = []
alerts = []

# Helper function to generate IDs
def generate_id():
    return str(uuid.uuid4())

# Metrics operations
def get_metrics(skip: int = 0, limit: int = 100) -> List[Dict]:
    return metrics[skip:skip + limit]

def get_metric_by_id(metric_id: str) -> Optional[Dict]:
    for metric in metrics:
        if metric["id"] == metric_id:
            return metric
    return None

def get_metrics_by_name(name: str) -> List[Dict]:
    return [metric for metric in metrics if metric["name"] == name]

def create_metric(metric_data: Dict) -> Dict:
    metric = {
        "id": generate_id(),
        "name": metric_data["name"],
        "value": metric_data["value"],
        "unit": metric_data["unit"],
        "timestamp": datetime.now().isoformat()
    }
    metrics.append(metric)
    return metric

# Alerts operations
def get_alerts(skip: int = 0, limit: int = 100, active_only: bool = False) -> List[Dict]:
    if active_only:
        filtered_alerts = [alert for alert in alerts if alert["is_active"]]
        return filtered_alerts[skip:skip + limit]
    return alerts[skip:skip + limit]

def get_alert_by_id(alert_id: str) -> Optional[Dict]:
    for alert in alerts:
        if alert["id"] == alert_id:
            return alert
    return None

def create_alert(alert_data: Dict) -> Dict:
    alert = {
        "id": generate_id(),
        "title": alert_data["title"],
        "message": alert_data["message"],
        "severity": alert_data["severity"],
        "is_active": True,
        "created_at": datetime.now().isoformat(),
        "resolved_at": None
    }
    alerts.append(alert)
    return alert

def update_alert(alert_id: str, update_data: Dict) -> Optional[Dict]:
    alert = get_alert_by_id(alert_id)
    if not alert:
        return None
    
    for key, value in update_data.items():
        alert[key] = value
    
    if update_data.get("is_active") is False and not alert.get("resolved_at"):
        alert["resolved_at"] = datetime.now().isoformat()
    
    return alert

# Add some sample data
def add_sample_data():
    # Sample metrics
    create_metric({"name": "cpu_usage", "value": 45.2, "unit": "%"})
    create_metric({"name": "memory_usage", "value": 3.7, "unit": "GB"})
    create_metric({"name": "disk_space", "value": 256.8, "unit": "GB"})
    create_metric({"name": "network_in", "value": 1.2, "unit": "MB/s"})
    create_metric({"name": "network_out", "value": 0.8, "unit": "MB/s"})
    
    # Sample alerts
    create_alert({
        "title": "High CPU Usage", 
        "message": "CPU usage has exceeded 80% for the last 5 minutes", 
        "severity": "warning"
    })
    create_alert({
        "title": "Memory Leak Detected", 
        "message": "Possible memory leak in application server", 
        "severity": "critical"
    })
    create_alert({
        "title": "New Update Available", 
        "message": "System update v2.1.0 is available for installation", 
        "severity": "info"
    })

# Initialize sample data
add_sample_data() 