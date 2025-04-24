<template>
  <div class="bg-dark-800 rounded-lg p-4 mb-6">
    <div 
      @click="isExpanded = !isExpanded" 
      class="flex justify-between items-center cursor-pointer"
    >
      <h2 class="text-xl font-bold text-blue-400">MLOps Implementation Guide</h2>
      <i :class="isExpanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" class="text-blue-400"></i>
    </div>
    
    <div v-if="isExpanded" class="mt-4 text-gray-300 space-y-4">
      <div>
        <h3 class="text-lg font-semibold text-blue-300 mb-2">What is MLOps?</h3>
        <p>MLOps is the practice of applying DevOps principles to machine learning systems. It aims to standardize and streamline the lifecycle of ML models from development to deployment and monitoring, ensuring reliability, scalability, and maintainability.</p>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-blue-300 mb-2">Implementation Approach</h3>
        <p>Our implementation guide focuses on a phased approach to MLOps, starting with the essential components and gradually expanding to more advanced capabilities. This ensures you can begin with a minimal viable MLOps setup and scale as your needs grow.</p>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-blue-300 mb-2">Key Best Practices</h3>
        <ul class="list-disc pl-5 space-y-1">
          <li>Version control for code, data, and models</li>
          <li>Automated testing and validation</li>
          <li>Continuous integration and deployment</li>
          <li>Monitoring model performance in production</li>
          <li>Reproducible ML workflows</li>
          <li>Documentation and metadata management</li>
        </ul>
      </div>
      
      <div>
        <h3 class="text-lg font-semibold text-blue-300 mb-2">Getting Started</h3>
        <p>Follow the six-step implementation guide below to establish your MLOps practice. Each step builds on the previous one, providing a structured path to operationalizing your ML workflows.</p>
        <slot name="custom-content"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isExpanded = ref(false);
</script>

<style scoped>
</style> 