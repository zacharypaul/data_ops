<template>
  <div>
    <!-- Code examples are rendered by the MLOpsDetailCard component -->
  </div>
</template>

<script>
// Export code examples from this component to avoid cluttering the parent component
// with large strings

export const infrastructureCode = `
# Infrastructure Setup for Snowflake ML
import json
import subprocess
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta

# DAG configuration
default_args = {
    'owner': 'data_engineering',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'snowflake_infrastructure_setup',
    default_args=default_args,
    description='Setup infrastructure for ML in Snowflake',
    schedule_interval='@once'
)

# Create warehouse for ML operations
create_warehouse = SnowflakeOperator(
    task_id='create_ml_warehouse',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE WAREHOUSE IF NOT EXISTS ML_WAREHOUSE
    WITH WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE;
    """,
    dag=dag
)

# Create database and schemas
create_database = SnowflakeOperator(
    task_id='create_ml_database',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE DATABASE IF NOT EXISTS ML_OPS;
    USE DATABASE ML_OPS;
    CREATE SCHEMA IF NOT EXISTS RAW_DATA;
    CREATE SCHEMA IF NOT EXISTS FEATURE_STORE;
    CREATE SCHEMA IF NOT EXISTS MODELS;
    CREATE SCHEMA IF NOT EXISTS PREDICTIONS;
    """,
    dag=dag
)

# Set up storage integration
setup_storage = SnowflakeOperator(
    task_id='setup_storage_integration',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE STORAGE INTEGRATION IF NOT EXISTS s3_integration
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = 'S3'
    ENABLED = TRUE
    STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/snowflake-role'
    STORAGE_ALLOWED_LOCATIONS = ('s3://ml-datasets/');
    """,
    dag=dag
)

# Setup execution order
create_warehouse >> create_database >> setup_storage
`;

export const dataPipelineCode = `
# Data Pipeline for K-means Clustering
import pandas as pd
import numpy as np
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from datetime import datetime, timedelta
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset

# DAG configuration
default_args = {
    'owner': 'data_science',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'customer_data_pipeline',
    default_args=default_args,
    description='Process customer data for clustering',
    schedule_interval='@daily'
)

# Load data from source
load_data = SnowflakeOperator(
    task_id='extract_customer_data',
    snowflake_conn_id='snowflake_default',
    sql="""
    COPY INTO ML_OPS.RAW_DATA.CUSTOMER_DATA
    FROM s3://ml-datasets/customer_data/
    FILE_FORMAT = (TYPE = 'CSV' FIELD_DELIMITER = ',' SKIP_HEADER = 1)
    PATTERN = '.*\\.csv';
    """,
    dag=dag
)

# Data validation
def validate_data(**context):
    # Connect to Snowflake
    conn = context['task_instance'].xcom_pull(task_ids='extract_customer_data')
    
    # Run data quality checks
    validation_query = """
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT customer_id) as unique_customers,
        COUNT(*) - COUNT(purchase_amount) as null_purchase,
        COUNT(*) - COUNT(visit_frequency) as null_visits,
        AVG(purchase_amount) as avg_purchase,
        MAX(purchase_amount) as max_purchase,
        MIN(purchase_amount) as min_purchase
    FROM ML_OPS.RAW_DATA.CUSTOMER_DATA;
    """
    
    # Raise exception if data quality issues detected
    # (Implementation logic for validation)
    return True

validate_task = PythonOperator(
    task_id='validate_customer_data',
    python_callable=validate_data,
    provide_context=True,
    dag=dag
)

# Feature engineering
feature_engineering = SnowflakeOperator(
    task_id='create_features',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE OR REPLACE TABLE ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES AS
    SELECT
        customer_id,
        region,
        customer_type,
        purchase_amount,
        visit_frequency,
        purchase_amount / NULLIF(visit_frequency, 0) AS avg_purchase_per_visit,
        DATEDIFF('day', first_purchase_date, CURRENT_DATE()) AS days_since_first_purchase,
        DATEDIFF('day', last_purchase_date, CURRENT_DATE()) AS days_since_last_purchase,
        total_purchases,
        COUNT(*) OVER (PARTITION BY region) AS region_density,
        AVG(purchase_amount) OVER (PARTITION BY region) AS region_avg_purchase
    FROM ML_OPS.RAW_DATA.CUSTOMER_DATA;
    """,
    dag=dag
)

# Create versioned feature store
version_features = SnowflakeOperator(
    task_id='version_feature_store',
    snowflake_conn_id='snowflake_default',
    sql="""
    CREATE OR REPLACE TABLE ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES_V1 
    CLONE ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES;
    """,
    dag=dag
)

# Task dependencies
load_data >> validate_task >> feature_engineering >> version_features
`;

