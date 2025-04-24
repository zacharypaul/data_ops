<template>
  <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4 h-full">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h3>
      <div class="flex items-center space-x-2" v-if="showControls">
        <button 
          class="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
          @click="refreshData"
          :disabled="loading"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="flex items-center justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="error" class="flex flex-col items-center justify-center py-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-red-500 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">{{ error }}</p>
      <button 
        @click="refreshData" 
        class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Try Again
      </button>
    </div>
    
    <div v-else-if="!testResults || testResults.length === 0" class="flex flex-col items-center justify-center py-8 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">No test results available for the selected time range</p>
    </div>
    
    <div v-else>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Table</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Test</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Timestamp</th>
              <th scope="col" class="px-3 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Details</th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="(result, index) in paginatedResults" :key="index" 
                :class="{'bg-gray-50 dark:bg-gray-700': index % 2 === 0}">
              <td class="px-3 py-2 whitespace-nowrap">
                <span v-if="result.status === 'passed'" 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  Passed
                </span>
                <span v-else-if="result.status === 'failed'" 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200">
                  Failed
                </span>
                <span v-else 
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200">
                  Warning
                </span>
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ result.table }}
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ result.test }}
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ formatDateTime(result.timestamp) }}
              </td>
              <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                <button @click="showTestDetails(result)" 
                        class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-300">
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div v-if="totalPages > 1" class="flex justify-between items-center mt-4 px-2">
        <div class="text-sm text-gray-700 dark:text-gray-300">
          Showing <span class="font-medium">{{ startIndex + 1 }}</span> to 
          <span class="font-medium">{{ Math.min(endIndex, testResults.length) }}</span> of 
          <span class="font-medium">{{ testResults.length }}</span> results
        </div>
        <div class="flex space-x-2">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            :class="{'opacity-50 cursor-not-allowed': currentPage === 1}"
            class="inline-flex items-center px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            Previous
          </button>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            :class="{'opacity-50 cursor-not-allowed': currentPage === totalPages}"
            class="inline-flex items-center px-2 py-1 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600"
          >
            Next
          </button>
        </div>
      </div>
    </div>
    
    <!-- Modal for test details -->
    <div v-if="selectedTest" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
        <div class="p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Test Details</h3>
          <button @click="selectedTest = null" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div class="p-4">
          <div class="mb-4">
            <div class="flex justify-between">
              <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Status</div>
              <div v-if="selectedTest.status === 'passed'" class="text-green-600 dark:text-green-400 font-medium">Passed</div>
              <div v-else-if="selectedTest.status === 'failed'" class="text-red-600 dark:text-red-400 font-medium">Failed</div>
              <div v-else class="text-yellow-600 dark:text-yellow-400 font-medium">Warning</div>
            </div>
          </div>
          <div class="mb-4">
            <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Table</div>
            <div class="mt-1 text-gray-900 dark:text-white">{{ selectedTest.table }}</div>
          </div>
          <div class="mb-4">
            <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Test</div>
            <div class="mt-1 text-gray-900 dark:text-white">{{ selectedTest.test }}</div>
          </div>
          <div class="mb-4">
            <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Timestamp</div>
            <div class="mt-1 text-gray-900 dark:text-white">{{ formatDateTime(selectedTest.timestamp) }}</div>
          </div>
          <div class="mb-4">
            <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Description</div>
            <div class="mt-1 text-gray-900 dark:text-white">{{ selectedTest.description || 'No description available' }}</div>
          </div>
          <div v-if="selectedTest.details">
            <div class="text-sm font-medium text-gray-500 dark:text-gray-400">Additional Details</div>
            <pre class="mt-1 p-2 bg-gray-100 dark:bg-gray-900 rounded overflow-x-auto text-xs text-gray-900 dark:text-white">{{ formatDetails(selectedTest.details) }}</pre>
          </div>
        </div>
        <div class="p-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
          <button @click="selectedTest = null" class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Recent Quality Test Results'
  },
  testResults: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: ''
  },
  showControls: {
    type: Boolean,
    default: true
  },
  itemsPerPage: {
    type: Number,
    default: 10
  }
});

const emit = defineEmits(['refresh']);
const selectedTest = ref(null);
const currentPage = ref(1);

// Reset pagination when testResults changes
watch(() => props.testResults, () => {
  currentPage.value = 1;
});

const totalPages = computed(() => {
  return Math.ceil(props.testResults.length / props.itemsPerPage);
});

const startIndex = computed(() => {
  return (currentPage.value - 1) * props.itemsPerPage;
});

const endIndex = computed(() => {
  return startIndex.value + props.itemsPerPage;
});

const paginatedResults = computed(() => {
  return props.testResults.slice(startIndex.value, endIndex.value);
});

const refreshData = () => {
  emit('refresh');
};

const showTestDetails = (test) => {
  selectedTest.value = test;
};

const formatDateTime = (timestamp) => {
  if (!timestamp) return 'N/A';
  
  const date = new Date(timestamp);
  return date.toLocaleString();
};

const formatDetails = (details) => {
  if (typeof details === 'string') {
    return details;
  }
  
  try {
    return JSON.stringify(details, null, 2);
  } catch (e) {
    return String(details);
  }
};
</script> 