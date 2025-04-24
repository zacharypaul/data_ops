<template>
  <div class="mb-6">
    <h4 class="text-lg font-semibold mb-3 text-primary-300">Implementation Steps</h4>
    
    <div class="space-y-4">
      <!-- Step 1 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            1
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Infrastructure Setup</h5>
            <p class="text-sm mt-1">
              Establish cloud resources, containerization, and orchestration tools. Configure CI/CD pipelines for automated model deployment.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Step 2 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            2
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Data Pipeline Management</h5>
            <p class="text-sm mt-1">
              Implement data versioning, quality checks, and feature stores. Create reproducible ETL pipelines for consistent processing.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Step 3 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            3
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Model Training Workflows</h5>
            <p class="text-sm mt-1">
              Set up experiment tracking, hyperparameter optimization, and distributed training. Implement model validation practices with clear metrics.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Step 4 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            4
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Model Registry & Versioning</h5>
            <p class="text-sm mt-1">
              Create a central repository for model artifacts, metadata, and lineage tracking. Implement approval workflows for production candidates.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Step 5 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            5
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Deployment & Serving</h5>
            <p class="text-sm mt-1">
              Configure model serving infrastructure with appropriate scaling. Implement canary deployments, A/B testing, and rollback mechanisms.
            </p>
          </div>
        </div>
      </div>
      
      <!-- Step 6 -->
      <div class="p-4 bg-dark-800 rounded-lg border-l-4 border-primary-500">
        <div class="flex items-start">
          <div class="flex-shrink-0 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center mr-3">
            6
          </div>
          <div>
            <h5 class="font-semibold text-primary-200">Monitoring & Feedback</h5>
            <p class="text-sm mt-1">
              Implement monitoring for model performance, data drift, and system health. Create automated retraining triggers based on performance metrics.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No additional props or state needed for this component
</script>

<style scoped>
</style> 