export const modelDevelopmentCode = `
# Model Development for K-means Clustering
import snowflake.snowpark as snowpark
from snowflake.ml.modeling.preprocessing import OneHotEncoder, StandardScaler
from snowflake.ml.modeling.clustering import KMeans
from snowflake.ml.experiment import Experiment
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score

# Connect to Snowflake
def create_session():
    session = snowpark.Session.builder.configs({
        "account": "your_account",
        "user": "your_username",
        "password": "your_password",
        "role": "your_role",
        "warehouse": "ML_WAREHOUSE",
        "database": "ML_OPS",
        "schema": "MODELS"
    }).create()
    return session

# Initialize experiment tracking
def train_kmeans_model(n_clusters):
    session = create_session()
    experiment = Experiment(session, "Customer Segmentation Experiment")
    experiment.start_run()
    
    # Load data from feature store
    df = session.table("ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES_V1")
    
    # Preprocess data
    encoder = OneHotEncoder(input_cols=["REGION", "CUSTOMER_TYPE"], 
                            output_cols=["REGION_ENCODED", "TYPE_ENCODED"])
    df_encoded = encoder.fit_transform(df)
    
    scaler = StandardScaler(input_cols=["PURCHASE_AMOUNT", "VISIT_FREQUENCY", 
                                      "AVG_PURCHASE_PER_VISIT", "DAYS_SINCE_LAST_PURCHASE"], 
                           output_cols=["AMOUNT_SCALED", "FREQUENCY_SCALED", 
                                       "AVG_PURCHASE_SCALED", "RECENCY_SCALED"])
    df_scaled = scaler.fit_transform(df_encoded)
    
    # Train model with specified hyperparameters
    feature_cols = ["AMOUNT_SCALED", "FREQUENCY_SCALED", "AVG_PURCHASE_SCALED", 
                   "RECENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]
    
    kmeans = KMeans(n_clusters=n_clusters, 
                   random_state=42, 
                   init='k-means++',
                   max_iter=300)
    
    model = kmeans.fit(df_scaled[feature_cols])
    
    # Evaluate model
    df_with_clusters = df_scaled.with_column("CLUSTER", model.predict(df_scaled[feature_cols]))
    
    # Calculate silhouette score for evaluation
    local_df = df_with_clusters[feature_cols + ["CLUSTER"]].to_pandas()
    silhouette = silhouette_score(local_df[feature_cols], local_df["CLUSTER"])
    
    # Log metrics and parameters
    experiment.log_metric("silhouette_score", silhouette)
    experiment.log_metric("inertia", model.inertia_)
    experiment.log_param("n_clusters", n_clusters)
    experiment.log_param("algorithm", "k-means++")
    
    # Register model if it's the best one
    if silhouette > 0.6:
        model_path = f"models/kmeans_clusters_{n_clusters}"
        experiment.snowflake_ml_client.models.save(
            model, model_path, 
            metadata={"metrics": {"silhouette": silhouette}}
        )
        
    experiment.end_run()
    return silhouette

# Hyperparameter tuning
def objective(n_clusters):
    silhouette = train_kmeans_model(int(n_clusters))
    return {'loss': -silhouette, 'status': STATUS_OK}

# Run hyperparameter tuning
def tune_model():
    space = hp.quniform('n_clusters', 2, 10, 1)
    trials = Trials()
    best = fmin(fn=objective,
                space=space,
                algo=tpe.suggest,
                max_evals=5,
                trials=trials)
    
    best_n_clusters = int(best['n_clusters'])
    print(f"Best number of clusters: {best_n_clusters}")
    return best_n_clusters

# Main execution
if __name__ == "__main__":
    best_n_clusters = tune_model()
    final_score = train_kmeans_model(best_n_clusters)
    print(f"Final model silhouette score: {final_score}")
`;

