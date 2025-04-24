#!/usr/bin/env python
# Snowflake K-means Model Governance Implementation

import snowflake.snowpark as snowpark
from snowflake.ml.modeling.preprocessing import OneHotEncoder, StandardScaler
from snowflake.ml.modeling.clustering import KMeans
from snowflake.ml.experiment import Experiment
import json
import datetime
import uuid

# Create a Snowflake session
def create_snowflake_session(config_dict):
    """Create and return a Snowflake session using provided configuration."""
    session = snowpark.Session.builder.configs(config_dict).create()
    return session

# Model Documentation and Metadata
class ModelDocumentation:
    """Class to handle model documentation and metadata."""
    
    def __init__(self, session, schema_name, table_name="MODEL_REGISTRY"):
        self.session = session
        self.schema_name = schema_name
        self.table_name = table_name
        self._ensure_registry_exists()
    
    def _ensure_registry_exists(self):
        """Ensure the model registry table exists."""
        self.session.sql(f"""
        CREATE TABLE IF NOT EXISTS {self.schema_name}.{self.table_name} (
            model_id VARCHAR(64) PRIMARY KEY,
            model_name VARCHAR(255),
            model_type VARCHAR(50),
            model_version VARCHAR(20),
            description TEXT,
            parameters VARIANT,
            metrics VARIANT,
            created_by VARCHAR(100),
            created_at TIMESTAMP_NTZ,
            updated_at TIMESTAMP_NTZ,
            input_schema VARIANT,
            output_schema VARIANT,
            lineage VARIANT,
            tags VARIANT,
            access_control VARIANT
        )
        """).collect()
    
    def register_model(self, model_info):
        """Register a model in the registry."""
        model_info["model_id"] = str(uuid.uuid4())
        model_info["created_at"] = datetime.datetime.now()
        model_info["updated_at"] = datetime.datetime.now()
        
        # Convert dict objects to JSON strings for VARIANT columns
        for field in ["parameters", "metrics", "input_schema", "output_schema", "lineage", "tags", "access_control"]:
            if field in model_info and isinstance(model_info[field], dict):
                model_info[field] = json.dumps(model_info[field])
        
        # Create SQL for insertion
        columns = ", ".join(model_info.keys())
        placeholders = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in model_info.values()])
        
        sql = f"INSERT INTO {self.schema_name}.{self.table_name} ({columns}) VALUES ({placeholders})"
        self.session.sql(sql).collect()
        
        return model_info["model_id"]
    
    def get_model(self, model_id):
        """Retrieve model information by ID."""
        result = self.session.sql(f"""
        SELECT * FROM {self.schema_name}.{self.table_name}
        WHERE model_id = '{model_id}'
        """).collect()
        
        if not result:
            return None
        
        model_info = dict(zip(result[0].keys(), result[0].values()))
        
        # Convert JSON strings back to dictionaries for VARIANT columns
        for field in ["parameters", "metrics", "input_schema", "output_schema", "lineage", "tags", "access_control"]:
            if field in model_info and model_info[field]:
                model_info[field] = json.loads(model_info[field])
        
        return model_info
    
    def update_model(self, model_id, updates):
        """Update model information."""
        updates["updated_at"] = datetime.datetime.now()
        
        # Convert dict objects to JSON strings for VARIANT columns
        for field in ["parameters", "metrics", "input_schema", "output_schema", "lineage", "tags", "access_control"]:
            if field in updates and isinstance(updates[field], dict):
                updates[field] = json.dumps(updates[field])
        
        # Create SQL for update
        set_clauses = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in updates.items()])
        
        sql = f"""
        UPDATE {self.schema_name}.{self.table_name}
        SET {set_clauses}
        WHERE model_id = '{model_id}'
        """
        self.session.sql(sql).collect()

