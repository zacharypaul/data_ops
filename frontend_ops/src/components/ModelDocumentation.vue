<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Model Documentation</h2>
    <p class="mb-6">Comprehensive documentation for all machine learning models, including methodologies, parameters, and implementation details.</p>
    
    <div class="flex justify-between items-center mb-4">
      <div class="relative">
        <input
          type="text"
          placeholder="Search documentation..."
          class="pl-10 pr-4 py-2 bg-dark-800 border border-dark-600 rounded-lg w-64 focus:outline-none focus:ring-1 focus:ring-primary-500 text-white"
          v-model="searchQuery"
        />
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400 absolute left-3 top-2.5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
        </svg>
      </div>
      <button class="btn-primary py-1.5 px-3">Add Documentation</button>
    </div>
    
    <div class="grid grid-cols-1 gap-6">
      <!-- Intent Models -->
      <ModelDoc 
        v-for="model in filteredIntentModels" 
        :key="model.id" 
        :model="model" 
        type="intent" 
      />
      
      <!-- Fit Models -->
      <ModelDoc 
        v-for="model in filteredFitModels" 
        :key="model.id" 
        :model="model" 
        type="fit" 
      />
    </div>
    
    <!-- Pagination -->
    <div class="flex justify-center mt-6">
      <button class="px-3 py-1 bg-dark-800 rounded-l-md border border-dark-600 text-gray-400 hover:bg-dark-700">
        &laquo;
      </button>
      <button class="px-3 py-1 bg-primary-900 border-t border-b border-dark-600 text-white">
        1
      </button>
      <button class="px-3 py-1 bg-dark-800 border-t border-b border-dark-600 text-gray-400 hover:bg-dark-700">
        2
      </button>
      <button class="px-3 py-1 bg-dark-800 rounded-r-md border border-dark-600 text-gray-400 hover:bg-dark-700">
        &raquo;
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import ModelDoc from './ModelDoc.vue';

const searchQuery = ref('');