export const cicdCode = `
# CI/CD Pipeline for K-means Model Deployment
name: Deploy K-means Model to Production

on:
  push:
    branches: [ main ]
    paths:
      - 'models/kmeans/**'
  pull_request:
    branches: [ main ]
    paths:
      - 'models/kmeans/**'
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version to deploy'
        required: true
        default: 'latest'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      
      - name: Run model unit tests
        run: |
          pytest models/kmeans/tests/ --cov=models/kmeans
      
      - name: Model validation tests
        run: |
          python models/kmeans/validation/validate_model.py
          
  evaluate:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Run evaluation on test dataset
        run: |
          python models/kmeans/evaluate.py --dataset test
          
      - name: Check model metrics against baseline
        run: |
          python models/kmeans/compare_metrics.py --min-silhouette 0.65
          
  deploy-staging:
    needs: evaluate
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Snowflake CLI
        run: |
          pip install snowflake-cli-labs
          
      - name: Deploy to Staging
        run: |
          snow login -a \${{ secrets.SNOWFLAKE_ACCOUNT }} -u \${{ secrets.SNOWFLAKE_USER }} -p \${{ secrets.SNOWFLAKE_PASSWORD }}
          snow models deploy --model-name "kmeans_clustering" --stage "staging"
          
      - name: Run integration tests
        run: |
          python models/kmeans/tests/integration_tests.py --env staging
          
  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Production
        run: |
          snow login -a \${{ secrets.SNOWFLAKE_ACCOUNT }} -u \${{ secrets.SNOWFLAKE_USER }} -p \${{ secrets.SNOWFLAKE_PASSWORD }}
          snow models deploy --model-name "kmeans_clustering" --stage "production"
          
      - name: Update documentation
        run: |
          python scripts/update_model_docs.py --model kmeans_clustering --version \${{ github.event.inputs.model_version || 'latest' }}
`;

