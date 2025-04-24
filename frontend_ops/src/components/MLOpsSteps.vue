<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">Implementation Steps</h2>
    
    <p class="mb-6">Effectively setting up an MLOps environment involves several crucial steps:</p>
    
    <div class="grid grid-cols-1 gap-6">
      <!-- Infrastructure Setup -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(1)"
          :class="{'border-b border-gray-700': selectedStepId === 1}"
        >
          <div class="flex items-center">
            <div class="bg-purple-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">1</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">Infrastructure Setup</h3>
              <p class="text-gray-300">Configure compute resources, storage, and networking to support your ML workflow</p>
            </div>
            <div>
              <i :class="selectedStepId === 1 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 1" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
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
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
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
            </pre>
          </div>
        </div>
      </div>
      
      <!-- Data Pipeline -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(2)"
          :class="{'border-b border-gray-700': selectedStepId === 2}"
        >
          <div class="flex items-center">
            <div class="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">2</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">Data Pipeline</h3>
              <p class="text-gray-300">Build robust data pipelines for data ingestion, preprocessing, and feature engineering</p>
            </div>
            <div>
              <i :class="selectedStepId === 2 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 2" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
            <p>Build robust data pipelines for data ingestion, preprocessing, and feature engineering to prepare data for K-means clustering in Snowflake.</p>
            
            <h5 class="text-md font-semibold mt-4">Key Data Pipeline Components:</h5>
            <ul class="pl-5 list-disc">
              <li><strong>Data Ingestion:</strong> Extract data from source systems into Snowflake</li>
              <li><strong>Data Validation:</strong> Apply quality checks and validation rules</li>
              <li><strong>Data Transformation:</strong> Clean, normalize, and prepare data</li>
              <li><strong>Feature Engineering:</strong> Create features for clustering models</li>
              <li><strong>Feature Store:</strong> Manage and version features for consistency</li>
            </ul>
            
            <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
-- Create a feature store in Snowflake
CREATE TABLE IF NOT EXISTS ML_OPS.PROCESSED_DATA.KMEANS_FEATURES (
  FEATURE_ID VARCHAR NOT NULL,
  FEATURE_NAME VARCHAR NOT NULL,
  FEATURE_VALUE FLOAT,
  FEATURE_VERSION INTEGER DEFAULT 1,
  ENTITY_ID VARCHAR NOT NULL,
  ENTITY_TYPE VARCHAR,
  CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  UPDATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (FEATURE_ID, ENTITY_ID, FEATURE_VERSION)
);
            </pre>
          </div>
        </div>
      </div>
      
      <!-- Model Development -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(3)"
          :class="{'border-b border-gray-700': selectedStepId === 3}"
        >
          <div class="flex items-center">
            <div class="bg-green-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">3</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">Model Development</h3>
              <p class="text-gray-300">Develop, train, and evaluate K-means clustering models with experiment tracking</p>
            </div>
            <div>
              <i :class="selectedStepId === 3 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 3" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
            <p>Develop, train, and evaluate K-means clustering models in Snowflake ML, with experiment tracking for hyperparameter tuning and model selection.</p>
            
            <h5 class="text-md font-semibold mt-4">Key Model Development Components:</h5>
            <ul class="pl-5 list-disc">
              <li><strong>Hyperparameter Tuning:</strong> Find optimal K value and other parameters</li>
              <li><strong>Model Training:</strong> Create workflows for reproducible model training</li>
              <li><strong>Evaluation:</strong> Set up metrics and procedures to assess model quality</li>
              <li><strong>Experiment Tracking:</strong> Record all experiments for comparison</li>
            </ul>
            
            <h5 class="text-md font-semibold mt-4">K-means Implementation in Snowflake:</h5>
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
-- Create UDF for K-means clustering in Snowflake
CREATE OR REPLACE PROCEDURE ML_OPS.MODELS.TRAIN_KMEANS_MODEL(
  INPUT_TABLE STRING,
  FEATURE_COLS ARRAY,
  NUM_CLUSTERS INTEGER,
  MAX_ITERATIONS INTEGER,
  RANDOM_STATE INTEGER,
  OUTPUT_TABLE STRING
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python', 'scikit-learn', 'pandas', 'numpy')
HANDLER = 'run'
AS
$$
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from snowflake.snowpark import Session
import snowflake.snowpark.functions as F

def run(session, input_table, feature_cols, num_clusters, max_iterations, random_state, output_table):
    # Load data
    df = session.table(input_table)
    
    # Select features and convert to pandas
    features_df = df.select(feature_cols).to_pandas()
    
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_df)
    
    # Train K-means model
    kmeans = KMeans(
        n_clusters=num_clusters,
        max_iter=max_iterations,
        random_state=random_state,
        n_init=10
    )
    
    cluster_labels = kmeans.fit_predict(scaled_features)
    
    # Calculate silhouette score
    from sklearn.metrics import silhouette_score
    silhouette = silhouette_score(scaled_features, cluster_labels)
    inertia = kmeans.inertia_
    
    # Add cluster labels back to original dataframe
    result_df = df.to_pandas()
    result_df['CLUSTER_LABEL'] = cluster_labels
    
    # Save results to output table
    session.create_dataframe(result_df).write.mode("overwrite").save_as_table(output_table)
    
    # Log model parameters and metrics
    session.sql(f"""
    INSERT INTO ML_OPS.MODELS.MODEL_REGISTRY (
        MODEL_NAME,
        MODEL_VERSION,
        MODEL_TYPE,
        PARAMETERS,
        METRICS,
        CREATED_AT
    ) VALUES (
        'kmeans_clustering',
        (SELECT COALESCE(MAX(MODEL_VERSION), 0) + 1 FROM ML_OPS.MODELS.MODEL_REGISTRY WHERE MODEL_NAME = 'kmeans_clustering'),
        'KMeans',
        PARSE_JSON('{"n_clusters": ' || {num_clusters} || ', "random_state": ' || {random_state} || '}'),
        PARSE_JSON('{"silhouette_score": ' || {silhouette} || ', "inertia": ' || {inertia} || '}'),
        CURRENT_TIMESTAMP()
    )
    """).collect()
    
    return f"Model trained with {num_clusters} clusters. Silhouette score: {silhouette:.4f}"