// Intent Models Data
const intentModels = [
  {
    id: 'intent-model-1',
    name: 'Intent Clustering Model 1',
    version: '1.0',
    description: 'Basic K-means clustering model for user intent classification',
    longDescription: 'The first version of our intent clustering model uses basic K-means to identify user intent patterns. This model established our baseline for customer segmentation and provided initial insights into purchase intent patterns.',
    algorithm: 'K-means clustering',
    inputFeatures: '8 behavioral features',
    output: '3 distinct clusters',
    implementationIntro: 'The model is implemented in Snowflake ML using the K-means algorithm with the following parameters:',
    parameters: [
      'Number of clusters: 3',
      'Initialization method: random',
      'Maximum iterations: 100',
      'Convergence tolerance: 1e-3',
      'Random seed: 42'
    ],
    characteristicsDescription: 'This model identifies the following key features:',
    characteristicsList: [
      'Session duration: Time spent on site (seconds)',
      'Page views: Number of pages viewed per session',
      'Product detail views: Number of product pages viewed',
      'Search count: Number of searches performed',
      'Cart additions: Items added to cart',
      'Wishlist adds: Items added to wishlist',
      'Time on product pages: Time spent on product pages (seconds)',
      'Return visitor: Boolean (0/1) indicating returning visitor'
    ],
    metrics: {
      inferenceTime: 'Average: 32ms per user',
      accuracy: 'Silhouette score: 0.58',
      memoryFootprint: '3.5MB',
      monitoring: 'Weekly check, 5% threshold'
    }
  },
  {
    id: 'intent-model-2',
    name: 'Intent Clustering Model 2',
    version: '2.0',
    description: 'Enhanced K-means++ model with improved feature selection',
    longDescription: 'The second iteration of our intent model uses K-means++ initialization and adds four new behavioral features. It provides better cluster separation and more actionable user segments for marketing campaigns.',
    algorithm: 'K-means++ clustering',
    inputFeatures: '12 behavioral features',
    output: '4 distinct clusters',
    implementationIntro: 'The model is implemented in Snowflake ML using the K-means algorithm with the following parameters:',
    parameters: [
      'Number of clusters: 4',
      'Initialization method: k-means++',
      'Maximum iterations: 300',
      'Convergence tolerance: 1e-4',
      'Random seed: 42'
    ],
    characteristicsDescription: 'This model identifies the following key features:',
    characteristicsList: [
      'Session duration: Time spent on site (seconds)',
      'Page views: Number of pages viewed per session',
      'Product detail views: Number of product pages viewed',
      'Search count: Number of searches performed',
      'Filter usage: Number of filters applied',
      'Cart additions: Items added to cart',
      'Cart removals: Items removed from cart',
      'Wishlist adds: Items added to wishlist',
      'Comparison views: Number of comparison pages viewed',
      'Review reads: Number of product reviews read',
      'Time on product pages: Time spent on product pages (seconds)',
      'Return visitor: Boolean (0/1) indicating returning visitor'
    ],
    metrics: {
      inferenceTime: 'Average: 45ms per user',
      accuracy: 'Silhouette score: 0.72',
      memoryFootprint: '5.2MB',
      monitoring: 'Daily check, 2% threshold'
    }
  },
  {
    id: 'intent-model-3',
    name: 'Intent Clustering Model 3',
    version: '3.0',
    description: 'Advanced model with behavioral and demographic features',
    longDescription: 'The third version incorporates both behavioral and demographic data to create a more nuanced understanding of user intent. This model detects subtle patterns in browsing behavior and connects them to user demographics.',
    algorithm: 'K-means clustering with PCA preprocessing',
    inputFeatures: '18 behavioral & demographic features',
    output: '5 distinct clusters',
    implementationIntro: 'The model is implemented in Snowflake ML using the K-means algorithm with PCA preprocessing:',
    parameters: [
      'Number of clusters: 5',
      'Initialization method: k-means++',
      'Maximum iterations: 400',
      'Convergence tolerance: 1e-4',
      'PCA components: 12',
      'Random seed: 42'
    ],
    characteristicsDescription: 'This model builds on previous versions and adds:',
    characteristicsList: [
      'All 12 features from Intent Model 2',
      'Age group: Encoded categorical variable',
      'Device type: Encoded categorical variable',
      'Geographic region: Encoded categorical variable',
      'Previous purchase count: Numerical count',
      'Account age: Days since registration',
      'Engagement score: Composite metric of interaction'
    ],
    metrics: {
      inferenceTime: 'Average: 68ms per user',
      accuracy: 'Silhouette score: 0.76',
      memoryFootprint: '8.3MB',
      monitoring: 'Daily check, 1.5% threshold'
    }
  },
  {
    id: 'intent-model-4',
    name: 'Intent Clustering Model 4',
    version: '4.0',
    description: 'Real-time intent prediction with sequential behavioral analysis',
    longDescription: 'Our most advanced intent model incorporates sequential behavior analysis to predict user intent in real-time. This model can detect changes in intent during a single session and adjust predictions accordingly.',
    algorithm: 'DBSCAN with RNN-based feature extraction',
    inputFeatures: '24 features including sequential patterns',
    output: '6 intent clusters with confidence scores',
    implementationIntro: 'The model combines DBSCAN clustering with recurrent neural network features:',
    parameters: [
      'Epsilon (neighborhood size): 0.4',
      'Min samples: 8',
      'RNN layers: 3',
      'Hidden units: 128',
      'Sequence length: 15 actions',
      'Training epochs: 50'
    ],
    characteristicsDescription: 'This model introduces novel sequential features:',
    characteristicsList: [
      'Click sequence patterns: Encoded user navigation flows',
      'Time between actions: Distribution of inter-action times',
      'Session progression features: Early vs. late session behavior',
      'Category transition matrix: How users move between product categories',
      'Repeat view patterns: Which items users return to',
      'Hover-to-click ratio: Mouse behavior metrics',
      'Plus all features from Intent Model 3'
    ],
    metrics: {
      inferenceTime: 'Average: 120ms per user',
      accuracy: 'Silhouette score: 0.83',
      memoryFootprint: '15.7MB',
      monitoring: 'Real-time drift detection'
    }
  }
];