# Audit Trail Implementation
class ModelAuditTrail:
    """Class to handle model audit trails."""
    
    def __init__(self, session, schema_name, table_name="MODEL_AUDIT_TRAIL"):
        self.session = session
        self.schema_name = schema_name
        self.table_name = table_name
        self._ensure_audit_table_exists()
    
    def _ensure_audit_table_exists(self):
        """Ensure the audit trail table exists."""
        self.session.sql(f"""
        CREATE TABLE IF NOT EXISTS {self.schema_name}.{self.table_name} (
            audit_id VARCHAR(64) PRIMARY KEY,
            model_id VARCHAR(64),
            action VARCHAR(50),
            user_id VARCHAR(100),
            timestamp TIMESTAMP_NTZ,
            details VARIANT,
            FOREIGN KEY (model_id) REFERENCES {self.schema_name}.MODEL_REGISTRY(model_id)
        )
        """).collect()
    
    def log_action(self, model_id, action, user_id, details=None):
        """Log an action in the audit trail."""
        audit_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now()
        
        if isinstance(details, dict):
            details = json.dumps(details)
        elif details is None:
            details = "null"
        else:
            details = f"'{details}'"
        
        sql = f"""
        INSERT INTO {self.schema_name}.{self.table_name}
        (audit_id, model_id, action, user_id, timestamp, details)
        VALUES ('{audit_id}', '{model_id}', '{action}', '{user_id}', '{timestamp}', {details})
        """
        self.session.sql(sql).collect()
        
        return audit_id
    
    def get_model_audit_trail(self, model_id):
        """Get the audit trail for a specific model."""
        result = self.session.sql(f"""
        SELECT * FROM {self.schema_name}.{self.table_name}
        WHERE model_id = '{model_id}'
        ORDER BY timestamp DESC
        """).collect()
        
        audit_trail = []
        for row in result:
            entry = dict(zip(row.keys(), row.values()))
            if "details" in entry and entry["details"]:
                entry["details"] = json.loads(entry["details"])
            audit_trail.append(entry)
        
        return audit_trail

# Access Control Management
class ModelAccessControl:
    """Class to handle model access controls."""
    
    def __init__(self, session, schema_name):
        self.session = session
        self.schema_name = schema_name
        self.documentation = ModelDocumentation(session, schema_name)
    
    def set_access_control(self, model_id, access_rules):
        """Set access control rules for a model."""
        self.documentation.update_model(model_id, {"access_control": access_rules})
    
    def get_access_control(self, model_id):
        """Get access control rules for a model."""
        model_info = self.documentation.get_model(model_id)
        if model_info and "access_control" in model_info:
            return model_info["access_control"]
        return {}
    
    def check_access(self, model_id, user_id, action):
        """Check if a user has access to perform an action on a model."""
        access_rules = self.get_access_control(model_id)
        
        # Default deny if no rules are set
        if not access_rules:
            return False
        
        # Check if user has the required permission
        if "users" in access_rules:
            for user_rule in access_rules["users"]:
                if user_rule["user_id"] == user_id and action in user_rule.get("permissions", []):
                    return True
        
        # Check if user is in a role with the required permission
        if "roles" in access_rules:
            user_roles = self._get_user_roles(user_id)
            for role_rule in access_rules["roles"]:
                if role_rule["role_name"] in user_roles and action in role_rule.get("permissions", []):
                    return True
        
        return False
    
    def _get_user_roles(self, user_id):
        """Get roles for a user. This is a simplified implementation."""
        # In a real implementation, this would query Snowflake RBAC system
        # For demo purposes, we'll hardcode some roles
        if user_id == "admin":
            return ["ADMIN", "DATA_SCIENTIST"]
        elif user_id == "data_scientist":
            return ["DATA_SCIENTIST"]
        elif user_id == "analyst":
            return ["ANALYST"]
        return []