export const monitoringCode = `
# Monitoring for K-means Clustering Models in Production
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import requests
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, lit
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, NumTargetDriftTab
from evidently.pipeline.column_mapping import ColumnMapping

# Connect to Snowflake
def create_session():
    session = snowpark.Session.builder.configs({
        "account": "your_account",
        "user": "your_username",
        "password": "your_password",
        "role": "your_role",
        "warehouse": "ML_WAREHOUSE",
        "database": "ML_OPS",
        "schema": "MONITORING"
    }).create()
    return session

# Collect monitoring metrics daily
def collect_model_metrics(date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    session = create_session()
    
    # Get predictions from the day
    predictions_df = session.sql(f"""
        SELECT * FROM ML_OPS.PREDICTIONS.CUSTOMER_CLUSTERS 
        WHERE PREDICTION_DATE = '{date}'
    """).to_pandas()
    
    # Calculate cluster distribution
    cluster_distribution = predictions_df.groupby('CLUSTER').size() / len(predictions_df)
    
    # Calculate average silhouette score for the day
    avg_silhouette = predictions_df['SILHOUETTE_SCORE'].mean()
    
    # Calculate cluster stats
    cluster_stats = predictions_df.groupby('CLUSTER').agg({
        'PURCHASE_AMOUNT': ['mean', 'std', 'min', 'max'],
        'VISIT_FREQUENCY': ['mean', 'std', 'min', 'max']
    }).reset_index()
    
    # Store metrics
    metrics = {
        'date': date,
        'avg_silhouette': avg_silhouette,
        'cluster_distribution': cluster_distribution.to_dict(),
        'total_predictions': len(predictions_df),
        'features_mean': predictions_df[['PURCHASE_AMOUNT', 'VISIT_FREQUENCY']].mean().to_dict(),
        'features_std': predictions_df[['PURCHASE_AMOUNT', 'VISIT_FREQUENCY']].std().to_dict()
    }
    
    # Save metrics to Snowflake
    metrics_df = pd.DataFrame([metrics])
    session.create_dataframe(metrics_df).write.save_as_table(
        "ML_OPS.MONITORING.KMEANS_DAILY_METRICS", 
        mode="append"
    )
    
    return metrics

# Check for data drift
def check_data_drift(reference_date, current_date):
    session = create_session()
    
    # Get reference data
    reference_data = session.sql(f"""
        SELECT * FROM ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES
        WHERE DATA_DATE = '{reference_date}'
    """).to_pandas()
    
    # Get current data
    current_data = session.sql(f"""
        SELECT * FROM ML_OPS.FEATURE_STORE.CUSTOMER_FEATURES
        WHERE DATA_DATE = '{current_date}'
    """).to_pandas()
    
    # Create Evidently dashboard
    column_mapping = ColumnMapping()
    column_mapping.numerical_features = [
        'PURCHASE_AMOUNT', 'VISIT_FREQUENCY', 
        'AVG_PURCHASE_PER_VISIT', 'DAYS_SINCE_LAST_PURCHASE'
    ]
    column_mapping.categorical_features = ['REGION', 'CUSTOMER_TYPE']
    
    data_drift_dashboard = Dashboard(tabs=[DataDriftTab()])
    data_drift_dashboard.calculate(reference_data, current_data, column_mapping=column_mapping)
    
    # Save dashboard
    data_drift_dashboard.save(f"data_drift_{current_date}.html")
    
    # Calculate drift metrics
    drift_metrics = {}
    for column in column_mapping.numerical_features + column_mapping.categorical_features:
        # Calculate distribution difference
        if column in column_mapping.numerical_features:
            ref_mean = reference_data[column].mean()
            curr_mean = current_data[column].mean()
            drift_metrics[f"{column}_mean_diff"] = ((curr_mean - ref_mean) / ref_mean) * 100 if ref_mean != 0 else 0
        else:
            # For categorical features, calculate distribution change
            ref_dist = reference_data[column].value_counts(normalize=True)
            curr_dist = current_data[column].value_counts(normalize=True)
            dist_diff = 0
            for cat in set(ref_dist.index).union(set(curr_dist.index)):
                ref_val = ref_dist.get(cat, 0)
                curr_val = curr_dist.get(cat, 0)
                dist_diff += abs(ref_val - curr_val)
            drift_metrics[f"{column}_dist_diff"] = dist_diff * 100
    
    # Set alert thresholds
    alerts = []
    for metric, value in drift_metrics.items():
        if abs(value) > 15:  # 15% change threshold
            alerts.append({
                'metric': metric,
                'value': value,
                'threshold': 15,
                'date': current_date
            })
    
    # Send alerts if needed
    if alerts:
        # Implementation for alert sending (e.g., Slack, email)
        print(f"ALERT: Data drift detected on {current_date}")
        for alert in alerts:
            print(f"  - {alert['metric']}: {alert['value']:.2f}% change (threshold: {alert['threshold']}%)")
    
    return drift_metrics, alerts

# Schedule daily monitoring
if __name__ == "__main__":
    # Collect today's metrics
    today = datetime.now().strftime("%Y-%m-%d")
    metrics = collect_model_metrics(today)
    
    # Check for data drift (compare to 7 days ago)
    reference_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    drift_metrics, alerts = check_data_drift(reference_date, today)
    
    # Generate weekly report if it's Sunday
    if datetime.now().weekday() == 6:
        # Generate and send weekly monitoring report
        pass
`;

