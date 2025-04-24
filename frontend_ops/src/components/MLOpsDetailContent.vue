<template>
  <div class="bg-dark-800 border border-dark-600 rounded-lg p-6 mt-6">
    <div v-if="selectedStep">
      <!-- Implementation Notes Section -->
      <div class="mb-6">
        <h3 class="text-xl font-semibold mb-4 flex items-center">
          <span class="bg-primary-600 w-8 h-8 rounded-full flex items-center justify-center mr-3">
            <i class="fas fa-clipboard-list text-dark-900"></i>
          </span>
          Implementation Notes
        </h3>
        <div class="pl-11">
          <div v-if="selectedStep === 'infrastructure'">
            <p class="text-gray-300 mb-2">Setting up robust infrastructure is the foundation of any MLOps implementation:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Use containerization (Docker) to ensure environment consistency</li>
              <li>Implement infrastructure as code using tools like Terraform or CloudFormation</li>
              <li>Set up consistent development environments with tools like conda or virtualenv</li>
              <li>Establish compute resources suitable for ML workloads (GPUs, TPUs, etc.)</li>
              <li>Configure resource autoscaling for training and inference workloads</li>
            </ul>
            <p class="text-sm text-gray-400">Start with local development environments and gradually move to cloud-based infrastructure as your needs scale.</p>
          </div>
          
          <div v-if="selectedStep === 'data'">
            <p class="text-gray-300 mb-2">Efficient data pipelines are critical for ML success:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Establish data extraction, transformation, and loading (ETL) processes</li>
              <li>Implement data versioning and lineage tracking</li>
              <li>Set up feature stores for consistent feature access across training and production</li>
              <li>Create automated data quality validation checks</li>
              <li>Ensure proper data splitting for training, validation, and testing</li>
            </ul>
            <p class="text-sm text-gray-400">Focus on reproducibility and consistency in your data pipeline to ensure reliable model training.</p>
          </div>
          
          <div v-if="selectedStep === 'model'">
            <p class="text-gray-300 mb-2">Implement best practices for model development:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Use experiment tracking tools to monitor training metrics and hyperparameters</li>
              <li>Implement model versioning with tools like DVC or MLflow</li>
              <li>Establish reproducible training pipelines with consistent environments</li>
              <li>Document model architecture, training procedures, and evaluation metrics</li>
              <li>Set up model registry to catalog and manage model versions</li>
            </ul>
            <p class="text-sm text-gray-400">Focus on experimentation tracking and version control to ensure reproducibility and traceability.</p>
          </div>
          
          <div v-if="selectedStep === 'deployment'">
            <p class="text-gray-300 mb-2">Streamline the model deployment process:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Implement CI/CD pipelines for model deployment automation</li>
              <li>Establish standard model serving interfaces (REST, gRPC, etc.)</li>
              <li>Configure deployment strategies (canary, blue/green, shadow)</li>
              <li>Set up model packaging standards (Docker, ONNX, TensorRT, etc.)</li>
              <li>Implement automated testing for deployed models</li>
            </ul>
            <p class="text-sm text-gray-400">Aim for repeatable, automated deployments that reduce human error and deployment time.</p>
          </div>
          
          <div v-if="selectedStep === 'monitoring'">
            <p class="text-gray-300 mb-2">Implement comprehensive monitoring to ensure model reliability:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Monitor model performance metrics (accuracy, F1-score, etc.)</li>
              <li>Track data drift and concept drift indicators</li>
              <li>Set up system performance monitoring (latency, throughput, etc.)</li>
              <li>Implement alerting for critical performance degradation</li>
              <li>Create dashboards for visualization of key metrics</li>
            </ul>
            <p class="text-sm text-gray-400">Effective monitoring helps detect issues early and maintain model performance over time.</p>
          </div>
          
          <div v-if="selectedStep === 'governance'">
            <p class="text-gray-300 mb-2">Implement governance and security controls:</p>
            <ul class="list-disc pl-5 text-gray-300 space-y-2 mb-4">
              <li>Establish model documentation standards and model cards</li>
              <li>Implement access controls and data security measures</li>
              <li>Set up model validation and approval workflows</li>
              <li>Create procedures for model updates and retirement</li>
              <li>Implement audit logging for compliance and traceability</li>
            </ul>
            <p class="text-sm text-gray-400">Strong governance ensures regulatory compliance and builds trust in your ML systems.</p>
          </div>
        </div>
      </div>
      
      <!-- Code Examples Section -->
      <div>
        <h3 class="text-xl font-semibold mb-4 flex items-center">
          <span class="bg-primary-600 w-8 h-8 rounded-full flex items-center justify-center mr-3">
            <i class="fas fa-code text-dark-900"></i>
          </span>
          Example Implementation
        </h3>
        <div class="pl-11">
          <!-- Infrastructure Example -->
          <div v-if="selectedStep === 'infrastructure'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">terraform/main.tf</span>
              <span class="text-xs text-gray-400">Infrastructure as Code Example</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code>provider "aws" {
  region = "us-west-2"
}

