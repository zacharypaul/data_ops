<template>
  <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4 h-full">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h3>
      <button 
        v-if="showControls"
        class="p-1 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700"
        @click="refreshData"
        :disabled="loading"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
    
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
    </div>
    
    <div v-else-if="error" class="flex flex-col items-center justify-center h-64 text-center">
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
    
    <div v-else-if="!timelineData || timelineData.length === 0" class="flex flex-col items-center justify-center h-64 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">No schema changes detected for the selected time range</p>
    </div>
    
    <div v-else>
      <div class="mb-4 flex flex-col sm:flex-row sm:items-center justify-between">
        <div class="text-sm text-gray-500 dark:text-gray-400 mb-2 sm:mb-0">
          <span class="font-medium">{{ timelineData.length }}</span> changes detected
        </div>
        <div class="flex space-x-4">
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-green-500 rounded-full"></div>
            <span class="text-xs text-gray-600 dark:text-gray-400">Added</span>
          </div>
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-red-500 rounded-full"></div>
            <span class="text-xs text-gray-600 dark:text-gray-400">Removed</span>
          </div>
          <div class="flex items-center space-x-1">
            <div class="w-3 h-3 bg-blue-500 rounded-full"></div>
            <span class="text-xs text-gray-600 dark:text-gray-400">Modified</span>
          </div>
        </div>
      </div>
      
      <div class="relative overflow-hidden">
        <div class="overflow-x-auto max-h-[450px] pb-4">
          <div class="timeline-wrapper">
            <!-- Timeline header -->
            <div class="grid grid-cols-[150px_1fr] mb-2">
              <div class="font-medium text-sm text-gray-700 dark:text-gray-300">Table</div>
              <div class="pl-6 relative">
                <div class="absolute left-0 top-1/2 w-full h-0.5 bg-gray-200 dark:bg-gray-700"></div>
                <div class="flex justify-between relative z-10">
                  <template v-for="(date, index) in timelineDates" :key="date">
                    <div 
                      class="px-2 py-1 bg-white dark:bg-gray-800 text-xs text-gray-600 dark:text-gray-400 rounded transform -rotate-45 origin-left"
                      :class="{'ml-auto': index === timelineDates.length - 1}"
                    >
                      {{ formatDate(date) }}
                    </div>
                  </template>
                </div>
              </div>
            </div>
            
            <!-- Timeline rows -->
            <div v-for="table in uniqueTables" :key="table" class="grid grid-cols-[150px_1fr] mb-6">
              <div class="pr-4 text-sm text-gray-800 dark:text-gray-200 font-medium truncate">
                {{ table }}
              </div>
              <div class="pl-6 relative">
                <!-- Timeline line -->
                <div class="absolute left-0 top-1/2 w-full h-0.5 bg-gray-200 dark:bg-gray-700"></div>
                
                <!-- Timeline events -->
                <div class="relative">
                  <div 
                    v-for="event in getTableEvents(table)" 
                    :key="`${event.id}-${event.timestamp}`"
                    class="absolute top-0 transform -translate-y-1/2"
                    :style="{ left: `${calculateEventPosition(event.timestamp)}%` }"
                    @mouseenter="activeEvent = event"
                    @mouseleave="activeEvent = null"
                  >
                    <div 
                      class="w-5 h-5 rounded-full flex items-center justify-center cursor-pointer z-10 relative"
                      :class="getEventColorClass(event.changeType)"
                    >
                      <span class="text-white text-xs font-bold">{{ event.changeType === 'added' ? '+' : (event.changeType === 'removed' ? '-' : 'M') }}</span>
                    </div>
                    
                    <!-- Tooltip -->
                    <div 
                      v-if="activeEvent === event"
                      class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 w-64 p-3 bg-white dark:bg-gray-700 rounded-lg shadow-lg z-20"
                    >
                      <div class="font-medium text-sm text-gray-800 dark:text-gray-200 mb-1">{{ formatTimestamp(event.timestamp) }}</div>
                      <div class="font-medium text-xs text-gray-600 dark:text-gray-400 mb-2">
                        <span class="px-2 py-0.5 rounded-full text-white text-xs"
                          :class="getEventColorClass(event.changeType)">
                          {{ formatChangeType(event.changeType) }}
                        </span>
                      </div>
                      <div v-if="event.field" class="mb-1">
                        <span class="text-xs text-gray-500 dark:text-gray-400">Field:</span>
                        <span class="text-xs font-medium text-gray-800 dark:text-gray-200 ml-1">{{ event.field }}</span>
                      </div>
                      <div v-if="event.dataType" class="mb-1">
                        <span class="text-xs text-gray-500 dark:text-gray-400">Type:</span>
                        <span class="text-xs font-medium text-gray-800 dark:text-gray-200 ml-1">{{ event.dataType }}</span>
                      </div>
                      <div v-if="event.oldValue" class="mb-1">
                        <span class="text-xs text-gray-500 dark:text-gray-400">From:</span>
                        <span class="text-xs font-medium text-gray-800 dark:text-gray-200 ml-1">{{ event.oldValue }}</span>
                      </div>
                      <div v-if="event.newValue" class="mb-1">
                        <span class="text-xs text-gray-500 dark:text-gray-400">To:</span>
                        <span class="text-xs font-medium text-gray-800 dark:text-gray-200 ml-1">{{ event.newValue }}</span>
                      </div>
                      <div v-if="event.description" class="text-xs text-gray-600 dark:text-gray-400 mt-2 border-t border-gray-200 dark:border-gray-600 pt-2">
                        {{ event.description }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
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
    default: 'Schema Change Timeline'
  },
  timelineData: {
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
  timeRange: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['refresh']);
