import requests
import json
from urllib.parse import urljoin

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(urljoin(BASE_URL, "/api/health"))
    print("Health Check:", response.status_code, response.json())

def test_dashboard():
    response = requests.get(urljoin(BASE_URL, "/api/dashboard"))
    print("Dashboard Summary:", response.status_code)
    print(json.dumps(response.json(), indent=2))

def test_metrics():
    # Get all metrics
    response = requests.get(urljoin(BASE_URL, "/api/metrics"))
    print("All Metrics:", response.status_code)
    metrics = response.json()["metrics"]
    print(f"Found {len(metrics)} metrics")
    
    if metrics:
        # Get a specific metric
        metric_id = metrics[0]["id"]
        response = requests.get(urljoin(BASE_URL, f"/api/metrics/{metric_id}"))
        print(f"Metric {metric_id}:", response.status_code, response.json())
    
    # Create a new metric
    new_metric = {
        "name": "api_latency",
        "value": 132.5,
        "unit": "ms"
    }
    response = requests.post(urljoin(BASE_URL, "/api/metrics"), json=new_metric)
    print("Create Metric:", response.status_code, response.json())

def test_alerts():
    # Get all alerts
    response = requests.get(urljoin(BASE_URL, "/api/alerts"))
    print("All Alerts:", response.status_code)
    alerts = response.json()["alerts"]
    print(f"Found {len(alerts)} alerts")
    
    if alerts:
        # Get a specific alert
        alert_id = alerts[0]["id"]
        response = requests.get(urljoin(BASE_URL, f"/api/alerts/{alert_id}"))
        print(f"Alert {alert_id}:", response.status_code, response.json())
    
    # Create a new alert
    new_alert = {
        "title": "Test Alert",
        "message": "This is a test alert from the API test script",
        "severity": "info"
    }
    response = requests.post(urljoin(BASE_URL, "/api/alerts"), json=new_alert)
    print("Create Alert:", response.status_code, response.json())
    
    # Update the alert we just created
    created_alert = response.json()
    update_data = {
        "is_active": False
    }
    response = requests.patch(urljoin(BASE_URL, f"/api/alerts/{created_alert['id']}"), json=update_data)
    print("Update Alert:", response.status_code, response.json())

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_health()
    print("\n")
    test_dashboard()
    print("\n")
    test_metrics()
    print("\n")
    test_alerts()
    print("\nAPI tests completed.") 