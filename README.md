# Operations Dashboard

A monitoring and operations dashboard with a Vue.js frontend and FastAPI backend.

## Docker Setup

The easiest way to run the application is using Docker Compose:

```bash
# Build and start the containers
docker compose up -d

# View logs
docker compose logs -f

# Stop the containers
docker compose down
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Development Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend

```bash
cd frontend_ops
npm install
npm run dev
```

## Architecture

The application consists of two main components:

1. **Frontend**: A Vue.js application with a modern dashboard UI.
2. **Backend**: A FastAPI server providing APIs for metrics and alerts.

Data is stored in memory for simplicity, but the backend is designed to be easily extended to use a database.

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/dashboard` - Dashboard summary
- `GET /api/metrics` - List metrics
- `GET /api/alerts` - List alerts

For a complete list of endpoints, see the API docs at http://localhost:8000/docs when the server is running. 