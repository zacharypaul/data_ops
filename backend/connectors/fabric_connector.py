import os
import logging
import json
from typing import Dict, List, Any, Optional, Union

import httpx
from azure.identity import ClientSecretCredential, InteractiveBrowserCredential
from azure.core.exceptions import ClientAuthenticationError

logger = logging.getLogger(__name__)

class FabricConnector:
    """
    Connector for interacting with Microsoft Fabric services.
    Handles authentication and provides methods for data access.
    
    Note: Microsoft Fabric is relatively new, and this connector is designed
    to work with its REST APIs. As the official SDK evolves, this connector
    may need to be updated.
    """
    
    # API endpoints
    BASE_URL = "https://api.fabric.microsoft.com/v1"
    LAKEHOUSE_API = "/lakehouses"
    WAREHOUSE_API = "/warehouses"
    WORKSPACE_API = "/workspaces"
    PIPELINE_API = "/pipelines"
    
    def __init__(self, 
                 tenant_id: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 workspace_id: str = None,
                 use_interactive: bool = False):
        """
        Initialize the Fabric connector with authentication parameters.
        If parameters are not provided, they will be loaded from environment variables.
        """
        self.tenant_id = tenant_id or os.environ.get("FABRIC_TENANT_ID")
        self.client_id = client_id or os.environ.get("FABRIC_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("FABRIC_CLIENT_SECRET")
        self.workspace_id = workspace_id or os.environ.get("FABRIC_WORKSPACE_ID")
        self.use_interactive = use_interactive
        
        self._credential = None
        self._token = None
        
        # Validate required parameters
        if not self.use_interactive and not all([self.tenant_id, self.client_id, self.client_secret]):
            logger.error("Missing required Fabric authentication parameters")
            raise ValueError("Missing required Fabric authentication parameters for service principal authentication")
    
    def get_credential(self):
        """
        Get or create an Azure credential for authentication.
        """
        if self._credential is None:
            try:
                if self.use_interactive:
                    # Use interactive browser login for development
                    self._credential = InteractiveBrowserCredential()
                    logger.info("Using interactive browser authentication for Fabric")
                else:
                    # Use service principal authentication for production
                    self._credential = ClientSecretCredential(
                        tenant_id=self.tenant_id,
                        client_id=self.client_id,
                        client_secret=self.client_secret
                    )
                    logger.info(f"Created service principal credential for Fabric tenant: {self.tenant_id}")
            except Exception as e:
                logger.error(f"Error creating Azure credential: {str(e)}")
                raise
        return self._credential
    
    async def get_token(self):
        """
        Get an access token for Fabric API authentication.
        """
        if self._token is None:
            try:
                credential = self.get_credential()
                scopes = ["https://fabric.microsoft.com/.default"]
                self._token = await credential.get_token(*scopes)
                logger.info("Acquired Fabric access token")
            except ClientAuthenticationError as e:
                logger.error(f"Authentication error for Fabric: {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Error getting Fabric access token: {str(e)}")
                raise
        return self._token
    
    async def _get_headers(self):
        """
        Get headers for API requests including authorization.
        """
        token = await self.get_token()
        return {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None):
        """
        Make an HTTP request to the Fabric API.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = await self._get_headers()
        
        try:
            async with httpx.AsyncClient() as client:
                if method.lower() == "get":
                    response = await client.get(url, headers=headers, params=params)
                elif method.lower() == "post":
                    response = await client.post(url, headers=headers, json=data, params=params)
                elif method.lower() == "put":
                    response = await client.put(url, headers=headers, json=data, params=params)
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
    
    async def get_workspaces(self) -> List[Dict[str, Any]]:
        """
        Get list of available workspaces.
        """
        return await self._make_request("GET", self.WORKSPACE_API)
    
    async def get_workspace_details(self, workspace_id: str = None) -> Dict[str, Any]:
        """
        Get details for a specific workspace.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}"
        return await self._make_request("GET", endpoint)
    
    async def get_lakehouses(self, workspace_id: str = None) -> List[Dict[str, Any]]:
        """
        Get list of lakehouses in a workspace.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.LAKEHOUSE_API}"
        return await self._make_request("GET", endpoint)
    
    async def get_lakehouse_tables(self, lakehouse_id: str, workspace_id: str = None) -> List[Dict[str, Any]]:
        """
        Get tables in a lakehouse.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.LAKEHOUSE_API}/{lakehouse_id}/tables"
        return await self._make_request("GET", endpoint)
    
    async def get_warehouses(self, workspace_id: str = None) -> List[Dict[str, Any]]:
        """
        Get list of warehouses in a workspace.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.WAREHOUSE_API}"
        return await self._make_request("GET", endpoint)
    
    async def run_warehouse_query(self, warehouse_id: str, sql_query: str, workspace_id: str = None) -> Dict[str, Any]:
        """
        Run a SQL query on a warehouse.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.WAREHOUSE_API}/{warehouse_id}/query"
        data = {"query": sql_query}
        return await self._make_request("POST", endpoint, data=data)
    
    async def get_pipelines(self, workspace_id: str = None) -> List[Dict[str, Any]]:
        """
        Get list of pipelines in a workspace.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.PIPELINE_API}"
        return await self._make_request("GET", endpoint)
    
    async def get_pipeline_runs(self, pipeline_id: str, workspace_id: str = None) -> List[Dict[str, Any]]:
        """
        Get runs of a specific pipeline.
        """
        workspace_id = workspace_id or self.workspace_id
        if not workspace_id:
            raise ValueError("Workspace ID is required")
        
        endpoint = f"{self.WORKSPACE_API}/{workspace_id}{self.PIPELINE_API}/{pipeline_id}/runs"
        return await self._make_request("GET", endpoint)
    
    async def validate_connection(self) -> bool:
        """
        Test the connection to Fabric.
        """
        try:
            # Try to list workspaces to validate connection
            await self.get_workspaces()
            logger.info("Fabric connection validated")
            return True
        except Exception as e:
            logger.error(f"Fabric connection validation failed: {str(e)}")
            return False
    
    def close(self) -> None:
        """
        Reset credentials and tokens.
        """
        self._credential = None
        self._token = None
        logger.info("Fabric connection resources released")


# Example usage with asyncio
if __name__ == "__main__":
    import asyncio
    
    async def main():
        logging.basicConfig(level=logging.INFO)
        
        # Create connector from environment variables
        connector = FabricConnector()
        
        # Validate the connection
        is_valid = await connector.validate_connection()
        print(f"Connection is valid: {is_valid}")
        
        # Example queries
        if is_valid:
            workspaces = await connector.get_workspaces()
            print(f"Found {len(workspaces)} workspaces")
            
            if connector.workspace_id:
                lakehouses = await connector.get_lakehouses()
                print(f"Found {len(lakehouses)} lakehouses in workspace")
            
            # Clean up resources
            connector.close()
    
    asyncio.run(main()) 