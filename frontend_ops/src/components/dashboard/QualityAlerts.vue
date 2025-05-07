<template>
  <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-display font-bold">Data Quality Alerts</h2>
      <div class="flex space-x-2">
        <button class="text-dark-300 hover:text-white transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
        </button>
        <button class="text-dark-300 hover:text-white transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 01.707.293l3 3a1 1 0 01-1.414 1.414L10 5.414 7.707 7.707a1 1 0 01-1.414-1.414l3-3A1 1 0 0110 3zm-3.707 9.293a1 1 0 011.414 0L10 14.586l2.293-2.293a1 1 0 011.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <div v-if="alerts.length === 0" class="text-center py-8 text-dark-300">
      No alerts at this time
    </div>

    <div v-else class="space-y-4">
      <div 
        v-for="alert in alerts" 
        :key="alert.id"
        :class="`p-4 rounded-md bg-${alert.type}-900/40 border border-${alert.type}-700 flex items-center`"
      >
        <div :class="`h-3 w-3 rounded-full bg-${alert.type}-500 mr-3`"></div>
        <div>
          <h4 class="font-medium text-white">{{ alert.title }}</h4>
          <p class="text-sm text-dark-300">{{ alert.description }}</p>
        </div>
        <div class="ml-auto flex items-center space-x-3">
          <span :class="`px-2 py-1 text-xs rounded-full bg-${alert.type}-900 text-${alert.type}-300`">{{ alert.severity }}</span>
          <button class="text-dark-300 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="alerts.length > 0" class="flex justify-between mt-4">
      <span class="text-sm text-dark-300">Showing {{ alerts.length }} alerts</span>
      <button class="text-primary-400 hover:text-primary-300 text-sm font-medium">View All Alerts</button>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  alerts: {
    type: Array,
    required: true
  }
});
</script> 