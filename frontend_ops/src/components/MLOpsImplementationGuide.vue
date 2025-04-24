<template>
  <div class="bg-dark-800 border border-dark-600 rounded-lg p-6 mb-8">
    <div class="flex justify-between items-center cursor-pointer" @click="isExpanded = !isExpanded">
      <div class="flex items-center">
        <div class="bg-primary-600 w-10 h-10 rounded-full flex items-center justify-center mr-4">
          <i class="fas fa-map text-dark-900"></i>
        </div>
        <h2 class="text-xl font-bold">MLOps Implementation Guide</h2>
      </div>
      <i class="fas" :class="isExpanded ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
    </div>
    
    <div v-if="isExpanded" class="mt-6 space-y-6 text-gray-300">
      <div>
        <h3 class="text-lg font-semibold text-white mb-2">What is MLOps?</h3>
        <p>
          MLOps (Machine Learning Operations) is a set of practices that aims to deploy and maintain 
          machine learning models in production reliably and efficiently. It combines machine learning, 
          DevOps, and data engineering to create a systematic approach for building, deploying, and 
          monitoring ML systems.
        </p>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-white mb-2">Implementation Approach</h3>
        <p>The MLOps implementation process typically follows these steps:</p>
        <ol class="list-decimal pl-5 space-y-2 mt-2">
          <li>
            <span class="font-semibold text-white">Assessment</span>: Evaluate your current ML workflow, identify gaps, and prioritize improvements.
          </li>
          <li>
            <span class="font-semibold text-white">Infrastructure Setup</span>: Establish cloud resources, containerization, and development environments.
          </li>
          <li>
            <span class="font-semibold text-white">Data Pipeline</span>: Implement reproducible data processing with version control and quality validation.
          </li>
          <li>
            <span class="font-semibold text-white">Model Development</span>: Set up experiment tracking, version control, and reproducible training.
          </li>
          <li>
            <span class="font-semibold text-white">Deployment Automation</span>: Create CI/CD pipelines for testing and deploying models to production.
          </li>
          <li>
            <span class="font-semibold text-white">Monitoring</span>: Establish systems to track model performance, data drift, and system health.
          </li>
          <li>
            <span class="font-semibold text-white">Governance</span>: Implement documentation, access controls, and audit processes.
          </li>
        </ol>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-white mb-2">Key Best Practices</h3>
        <ul class="list-disc pl-5 space-y-2">
          <li>Automate repetitive tasks in the ML workflow</li>
          <li>Version control everything (code, data, models, environments)</li>
          <li>Build modular, reusable components</li>
          <li>Implement robust testing at all stages</li>
          <li>Monitor model performance and data drift continuously</li>
          <li>Document models, pipelines, and decisions</li>
          <li>Establish clear roles and responsibilities</li>
        </ul>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-white mb-2">Getting Started</h3>
        <p>
          To implement MLOps effectively, start with small, incremental improvements to your existing 
          workflow rather than attempting a complete overhaul at once. Begin by addressing the most 
          critical pain points in your current process, then gradually expand your MLOps implementation.
        </p>
        <p class="mt-3">
          Select components from the MLOps roadmap below to see detailed implementation notes and code examples.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isExpanded = ref(false);
</script> 