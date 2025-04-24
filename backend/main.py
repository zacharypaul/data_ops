import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from routes import metrics, alerts, sop_generator, csv_upload

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Operations Dashboard API",
    description="Backend API for Vue Operations Dashboard",
    version="0.1.0"
)

# Configure CORS - allow all origins in development
origins = [
    "http://localhost:5173",  # Vue development server
    "http://localhost:4173",  # Vite preview
    "http://localhost:8080",  # Production URL
    os.getenv("FRONTEND_URL", "http://localhost:8080"),
    "http://frontend",        # Docker service name
    "*",                      # Allow all origins in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(metrics.router)
app.include_router(alerts.router)
app.include_router(sop_generator.router)
app.include_router(csv_upload.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Operations Dashboard API"}

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.get("/api/dashboard")
async def dashboard_summary():
    """
    Get a summary of dashboard data for the main view.
    """
    import data
    
    # Get the latest 5 metrics and alerts
    recent_metrics = data.get_metrics(limit=5)
    active_alerts = data.get_alerts(limit=5, active_only=True)
    
    # Create a summary
    summary = {
        "metrics_count": len(data.metrics),
        "alerts_count": len(data.alerts),
        "active_alerts_count": len([a for a in data.alerts if a["is_active"]]),
        "recent_metrics": recent_metrics,
        "active_alerts": active_alerts
    }
    
    return JSONResponse(content=summary)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 