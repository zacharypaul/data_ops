<template>
  <div class="w-full">
    <h1 class="text-3xl font-bold mb-6">ML Ops Platform</h1>
    <p class="text-lg mb-8">Unified platform for machine learning and generative AI operations</p>
    
    <!-- MLOps Implementation Steps -->
    <section class="mb-10 bg-dark-800 rounded-lg p-6">
      <h2 class="text-2xl font-bold mb-6">MLOps Setup Process</h2>
      <MLOpsSteps />
    </section>
    
    <!-- K-means Model Lifecycle Journey -->
    <section class="mb-10">
      <h2 class="text-2xl font-bold mb-6">K-means Model Development Journey</h2>
      <p class="mb-4 text-gray-300">Follow this iterative workflow to develop, deploy and continuously improve your K-means clustering models.</p>
      <KMeansJourney />
    </section>
    
    <!-- MLOps Guide Expander -->
    <MLOpsGuide @show-detail-card="showDetailCard" />
    
    <!-- Implementation Notes -->
    <ImplementationNotes />
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Dashboard Summary Cards -->
      <SummaryCard 
        title="ML Experiments"
        description="Track and manage your machine learning experiments"
        stats="7 active experiments"
      />
      
      <SummaryCard 
        title="Model Registry"
        description="Version and deploy ML models"
        stats="12 registered models"
      />
      
      <SummaryCard 
        title="GenAI Apps"
        description="Monitor generative AI applications"
        stats="4 deployed applications"
      />
    </div>
    
    <!-- Tab Navigation -->
    <TabNavigation
      :tabs="tabs"
      :activeTab="activeTab"
      @update:activeTab="activeTab = $event"
    />
    
    <!-- Tab Content -->
    <div class="glass-card p-6">
      <!-- Experiments Tab -->
      <div v-if="activeTab === 'experiments'">
        <h2 class="text-2xl font-bold mb-4">ML Experiments</h2>
        <p class="mb-6">Track, compare, and manage machine learning experiments across multiple platforms.</p>
        
        <div class="mb-6">
          <ExperimentsList
            :experiments="experiments"
            :platformColors="platformColors"
            :statusColors="statusColors"
            :viewMode="experimentViewMode"
            @update:viewMode="experimentViewMode = $event"
            @newExperiment="newExperimentModalOpen = true"
          />
          
          <!-- New Experiment Modal -->
          <div v-if="newExperimentModalOpen" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
            <div class="bg-dark-800 rounded-lg shadow-lg p-6 max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold text-white">Create New ML Experiment</h3>
                <button @click="newExperimentModalOpen = false" class="text-gray-400 hover:text-white">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              <div class="space-y-6">
                <!-- Performance Alert - Now at the top and without activeTab condition -->
                <div class="bg-gradient-to-r from-blue-900/30 to-purple-900/30 border border-blue-500/30 rounded-lg p-4 mb-6">
                  <div class="flex items-start">
                    <div class="flex-shrink-0 bg-blue-900 p-2 rounded mr-3">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold text-blue-300 mb-2">K-Means Analysis Insights</h3>
                      <div class="space-y-3 text-gray-300">
                        <p><span class="font-medium text-blue-300">Key Findings:</span> Our latest K-means analysis shows optimal cluster count is 4, with a 15% improvement in cluster separation compared to previous model.</p>
                        
                        <ul class="list-disc list-inside pl-2 space-y-1 text-sm">
                          <li>Silhouette score increased from 0.58 to 0.68</li>
                          <li>Clear customer segments emerged with distinct behavior patterns</li>
                          <li>Cluster 3 shows highest conversion potential (23% vs 12% avg)</li>
                          <li>Model v2 outperforms v1 on all evaluation metrics</li>
                        </ul>
                        
                        <p class="font-medium text-blue-300">Recommendations:</p>
                        <ul class="list-disc list-inside pl-2 text-sm">
                          <li>Deploy model v2 to production</li>
                          <li>Target Cluster 3 with specialized marketing campaigns</li>
                          <li>Update customer dashboards with new segmentation</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Frontend Integration Instructions - Now first option -->
                <div class="border border-dark-600 rounded-lg p-4">
                  <h4 class="text-lg font-medium text-green-400 mb-2">Option 1: Run Experiments from the Frontend</h4>
                  <p class="text-gray-300 mb-3">When you merge your ML code into GitHub, you can run experiments directly from this dashboard:</p>
                  
                  <ol class="list-decimal text-gray-300 ml-5 space-y-2">
                    <li>Push your ML code to your repository with proper experiment tracking setup</li>
                    <li>Configure the GitHub integration in the <span class="text-green-400">Integrations</span> tab</li>
                    <li>Use the form below to specify experiment parameters</li>
                    <li>Click "Start Experiment" to trigger a GitHub Actions workflow</li>
                    <li>Track results in real-time on this dashboard</li>
                  </ol>
                  
                  <div class="mt-4 mb-2 border-t border-dark-600 pt-4">
                    <h5 class="text-white font-medium mb-3">Experiment Configuration</h5>
                    <form class="space-y-4">
                      <div>
                        <label class="block text-gray-400 mb-1">Experiment Name</label>
                        <input type="text" placeholder="Customer Segmentation v2" 
                               class="w-full bg-dark-900 border border-dark-600 rounded py-2 px-3 text-white">
                      </div>
                      <div>
                        <label class="block text-gray-400 mb-1">Repository</label>
                        <select class="w-full bg-dark-900 border border-dark-600 rounded py-2 px-3 text-white">
                          <option>ml-models/customer-segmentation</option>
                          <option>ml-models/product-recommendations</option>
                          <option>ml-models/churn-prediction</option>
                        </select>
                      </div>
                      <div>
                        <label class="block text-gray-400 mb-1">Parameters (JSON)</label>
                        <textarea rows="4" 
                                  class="w-full bg-dark-900 border border-dark-600 rounded py-2 px-3 text-white font-mono text-sm"
                                  placeholder='{"n_clusters": 4, "random_state": 42, "algorithm": "k-means"}'></textarea>
                      </div>
                      <div>
                        <label class="block text-gray-400 mb-1">Compute Resources</label>
                        <select class="w-full bg-dark-900 border border-dark-600 rounded py-2 px-3 text-white">
                          <option>X-Small (2 vCPU, 4GB RAM)</option>
                          <option>Small (4 vCPU, 8GB RAM)</option>
                          <option selected>Medium (8 vCPU, 16GB RAM)</option>
                          <option>Large (16 vCPU, 32GB RAM)</option>
                        </select>
                      </div>
                      <div class="pt-2">
                        <button type="button" 
                                class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded">
                          Start Experiment
                        </button>
                        <button type="button" 
                                @click="newExperimentModalOpen = false"
                                class="ml-2 border border-gray-600 hover:border-gray-500 text-gray-300 py-2 px-4 rounded">
                          Cancel
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
                
                <!-- Snowflake ML Instructions - Now second option -->
                <div class="border border-dark-600 rounded-lg p-4">
                  <h4 class="text-lg font-medium text-blue-400 mb-2">Option 2: Run Experiments in Snowflake ML</h4>
                  <p class="text-gray-300 mb-3">Follow these steps to create and track an ML experiment using Snowflake ML:</p>
                  
                  <div class="bg-dark-900 p-3 rounded font-mono text-sm overflow-x-auto">
                    <pre class="text-gray-300">
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