module "ml_infrastructure" {
  source = "./modules/ml_infrastructure"
  
  environment    = "development"
  instance_type  = "p3.2xlarge"  # GPU instance
  min_instances  = 1
  max_instances  = 5
  vpc_id         = var.vpc_id
  subnet_ids     = var.subnet_ids
}

# S3 bucket for model artifacts
resource "aws_s3_bucket" "model_artifacts" {
  bucket = "company-ml-model-artifacts"
  acl    = "private"
  
  versioning {
    enabled = true
  }
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}</code></pre>
          </div>
          
          <!-- Data Pipeline Example -->
          <div v-if="selectedStep === 'data'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">data_pipeline.py</span>
              <span class="text-xs text-gray-400">Data Processing Pipeline</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code>import pandas as pd
from sklearn.model_selection import train_test_split
from great_expectations.dataset import PandasDataset

def validate_data(df):
    """Validate data quality using Great Expectations"""
    ge_df = PandasDataset(df)
    
    # Set expectations
    ge_df.expect_column_values_to_not_be_null("customer_id")
    ge_df.expect_column_values_to_be_between("age", 18, 120)
    ge_df.expect_column_values_to_be_in_set("status", ["active", "inactive", "pending"])
    
    # Run validation
    results = ge_df.validate()
    return results["success"]

def process_data(raw_data_path, output_path):
    """Process raw data and prepare for model training"""
    # Load data
    df = pd.read_csv(raw_data_path)
    
    # Validate data quality
    if not validate_data(df):
        raise ValueError("Data validation failed!")
    
    # Feature engineering
    df["account_age_days"] = (pd.Timestamp.now() - pd.to_datetime(df["signup_date"])).dt.days
    df["is_active"] = df["status"] == "active"
    
    # Split data
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    # Save processed datasets
    train_df.to_parquet(f"{output_path}/train.parquet")
    test_df.to_parquet(f"{output_path}/test.parquet")
    
    # Log data metrics
    print(f"Processed {len(df)} records. Train: {len(train_df)}, Test: {len(test_df)}")</code></pre>
          </div>
          
          <!-- Model Development Example -->
          <div v-if="selectedStep === 'model'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">train_model.py</span>
              <span class="text-xs text-gray-400">Model Training with MLflow</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code>import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Start MLflow experiment
mlflow.set_experiment("customer_churn_prediction")

# Load training data
train_data = pd.read_parquet("data/processed/train.parquet")
test_data = pd.read_parquet("data/processed/test.parquet")

# Prepare features and target
X_train = train_data.drop(["customer_id", "churn"], axis=1)
y_train = train_data["churn"]
X_test = test_data.drop(["customer_id", "churn"], axis=1)
y_test = test_data["churn"]

# Define hyperparameters
params = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 5,
    "random_state": 42
}

