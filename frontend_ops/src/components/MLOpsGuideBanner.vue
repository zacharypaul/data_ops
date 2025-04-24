<template>
  <div class="mb-8 border border-dark-600 rounded-lg overflow-hidden">
    <!-- Guide Header - Clickable to expand/collapse -->
    <div 
      class="p-4 flex justify-between items-center cursor-pointer bg-dark-700 hover:bg-dark-600 transition-colors"
      @click="toggleGuide"
    >
      <div class="flex items-center">
        <div class="bg-primary-600 w-8 h-8 rounded-full flex items-center justify-center mr-3">
          <i class="fas fa-lightbulb text-dark-900"></i>
        </div>
        <h3 class="text-lg font-semibold">MLOps Quick Guide</h3>
      </div>
      <div class="text-gray-300">
        <i :class="[isExpanded ? 'fas fa-chevron-up' : 'fas fa-chevron-down']"></i>
      </div>
    </div>
    
    <!-- Guide Content - Expanded when isExpanded is true -->
    <div 
      v-if="isExpanded"
      class="p-4 border-t border-dark-600 bg-dark-800"
    >
      <div class="mb-4">
        <h4 class="font-semibold mb-2">What is MLOps?</h4>
        <p class="text-sm text-gray-300">
          MLOps (Machine Learning Operations) combines ML, DevOps, and data engineering practices to streamline and automate ML lifecycle management. 
          It bridges the gap between development and operational systems, focusing on automation, monitoring, and governance.
        </p>
      </div>
      
      <div class="mb-4">
        <h4 class="font-semibold mb-2">Key Benefits</h4>
        <ul class="list-disc pl-5 text-sm text-gray-300 space-y-1">
          <li>Reduced time to production for ML models</li>
          <li>Improved model quality and reliability</li>
          <li>Better governance and compliance</li>
          <li>Increased collaboration between data scientists and operations</li>
          <li>Scalable ML infrastructure with reduced manual overhead</li>
        </ul>
      </div>
      
      <div>
        <h4 class="font-semibold mb-2">Implementation Approach</h4>
        <p class="text-sm text-gray-300 mb-2">
          Follow an incremental approach based on your organization's maturity:
        </p>
        <div class="relative h-16 bg-dark-700 rounded-lg mb-2">
          <div class="absolute inset-0 flex">
            <div class="w-1/3 h-full bg-green-800 bg-opacity-40 rounded-l-lg flex items-center justify-center text-xs text-gray-200 font-medium">Beginning</div>
            <div class="w-1/3 h-full bg-blue-800 bg-opacity-40 flex items-center justify-center text-xs text-gray-200 font-medium">Intermediate</div>
            <div class="w-1/3 h-full bg-purple-800 bg-opacity-40 rounded-r-lg flex items-center justify-center text-xs text-gray-200 font-medium">Advanced</div>
          </div>
        </div>
        <p class="text-xs text-gray-400">
          Start with manual processes and gradually automate. The components below outline the key areas of an MLOps stack, which you can implement incrementally based on your needs.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const isExpanded = ref(false);

function toggleGuide() {
  isExpanded.value = !isExpanded.value;
}
</script>

<style scoped>
</style> 