# End run
experiment.end_run()
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Time Series View -->
          <TimeSeriesChart 
            v-if="experimentViewMode === 'timeseries'"
            :initialMetric="selectedTimeseriesMetric"
            :initialTimeRange="timeseriesRange"
            :showInfo="showTimeSeriesInfo"
            @update:selectedMetric="selectedTimeseriesMetric = $event"
            @update:timeRange="timeseriesRange = $event"
            @update:showInfo="showTimeSeriesInfo = $event"
          />
        </div>
        
        <!-- Experiment Guide Expander -->
        <div class="mb-8 glass-card">
          <div 
            @click="experimentGuideOpen = !experimentGuideOpen" 
            class="p-4 flex justify-between items-center cursor-pointer border-b border-dark-700"
          >
            <h3 class="text-xl font-semibold flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-primary-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
              </svg>
              Experiment Tracking Guide
            </h3>
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              class="h-5 w-5 transition-transform" 
              :class="{'rotate-180': experimentGuideOpen}"
              viewBox="0 0 20 20" 
              fill="currentColor"
            >
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </div>
          
          <div v-show="experimentGuideOpen" class="p-5 space-y-4">
            <div class="mb-6">
              <h4 class="text-lg font-semibold mb-2 text-primary-300">How to Track Experiments</h4>
              <p class="mb-3">Effective experiment tracking is crucial for reproducible machine learning. Follow these best practices:</p>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div class="p-4 border border-dark-600 rounded-lg">
                  <div class="flex items-center mb-2">
                    <div class="bg-primary-900 w-8 h-8 rounded-full flex items-center justify-center mr-2 text-primary-300 font-bold">1</div>
                    <h5 class="font-bold">Define Parameters</h5>
                  </div>
                  <p class="text-sm text-gray-300">Track all hyperparameters, dataset versions, and preprocessing steps for complete reproducibility.</p>
                </div>
                
                <div class="p-4 border border-dark-600 rounded-lg">
                  <div class="flex items-center mb-2">
                    <div class="bg-primary-900 w-8 h-8 rounded-full flex items-center justify-center mr-2 text-primary-300 font-bold">2</div>
                    <h5 class="font-bold">Log All Metrics</h5>
                  </div>
                  <p class="text-sm text-gray-300">Monitor key metrics like accuracy, F1 score, RMSE, and platform-specific measures across training runs.</p>
                </div>
                
                <div class="p-4 border border-dark-600 rounded-lg">
                  <div class="flex items-center mb-2">
                    <div class="bg-primary-900 w-8 h-8 rounded-full flex items-center justify-center mr-2 text-primary-300 font-bold">3</div>
                    <h5 class="font-bold">Save Artifacts</h5>
                  </div>
                  <p class="text-sm text-gray-300">Store model files, feature importance data, confusion matrices, and validation plots for each run.</p>
                </div>
              </div>
              
              <div class="p-4 bg-dark-800 rounded-lg mb-4">
                <h5 class="font-semibold mb-2 text-primary-200">Platform-Specific Tracking</h5>
                <ul class="list-disc list-inside space-y-2 text-sm">
                  <li><span class="text-blue-400 font-semibold">Snowflake ML:</span> Use Snowflake tasks to track execution metrics and model tables for version control.</li>
                  <li><span class="text-cyan-400 font-semibold">Azure ML:</span> Leverage Azure ML experiments to track runs with automatic metadata logging.</li>
                  <li><span class="text-indigo-400 font-semibold">MLflow:</span> Use tracking API with experiment_id to organize runs and log parameters and metrics.</li>
                </ul>
              </div>
            </div>
            
            <div>
              <h4 class="text-lg font-semibold mb-2 text-primary-300">What to Do with Experiment Results</h4>
              <p class="mb-3">Experiment results provide valuable insights that guide your ML workflow. Here's how to use them:</p>
              
              <div class="mb-4 space-y-4">
                <div class="p-4 border-l-4 border-green-500 bg-dark-800 rounded-r-lg">
                  <h5 class="font-bold mb-1">Model Selection</h5>
                  <p class="text-sm text-gray-300">Compare experiments across different models, hyperparameters, and features to identify the best performing model based on your specific business metrics.</p>
                </div>
                
                <div class="p-4 border-l-4 border-blue-500 bg-dark-800 rounded-r-lg">
                  <h5 class="font-bold mb-1">Promote to Registry</h5>
                  <p class="text-sm text-gray-300">Once you've identified your best model, register it in the Model Registry for versioning and deployment through the ML Ops pipeline.</p>
                </div>
                
                <div class="p-4 border-l-4 border-purple-500 bg-dark-800 rounded-r-lg">
                  <h5 class="font-bold mb-1">Document Findings</h5>
                  <p class="text-sm text-gray-300">Record key insights in the Model Documentation section to communicate your approach, findings, and recommendations to stakeholders.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Model Registry Tab -->
      <div v-if="activeTab === 'models'">
        <h2 class="text-2xl font-bold mb-4">Model Registry</h2>
        <p class="mb-6">Version, manage, and deploy machine learning models across your organization.</p>
        
        <div class="overflow-x-auto mb-8">
          <table class="min-w-full divide-y divide-dark-700">
            <thead>
              <tr>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Model Name</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Platform</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Version</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Stage</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Description</th>
                <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-dark-700">
              <tr v-for="(model, index) in models" :key="index" class="hover:bg-dark-800 transition-colors">
                <td class="px-4 py-3 whitespace-nowrap font-medium">{{ model.name }}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="`text-${platformColors[model.platform]}-400`">{{ model.platform }}</span>
                </td>
                <td class="px-4 py-3 whitespace-nowrap">{{ model.version }}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${stageColors[model.stage]}-900 text-${stageColors[model.stage]}-300`">
                    {{ model.stage }}
                  </span>
                </td>
                <td class="px-4 py-3 text-gray-300 max-w-md truncate">{{ model.description }}</td>
                <td class="px-4 py-3 whitespace-nowrap">
                  <div class="flex space-x-2">
                    <button class="btn-secondary py-1 px-2 text-xs">Deploy</button>
                    <button class="btn-secondary py-1 px-2 text-xs">Documents</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Documentation Tab -->
      <div v-if="activeTab === 'documentation'">
        <ModelDocumentation />
      </div>
      
      <!-- Integration Tab -->
      <div v-if="activeTab === 'integration'">
        <PlatformIntegration :integrations="integrationData" />
      </div>
    </div>
    
    <!-- Detail Cards for MLOps Steps -->
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'infrastructure'"
      :show="activeDetailCard === 'infrastructure'"
      :step-number="1"
      step-id="infrastructure"
      title="Infrastructure Setup"
      description="Configure compute resources, storage, and networking to support your ML workflow. This example demonstrates setting up Snowflake and compute resources using Airflow."
      :example-description="'This Airflow DAG initializes the required Snowflake compute resources and warehouse configurations needed for K-means clustering. It provisions the necessary compute resources, sets up storage integration, and configures network access.'"
      :code-example="infrastructureCode"
      :notes="[infrastructureNotes]"
      @close="activeDetailCard = null"
    />
    
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'data-pipeline'"
      :show="activeDetailCard === 'data-pipeline'"
      :step-number="2"
      step-id="data-pipeline"
      title="Data Pipeline"
      description="Build robust data pipelines for data ingestion, preprocessing, and feature engineering to prepare data for K-means clustering in Snowflake."
      :example-description="'This Airflow DAG handles data ingestion into Snowflake, performs data cleaning, and creates feature engineering transformations for K-means clustering. It includes steps for data validation, transformation, and feature store management.'"
      :code-example="dataPipelineCode"
      :notes="[dataPipelineNotes]"
      @close="activeDetailCard = null"
    />
    
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'model-development'"
      :show="activeDetailCard === 'model-development'"
      :step-number="3"
      step-id="model-development"
      title="Model Development"
      description="Develop, train, and evaluate K-means clustering models in Snowflake ML, with experiment tracking for hyperparameter tuning and model selection."
      :example-description="'This Airflow DAG orchestrates the training of K-means clustering models in Snowflake ML. It includes hyperparameter tuning, model training, and evaluation tasks.'"
      :code-example="modelDevelopmentCode"
      :notes="[modelDevelopmentNotes]"
      @close="activeDetailCard = null"
    />
    
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'cicd'"
      :show="activeDetailCard === 'cicd'"
      :step-number="4"
      step-id="cicd"
      title="CI/CD Pipeline"
      description="Implement continuous integration and deployment pipelines to automate testing, validation, and deployment of K-means models to production."
      :example-description="'This Airflow DAG handles the CI/CD process for K-means models in Snowflake. It runs tests, validates model performance, and manages the deployment to different environments.'"
      :code-example="cicdCode"
      :notes="[cicdNotes]"
      @close="activeDetailCard = null"
    />
    
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'monitoring'"
      :show="activeDetailCard === 'monitoring'"
      :step-number="5"
      step-id="monitoring"
      title="Monitoring"
      description="Set up monitoring systems to track performance, detect data drift, and ensure reliable operation of production K-means models."
      :example-description="'This Airflow DAG implements monitoring for K-means clustering models in production. It collects performance metrics, checks for data drift, and triggers alerts if issues are detected.'"
      :code-example="monitoringCode"
      :notes="[monitoringNotes]"
      @close="activeDetailCard = null"
    />
    
    <MLOpsDetailCard 
      v-if="activeDetailCard === 'governance'"
      :show="activeDetailCard === 'governance'"
      :step-number="6"
      step-id="governance"
      title="Governance"
      description="Establish model governance practices including documentation, audit trails, and access controls for K-means models in Snowflake."
      :example-description="'This Airflow DAG implements governance processes for K-means models. It handles model documentation, lineage tracking, and access control management.'"
      :code-example="governanceCode"
      :notes="[governanceNotes]"
      @close="activeDetailCard = null"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SummaryCard from '../components/SummaryCard.vue';
import TabNavigation from '../components/TabNavigation.vue';
import ExperimentsList from '../components/ExperimentsList.vue';
import TimeSeriesChart from '../components/TimeSeriesChart.vue';
import ModelDocumentation from '../components/ModelDocumentation.vue';
import PlatformIntegration from '../components/PlatformIntegration.vue';
import MLOpsDetailCard from '../components/MLOpsDetailCard.vue';
import MLOpsGuide from '../components/MLOpsGuide.vue';
import ImplementationNotes from '../components/ImplementationNotes.vue';
import { 
  infrastructureCode, dataPipelineCode, modelDevelopmentCode, 
  cicdCode, monitoringCode, governanceCode,
  infrastructureNotes, dataPipelineNotes, modelDevelopmentNotes,
  cicdNotes, monitoringNotes, governanceNotes
} from '../components/CodeExamples.vue';
import MLOpsSteps from '../components/MLOpsSteps.vue';
import KMeansJourney from '../components/KMeansJourney.vue';

// Active tab state
const activeTab = ref('models');
const experimentGuideOpen = ref(false);
const experimentViewMode = ref('snapshot');
const selectedTimeseriesMetric = ref('silhouette');
const timeseriesRange = ref('30d');
const showTimeSeriesInfo = ref(false);
const showPerformanceInfo = ref(false);
const newExperimentModalOpen = ref(false);
const activeDetailCard = ref(null);

// Function to show the detail card
const showDetailCard = (cardId) => {
  activeDetailCard.value = cardId;
};

// Tab definitions
const tabs = [
  { id: 'models', name: 'Model Registry' },
  { id: 'experiments', name: 'Experiments' },
  { id: 'documentation', name: 'Model Documentation' },
  { id: 'integration', name: 'Integrations' }
];

// Mock data
const platformColors = {
  'Snowflake': 'blue',
  'Azure': 'cyan',
  'MLflow': 'indigo',
  'HuggingFace': 'yellow',
  'OpenAI': 'green'
};

const statusColors = {
  'Running': 'green',
  'Completed': 'blue',
  'Failed': 'red',
  'Stopped': 'gray',
  'Pending': 'yellow',
  'Production': 'emerald',
  'Staging': 'amber',
  'Development': 'blue'
};

const stageColors = {
  'Production': 'green',
  'Staging': 'yellow',
  'Development': 'blue',
  'Archived': 'gray'
};

// Experiment data
const experiments = [
  { name: 'Intent Scoring Model 1', platform: 'Snowflake', modelType: 'K-means', status: 'Completed', created: '2025-10-24', metrics: 'Silhouette: 0.68' },
  { name: 'Intent Scoring Model 2', platform: 'Snowflake', modelType: 'K-means', status: 'Running', created: '2025-10-23', metrics: 'Silhouette: 0.72' },
  { name: 'Intent Scoring Model 3', platform: 'Snowflake', modelType: 'K-means', status: 'Completed', created: '2025-10-20', metrics: 'Silhouette: 0.71' },
  { name: 'Intent Scoring Model 4', platform: 'Snowflake', modelType: 'K-means++', status: 'Failed', created: '2025-10-18', metrics: 'Silhouette: N/A' },
  { name: 'Fit Scoring Model 1', platform: 'Snowflake', modelType: 'K-means++', status: 'Failed', created: '2025-10-18', metrics: 'Silhouette: N/A' },
  { name: 'Fit Scoring Model 2', platform: 'Snowflake', modelType: 'K-means++', status: 'Failed', created: '2025-10-18', metrics: 'Silhouette: N/A' },
  { name: 'Fit Scoring Model 3', platform: 'Snowflake', modelType: 'K-means++', status: 'Failed', created: '2025-10-18', metrics: 'Silhouette: N/A' },
  { name: 'Fit Scoring Model 4', platform: 'Snowflake', modelType: 'K-means++', status: 'Failed', created: '2025-10-18', metrics: 'Silhouette: N/A' }
];

// Model registry data
const models = [
  { name: 'intent-model1', platform: 'Snowflake', version: '1.0', stage: 'Production', description: 'Customer intent scoring model using K-means (first version)' },
  { name: 'intent-model2', platform: 'Snowflake', version: '1.0', stage: 'Staging', description: 'Intent scoring model with improved clustering features' },
  { name: 'intent-model3', platform: 'Snowflake', version: '1.0', stage: 'Development', description: 'Intent model with enhanced feature extraction' },
  { name: 'intent-model4', platform: 'Snowflake', version: '1.0', stage: 'Development', description: 'Intent model with enhanced feature extraction' },
  { name: 'fit-model1', platform: 'Snowflake', version: '1.0', stage: 'Production', description: 'Clothing fit prediction model for size recommendations' },
  { name: 'fit-model2', platform: 'Snowflake', version: '1.0', stage: 'Staging', description: 'Updated fit prediction with returns data integration' },
  { name: 'fit-model3', platform: 'Snowflake', version: '1.0', stage: 'Development', description: 'Advanced fit model with body measurement data' },
  { name: 'fit-model4', platform: 'Snowflake', version: '1.0', stage: 'Development', description: 'Advanced fit model with body measurement data' }
];

// Integration data
const integrationData = [
  {
    name: 'Snowflake ML',
    description: 'Integrate with Snowflake for ML model training, deployment, and inference.',
    status: {
      value: 'connected',
      label: 'Connected',
      color: 'green'
    }
  },
  {
    name: 'Azure AI',
    description: 'Leverage Azure AI services for model training, deployment, and management.',
    status: {
      value: 'connected',
      label: 'Connected',
      color: 'green'
    }
  },
  {
    name: 'MLflow',
    description: 'Connect with MLflow for experiment tracking and model registry.',
    status: {
      value: 'partial',
      label: 'Partial Connection',
      color: 'yellow'
    }
  },
  {
    name: 'HuggingFace',
    description: 'Access HuggingFace models and APIs for GenAI applications.',
    status: {
      value: 'not-connected',
      label: 'Not Connected',
      color: 'red'
    }
  }
];
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.btn-primary {
  @apply bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors;
}

.btn-secondary {
  @apply bg-dark-700 hover:bg-dark-600 text-white rounded-md transition-colors;
}
</style>