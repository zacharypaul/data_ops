<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-purple-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-code-branch text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">CI/CD Pipeline</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Implement continuous integration and deployment pipelines to automate testing, validation, and deployment of K-means models to production</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Automated testing</li>
        <li>Model validation</li>
        <li>Deployment automation</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 2-3 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <div class="mb-6 bg-dark-800 rounded-lg p-4">
        <h4 class="text-xl font-semibold mb-3">Snowflake ML K-means Example</h4>
        <p class="text-gray-300">This Airflow DAG handles the CI/CD process for K-means models in Snowflake. It runs tests, validates model performance, and manages the deployment to different environments.</p>
      </div>

      <div class="mb-4">
        <div class="flex justify-between items-center bg-dark-800 py-2 px-4 rounded-t-lg">
          <span class="text-sm font-medium">Airflow DAG Example</span>
          <span class="text-sm text-gray-400">snowflake_kmeans_cicd.py</span>
        </div>
        <pre class="bg-dark-900 p-4 rounded-b-lg text-sm text-gray-300 overflow-x-auto">
# Import the necessary libraries
import snowflake.snowpark as snowpark
from snowflake.ml.modeling.preprocessing import OneHotEncoder, StandardScaler
from snowflake.ml.modeling.clustering import KMeans
from snowflake.ml.experiment import Experiment

# Create a Snowflake session
session = snowpark.Session.builder.configs({
    "account": "your_account",
    "user": "your_username",
    "password": "your_password",
    "role": "your_role",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema"
}).create()

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
</pre>
      </div>
      
      <div class="prose prose-dark text-gray-300">
        <h5 class="text-md font-semibold mt-4">CI/CD Pipeline Components:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Continuous Integration:</strong> Automated testing and validation of ML code</li>
          <li><strong>Continuous Delivery:</strong> Automated deployment of models to staging environments</li>
          <li><strong>Continuous Deployment:</strong> Automated deployment to production with safeguards</li>
          <li><strong>Pipeline Orchestration:</strong> Managing the flow of models through the pipeline</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Build CI/CD pipelines for K-means models in Snowflake:</p>
        <ul class="pl-5 list-disc">
          <li>Implement Git-based version control for model code</li>
          <li>Set up automated testing with pytest for model validation</li>
          <li>Use GitHub Actions for CI/CD automation</li>
          <li>Configure multi-environment deployments (dev, test, prod)</li>
          <li>Implement automated model validation checks</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">CI/CD Configuration:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# GitHub Actions workflow file (.github/workflows/kmeans-model-cicd.yml)
name: K-means Model CI/CD

on:
  push:
    branches: [ main ]
    paths:
      - 'models/kmeans/**'
      - '.github/workflows/kmeans-model-cicd.yml'
  pull_request:
    branches: [ main ]
    paths:
      - 'models/kmeans/**'

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
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest pytest-cov
      - name: Test with pytest
        run: |
          pytest models/kmeans/tests/ --cov=models/kmeans --cov-report=xml
      - name: Upload coverage report
        uses: codecov/codecov-action@v1

  validate:
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
      - name: Validate model
        run: python models/kmeans/validate_model.py
      - name: Upload validation report
        uses: actions/upload-artifact@v2
        with:
          name: model-validation-report
          path: models/kmeans/validation_report.json

  deploy-dev:
    needs: validate
    if: github.event_name == 'pull_request'
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
      - name: Deploy to dev
        run: python models/kmeans/deploy.py --env dev
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}

  deploy-prod:
    needs: validate
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
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
      - name: Deploy to production
        run: python models/kmeans/deploy.py --env prod
        env:
          SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}
          SNOWFLAKE_USER: ${{ secrets.SNOWFLAKE_USER }}
          SNOWFLAKE_PASSWORD: ${{ secrets.SNOWFLAKE_PASSWORD }}
          SNOWFLAKE_ROLE: ${{ secrets.SNOWFLAKE_ROLE }}
</pre>
        
        <h5 class="text-md font-semibold mt-4">Model Validation Script:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# models/kmeans/validate_model.py
import json
import snowflake.snowpark as snowpark
from snowflake.ml.modeling.clustering import KMeans
import os
import joblib
import numpy as np

def validate_model():
    """Validate the K-means model against acceptance criteria."""
    # Set up Snowflake session
    session = snowpark.Session.builder.configs({
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": os.environ["SNOWFLAKE_ROLE"],
        "warehouse": "ML_VALIDATION_WH",
        "database": "ML_OPS",
        "schema": "VALIDATION"
    }).create()
    
    # Load validation data
    df = session.table("VALIDATION_DATA")
    
    # Load the model
    model = joblib.load('models/kmeans/model.joblib')
    
    # Make predictions
    predictions = model.predict(df.to_pandas())
    
    # Calculate validation metrics
    silhouette_score = model.score(df.to_pandas())
    inertia = model.inertia_
    
    # Define acceptance criteria
    acceptance_criteria = {
        "silhouette_score_min": 0.6,
        "max_cluster_imbalance": 0.3  # Max allowed cluster size imbalance ratio
    }
    
    # Calculate cluster sizes
    cluster_sizes = np.bincount(predictions)
    max_size = np.max(cluster_sizes)
    min_size = np.min(cluster_sizes)
    imbalance_ratio = (max_size - min_size) / len(predictions)
    
    # Perform validation
    is_valid = (
        silhouette_score >= acceptance_criteria["silhouette_score_min"] and 
        imbalance_ratio <= acceptance_criteria["max_cluster_imbalance"]
    )
    
    # Create validation report
    validation_report = {
        "is_valid": is_valid,
        "metrics": {
            "silhouette_score": float(silhouette_score),
            "inertia": float(inertia),
            "cluster_imbalance_ratio": float(imbalance_ratio),
            "cluster_sizes": cluster_sizes.tolist()
        },
        "acceptance_criteria": acceptance_criteria
    }
    
    # Save report
    with open("models/kmeans/validation_report.json", "w") as f:
        json.dump(validation_report, f, indent=2)
    
    # Close Snowflake session
    session.close()
    
    # Return the validation result
    return is_valid

if __name__ == "__main__":
    is_valid = validate_model()
    print(f"Model validation {'passed' if is_valid else 'failed'}")
    exit(0 if is_valid else 1)
</pre>
        
        <h5 class="text-md font-semibold mt-4">CI/CD Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Establish clear model acceptance criteria</li>
          <li>Implement automated testing for model validation</li>
          <li>Use feature branches for model development</li>
          <li>Require code reviews for model changes</li>
          <li>Maintain separate environments for dev, test, and production</li>
          <li>Implement model deployment rollback capabilities</li>
          <li>Automate deployment verification</li>
          <li>Secure credentials using environment secrets</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CICDPipelineStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 