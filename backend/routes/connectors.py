import csv
import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Connector(BaseModel):
    name: str
    type: str
    technology: str
    owner: Optional[str] = None

@router.get("/connectors", response_model=List[Connector])
async def get_connectors():
    """
    Get all connectors from the CSV file
    """
    try:
        connectors = []
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "connectors.csv")
        
        # Simple logging to debug
        print(f"Looking for CSV file at: {csv_path}")
        if os.path.exists(csv_path):
            print(f"CSV file found at: {csv_path}")
        else:
            print(f"CSV file NOT found at: {csv_path}")
            # Fallback to sample data if file not found
            return [
                Connector(name="sample_pipeline1", type="ingestion", technology="Snowflake Airflow", owner="twks"),
                Connector(name="sample_pipeline2", type="ingestion", technology="Snowflake Fivetran", owner="ind"),
                Connector(name="sample_pipeline3", type="transformation", technology="Snowflake ADF", owner="zach")
            ]
        
        with open(csv_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                connectors.append(Connector(
                    name=row['name'],
                    type=row.get('type', 'ingestion'),  # Default to 'ingestion' if type is missing
                    technology=row['technology'],
                    owner=row.get('owner', 'twks')  # Default to 'twks' if owner is missing
                ))
        
        if not connectors:
            # Provide sample data if CSV was empty
            return [
                Connector(name="sample_pipeline1", type="ingestion", technology="Snowflake Airflow", owner="twks"),
                Connector(name="sample_pipeline2", type="ingestion", technology="Snowflake Fivetran", owner="ind"),
                Connector(name="sample_pipeline3", type="transformation", technology="Snowflake ADF", owner="zach")
            ]
        
        return connectors
    except Exception as e:
        print(f"Error fetching connectors: {str(e)}")
        # Return sample data on error
        return [
            Connector(name="sample_pipeline1", type="ingestion", technology="Snowflake Airflow", owner="twks"),
            Connector(name="sample_pipeline2", type="ingestion", technology="Snowflake Fivetran", owner="ind"),
            Connector(name="sample_pipeline3", type="transformation", technology="Snowflake ADF", owner="zach")
        ] 