<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-orange-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-rocket text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Model Deployment</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Automate the deployment of ML models to production environments</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Model packaging & containerization</li>
        <li>Automated CI/CD pipelines</li>
        <li>Multi-environment deployment</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 2-4 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-orange-600 hover:bg-orange-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
      
      <div class="prose prose-dark text-gray-300">
        <p>Reliable model deployment ensures that models transition from development to production seamlessly with minimal risk.</p>
        
        <h5 class="text-md font-semibold mt-4">Deployment Strategies:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Blue-Green Deployment:</strong> Create duplicate environments and switch traffic</li>
          <li><strong>Canary Releases:</strong> Gradually roll out to a subset of users</li>
          <li><strong>Shadow Deployment:</strong> Run new model alongside existing one without affecting outputs</li>
          <li><strong>A/B Testing:</strong> Split traffic between model versions and compare performance</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Leverage Snowflake's capabilities for model deployment:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowflake's Snowpark Container Services for model serving</li>
          <li>Deploy models as User-Defined Functions (UDFs) within Snowflake</li>
          <li>Implement Stored Procedures for complex model inference workflows</li>
          <li>Configure role-based access control for model endpoints</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Deployment Pipeline:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# Example CI/CD pipeline configuration for Snowflake model deployment
name: Deploy K-means Model to Snowflake

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
    
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
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/
        
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Package model
        run: python scripts/package_model.py
      - name: Deploy model to Snowflake (DEV)
        if: github.event_name == 'pull_request'
        run: python scripts/deploy_to_snowflake.py --environment dev
      - name: Deploy model to Snowflake (PROD)
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: python scripts/deploy_to_snowflake.py --environment prod
</pre>
        
        <h5 class="text-md font-semibold mt-4">Deploying as a Snowflake UDF:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create UDF for K-means prediction
CREATE OR REPLACE FUNCTION ml_schema.predict_customer_segment(
    amount FLOAT,
    frequency FLOAT,
    region VARCHAR,
    customer_type VARCHAR
)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python', 'scikit-learn')
IMPORTS = ('@ml_models/kmeans_model.pkl')
HANDLER = 'predict_segment'
AS
$$
import pickle
import pandas as pd
from snowflake.snowpark.vectorized import pandas_udf

def predict_segment(amount, frequency, region, customer_type):
    # Load the model
    with open('kmeans_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Preprocess input features
    # (In production, this would include encoding and scaling)
    
    # Make prediction
    cluster = model.predict([[amount, frequency, 0, 0]])[0]
    
    # Map cluster to business segment
    segments = {
        0: 'Low Value',
        1: 'Medium Value',
        2: 'High Value',
        3: 'VIP'
    }
    
    return segments.get(cluster, 'Unknown')
$$;
</pre>

        <h5 class="text-md font-semibold mt-4">Model Deployment Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Automate deployment processes with CI/CD pipelines</li>
          <li>Use versioning for all model artifacts</li>
          <li>Implement gradual rollout strategies with controlled exposure</li>
          <li>Create rollback plans for model deployments</li>
          <li>Monitor models immediately after deployment</li>
          <li>Use feature flags to control model behavior in production</li>
          <li>Ensure all dependencies are properly managed</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelDeploymentStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 