$$;
            </pre>
          </div>
        </div>
      </div>
      
      <!-- CI/CD Pipeline -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(4)"
          :class="{'border-b border-gray-700': selectedStepId === 4}"
        >
          <div class="flex items-center">
            <div class="bg-amber-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">4</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">CI/CD Pipeline</h3>
              <p class="text-gray-300">Implement continuous integration and deployment pipelines for model automation</p>
            </div>
            <div>
              <i :class="selectedStepId === 4 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 4" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
            <p>Implement continuous integration and deployment pipelines to automate testing, validation, and deployment of K-means models to production.</p>
            
            <h5 class="text-md font-semibold mt-4">Key CI/CD Components:</h5>
            <ul class="pl-5 list-disc">
              <li><strong>Model Testing:</strong> Automated validation of models before deployment</li>
              <li><strong>Deployment Strategy:</strong> Define staging and production deployment processes</li>
              <li><strong>Rollback Mechanism:</strong> Procedures for reverting to previous versions</li>
              <li><strong>Pipeline Automation:</strong> Tools for orchestrating the CI/CD process</li>
            </ul>
            
            <h5 class="text-md font-semibold mt-4">CI/CD Pipeline Example:</h5>
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
name: K-means Model CI/CD

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

jobs:
  test:
    name: Test Model
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest models/kmeans/tests/
          
  build_and_register:
    name: Build and Register Model
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build model artifact
        run: |
          python models/kmeans/build_artifact.py
      - name: Register model in Snowflake
        run: |
          python models/kmeans/register_model.py
            </pre>
          </div>
        </div>
      </div>
      
      <!-- Model Monitoring -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(5)"
          :class="{'border-b border-gray-700': selectedStepId === 5}"
        >
          <div class="flex items-center">
            <div class="bg-red-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">5</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">Model Monitoring</h3>
              <p class="text-gray-300">Set up monitoring systems to track performance and detect data drift</p>
            </div>
            <div>
              <i :class="selectedStepId === 5 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 5" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
            <p>Set up monitoring systems to track performance, detect data drift, and ensure reliable operation of production K-means models.</p>
            
            <h5 class="text-md font-semibold mt-4">Key Monitoring Components:</h5>
            <ul class="pl-5 list-disc">
              <li><strong>Performance Metrics:</strong> Track silhouette score, inertia, and business KPIs</li>
              <li><strong>Data Drift Detection:</strong> Monitor changes in feature distributions</li>
              <li><strong>Alerting System:</strong> Set up notifications for metric thresholds</li>
              <li><strong>Dashboards:</strong> Create visualizations of model performance</li>
            </ul>
            
            <h5 class="text-md font-semibold mt-4">Monitoring Implementation:</h5>
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
-- Create a task to monitor model performance
CREATE OR REPLACE TASK ML_OPS.MODELS.MONITOR_KMEANS_PERFORMANCE
  WAREHOUSE = ML_INFERENCE_WH
  SCHEDULE = 'USING CRON 0 0 * * * America/Los_Angeles'
