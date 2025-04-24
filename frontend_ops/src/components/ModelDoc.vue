<template>
  <div class="glass-card p-5 border-l-4" :class="borderColorClass">
    <div class="flex justify-between items-start">
      <div>
        <h3 class="text-xl font-bold" :class="titleColorClass">{{ model.name }}</h3>
        <p class="text-gray-400 text-sm">{{ model.description }}</p>
      </div>
      <div class="flex items-center">
        <span :class="`${versionColorClass} text-sm mr-3`">Latest: v{{ model.version }}</span>
        <button @click="isExpanded = !isExpanded" class="text-gray-400 hover:text-white">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 transition-transform" :class="{'rotate-180': isExpanded}" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <div v-show="isExpanded" class="mt-4 space-y-6">
      <div>
        <h4 class="font-semibold mb-2" :class="sectionTitleClass">Description</h4>
        <p class="text-gray-300 text-sm">{{ model.longDescription }}</p>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-dark-800/50 p-3 rounded-lg">
          <h5 class="font-semibold text-gray-300 text-sm mb-1">Algorithm</h5>
          <p class="text-gray-400 text-sm">{{ model.algorithm }}</p>
        </div>
        <div class="bg-dark-800/50 p-3 rounded-lg">
          <h5 class="font-semibold text-gray-300 text-sm mb-1">Input Features</h5>
          <p class="text-gray-400 text-sm">{{ model.inputFeatures }}</p>
        </div>
        <div class="bg-dark-800/50 p-3 rounded-lg">
          <h5 class="font-semibold text-gray-300 text-sm mb-1">Output</h5>
          <p class="text-gray-400 text-sm">{{ model.output }}</p>
        </div>
      </div>
      
      <div>
        <h4 class="font-semibold mb-2" :class="sectionTitleClass">Implementation Details</h4>
        <div class="text-sm text-gray-300">
          <p class="mb-2">{{ model.implementationIntro }}</p>
          <ul class="list-disc pl-5 space-y-1 mb-4">
            <li v-for="(param, index) in model.parameters" :key="index">{{ param }}</li>
          </ul>
        </div>
      </div>
      
      <div>
        <h4 class="font-semibold mb-2" :class="sectionTitleClass">Key Characteristics</h4>
        <div class="text-sm text-gray-300">
          <p class="mb-2">{{ model.characteristicsDescription }}</p>
          <div class="bg-dark-900/50 p-4 rounded-lg mb-4">
            <ul class="list-disc pl-5 space-y-1">
              <li v-for="(feature, index) in model.characteristicsList" :key="index">{{ feature }}</li>
            </ul>
          </div>
        </div>
      </div>
      
      <div>
        <h4 class="font-semibold mb-2" :class="sectionTitleClass">Performance Metrics</h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div class="bg-dark-800/50 p-3 rounded-lg">
            <h5 class="font-semibold text-gray-300 text-sm mb-1">Inference Time</h5>
            <p class="text-gray-400 text-sm">{{ model.metrics.inferenceTime }}</p>
          </div>
          <div class="bg-dark-800/50 p-3 rounded-lg">
            <h5 class="font-semibold text-gray-300 text-sm mb-1">Accuracy</h5>
            <p class="text-gray-400 text-sm">{{ model.metrics.accuracy }}</p>
          </div>
          <div class="bg-dark-800/50 p-3 rounded-lg">
            <h5 class="font-semibold text-gray-300 text-sm mb-1">Memory Footprint</h5>
            <p class="text-gray-400 text-sm">{{ model.metrics.memoryFootprint }}</p>
          </div>
          <div class="bg-dark-800/50 p-3 rounded-lg">
            <h5 class="font-semibold text-gray-300 text-sm mb-1">Monitoring</h5>
            <p class="text-gray-400 text-sm">{{ model.metrics.monitoring }}</p>
          </div>
        </div>
      </div>
      
      <div class="flex space-x-3">
        <a href="#full-documentation" class="text-sm py-1.5 px-3 rounded hover:bg-opacity-80 flex items-center"
          :class="actionButtonClass">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
          </svg>
          Full Documentation
        </a>
        <a href="#edit" class="text-sm py-1.5 px-3 bg-dark-700 text-gray-300 rounded hover:bg-dark-600 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
          Edit
        </a>
        <a href="#history" class="text-sm py-1.5 px-3 bg-dark-700 text-gray-300 rounded hover:bg-dark-600 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
          Version History
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  model: {
    type: Object,
    required: true
  },
  type: {
    type: String,
    default: 'intent', // 'intent' or 'fit'
    validator: (value) => ['intent', 'fit'].includes(value)
  }
});

const isExpanded = ref(false);

// Computed color schemes based on model type
const borderColorClass = computed(() => {
  return props.type === 'intent' ? 'border-blue-500' : 'border-purple-500';
});

const titleColorClass = computed(() => {
  return props.type === 'intent' ? 'text-blue-300' : 'text-purple-300';
});

const versionColorClass = computed(() => {
  return props.type === 'intent' ? 'text-blue-400' : 'text-purple-400';
});

const sectionTitleClass = computed(() => {
  return props.type === 'intent' ? 'text-blue-200' : 'text-purple-200';
});

const actionButtonClass = computed(() => {
  return props.type === 'intent' 
    ? 'bg-blue-900/50 text-blue-300' 
    : 'bg-purple-900/50 text-purple-300';
});
</script> 