// Fit Models Data
const fitModels = [
  {
    id: 'fit-model-1',
    name: 'Fit Clustering Model 1',
    version: '1.0',
    description: 'Basic clustering for apparel size preferences',
    longDescription: 'Our initial fit prediction model focuses on identifying basic size preference patterns across different apparel categories. It helps establish baseline size recommendations for new customers.',
    algorithm: 'K-means clustering',
    inputFeatures: '6 customer fit attributes',
    output: '3 fit preference clusters',
    implementationIntro: 'The model is implemented in Azure ML using the K-means algorithm with the following parameters:',
    parameters: [
      'Number of clusters: 3',
      'Initialization method: random',
      'Maximum iterations: 100',
      'Convergence tolerance: 1e-3',
      'Random seed: 42'
    ],
    characteristicsDescription: 'The model uses these primary features:',
    characteristicsList: [
      'Size deviation: Preferred size vs. standard size chart',
      'Return rate: Overall return frequency',
      'Purchase history: Categories and sizes bought',
      'Body type: Self-reported body shape (categorical)',
      'Fit preference: Self-reported fit preference (tight, regular, loose)',
      'Age group: Age range in 10-year intervals'
    ],
    metrics: {
      inferenceTime: 'Average: 28ms per recommendation',
      accuracy: 'Correct size rate: 68%',
      memoryFootprint: '2.8MB',
      monitoring: 'Weekly evaluation'
    }
  },
  {
    id: 'fit-model-2',
    name: 'Fit Clustering Model 2',
    version: '2.0',
    description: 'DBSCAN model for apparel fit preferences with return data',
    longDescription: 'The second version of our fit model uses DBSCAN to identify more natural groupings in customer fit preferences. It incorporates detailed return reason data to better understand fit issues.',
    algorithm: 'DBSCAN clustering',
    inputFeatures: '15 customer fit attributes',
    output: '5 fit preference clusters',
    implementationIntro: 'The model is implemented in Azure ML using the DBSCAN algorithm with the following parameters:',
    parameters: [
      'Epsilon (neighborhood size): 0.5',
      'Min samples (core point threshold): 5',
      'Distance metric: Euclidean',
      'Algorithm: auto (selects best between ball_tree, kd_tree, and brute-force)',
      'Leaf size: 30'
    ],
    characteristicsDescription: 'This model expands on version 1 with return-specific features:',
    characteristicsList: [
      'Size deviation: Preferred size vs. standard size chart',
      'Return rate fit issues: Return frequency due to fit',
      'Fit feedback scores: Average rating from fit surveys',
      'Body measurements: Self-reported measurements (normalized)',
      'Preferred brands: Encoded brand preference features',
      'Return reasons: Detailed categorization of fit-related returns',
      'Size consistency: Consistency in size selection across categories',
      'Material preferences: Fabric stretch preferences from purchase history',
      'Style preferences: Cut and style preferences from purchase history'
    ],
    metrics: {
      inferenceTime: 'Average: 42ms per recommendation',
      accuracy: 'Correct size rate: 78%',
      memoryFootprint: '4.5MB',
      monitoring: 'Daily evaluation'
    }
  },
  {
    id: 'fit-model-3',
    name: 'Fit Clustering Model 3',
    version: '3.0',
    description: 'Advanced fit model with body measurement integration',
    longDescription: 'The third iteration integrates detailed body measurement data with extensive purchase and return history to create a high-precision fit recommendation system, especially effective for new products.',
    algorithm: 'Gaussian Mixture Model (GMM)',
    inputFeatures: '22 customer fit and measurement attributes',
    output: '8 fit preference clusters with probability scores',
    implementationIntro: 'The model uses a Gaussian Mixture Model with the following configuration:',
    parameters: [
      'Number of components: 8',
      'Covariance type: full',
      'Maximum iterations: 200',
      'Convergence threshold: 1e-5',
      'Initialization: k-means',
      'Warm start: True'
    ],
    characteristicsDescription: 'This model introduces precise body measurements:',
    characteristicsList: [
      'All features from Fit Model 2',
      'Detailed body measurements: 8 precise measurement points',
      'Body proportion ratios: Calculated proportions between measurements',
      'Garment-specific fit preferences: Category-specific fit choices',
      'Seasonal variation: Changes in size preference by season',
      'Brand size variation adjustment: Brand-specific size chart differences',
      'Product material properties: Elasticity, structure, and fabric behavior'
    ],
    metrics: {
      inferenceTime: 'Average: 65ms per recommendation',
      accuracy: 'Correct size rate: 87%',
      memoryFootprint: '9.2MB',
      monitoring: 'Continuous evaluation with daily reports'
    }
  },
  {
    id: 'fit-model-4',
    name: 'Fit Clustering Model 4',
    version: '4.0',
    description: 'Next-gen fit prediction with 3D body modeling',
    longDescription: 'Our most sophisticated fit model incorporates virtual try-on data and 3D body modeling to create an extremely accurate fit prediction system that can visualize how garments will fit different body types.',
    algorithm: 'Deep learning ensemble with 3D convolution',
    inputFeatures: '35+ features including 3D scan data',
    output: '12 precise fit clusters with garment-specific adjustments',
    implementationIntro: 'This advanced model uses a neural network ensemble:',
    parameters: [
      'CNN layers: 12 (for 3D feature extraction)',
      'Dense layers: 4',
      'Activation: Leaky ReLU',
      'Regularization: Dropout (0.25) and L2',
      'Learning rate: 0.0001 with decay',
      'Batch size: 64'
    ],
    characteristicsDescription: 'This model leverages cutting-edge 3D body modeling:',
    characteristicsList: [
      'Virtual try-on data: Simulated garment draping on customer body models',
      '3D body scan approximations: Generated from 2D images or previous purchases',
      'Dynamic fit prediction: How garments behave during movement',
      'Fabric physics simulation: Material properties and behavior modeled',
      'Style preference mapping: Personal style to fit correlation',
      'Trend-based adjustments: Accounting for fashion trend influences',
      'Cross-category fit consistency: Unified size recommendations across product types'
    ],
    metrics: {
      inferenceTime: 'Average: 180ms per recommendation',
      accuracy: 'Correct size rate: 94%',
      memoryFootprint: '22.5MB',
      monitoring: 'Real-time accuracy tracking with A/B testing'
    }
  }
];

// Filtered models based on search query
const filteredIntentModels = computed(() => {
  if (!searchQuery.value) return intentModels;
  const query = searchQuery.value.toLowerCase();
  return intentModels.filter(model => 
    model.name.toLowerCase().includes(query) || 
    model.description.toLowerCase().includes(query)
  );
});

const filteredFitModels = computed(() => {
  if (!searchQuery.value) return fitModels;
  const query = searchQuery.value.toLowerCase();
  return fitModels.filter(model => 
    model.name.toLowerCase().includes(query) || 
    model.description.toLowerCase().includes(query)
  );
});
</script> 