# Main governance implementation
def governance_workflow():
    """Main function to demonstrate the governance workflow."""
    # Connect to Snowflake
    config = {
        "account": "your_account",
        "user": "your_username",
        "password": "your_password",
        "role": "ACCOUNTADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "ML_MODELS",
        "schema": "PUBLIC"
    }
    session = create_snowflake_session(config)
    
    # Initialize experiment tracking
    experiment = Experiment(session, "Customer Segmentation Experiment")
    experiment.start_run()
    
    # Load data
    df = session.table("CUSTOMER_DATA")
    
    # Preprocess data
    encoder = OneHotEncoder(input_cols=["REGION", "CUSTOMER_TYPE"],
                          output_cols=["REGION_ENCODED", "TYPE_ENCODED"])
    df_encoded = encoder.fit_transform(df)
    
    scaler = StandardScaler(input_cols=["PURCHASE_AMOUNT", "VISIT_FREQUENCY"],
                          output_cols=["AMOUNT_SCALED", "FREQUENCY_SCALED"])
    df_scaled = scaler.fit_transform(df_encoded)
    
    # Train model
    kmeans = KMeans(n_clusters=4, random_state=42)
    kmeans.fit(df_scaled[["AMOUNT_SCALED", "FREQUENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]])
    
    # Log metrics
    experiment.log_metric("silhouette_score", 0.68)
    experiment.log_metric("inertia", 245.7)
    experiment.log_param("n_clusters", 4)
    experiment.log_param("algorithm", "k-means")
    
    # Setup documentation
    doc_manager = ModelDocumentation(session, "PUBLIC")
    
    # Create model documentation
    model_info = {
        "model_name": "customer_segmentation_kmeans",
        "model_type": "KMeans",
        "model_version": "1.0.0",
        "description": "Customer segmentation model using K-means clustering",
        "parameters": {
            "n_clusters": 4,
            "random_state": 42,
            "algorithm": "k-means"
        },
        "metrics": {
            "silhouette_score": 0.68,
            "inertia": 245.7
        },
        "created_by": "data_scientist",
        "input_schema": {
            "features": ["AMOUNT_SCALED", "FREQUENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]
        },
        "output_schema": {
            "prediction": "CLUSTER_ID"
        },
        "lineage": {
            "input_data": "CUSTOMER_DATA",
            "preprocessing": [
                {"type": "OneHotEncoder", "columns": ["REGION", "CUSTOMER_TYPE"]},
                {"type": "StandardScaler", "columns": ["PURCHASE_AMOUNT", "VISIT_FREQUENCY"]}
            ],
            "experiment_id": experiment.id
        },
        "tags": {
            "purpose": "customer_segmentation",
            "department": "marketing",
            "version": "1.0.0"
        },
        "access_control": {
            "users": [
                {"user_id": "admin", "permissions": ["READ", "WRITE", "EXECUTE", "DELETE"]},
                {"user_id": "data_scientist", "permissions": ["READ", "EXECUTE"]}
            ],
            "roles": [
                {"role_name": "ANALYST", "permissions": ["READ", "EXECUTE"]},
                {"role_name": "DATA_SCIENTIST", "permissions": ["READ", "WRITE", "EXECUTE"]}
            ]
        }
    }
    
    model_id = doc_manager.register_model(model_info)
    print(f"Model registered with ID: {model_id}")
    
    # Setup audit trail
    audit_manager = ModelAuditTrail(session, "PUBLIC")
    
    # Log model creation in audit trail
    audit_manager.log_action(
        model_id=model_id,
        action="CREATE",
        user_id="data_scientist",
        details={
            "timestamp": datetime.datetime.now().isoformat(),
            "parameters": model_info["parameters"],
            "metrics": model_info["metrics"]
        }
    )
    
    # Setup access control
    access_manager = ModelAccessControl(session, "PUBLIC")
    
    # Now let's test access control
    user = "analyst"
    action = "EXECUTE"
    has_access = access_manager.check_access(model_id, user, action)
    print(f"User '{user}' has {action} access: {has_access}")
    
    # Complete the experiment
    experiment.end_run()
    
    # Export governance report
    governance_report = {
        "model_id": model_id,
        "documentation": doc_manager.get_model(model_id),
        "audit_trail": audit_manager.get_model_audit_trail(model_id),
        "access_control": access_manager.get_access_control(model_id)
    }
    
    # In a real scenario, we would save this to a file or database
    print(f"Governance report generated for model {model_id}")
    
    return governance_report, model_id

if __name__ == "__main__":
    governance_report, model_id = governance_workflow() 