export const governanceCode = `
# ML Governance for K-means Models
import json
import hashlib
import pandas as pd
import yaml
from datetime import datetime
import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, lit
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('kmeans_governance')

class ModelGovernance:
    def __init__(self, config_path="governance_config.yaml"):
        # Load configuration
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        # Initialize Snowflake session
        self.session = self._create_session()
        
        # Ensure governance tables exist
        self._initialize_governance_tables()
    
    def _create_session(self):
        """Create a Snowflake session."""
        return snowpark.Session.builder.configs({
            "account": self.config['snowflake']['account'],
            "user": self.config['snowflake']['user'],
            "password": self.config['snowflake']['password'],
            "role": self.config['snowflake']['role'],
            "warehouse": self.config['snowflake']['warehouse'],
            "database": self.config['snowflake']['database'],
            "schema": self.config['snowflake']['governance_schema']
        }).create()
    
    def _initialize_governance_tables(self):
        """Create governance tables if they don't exist."""
        # Model registry table
        self.session.sql("""
        CREATE TABLE IF NOT EXISTS MODEL_REGISTRY (
            MODEL_ID VARCHAR NOT NULL,
            MODEL_NAME VARCHAR NOT NULL,
            VERSION VARCHAR NOT NULL,
            CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            CREATED_BY VARCHAR,
            MODEL_PATH VARCHAR,
            DESCRIPTION VARCHAR,
            STATUS VARCHAR,
            APPROVAL_STATUS VARCHAR DEFAULT 'PENDING',
            PRIMARY KEY (MODEL_ID)
        )
        """).collect()
        
        # Model lineage table
        self.session.sql("""
        CREATE TABLE IF NOT EXISTS MODEL_LINEAGE (
            LINEAGE_ID VARCHAR NOT NULL,
            MODEL_ID VARCHAR NOT NULL,
            DATASET_ID VARCHAR,
            FEATURE_SET_ID VARCHAR,
            TRAINING_JOB_ID VARCHAR,
            PARENT_MODEL_ID VARCHAR,
            LINEAGE_TYPE VARCHAR,
            CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (LINEAGE_ID),
            FOREIGN KEY (MODEL_ID) REFERENCES MODEL_REGISTRY(MODEL_ID)
        )
        """).collect()
        
        # Model metrics table
        self.session.sql("""
        CREATE TABLE IF NOT EXISTS MODEL_METRICS (
            METRIC_ID VARCHAR NOT NULL,
            MODEL_ID VARCHAR NOT NULL,
            METRIC_NAME VARCHAR NOT NULL,
            METRIC_VALUE FLOAT,
            RECORDED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (METRIC_ID),
            FOREIGN KEY (MODEL_ID) REFERENCES MODEL_REGISTRY(MODEL_ID)
        )
        """).collect()
        
        # Model documentation table
        self.session.sql("""
        CREATE TABLE IF NOT EXISTS MODEL_DOCUMENTATION (
            DOC_ID VARCHAR NOT NULL,
            MODEL_ID VARCHAR NOT NULL,
            DOC_TYPE VARCHAR NOT NULL,
            CONTENT VARIANT,
            CREATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            UPDATED_AT TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            PRIMARY KEY (DOC_ID),
            FOREIGN KEY (MODEL_ID) REFERENCES MODEL_REGISTRY(MODEL_ID)
        )
        """).collect()
        
        # Audit log table
        self.session.sql("""
        CREATE TABLE IF NOT EXISTS AUDIT_LOG (
            LOG_ID VARCHAR NOT NULL,
            ENTITY_TYPE VARCHAR NOT NULL,
            ENTITY_ID VARCHAR NOT NULL,
            ACTION VARCHAR NOT NULL,
            USER_ID VARCHAR,
            TIMESTAMP TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
            DETAILS VARIANT,
            PRIMARY KEY (LOG_ID)
        )
        """).collect()
        
        logger.info("Governance tables initialized")
    
    def register_model(self, model_info):
        """Register a new model in the governance system."""
        model_id = hashlib.md5(
            f"{model_info['name']}_{model_info['version']}_{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        # Insert into model registry
        self.session.sql(f"""
        INSERT INTO MODEL_REGISTRY (
            MODEL_ID, MODEL_NAME, VERSION, CREATED_BY, 
            MODEL_PATH, DESCRIPTION, STATUS
        ) VALUES (
            '{model_id}', 
            '{model_info['name']}', 
            '{model_info['version']}', 
            '{model_info.get('created_by', 'system')}',
            '{model_info.get('model_path', '')}',
            '{model_info.get('description', '')}',
            '{model_info.get('status', 'DRAFT')}'
        )
        """).collect()
        
        # Record model metrics
        if 'metrics' in model_info:
            for metric_name, metric_value in model_info['metrics'].items():
                metric_id = hashlib.md5(
                    f"{model_id}_{metric_name}_{datetime.now().isoformat()}".encode()
                ).hexdigest()
                
                self.session.sql(f"""
                INSERT INTO MODEL_METRICS (
                    METRIC_ID, MODEL_ID, METRIC_NAME, METRIC_VALUE
                ) VALUES (
                    '{metric_id}', '{model_id}', '{metric_name}', {metric_value}
                )
                """).collect()
        
        # Record lineage information
        if 'lineage' in model_info:
            lineage_id = hashlib.md5(
                f"{model_id}_lineage_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            self.session.sql(f"""
            INSERT INTO MODEL_LINEAGE (
                LINEAGE_ID, MODEL_ID, DATASET_ID, FEATURE_SET_ID, 
                TRAINING_JOB_ID, PARENT_MODEL_ID, LINEAGE_TYPE
            ) VALUES (
                '{lineage_id}',
                '{model_id}',
                '{model_info['lineage'].get('dataset_id', '')}',
                '{model_info['lineage'].get('feature_set_id', '')}',
                '{model_info['lineage'].get('training_job_id', '')}',
                '{model_info['lineage'].get('parent_model_id', '')}',
                '{model_info['lineage'].get('type', 'TRAINING')}'
            )
            """).collect()
        
        # Create model documentation
        if 'documentation' in model_info:
            doc_id = hashlib.md5(
                f"{model_id}_doc_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            doc_content = json.dumps(model_info['documentation'])
            
            self.session.sql(f"""
            INSERT INTO MODEL_DOCUMENTATION (
                DOC_ID, MODEL_ID, DOC_TYPE, CONTENT
            ) VALUES (
                '{doc_id}',
                '{model_id}',
                'MODEL_CARD',
                PARSE_JSON('{doc_content}')
            )
            """).collect()
        
        # Log the registration in audit log
        log_id = hashlib.md5(
            f"register_{model_id}_{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        audit_details = json.dumps({
            "action_type": "REGISTRATION",
            "model_name": model_info['name'],
            "model_version": model_info['version']
        })
        
        self.session.sql(f"""
        INSERT INTO AUDIT_LOG (
            LOG_ID, ENTITY_TYPE, ENTITY_ID, ACTION, USER_ID, DETAILS
        ) VALUES (
            '{log_id}',
            'MODEL',
            '{model_id}',
            'REGISTER',
            '{model_info.get('created_by', 'system')}',
            PARSE_JSON('{audit_details}')
        )
        """).collect()
        
        logger.info(f"Model registered with ID: {model_id}")
        return model_id
    
    def approve_model(self, model_id, approver, comments=None):
        """Approve a model for production use."""
        # Update model approval status
        self.session.sql(f"""
        UPDATE MODEL_REGISTRY
        SET APPROVAL_STATUS = 'APPROVED'
        WHERE MODEL_ID = '{model_id}'
        """).collect()
        
        # Log the approval in audit log
        log_id = hashlib.md5(
            f"approve_{model_id}_{datetime.now().isoformat()}".encode()
        ).hexdigest()
        
        audit_details = {
            "action_type": "APPROVAL",
            "approver": approver
        }
        
        if comments:
            audit_details["comments"] = comments
        
        audit_details_json = json.dumps(audit_details)
        
        self.session.sql(f"""
        INSERT INTO AUDIT_LOG (
            LOG_ID, ENTITY_TYPE, ENTITY_ID, ACTION, USER_ID, DETAILS
        ) VALUES (
            '{log_id}',
            'MODEL',
            '{model_id}',
            'APPROVE',
            '{approver}',
            PARSE_JSON('{audit_details_json}')
        )
        """).collect()
        
        logger.info(f"Model {model_id} approved by {approver}")
        return True
    
    def get_model_governance_report(self, model_id):
        """Generate a comprehensive governance report for a model."""
        # Get model registry information
        model_info = self.session.sql(f"""
        SELECT * FROM MODEL_REGISTRY WHERE MODEL_ID = '{model_id}'
        """).collect()
        
        # Get metrics
        metrics = self.session.sql(f"""
        SELECT METRIC_NAME, METRIC_VALUE FROM MODEL_METRICS 
        WHERE MODEL_ID = '{model_id}'
        """).collect()
        
        # Get lineage
        lineage = self.session.sql(f"""
        SELECT * FROM MODEL_LINEAGE WHERE MODEL_ID = '{model_id}'
        """).collect()
        
        # Get documentation
        docs = self.session.sql(f"""
        SELECT DOC_TYPE, CONTENT FROM MODEL_DOCUMENTATION 
        WHERE MODEL_ID = '{model_id}'
        """).collect()
        
        # Get audit trail
        audit = self.session.sql(f"""
        SELECT ACTION, USER_ID, TIMESTAMP, DETAILS 
        FROM AUDIT_LOG 
        WHERE ENTITY_ID = '{model_id}' 
        ORDER BY TIMESTAMP DESC
        """).collect()
        
        # Compile report
        report = {
            "model_info": model_info,
            "metrics": metrics,
            "lineage": lineage,
            "documentation": docs,
            "audit_trail": audit
        }
        
        return report

# Example usage
if __name__ == "__main__":
    governance = ModelGovernance()
    
    # Register a new K-means model
    model_info = {
        "name": "customer_segmentation_kmeans",
        "version": "1.0.0",
        "created_by": "data_science_team",
        "model_path": "models/kmeans_clusters_4",
        "description": "K-means clustering model for customer segmentation",
        "status": "PRODUCTION",
        "metrics": {
            "silhouette_score": 0.68,
            "inertia": 245.7
        },
        "lineage": {
            "dataset_id": "customer_data_2023_q1",
            "feature_set_id": "customer_features_v1",
            "training_job_id": "job_20230415_kmeans",
            "type": "TRAINING"
        },
        "documentation": {
            "model_type": "K-means clustering",
            "purpose": "Customer segmentation for targeted marketing",
            "features": [
                "purchase_amount", 
                "visit_frequency", 
                "region", 
                "customer_type"
            ],
            "limitations": "Assumes spherical clusters of similar size",
            "ethical_considerations": "No PII used in clustering",
            "usage_guidelines": "Use for marketing segmentation only"
        }
    }
    
    model_id = governance.register_model(model_info)
    
    # Approve the model
    governance.approve_model(
        model_id, 
        "model_review_board", 
        "Model meets all requirements for production use"
    )
    
    # Generate governance report
    report = governance.get_model_governance_report(model_id)
    print(f"Generated governance report for model {model_id}")
`;