# Train model with MLflow tracking
with mlflow.start_run():
    # Log data versions
    mlflow.log_param("data_version", "v1.2")
    mlflow.log_param("features", list(X_train.columns))
    
    # Log hyperparameters
    for param, value in params.items():
        mlflow.log_param(param, value)
    
    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    
    # Log feature importance
    for idx, col in enumerate(X_train.columns):
        mlflow.log_metric(f"feature_importance_{col}", model.feature_importances_[idx])
    
    # Save model
    mlflow.sklearn.log_model(model, "model")</code></pre>
          </div>
          
          <!-- Deployment Example -->
          <div v-if="selectedStep === 'deployment'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">.github/workflows/deploy_model.yml</span>
              <span class="text-xs text-gray-400">CI/CD Pipeline for Model Deployment</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code>name: Deploy ML Model

on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'MLflow Model Version'
        required: true
      deployment_type:
        description: 'Deployment Type (canary/full)'
        required: true
        default: 'canary'

jobs:
  test_model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run model tests
        run: |
          python tests/test_model_performance.py --model-version ${{ github.event.inputs.model_version }}
          python tests/test_model_bias.py --model-version ${{ github.event.inputs.model_version }}

  build_container:
    needs: test_model
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: |
            company-registry.com/ml-models/churn-model:${{ github.event.inputs.model_version }}
            company-registry.com/ml-models/churn-model:latest
          build-args: |
            MODEL_VERSION=${{ github.event.inputs.model_version }}

  deploy_model:
    needs: build_container
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        uses: Azure/k8s-deploy@v1
        with:
          manifests: |
            k8s/model-deployment.yml
          images: |
            company-registry.com/ml-models/churn-model:${{ github.event.inputs.model_version }}
          strategy: ${{ github.event.inputs.deployment_type }}
      
      - name: Run smoke tests
        run: |
          python tests/smoke_test_endpoint.py

      - name: Update model registry status
        run: |
          python scripts/update_model_status.py \
            --model-version ${{ github.event.inputs.model_version }} \
            --status "deployed" \
            --environment "production"</code></pre>
          </div>
          
          <!-- Monitoring Example -->
          <div v-if="selectedStep === 'monitoring'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">monitoring/drift_detection.py</span>
              <span class="text-xs text-gray-400">Model Monitoring and Drift Detection</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code>import pandas as pd
import numpy as np
from scipy import stats
from prometheus_client import Counter, Gauge, start_http_server
import time
import logging
import json

# Setup metrics
PREDICTION_COUNT = Counter('model_predictions_total', 'Total number of predictions')
DRIFT_SCORE = Gauge('data_drift_score', 'Current data drift score')
FEATURE_DRIFT = Gauge('feature_drift', 'Feature drift by feature name', ['feature'])
MODEL_LATENCY = Gauge('model_inference_latency_seconds', 'Model inference latency in seconds')

# Reference data - from training set
with open('reference_data_stats.json', 'r') as f:
    reference_stats = json.load(f)

def calculate_drift(current_data):
    """Calculate drift between current data and reference data"""
    drift_scores = {}
    
    for feature in reference_stats:
        # Skip non-numeric features for this simple example
        if reference_stats[feature]['type'] != 'numeric':
            continue
            
        # Get current distribution
        current_values = current_data[feature].dropna().values
        
        # Skip if not enough data
        if len(current_values) < 30:
            continue
            
        # Calculate KS test
        ks_stat, p_value = stats.ks_2samp(
            current_values, 
            np.random.normal(
                reference_stats[feature]['mean'], 
                reference_stats[feature]['std'], 
                len(current_values)
            )
        )
        
        drift_scores[feature] = {
            'ks_stat': float(ks_stat),
            'p_value': float(p_value),
            'is_drift': p_value < 0.05
        }
        
        # Update Prometheus metrics
        FEATURE_DRIFT.labels(feature=feature).set(ks_stat)
        
    # Overall drift score (average KS statistic)
    overall_drift = np.mean([d['ks_stat'] for d in drift_scores.values()])
    DRIFT_SCORE.set(overall_drift)
    
    return drift_scores, overall_drift

