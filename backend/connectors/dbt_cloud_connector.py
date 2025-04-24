import os
import logging
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urljoin

import httpx

logger = logging.getLogger(__name__)

class DbtCloudConnector:
    """
    Connector for interacting with dbt Cloud API.
    Provides methods for managing jobs, monitoring runs, and accessing dbt metadata.
    """
    
    API_URL = "https://cloud.getdbt.com/api/v2/"
    
    def __init__(self, api_key: str = None, account_id: int = None):
        """
        Initialize the dbt Cloud connector with API credentials.
        If parameters are not provided, they will be loaded from environment variables.
        """
        self.api_key = api_key or os.environ.get("DBT_CLOUD_API_KEY")
        self.account_id = account_id or os.environ.get("DBT_CLOUD_ACCOUNT_ID")
        
        if self.account_id and isinstance(self.account_id, str):
            try:
                self.account_id = int(self.account_id)
            except ValueError:
                logger.error("DBT_CLOUD_ACCOUNT_ID must be an integer")
                raise ValueError("DBT_CLOUD_ACCOUNT_ID must be an integer")
        
        # Validate required parameters
        if not all([self.api_key, self.account_id]):
            logger.error("Missing required dbt Cloud API credentials")
            raise ValueError("Missing required dbt Cloud API credentials: api_key, account_id")
    
    def _get_headers(self):
        """
        Get headers for API requests including authorization.
        """
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None):
        """
        Make an HTTP request to the dbt Cloud API.
        """
        url = urljoin(self.API_URL, endpoint)
        headers = self._get_headers()
        
        try:
            async with httpx.AsyncClient() as client:
                if method.lower() == "get":
                    response = await client.get(url, headers=headers, params=params)
                elif method.lower() == "post":
                    response = await client.post(url, headers=headers, json=data, params=params)
                elif method.lower() == "patch":
                    response = await client.patch(url, headers=headers, json=data, params=params)
                elif method.lower() == "delete":
                    response = await client.delete(url, headers=headers, params=params)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {url}: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error making request to {url}: {str(e)}")
            raise
    
    async def get_account(self) -> Dict[str, Any]:
        """
        Get account details.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/")
    
    async def get_projects(self) -> Dict[str, Any]:
        """
        Get all projects in the account.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/projects/")
    
    async def get_project(self, project_id: int) -> Dict[str, Any]:
        """
        Get details for a specific project.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/projects/{project_id}/")
    
    async def get_environments(self, project_id: int) -> Dict[str, Any]:
        """
        Get all environments in a project.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/projects/{project_id}/environments/")
    
    async def get_jobs(self, project_id: int = None) -> Dict[str, Any]:
        """
        Get all jobs in a project or across the account.
        """
        if project_id:
            return await self._make_request("GET", f"accounts/{self.account_id}/projects/{project_id}/jobs/")
        else:
            return await self._make_request("GET", f"accounts/{self.account_id}/jobs/")
    
    async def get_job(self, job_id: int) -> Dict[str, Any]:
        """
        Get details for a specific job.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/jobs/{job_id}/")
    
    async def trigger_job_run(self, job_id: int, cause: str = "API Triggered", 
                             steps_override: List[str] = None) -> Dict[str, Any]:
        """
        Trigger a job run.
        
        Args:
            job_id: ID of the job to run
            cause: Cause for the run (displayed in the UI)
            steps_override: Optional override of job steps
        """
        data = {"cause": cause}
        if steps_override:
            data["steps_override"] = steps_override
            
        return await self._make_request("POST", f"accounts/{self.account_id}/jobs/{job_id}/run/", data=data)
    
    async def get_runs(self, job_id: int = None, project_id: int = None, limit: int = 100, status: str = None) -> Dict[str, Any]:
        """
        Get job runs filtered by various parameters.
        
        Args:
            job_id: Filter by job ID
            project_id: Filter by project ID
            limit: Maximum number of runs to return
            status: Filter by status (1=Running, 10=Success, 20=Error, 30=Cancelled)
        """
        params = {"limit": limit}
        
        if status:
            params["status"] = status
            
        if job_id:
            endpoint = f"accounts/{self.account_id}/jobs/{job_id}/runs/"
        elif project_id:
            endpoint = f"accounts/{self.account_id}/projects/{project_id}/runs/"
        else:
            endpoint = f"accounts/{self.account_id}/runs/"
            
        return await self._make_request("GET", endpoint, params=params)
    
    async def get_run(self, run_id: int) -> Dict[str, Any]:
        """
        Get details for a specific run.
        """
        return await self._make_request("GET", f"accounts/{self.account_id}/runs/{run_id}/")
    
    async def cancel_run(self, run_id: int) -> Dict[str, Any]:
        """
        Cancel a running job.
        """
        return await self._make_request("POST", f"accounts/{self.account_id}/runs/{run_id}/cancel/")
    
    async def get_run_artifacts(self, run_id: int, path: str = None) -> Dict[str, Any]:
        """
        Get artifacts from a completed run.
        
        Args:
            run_id: ID of the run
            path: Optional artifact path (e.g., 'manifest.json', 'catalog.json', etc.)
        """
        endpoint = f"accounts/{self.account_id}/runs/{run_id}/artifacts/"
        if path:
            endpoint += path
            
        return await self._make_request("GET", endpoint)
    
    async def get_run_status(self, run_id: int) -> Dict[str, Any]:
        """
        Get the status of a run with additional formatted information.
        """
        run_details = await self.get_run(run_id)
        run = run_details.get("data", {})
        
        return {
            "run_id": run_id,
            "status": run.get("status"),
            "status_humanized": run.get("status_humanized"),
            "started_at": run.get("created_at"),
            "finished_at": run.get("finished_at"),
            "duration_seconds": run.get("duration_seconds"),
            "job_id": run.get("job_id"),
            "job_name": run.get("job_name"),
            "is_complete": run.get("is_complete", False),
            "is_success": run.get("is_success", False),
            "is_error": run.get("is_error", False),
            "is_cancelled": run.get("is_cancelled", False)
        }
    
    async def wait_for_run_completion(self, run_id: int, timeout: int = 3600, poll_interval: int = 10) -> Dict[str, Any]:
        """
        Wait for a run to complete.
        
        Args:
            run_id: ID of the run to monitor
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            The final run status
        """
        import asyncio
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            run_status = await self.get_run_status(run_id)
            
            if run_status["is_complete"]:
                return run_status
            
            logger.info(f"Run {run_id} is still in progress (status: {run_status['status_humanized']}). Waiting {poll_interval} seconds...")
            await asyncio.sleep(poll_interval)
        
        raise TimeoutError(f"Run {run_id} did not complete within {timeout} seconds")
    
    async def get_repository_files(self, project_id: int, branch: str = None) -> Dict[str, Any]:
        """
        Get files from a project's repository.
        
        Args:
            project_id: ID of the project
            branch: Optional branch name (defaults to project default branch)
        """
        params = {}
        if branch:
            params["branch"] = branch
            
        return await self._make_request("GET", f"accounts/{self.account_id}/projects/{project_id}/files/", params=params)
    
    async def get_repository_file(self, project_id: int, path: str, branch: str = None) -> Dict[str, Any]:
        """
        Get a specific file from a project's repository.
        
        Args:
            project_id: ID of the project
            path: Path to the file
            branch: Optional branch name (defaults to project default branch)
        """
        params = {}
        if branch:
            params["branch"] = branch
            
        return await self._make_request("GET", f"accounts/{self.account_id}/projects/{project_id}/files/{path}", params=params)
    
    async def get_job_test_failures(self, run_id: int) -> List[Dict[str, Any]]:
        """
        Get list of test failures from a completed run.
        
        Args:
            run_id: ID of the run
        """
        try:
            artifacts = await self.get_run_artifacts(run_id, "run_results.json")
            run_results = artifacts.get("data", {})
            
            failures = []
            for result in run_results.get("results", []):
                if result.get("status") != "pass" and result.get("node", {}).get("resource_type") == "test":
                    failures.append({
                        "test_name": result.get("node", {}).get("name"),
                        "test_path": result.get("node", {}).get("original_file_path"),
                        "status": result.get("status"),
                        "message": result.get("message"),
                        "failures": result.get("failures"),
                        "execution_time": result.get("execution_time")
                    })
            
            return failures
        except Exception as e:
            logger.error(f"Error getting test failures for run {run_id}: {str(e)}")
            return []
    
    async def get_all_job_run_statuses(self) -> List[Dict[str, Any]]:
        """
        Get status information for all recent job runs.
        """
        jobs_response = await self.get_jobs()
        jobs = jobs_response.get("data", [])
        
        all_statuses = []
        for job in jobs:
            job_id = job["id"]
            try:
                runs_response = await self.get_runs(job_id=job_id, limit=1)
                runs = runs_response.get("data", [])
                
                if runs:
                    run = runs[0]
                    status = {
                        "run_id": run["id"],
                        "job_id": job_id,
                        "job_name": job["name"],
                        "status": run["status"],
                        "status_humanized": run["status_humanized"],
                        "started_at": run["created_at"],
                        "finished_at": run["finished_at"],
                        "duration_seconds": run["duration_seconds"],
                        "is_complete": run["is_complete"],
                        "is_success": run["is_success"],
                        "is_error": run["is_error"],
                        "environment_name": job["environment_name"],
                        "project_id": job["project_id"]
                    }
                    all_statuses.append(status)
            except Exception as e:
                logger.error(f"Error getting runs for job {job_id}: {str(e)}")
                continue
                
        return all_statuses
    
    async def validate_connection(self) -> bool:
        """
        Test the connection to dbt Cloud API.
        """
        try:
            # Try to get account information to validate connection
            await self.get_account()
            logger.info("dbt Cloud API connection validated")
            return True
        except Exception as e:
            logger.error(f"dbt Cloud API connection validation failed: {str(e)}")
            return False


# Example usage with asyncio
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logging.basicConfig(level=logging.INFO)
        
        # Create connector from environment variables
        connector = DbtCloudConnector()
        
        # Validate the connection
        is_valid = await connector.validate_connection()
        print(f"Connection is valid: {is_valid}")
        
        # Example operations
        if is_valid:
            # Get all projects
            projects = await connector.get_projects()
            print(f"Found {len(projects.get('data', []))} projects")
            
            # Get job run statuses
            run_statuses = await connector.get_all_job_run_statuses()
            for status in run_statuses:
                print(f"Job {status['job_name']}: {status['status_humanized']}")
    
    asyncio.run(main()) 