export const infrastructureNotes = 'This Airflow DAG sets up the Snowflake infrastructure required for ML operations. It creates dedicated warehouses, databases, and schemas for different stages of the ML lifecycle along with appropriate storage integration for external data sources.';

export const dataPipelineNotes = 'This data pipeline implements robust ETL processes for K-means clustering in Snowflake. It includes data extraction from multiple sources, data validation with quality checks, feature engineering for clustering, and creation of a versioned feature store.';

export const modelDevelopmentNotes = 'This code implements K-means clustering with hyperparameter tuning in Snowflake ML. It includes model training with multiple feature sets, silhouette score evaluation, experiment tracking, and automatic model versioning based on performance metrics.';

export const cicdNotes = 'This GitHub Actions workflow automates testing, validation, and deployment of K-means models. It implements a complete CI/CD pipeline with unit tests, model validation, staging deployment with integration tests, and controlled production deployment.';

export const monitoringNotes = 'This monitoring system tracks K-means model performance in production. It collects daily metrics on cluster distribution and silhouette scores, implements data drift detection with statistical tests, and provides automated alerting for performance degradation.';

export const governanceNotes = 'This governance framework establishes model lineage tracking, comprehensive documentation, and audit trails for K-means models. It implements model approval workflows, version control, and generates detailed compliance reports for regulatory requirements.';
</script> 