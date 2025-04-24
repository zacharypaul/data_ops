import os
import io
import csv
from fastapi import APIRouter, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import AWS connector
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connectors.aws_connector import AWSConnector

# Create APIRouter
router = APIRouter(
    prefix="/api",
    tags=["CSV Upload"],
    responses={404: {"description": "Not found"}},
)

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    skip_rows: int = Query(0, description="Number of header rows to skip"),
    delimiter: str = Query(",", description="CSV delimiter character")
):
    """
    Upload and process a CSV file.
    Returns the processed data as JSON.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read file content
        contents = await file.read()
        
        # Convert to in-memory file
        in_memory_file = io.StringIO(contents.decode('utf-8'))
        
        # Process CSV using pandas
        df = pd.read_csv(in_memory_file, skiprows=skip_rows, delimiter=delimiter)
        
        # Convert to records (list of dictionaries)
        records = df.to_dict('records')
        
        # Basic stats about the data
        stats = {
            "total_rows": len(records),
            "columns": list(df.columns),
            "processed_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "filename": file.filename,
            "stats": stats,
            "data": records[:100],  # Return first 100 rows to avoid large payloads
            "has_more_data": len(records) > 100
        }
        
    except Exception as e:
        logger.error(f"Error processing CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@router.post("/analyze-csv")
async def analyze_csv(
    file: UploadFile = File(...),
    delimiter: str = Query(",", description="CSV delimiter character")
):
    """
    Analyze a CSV file and return statistics about each column.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read file content
        contents = await file.read()
        
        # Convert to in-memory file
        in_memory_file = io.StringIO(contents.decode('utf-8'))
        
        # Process CSV using pandas
        df = pd.read_csv(in_memory_file, delimiter=delimiter)
        
        # Generate statistics for each column
        column_stats = {}
        for column in df.columns:
            column_type = str(df[column].dtype)
            
            stats = {
                "dtype": column_type,
                "count": int(df[column].count()),
                "null_count": int(df[column].isna().sum()),
                "null_percentage": float(df[column].isna().mean() * 100),
                "unique_values": int(df[column].nunique())
            }
            
            # Add numeric stats if applicable
            if pd.api.types.is_numeric_dtype(df[column]):
                stats.update({
                    "min": float(df[column].min()) if not pd.isna(df[column].min()) else None,
                    "max": float(df[column].max()) if not pd.isna(df[column].max()) else None,
                    "mean": float(df[column].mean()) if not pd.isna(df[column].mean()) else None,
                    "median": float(df[column].median()) if not pd.isna(df[column].median()) else None,
                    "std": float(df[column].std()) if not pd.isna(df[column].std()) else None
                })
            
            column_stats[column] = stats
        
        # File level statistics
        file_stats = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "file_size": len(contents),
            "analyzed_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "filename": file.filename,
            "file_stats": file_stats,
            "column_stats": column_stats
        }
        
    except Exception as e:
        logger.error(f"Error analyzing CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing CSV: {str(e)}")

@router.post("/upload-to-s3")
async def upload_to_s3(
    file: UploadFile = File(...),
    bucket_name: str = Query(..., description="S3 bucket name"),
    folder_path: str = Query("uploads", description="Folder path in the S3 bucket")
):
    """
    Upload a CSV file to an S3 bucket using the AWS connector.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read file content
        contents = await file.read()
        
        # Generate S3 key (path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = os.path.splitext(file.filename)[0]
        s3_key = f"{folder_path}/{filename_base}_{timestamp}.csv"
        
        # Initialize AWS connector
        # Using environment variables for credentials
        aws_connector = AWSConnector()
        
        # Upload to S3
        try:
            # Convert bytes to file-like object
            file_obj = io.BytesIO(contents)
            
            # Upload the file
            response = aws_connector.upload_file_to_s3(
                bucket=bucket_name,
                key=s3_key,
                file_obj=file_obj,
                content_type="text/csv"
            )
            
            # Return success response
            return {
                "success": True,
                "filename": file.filename,
                "s3_location": f"s3://{bucket_name}/{s3_key}",
                "timestamp": timestamp,
                "file_size": len(contents)
            }
            
        except Exception as e:
            logger.error(f"AWS S3 upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error uploading to S3: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error processing upload request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}") 