import os
import logging
from typing import Dict, List, Any, Optional, Union
import json

import snowflake.connector
from snowflake.connector.connection import SnowflakeConnection
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

class SnowflakeConnector:
    """
    Connector for interacting with Snowflake data warehouse.
    Provides methods for executing queries and managing connections.
    """

    def __init__(self, 
                 account: str = None, 
                 user: str = None, 
                 password: str = None, 
                 database: str = None, 
                 schema: str = None, 
                 warehouse: str = None,
                 role: str = None):
        """
        Initialize the Snowflake connector with connection parameters.
        If parameters are not provided, they will be loaded from environment variables.
        """
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT")
        self.user = user or os.environ.get("SNOWFLAKE_USER")
        self.password = password or os.environ.get("SNOWFLAKE_PASSWORD")
        self.database = database or os.environ.get("SNOWFLAKE_DATABASE")
        self.schema = schema or os.environ.get("SNOWFLAKE_SCHEMA", "PUBLIC")
        self.warehouse = warehouse or os.environ.get("SNOWFLAKE_WAREHOUSE")
        self.role = role or os.environ.get("SNOWFLAKE_ROLE")
        
        self._connection = None
        self._engine = None
        
        # Validate required parameters
        if not all([self.account, self.user, self.password]):
            logger.error("Missing required Snowflake connection parameters")
            raise ValueError("Missing required Snowflake connection parameters: account, user, password")

    def get_connection(self) -> SnowflakeConnection:
        """
        Get or create a Snowflake connection.
        """
        if self._connection is None or self._connection.is_closed():
            try:
                self._connection = snowflake.connector.connect(
                    account=self.account,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    schema=self.schema,
                    warehouse=self.warehouse,
                    role=self.role
                )
                logger.info(f"Connected to Snowflake account: {self.account}, database: {self.database}")
            except Exception as e:
                logger.error(f"Error connecting to Snowflake: {str(e)}")
                raise
        return self._connection

    def get_sqlalchemy_engine(self) -> Engine:
        """
        Get or create a SQLAlchemy engine for Snowflake.
        """
        if self._engine is None:
            try:
                connection_url = URL(
                    account=self.account,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    schema=self.schema,
                    warehouse=self.warehouse,
                    role=self.role
                )
                self._engine = create_engine(connection_url)
                logger.info(f"Created SQLAlchemy engine for Snowflake: {self.account}")
            except Exception as e:
                logger.error(f"Error creating SQLAlchemy engine for Snowflake: {str(e)}")
                raise
        return self._engine

    def execute_query(self, query: str, params: Dict = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query on Snowflake and return the results as a list of dictionaries.
        """
        connection = self.get_connection()
        try:
            cursor = connection.cursor(snowflake.connector.DictCursor)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise
        finally:
            cursor.close()

    def get_tables(self, schema: str = None) -> List[str]:
        """
        Get list of tables in a schema.
        """
        schema = schema or self.schema
        query = f"SHOW TABLES IN {self.database}.{schema}"
        results = self.execute_query(query)
        return [row['name'] for row in results]

    def get_schema_info(self, table_name: str, schema: str = None) -> List[Dict[str, Any]]:
        """
        Get column information for a table.
        """
        schema = schema or self.schema
        query = f"DESCRIBE TABLE {self.database}.{schema}.{table_name}"
        return self.execute_query(query)

    def get_warehouse_usage(self, days: int = 30) -> Dict[str, Any]:
        """
        Get warehouse usage statistics for the last n days.
        """
        query = f"""
        SELECT 
            WAREHOUSE_NAME,
            DATE_TRUNC('DAY', START_TIME) as DATE,
            SUM(CREDITS_USED) as CREDITS_USED,
            AVG(EXECUTION_TIME) / 1000 as AVG_EXECUTION_TIME_SECONDS
        FROM 
            SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
        WHERE 
            START_TIME >= DATEADD(DAY, -{days}, CURRENT_DATE())
        GROUP BY 
            WAREHOUSE_NAME, DATE
        ORDER BY 
            DATE DESC, WAREHOUSE_NAME
        """
        return self.execute_query(query)

    def get_storage_usage(self) -> Dict[str, Any]:
        """
        Get database storage usage.
        """
        query = """
        SELECT
            DATABASE_NAME,
            AVERAGE_DATABASE_BYTES / (1024*1024*1024) as STORAGE_GB,
            DATE_TRUNC('DAY', USAGE_DATE) as DATE
        FROM
            SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
        WHERE
            USAGE_DATE >= DATEADD(MONTH, -1, CURRENT_DATE())
        ORDER BY
            USAGE_DATE DESC, DATABASE_NAME
        """
        return self.execute_query(query)

    def validate_connection(self) -> bool:
        """
        Test the connection to Snowflake.
        """
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT current_version()")
            version = cursor.fetchone()[0]
            cursor.close()
            logger.info(f"Snowflake connection validated. Version: {version}")
            return True
        except Exception as e:
            logger.error(f"Snowflake connection validation failed: {str(e)}")
            return False

    def close(self) -> None:
        """
        Close the Snowflake connection.
        """
        if self._connection and not self._connection.is_closed():
            self._connection.close()
            logger.info("Snowflake connection closed")
        self._connection = None


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create connector from environment variables
    connector = SnowflakeConnector()
    
    # Validate the connection
    is_valid = connector.validate_connection()
    print(f"Connection is valid: {is_valid}")
    
    # Example query
    if is_valid:
        tables = connector.get_tables()
        print(f"Tables in schema: {tables}")
        
        # Close connection when done
        connector.close() 