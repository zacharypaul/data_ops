import os
import logging
import json
import time
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from urllib.parse import urljoin

import httpx

logger = logging.getLogger(__name__)

class FivetranConnector:
    """
    Connector for interacting with Fivetran API.
    Provides methods for managing connectors, monitoring syncs, and retrieving metadata.
    """
    
    API_URL = "https://api.fivetran.com/v1/"
    
    def __init__(self, api_key: str = None, api_secret: str = None):
        """
        Initialize the Fivetran connector with API credentials.
        If parameters are not provided, they will be loaded from environment variables.
        """
        self.api_key = api_key or os.environ.get("FIVETRAN_API_KEY")
        self.api_secret = api_secret or os.environ.get("FIVETRAN_API_SECRET")
        
        # Validate required parameters
        if not all([self.api_key, self.api_secret]):
            logger.error("Missing required Fivetran API credentials")
            raise ValueError("Missing required Fivetran API credentials")
    
    def _get_auth(self):
        """
        Get HTTP Basic Auth tuple for Fivetran API.
        """
        return (self.api_key, self.api_secret)
    
    def _get_headers(self):
        """
        Get headers for API requests.
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None):
        """
        Make an HTTP request to the Fivetran API.
        """
        url = urljoin(self.API_URL, endpoint)
        auth = self._get_auth()
        headers = self._get_headers()
        
        try:
            async with httpx.AsyncClient() as client:
                if method.lower() == "get":
                    response = await client.get(url, auth=auth, headers=headers, params=params)
                elif method.lower() == "post":
                    response = await client.post(url, auth=auth, headers=headers, json=data, params=params)
                elif method.lower() == "patch":
                    response = await client.patch(url, auth=auth, headers=headers, json=data, params=params)
                elif method.lower() == "delete":
                    response = await client.delete(url, auth=auth, headers=headers, params=params)
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
    
    async def get_groups(self) -> Dict[str, Any]:
        """
        Get all connector groups in the account.
        """
        return await self._make_request("GET", "groups")
    
    async def get_group(self, group_id: str) -> Dict[str, Any]:
        """
        Get details for a specific connector group.
        """
        return await self._make_request("GET", f"groups/{group_id}")
    
    async def get_connectors(self, group_id: str = None, limit: int = 100) -> Dict[str, Any]:
        """
        Get all connectors in a group or across the account.
        """
        params = {"limit": limit}
        
        if group_id:
            return await self._make_request("GET", f"groups/{group_id}/connectors", params=params)
        else:
            return await self._make_request("GET", "connectors", params=params)
    
    async def get_connector(self, connector_id: str) -> Dict[str, Any]:
        """
        Get details for a specific connector.
        """
        return await self._make_request("GET", f"connectors/{connector_id}")
    
    async def get_connector_schema(self, connector_id: str) -> Dict[str, Any]:
        """
        Get schema information for a connector.
        """
        return await self._make_request("GET", f"connectors/{connector_id}/schemas")
    
    async def get_connector_logs(self, connector_id: str) -> Dict[str, Any]:
        """
        Get logs for a connector.
        """
        return await self._make_request("GET", f"connectors/{connector_id}/logs")
    
    async def sync_connector(self, connector_id: str) -> Dict[str, Any]:
        """
        Trigger a sync for a connector.
        """
        return await self._make_request("POST", f"connectors/{connector_id}/sync")
    
    async def get_connector_sync_status(self, connector_id: str) -> Dict[str, Any]:
        """
        Get the current sync status of a connector.
        """
        connector_details = await self.get_connector(connector_id)
        return {
            "connector_id": connector_id,
            "status": connector_details["data"]["status"],
            "sync_state": connector_details["data"]["sync_state"],
            "succeed_at": connector_details["data"]["succeed_at"],
            "failed_at": connector_details["data"]["failed_at"],
            "is_syncing": connector_details["data"]["status"] == "syncing"
        }
    
    async def update_connector_config(self, connector_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update configuration parameters for a connector.
        """
        return await self._make_request("PATCH", f"connectors/{connector_id}/config", data=config)
    
    async def update_connector_schedule(self, 
                                       connector_id: str, 
                                       sync_frequency: int = None, 
                                       paused: bool = None,
                                       pause_after_trial: bool = None) -> Dict[str, Any]:
        """
        Update the sync schedule for a connector.
        
        Args:
            connector_id: The ID of the connector to update
            sync_frequency: Sync frequency in minutes (must be between 5 and 1440)
            paused: Whether the connector should be paused
            pause_after_trial: Whether to pause the connector after trial
        """
        data = {}
        if sync_frequency is not None:
            if not 5 <= sync_frequency <= 1440:
                raise ValueError("Sync frequency must be between 5 and 1440 minutes")
            data["schedule_type"] = "custom_schedule"
            data["sync_frequency"] = sync_frequency
        
        if paused is not None:
            data["paused"] = paused
        
        if pause_after_trial is not None:
            data["pause_after_trial"] = pause_after_trial
        
        return await self._make_request("PATCH", f"connectors/{connector_id}/schedule", data=data)
    
    async def get_connector_usage(self, connector_id: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Get usage metrics for a connector.
        
        Dates should be in format YYYY-MM-DD
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        return await self._make_request("GET", f"connectors/{connector_id}/usage", params=params)
    
    async def get_users(self) -> Dict[str, Any]:
        """
        Get all users in the account.
        """
        return await self._make_request("GET", "users")
    
    async def get_destinations(self) -> Dict[str, Any]:
        """
        Get all destinations in the account.
        """
        return await self._make_request("GET", "destinations")
    
    async def get_destination(self, destination_id: str) -> Dict[str, Any]:
        """
        Get details for a specific destination.
        """
        return await self._make_request("GET", f"destinations/{destination_id}")
    
    async def get_account_usage(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """
        Get account-wide usage metrics.
        
        Dates should be in format YYYY-MM-DD
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        return await self._make_request("GET", "account/usage", params=params)
    
    async def wait_for_sync_completion(self, connector_id: str, timeout: int = 3600, poll_interval: int = 10) -> Dict[str, Any]:
        """
        Wait for a connector sync to complete.
        
        Args:
            connector_id: The ID of the connector to monitor
            timeout: Maximum time to wait in seconds
            poll_interval: Time between status checks in seconds
            
        Returns:
            The final sync status
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            sync_status = await self.get_connector_sync_status(connector_id)
            
            if not sync_status["is_syncing"]:
                return sync_status
            
            logger.info(f"Connector {connector_id} is still syncing. Waiting {poll_interval} seconds...")
            await asyncio.sleep(poll_interval)
        
        raise TimeoutError(f"Sync for connector {connector_id} did not complete within {timeout} seconds")
    
    async def get_all_connectors_status(self) -> List[Dict[str, Any]]:
        """
        Get sync status for all connectors in the account.
        """
        connectors_response = await self.get_connectors()
        connectors = connectors_response.get("data", [])
        
        connector_statuses = []
        for connector in connectors:
            connector_id = connector["id"]
            try:
                status = await self.get_connector_sync_status(connector_id)
                status["name"] = connector["name"]
                status["service"] = connector["service"]
                status["created_at"] = connector["created_at"]
                connector_statuses.append(status)
            except Exception as e:
                logger.error(f"Error getting status for connector {connector_id}: {str(e)}")
                continue
                
        return connector_statuses
    
    async def validate_connection(self) -> bool:
        """
        Test the connection to Fivetran API.
        """
        try:
            # Try to list groups to validate connection
            await self.get_groups()
            logger.info("Fivetran API connection validated")
            return True
        except Exception as e:
            logger.error(f"Fivetran API connection validation failed: {str(e)}")
            return False


# Example usage with asyncio
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logging.basicConfig(level=logging.INFO)
        
        # Create connector from environment variables
        connector = FivetranConnector()
        
        # Validate the connection
        is_valid = await connector.validate_connection()
        print(f"Connection is valid: {is_valid}")
        
        # Example queries
        if is_valid:
            groups = await connector.get_groups()
            print(f"Found {len(groups.get('data', []))} groups")
            
            # Get status of all connectors
            statuses = await connector.get_all_connectors_status()
            for status in statuses:
                print(f"Connector {status['name']} ({status['service']}): {status['sync_state']}")
    
    asyncio.run(main()) 