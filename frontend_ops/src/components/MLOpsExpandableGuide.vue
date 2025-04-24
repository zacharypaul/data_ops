<template>
  <div class="bg-dark-800 rounded-lg border border-dark-600 overflow-hidden mb-8">
    <!-- Header -->
    <div 
      @click="isExpanded = !isExpanded"
      class="p-4 flex justify-between items-center cursor-pointer hover:bg-dark-700 transition-colors duration-200"
    >
      <div class="flex items-center">
        <i class="fas fa-book-open text-blue-500 mr-3 text-xl"></i>
        <h3 class="text-xl font-bold">MLOps Guide</h3>
      </div>
      <i 
        class="fas transition-transform duration-300" 
        :class="isExpanded ? 'fa-chevron-up' : 'fa-chevron-down'"
      ></i>
    </div>
    
    <!-- Content -->
    <div 
      v-show="isExpanded"
      class="p-5 border-t border-dark-600 transition-all duration-300"
    >
      <div class="space-y-6">
        <!-- What is MLOps -->
        <div>
          <h4 class="text-lg font-semibold text-blue-400 mb-3">What is MLOps?</h4>
          <p class="mb-4">
            MLOps (Machine Learning Operations) is a practice that combines Machine Learning, 
            DevOps, and Data Engineering to reliably and efficiently deploy and maintain ML systems in production. 
            It addresses the unique challenges in ML system deployment including reproducibility, 
            versioning, testing, and monitoring of models and data.
          </p>
        </div>
        
        <!-- Implementation Approach -->
        <div>
          <h4 class="text-lg font-semibold text-blue-400 mb-3">Implementation Approach</h4>
          <p class="mb-4">
            We recommend an incremental approach to MLOps adoption, starting with the foundation 
            and gradually adding more advanced capabilities. This phased approach allows teams to 
            realize value quickly while building toward a comprehensive MLOps practice.
          </p>
          <div class="bg-dark-700 rounded-lg p-4 mb-4">
            <h5 class="font-semibold mb-2">Three Levels of MLOps Maturity:</h5>
            <ol class="list-decimal pl-6 space-y-2">
              <li><strong>Level 0:</strong> Manual process with basic version control</li>
              <li><strong>Level 1:</strong> Automation of model deployment with CI/CD</li>
              <li><strong>Level 2:</strong> Automated retraining and monitoring with feedback loops</li>
            </ol>
          </div>
        </div>
        
        <!-- Best Practices -->
        <div>
          <h4 class="text-lg font-semibold text-blue-400 mb-3">Key Best Practices</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-dark-700 p-3 rounded-lg">
              <div class="flex items-start">
                <i class="fas fa-code-branch text-blue-500 mt-1 mr-2"></i>
                <div>
                  <h5 class="font-semibold">Version Everything</h5>
                  <p class="text-sm">Code, data, models, and configurations must be versioned</p>
                </div>
              </div>
            </div>
            <div class="bg-dark-700 p-3 rounded-lg">
              <div class="flex items-start">
                <i class="fas fa-vial text-blue-500 mt-1 mr-2"></i>
                <div>
                  <h5 class="font-semibold">Automate Testing</h5>
                  <p class="text-sm">Test code, data quality, and model performance</p>
                </div>
              </div>
            </div>
            <div class="bg-dark-700 p-3 rounded-lg">
              <div class="flex items-start">
                <i class="fas fa-terminal text-blue-500 mt-1 mr-2"></i>
                <div>
                  <h5 class="font-semibold">Infrastructure as Code</h5>
                  <p class="text-sm">Define all infrastructure and deployment configs as code</p>
                </div>
              </div>
            </div>
            <div class="bg-dark-700 p-3 rounded-lg">
              <div class="flex items-start">
                <i class="fas fa-chart-line text-blue-500 mt-1 mr-2"></i>
                <div>
                  <h5 class="font-semibold">Monitor Everything</h5>
                  <p class="text-sm">Track data, models, and infrastructure</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Getting Started -->
        <div>
          <h4 class="text-lg font-semibold text-blue-400 mb-3">Getting Started</h4>
          <p class="mb-4">
            Follow the six-step implementation process below to establish MLOps in your organization.
            Each step builds on the previous ones, creating a comprehensive MLOps practice.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isExpanded = ref(false);
</script> 