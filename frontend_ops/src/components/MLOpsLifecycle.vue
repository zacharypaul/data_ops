<template>
  <div class="mlops-lifecycle">
    <h3 class="text-xl font-semibold mb-6 text-primary-300">MLOps Lifecycle Management</h3>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Model Development -->
      <div class="p-5 bg-dark-800 rounded-lg border border-dark-600">
        <h4 class="text-lg font-semibold text-primary-300 mb-3">
          <span class="inline-block mr-2 w-7 h-7 bg-primary-500 rounded-full text-center text-white">1</span>
          Model Development
        </h4>
        <ul class="space-y-2 ml-4">
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Experiment tracking &amp; versioning</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Data preprocessing pipelines</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Model training &amp; hyperparameter tuning</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Model evaluation &amp; validation</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Training infrastructure management</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Model registry &amp; artifact management</span>
          </li>
        </ul>
      </div>
      
      <!-- Model Deployment -->
      <div class="p-5 bg-dark-800 rounded-lg border border-dark-600">
        <h4 class="text-lg font-semibold text-primary-300 mb-3">
          <span class="inline-block mr-2 w-7 h-7 bg-primary-500 rounded-full text-center text-white">2</span>
          Model Deployment
        </h4>
        <ul class="space-y-2 ml-4">
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Model packaging &amp; containerization</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Serving infrastructure setup</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>CI/CD pipeline integration</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Canary &amp; blue-green deployments</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>A/B testing framework</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Model rollback mechanisms</span>
          </li>
        </ul>
      </div>
      
      <!-- Model Monitoring -->
      <div class="p-5 bg-dark-800 rounded-lg border border-dark-600">
        <h4 class="text-lg font-semibold text-primary-300 mb-3">
          <span class="inline-block mr-2 w-7 h-7 bg-primary-500 rounded-full text-center text-white">3</span>
          Model Monitoring
        </h4>
        <ul class="space-y-2 ml-4">
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Performance metrics tracking</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Data drift detection</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Concept drift monitoring</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Resource utilization tracking</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Alerting &amp; notification system</span>
          </li>
          <li class="flex items-start">
            <span class="text-primary-400 mr-2">•</span>
            <span>Automated retraining triggers</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional props or state needed for this component
</script>

<style scoped>
</style> 