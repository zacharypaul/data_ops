<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-purple-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-server text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Infrastructure Setup</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Configure compute resources, storage, and networking to support your ML workflow</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Snowflake warehouse configuration</li>
        <li>Storage integration</li>
        <li>Network access & security</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 1-2 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
      
      <div class="prose prose-dark text-gray-300">
        <p>Proper infrastructure setup ensures your ML workflow has the necessary compute resources and configurations for efficient execution.</p>
        
        <h5 class="text-md font-semibold mt-4">Key Infrastructure Components:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Compute Resources:</strong> Configure Snowflake virtual warehouses for different workloads</li>
          <li><strong>Storage:</strong> Set up internal and external stages for data and model artifacts</li>
          <li><strong>Networking:</strong> Configure secure network access and integrations</li>
          <li><strong>Environment Management:</strong> Create separate dev, test, and production environments</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Setup Snowflake resources for K-means ML workflows:</p>
        <ul class="pl-5 list-disc">
          <li>Create optimized warehouses for data processing, model training, and inference</li>
          <li>Configure external stages for storing model artifacts</li>
          <li>Set up network policies and authentication methods</li>
          <li>Enable appropriate Snowflake features and extensions</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Resource Configuration:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create database for ML operations
CREATE DATABASE IF NOT EXISTS ML_OPS;

-- Create schemas for different stages of ML workflow
CREATE SCHEMA IF NOT EXISTS ML_OPS.RAW_DATA;
CREATE SCHEMA IF NOT EXISTS ML_OPS.PROCESSED_DATA;
CREATE SCHEMA IF NOT EXISTS ML_OPS.MODELS;
CREATE SCHEMA IF NOT EXISTS ML_OPS.RESULTS;

-- Create warehouses optimized for different ML operations
CREATE WAREHOUSE IF NOT EXISTS ML_ETL_WH
  WAREHOUSE_SIZE = 'MEDIUM'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for ETL operations';

CREATE WAREHOUSE IF NOT EXISTS ML_TRAINING_WH
  WAREHOUSE_SIZE = 'LARGE'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  MAX_CLUSTER_COUNT = 3
  MIN_CLUSTER_COUNT = 1
  SCALING_POLICY = 'STANDARD'
  COMMENT = 'Warehouse for model training operations';

CREATE WAREHOUSE IF NOT EXISTS ML_INFERENCE_WH
  WAREHOUSE_SIZE = 'SMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Warehouse for model inference operations';

-- Set up storage integration (for storing models in external location)
CREATE STORAGE INTEGRATION IF NOT EXISTS s3_model_storage
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-access'
  STORAGE_ALLOWED_LOCATIONS = ('s3://my-bucket/ml-models/')
  COMMENT = 'Integration for ML model storage';

-- Create external stage for model storage
CREATE STAGE IF NOT EXISTS ML_OPS.MODELS.MODEL_ARTIFACTS
  URL = 's3://my-bucket/ml-models/'
  STORAGE_INTEGRATION = s3_model_storage;

-- Set up network policy for secure access
CREATE NETWORK POLICY IF NOT EXISTS ml_ops_network_policy
  ALLOWED_IP_LIST = ('192.168.0.0/16', '10.0.0.0/8')
  BLOCKED_IP_LIST = ('0.0.0.0/0')
  COMMENT = 'Network policy for ML operations';

-- Apply network policy to roles
ALTER ACCOUNT SET NETWORK_POLICY = ml_ops_network_policy;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Environment Configuration:</h5>
        <p>Configure Snowflake session parameters for ML operations:</p>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# Python code to set up Snowflake session with the right parameters
import snowflake.snowpark as snowpark

def create_snowflake_session(env='dev'):
    """Create a Snowflake session with the appropriate configuration."""
    # Choose environment-specific parameters
    if env == 'dev':
        warehouse = 'ML_ETL_WH'
        database = 'ML_OPS_DEV'
    elif env == 'test':
        warehouse = 'ML_ETL_WH'
        database = 'ML_OPS_TEST'
    elif env == 'prod':
        warehouse = 'ML_ETL_WH'
        database = 'ML_OPS'
    else:
        raise ValueError(f"Unknown environment: {env}")
        
    # Create session with appropriate parameters
    session = snowpark.Session.builder.configs({
        "account": "your_account",
        "user": "your_username",
        "password": "your_password",  # In production, use more secure methods
        "role": "ML_ENGINEER",
        "warehouse": warehouse,
        "database": database,
        "schema": "RAW_DATA",
        "application": "ML_KMEANS_CLUSTERING",
        # Set session parameters for ML operations
        "PYTHON_CONNECTOR_QUERY_RESULT_FORMAT": "ARROW",
        "STATEMENT_TIMEOUT_IN_SECONDS": 600,
        "CLIENT_SESSION_KEEP_ALIVE": True
    }).create()
    
    # Set additional session parameters
    session.sql("ALTER SESSION SET USE_CACHED_RESULT = TRUE").collect()
    session.sql("ALTER SESSION SET JDBC_TREAT_DECIMAL_AS_INT = FALSE").collect()
    session.sql("ALTER SESSION SET JDBC_TREAT_TIMESTAMP_NTZ_AS_UTC = FALSE").collect()
    
    return session
</pre>
        
        <h5 class="text-md font-semibold mt-4">Infrastructure Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Right-size warehouses based on workload requirements</li>
          <li>Implement auto-suspend and auto-resume for cost optimization</li>
          <li>Set appropriate timeouts and query limits to prevent runaway processes</li>
          <li>Use separate warehouses for different workload types (ETL, training, inference)</li>
          <li>Implement network security policies to restrict access</li>
          <li>Configure proper resource monitoring and alerting</li>
          <li>Use IAM roles for secure cross-cloud integration</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'InfrastructureSetupStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 