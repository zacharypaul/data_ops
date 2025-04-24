<template>
  <div v-if="show" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 overflow-y-auto">
    <div class="bg-dark-800 rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-xl font-semibold text-primary-300 flex items-center">
            <div class="bg-primary-900 w-8 h-8 rounded-full flex items-center justify-center mr-3 text-primary-300 font-bold">{{ stepNumber }}</div>
            {{ title }}
          </h3>
          <button @click="$emit('close')" class="text-gray-400 hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <p class="mb-4 text-gray-300">{{ description }}</p>
        
        <div class="mb-6 p-4 bg-gradient-to-r from-primary-900/20 to-dark-900 border border-primary-700/30 rounded-lg">
          <h4 class="text-lg font-medium text-primary-300 mb-3">Snowflake ML K-means Example</h4>
          <p class="mb-3 text-gray-300">{{ exampleDescription }}</p>
        </div>
        
        <div class="bg-dark-900 rounded-lg overflow-hidden mb-6">
          <div class="flex justify-between items-center bg-dark-700 px-4 py-2">
            <div class="text-sm font-medium text-gray-300">Airflow DAG Example</div>
            <div class="flex space-x-2">
              <span class="text-xs text-gray-400">snowflake_kmeans_{{ stepId }}.py</span>
            </div>
          </div>
          <pre class="p-4 text-sm text-gray-300 overflow-x-auto"><code>{{ codeExample }}</code></pre>
        </div>
        
        <div v-if="notes" class="p-4 bg-dark-900 rounded-lg mb-4">
          <h4 class="font-medium text-primary-300 mb-2">Implementation Notes</h4>
          <ul class="list-disc list-inside space-y-2 text-sm text-gray-300">
            <li v-for="(note, index) in notes" :key="index">{{ note }}</li>
          </ul>
        </div>
        
        <div class="flex justify-end">
          <button @click="$emit('close')" class="bg-primary-600 hover:bg-primary-700 text-white py-2 px-4 rounded">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  stepNumber: {
    type: Number,
    required: true
  },
  stepId: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  exampleDescription: {
    type: String,
    required: true
  },
  codeExample: {
    type: String,
    required: true
  },
  notes: {
    type: Array,
    default: () => []
  }
});

defineEmits(['close']);
</script> 