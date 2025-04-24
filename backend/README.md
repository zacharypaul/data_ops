# Operations Dashboard Backend API

This is a FastAPI backend for the Vue.js Operations Dashboard frontend.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python run.py
```

The server will start at http://localhost:8000

## API Documentation

Once the server is running, you can access the automatic API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

### Health Check
- `GET /api/health` - Check API health

### Dashboard
- `GET /api/dashboard` - Get dashboard summary data

### Metrics
- `GET /api/metrics` - List all metrics
- `GET /api/metrics/{metric_id}` - Get a specific metric
- `POST /api/metrics` - Create a new metric

### Alerts
- `GET /api/alerts` - List all alerts
- `GET /api/alerts/{alert_id}` - Get a specific alert
- `POST /api/alerts` - Create a new alert
- `PATCH /api/alerts/{alert_id}` - Update an alert (e.g., mark as resolved)

## Development

This backend uses in-memory data storage for simplicity. In a production environment, you would want to integrate with a proper database. 