def monitor_predictions(prediction_data, predictions, latency_ms):
    """Monitor predictions and detect drift"""
    # Update metrics
    PREDICTION_COUNT.inc()
    MODEL_LATENCY.set(latency_ms / 1000.0)  # Convert to seconds
    
    # Add to monitoring buffer
    global monitoring_buffer
    monitoring_buffer = monitoring_buffer.append(prediction_data)
    
    # Calculate drift if buffer is large enough
    if len(monitoring_buffer) >= 100:
        drift_scores, overall_drift = calculate_drift(monitoring_buffer)
        monitoring_buffer = pd.DataFrame()  # Reset buffer
        
        # Log results
        logging.info(f"Overall drift score: {overall_drift:.4f}")
        for feature, scores in drift_scores.items():
            if scores['is_drift']:
                logging.warning(f"Drift detected in feature {feature}: KS={scores['ks_stat']:.4f}, p={scores['p_value']:.4f}")
        
        # Alert if significant drift
        if overall_drift > 0.2:
            send_alert(f"High data drift detected: {overall_drift:.4f}")
            
# Start monitoring server
monitoring_buffer = pd.DataFrame()
start_http_server(8000)  # Prometheus metrics endpoint
logging.info("Model monitoring server started on port 8000")</code></pre>
          </div>
          
          <!-- Governance Example -->
          <div v-if="selectedStep === 'governance'" class="bg-dark-900 p-4 rounded-lg">
            <div class="flex justify-between mb-2">
              <span class="text-gray-300 text-sm">model_card.md</span>
              <span class="text-xs text-gray-400">Model Card Documentation</span>
            </div>
            <pre class="text-gray-300 text-sm whitespace-pre-wrap overflow-x-auto"><code># Model Card: Customer Churn Prediction Model

## Model Details
- **Model Name**: Customer Churn Prediction v2.1
- **Model Type**: Random Forest Classifier
- **Model Version**: 2.1
- **Date**: 2023-05-15
- **License**: Internal use only
- **Contact**: ml-team@company.com

## Intended Use
- **Primary intended uses**: Predict customer churn probability for proactive retention campaigns
- **Primary intended users**: Marketing and Customer Success teams
- **Out-of-scope use cases**: Individual customer profiling for credit or insurance decisions

## Training Data
- **Source**: Internal customer database, Jan 2020 - Dec 2022
- **Number of records**: 145,782
- **Features**: 28 features including customer demographics, usage patterns, and support interactions
- **Preprocessing**: Standardization, imputation of missing values, one-hot encoding of categorical features
- **Train/test split**: 80% training, 20% testing with temporal validation

## Performance Metrics
- **Accuracy**: 0.87
- **Precision**: 0.83
- **Recall**: 0.79
- **F1 Score**: 0.81
- **AUC-ROC**: 0.92

## Ethical Considerations
- **Fairness Assessment**: Model was evaluated for prediction disparity across age groups, geographic regions, and customer segments. Maximum disparity in prediction rates is 3.2%.
- **Potential Biases**: The model may underperform for new customer segments with limited historical data.
- **Mitigations**: Regular retraining with updated data, monitoring of performance across segments

## Limitations
- **Technical Limitations**: Model performance degrades for customers with less than 3 months of history.
- **Performance Tradeoffs**: Optimized for precision over recall to minimize false positives.

## Usage Guidelines
- **Recommended Thresholds**: 0.7 for high-risk customers, 0.5 for medium-risk
- **Confidence Intervals**: All predictions include 95% confidence intervals
- **Interpretation Guide**: See documentation at docs/model-interpretation.md

## Maintenance
- **Owner**: ML Team
- **Update Frequency**: Quarterly retraining
- **Update Process**: Full validation and A/B testing before deployment
- **Monitoring Plan**: Daily data drift checks, weekly performance metrics</code></pre>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-10 text-gray-400">
      <i class="fas fa-hand-point-up text-3xl mb-4"></i>
      <p>Select a component above to see implementation details</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  selectedStep: {
    type: String,
    default: null
  }
});
</script>

<style scoped>
pre {
  max-height: 400px;
}
</style> 