AS
CALL ML_OPS.MODELS.EVALUATE_MODEL_PERFORMANCE('kmeans_clustering', 'ML_OPS.RESULTS.KMEANS_CLUSTERS');
            </pre>
          </div>
        </div>
      </div>
      
      <!-- Governance & Security -->
      <div class="bg-dark-700 rounded-lg shadow-md overflow-hidden">
        <div 
          class="p-6 cursor-pointer" 
          @click="toggleStep(6)"
          :class="{'border-b border-gray-700': selectedStepId === 6}"
        >
          <div class="flex items-center">
            <div class="bg-teal-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
              <span class="text-white font-bold text-xl">6</span>
            </div>
            <div class="flex-grow">
              <h3 class="text-xl font-bold">Governance & Security</h3>
              <p class="text-gray-300">Establish model governance practices including documentation and access controls</p>
            </div>
            <div>
              <i :class="selectedStepId === 6 ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-gray-400"></i>
            </div>
          </div>
        </div>
        
        <div v-if="selectedStepId === 6" class="p-6 bg-dark-800 border-t border-gray-700">
          <div class="prose prose-dark text-gray-300">
            <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
            <p>Establish model governance practices including documentation, audit trails, and access controls for K-means models in Snowflake.</p>
            
            <h5 class="text-md font-semibold mt-4">Key Governance Components:</h5>
            <ul class="pl-5 list-disc">
              <li><strong>Model Documentation:</strong> Record model purpose, design, and limitations</li>
              <li><strong>Audit Trails:</strong> Track model training, usage, and changes</li>
              <li><strong>Access Controls:</strong> Manage who can access and modify models</li>
              <li><strong>Compliance:</strong> Ensure models adhere to organizational policies</li>
            </ul>
            
            <h5 class="text-md font-semibold mt-4">Governance Implementation:</h5>
            <pre class="bg-dark-900 p-3 rounded text-sm overflow-x-auto">
-- Create a model documentation table
CREATE TABLE IF NOT EXISTS ML_OPS.MODELS.MODEL_DOCUMENTATION (
  MODEL_ID VARCHAR PRIMARY KEY,
  MODEL_NAME VARCHAR NOT NULL,
  MODEL_VERSION INTEGER NOT NULL,
  PURPOSE VARCHAR,
  DESCRIPTION VARCHAR,
  AUTHOR VARCHAR,
  CREATED_DATE TIMESTAMP_NTZ,
  APPROVED_BY VARCHAR,
  APPROVAL_DATE TIMESTAMP_NTZ
);
            </pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedStepId = ref(null);

function toggleStep(stepId) {
  if (selectedStepId.value === stepId) {
    selectedStepId.value = null;
  } else {
    selectedStepId.value = stepId;
  }
}
</script>

<style scoped>
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-md:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.prose-dark {
  --tw-prose-body: theme('colors.gray.300');
  --tw-prose-headings: theme('colors.white');
  --tw-prose-lead: theme('colors.gray.300');
  --tw-prose-links: theme('colors.blue.400');
  --tw-prose-bold: theme('colors.white');
  --tw-prose-counters: theme('colors.gray.400');
  --tw-prose-bullets: theme('colors.gray.400');
  --tw-prose-hr: theme('colors.gray.700');
  --tw-prose-quotes: theme('colors.gray.300');
  --tw-prose-quote-borders: theme('colors.gray.700');
  --tw-prose-captions: theme('colors.gray.400');
  --tw-prose-code: theme('colors.white');
  --tw-prose-pre-code: theme('colors.gray.300');
  --tw-prose-pre-bg: theme('colors.gray.900');
  --tw-prose-th-borders: theme('colors.gray.700');
  --tw-prose-td-borders: theme('colors.gray.700');
}
</style> 