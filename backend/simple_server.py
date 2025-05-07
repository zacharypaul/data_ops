import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List, Optional
from pydantic import BaseModel

# Create FastAPI app
app = FastAPI(
    title="Simplified Operations Dashboard API",
    description="Simplified Backend API for Vue Operations Dashboard",
    version="0.1.0"
)

# Configure CORS - allow all origins in development
origins = [
    "http://localhost:5173",  # Vue development server
    "http://localhost:4173",  # Vite preview
    "http://localhost:80",    # Production URL
    "http://localhost:8080",  # Alternative port
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

class Connector(BaseModel):
    name: str
    type: str
    technology: str = "Snowflake Airflow"  # Default value
    owner: str = "twks"  # Default value

class ConnectorUpdate(BaseModel):
    name: str
    type: str
    technology: str
    owner: str 
    originalName: Optional[str] = None

@app.get("/connectors", response_model=List[Connector])
async def get_connectors():
    """
    Get all connectors from the CSV file
    """
    try:
        connectors = []
        csv_path = os.path.join(os.path.dirname(__file__), "connectors.csv")
        
        # Simple logging to debug
        print(f"Looking for CSV file at: {csv_path}")
        if os.path.exists(csv_path):
            print(f"CSV file found at: {csv_path}")
        else:
            print(f"CSV file NOT found at: {csv_path}")
            # Fallback to sample data if file not found
            return [
                Connector(name="sample_pipeline1", type="Snowflake Airflow", technology="Snowflake Airflow", owner="twks"),
                Connector(name="sample_pipeline2", type="Snowflake Fivetran", technology="Snowflake Fivetran", owner="ind"),
                Connector(name="sample_pipeline3", type="Snowflake ADF", technology="Snowflake ADF", owner="zach")
            ]
        
        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Add technology field if it doesn't exist in the CSV
                technology = row.get('technology', "Snowflake Airflow")
                owner = row.get('owner', "twks")
                connectors.append(Connector(
                    name=row['name'],
                    type=row['type'],
                    technology=technology,
                    owner=owner
                ))
        
        if not connectors:
            # Provide sample data if CSV was empty
            return [
                Connector(name="sample_pipeline1", type="Snowflake Airflow", technology="Snowflake Airflow", owner="twks"),
                Connector(name="sample_pipeline2", type="Snowflake Fivetran", technology="Snowflake Fivetran", owner="ind"),
                Connector(name="sample_pipeline3", type="Snowflake ADF", technology="Snowflake ADF", owner="zach")
            ]
        
        return connectors
    except Exception as e:
        print(f"Error fetching connectors: {str(e)}")
        # Return sample data on error
        return [
            Connector(name="sample_pipeline1", type="Snowflake Airflow", technology="Snowflake Airflow", owner="twks"),
            Connector(name="sample_pipeline2", type="Snowflake Fivetran", technology="Snowflake Fivetran", owner="ind"),
            Connector(name="sample_pipeline3", type="Snowflake ADF", technology="Snowflake ADF", owner="zach")
        ]

@app.put("/connectors", response_model=Connector)
async def update_connector(connector: ConnectorUpdate):
    """
    Update a connector in the CSV file
    """
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "connectors.csv")
        
        if not os.path.exists(csv_path):
            raise HTTPException(status_code=404, detail="CSV file not found")
        
        # Lookup name to update (if originalName provided, use that for lookup)
        lookup_name = connector.originalName if connector.originalName else connector.name
        
        # Read all connectors
        connectors = []
        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            headers = csv_reader.fieldnames
            for row in csv_reader:
                if row['name'] == lookup_name:
                    # Update this row
                    row['name'] = connector.name
                    row['type'] = connector.type
                    # Add technology field to row if it doesn't exist
                    if 'technology' not in row:
                        headers = list(headers)
                        if 'technology' not in headers:
                            headers.append('technology')
                    row['technology'] = connector.technology
                    # Add owner field to row if it doesn't exist
                    if 'owner' not in row:
                        headers = list(headers)
                        if 'owner' not in headers:
                            headers.append('owner')
                    row['owner'] = connector.owner
                connectors.append(row)
        
        # Write all connectors back to CSV
        with open(csv_path, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerows(connectors)
        
        return connector
    except Exception as e:
        print(f"Error updating connector: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating connector: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the Simplified Operations Dashboard API"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("simple_server:app", host="0.0.0.0", port=8000, reload=True) 