const activeEvent = ref(null);

// Extract unique tables and dates from the timeline data
const uniqueTables = computed(() => {
  if (!props.timelineData || props.timelineData.length === 0) return [];
  
  const tables = new Set();
  props.timelineData.forEach(event => {
    tables.add(event.table);
  });
  
  return Array.from(tables).sort();
});

const timelineDates = computed(() => {
  if (!props.timelineData || props.timelineData.length === 0) return [];
  
  // Get min and max dates
  const timestamps = props.timelineData.map(event => new Date(event.timestamp).getTime());
  const minTime = Math.min(...timestamps);
  const maxTime = Math.max(...timestamps);
  
  // Create an array of evenly spaced dates between min and max
  const dateCount = 5; // Number of date labels to show
  const result = [];
  
  for (let i = 0; i < dateCount; i++) {
    const time = minTime + (i / (dateCount - 1)) * (maxTime - minTime);
    result.push(new Date(time));
  }
  
  return result;
});

const timeRangeStart = computed(() => {
  if (timelineDates.value.length === 0) return null;
  return timelineDates.value[0];
});

const timeRangeEnd = computed(() => {
  if (timelineDates.value.length === 0) return null;
  return timelineDates.value[timelineDates.value.length - 1];
});

// Helper methods
const getTableEvents = (table) => {
  return props.timelineData.filter(event => event.table === table);
};

const calculateEventPosition = (timestamp) => {
  if (!timeRangeStart.value || !timeRangeEnd.value) return 0;
  
  const eventTime = new Date(timestamp).getTime();
  const startTime = timeRangeStart.value.getTime();
  const endTime = timeRangeEnd.value.getTime();
  
  const range = endTime - startTime;
  if (range === 0) return 50; // Default to middle if only one date
  
  return ((eventTime - startTime) / range) * 100;
};

const getEventColorClass = (changeType) => {
  switch (changeType.toLowerCase()) {
    case 'added':
      return 'bg-green-500';
    case 'removed':
      return 'bg-red-500';
    case 'modified':
      return 'bg-blue-500';
    default:
      return 'bg-gray-500';
  }
};

const formatDate = (date) => {
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
};

const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const formatChangeType = (changeType) => {
  switch (changeType.toLowerCase()) {
    case 'added':
      return 'Added';
    case 'removed':
      return 'Removed';
    case 'modified':
      return 'Modified';
    default:
      return changeType;
  }
};

const refreshData = () => {
  emit('refresh');
};

watch(() => props.timeRange, () => {
  // Reset active event when time range changes
  activeEvent.value = null;
}, { deep: true });
</script>

<style scoped>
.timeline-wrapper {
  min-width: 600px;
}
</style> 