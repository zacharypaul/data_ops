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
    
    <div v-else-if="!chartData || chartData.length === 0" class="flex flex-col items-center justify-center h-64 text-center">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-gray-600 dark:text-gray-400">No anomaly data available for the selected time range</p>
    </div>
    
    <div v-else>
      <div class="mb-3 flex items-center justify-between">
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Showing anomalies detected across {{ uniqueTables.length }} tables
        </div>
        <div class="flex items-center space-x-1">
          <span class="inline-block w-3 h-3 bg-green-200 rounded"></span>
          <span class="text-xs text-gray-500 dark:text-gray-400 mr-2">Normal</span>
          <span class="inline-block w-3 h-3 bg-yellow-200 rounded"></span>
          <span class="text-xs text-gray-500 dark:text-gray-400 mr-2">Warning</span>
          <span class="inline-block w-3 h-3 bg-orange-300 rounded"></span>
          <span class="text-xs text-gray-500 dark:text-gray-400 mr-2">Moderate</span>
          <span class="inline-block w-3 h-3 bg-red-400 rounded"></span>
          <span class="text-xs text-gray-500 dark:text-gray-400">Severe</span>
        </div>
      </div>
      
      <div class="h-64 overflow-y-auto">
        <div class="heatmap-container" :style="{ gridTemplateColumns: `auto repeat(${dateLabels.length}, 1fr)` }">
          <!-- Header row with dates -->
          <div class="heatmap-header font-medium text-xs text-gray-500 dark:text-gray-400 p-1 sticky top-0 left-0 bg-white dark:bg-gray-800 z-10">Table</div>
          <div v-for="(date, index) in dateLabels" :key="`date-${index}`" 
               class="heatmap-header font-medium text-xs text-gray-500 dark:text-gray-400 p-1 text-center sticky top-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            {{ formatDate(date) }}
          </div>
          
          <!-- Data rows -->
          <template v-for="(table, tableIndex) in uniqueTables" :key="`table-${tableIndex}`">
            <div class="heatmap-row-header font-medium text-xs text-gray-600 dark:text-gray-300 p-1 sticky left-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
              {{ table }}
            </div>
            <div v-for="(date, dateIndex) in dateLabels" :key="`cell-${tableIndex}-${dateIndex}`"
                 class="heatmap-cell p-1 border border-gray-100 dark:border-gray-700"
                 :class="getCellClass(table, date)"
                 @mouseenter="showTooltip(getAnomalyData(table, date))"
                 @mouseleave="hideTooltip()">
            </div>
          </template>
        </div>
      </div>
      
      <!-- Tooltip -->
      <div v-if="tooltipVisible" 
           class="absolute bg-white dark:bg-gray-800 shadow-lg rounded p-2 text-sm border border-gray-200 dark:border-gray-700 z-20"
           :style="{ top: `${tooltipY}px`, left: `${tooltipX}px` }">
        <div v-if="tooltipData">
          <div class="font-medium">{{ tooltipData.table }}</div>
          <div class="text-xs text-gray-500 dark:text-gray-400">{{ formatDateFull(tooltipData.date) }}</div>
          <div class="mt-1 flex items-center">
            <span :class="tooltipData.anomalyColor" class="inline-block w-2 h-2 rounded-full mr-1"></span>
            <span>{{ tooltipData.anomalyText }}</span>
          </div>
          <div v-if="tooltipData.details" class="mt-1 text-xs">{{ tooltipData.details }}</div>
        </div>
        <div v-else class="text-gray-500 dark:text-gray-400">No anomalies detected</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Anomaly Detection Heatmap'
  },
  chartData: {
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
  }
});

const emit = defineEmits(['refresh']);

// Tooltip handling
const tooltipVisible = ref(false);
const tooltipX = ref(0);
const tooltipY = ref(0);
const tooltipData = ref(null);

// Extract unique tables and dates for heatmap grid
const uniqueTables = computed(() => {
  const tables = new Set(props.chartData.map(item => item.table));
  return Array.from(tables).sort();
});

const dateLabels = computed(() => {
  // Get unique dates
  const dates = new Set(props.chartData.map(item => item.date));
  return Array.from(dates).sort();
});

// Get cell background color based on anomaly severity
const getCellClass = (table, date) => {
  const item = props.chartData.find(item => item.table === table && item.date === date);
  
  if (!item) return 'bg-gray-50 dark:bg-gray-700';
  
  switch (item.anomalyLevel) {
    case 0: return 'bg-green-200 dark:bg-green-900';
    case 1: return 'bg-yellow-200 dark:bg-yellow-900';
    case 2: return 'bg-orange-300 dark:bg-orange-900';
    case 3: return 'bg-red-400 dark:bg-red-900';
    default: return 'bg-gray-50 dark:bg-gray-700';
  }
};

const getAnomalyData = (table, date) => {
  const item = props.chartData.find(item => item.table === table && item.date === date);
  
  if (!item) return null;
  
  let anomalyText = 'Normal';
  let anomalyColor = 'bg-green-500';
  
  switch (item.anomalyLevel) {
    case 0:
      anomalyText = 'Normal';
      anomalyColor = 'bg-green-500';
      break;
    case 1:
      anomalyText = 'Warning';
      anomalyColor = 'bg-yellow-500';
      break;
    case 2:
      anomalyText = 'Moderate Anomaly';
      anomalyColor = 'bg-orange-500';
      break;
    case 3:
      anomalyText = 'Severe Anomaly';
      anomalyColor = 'bg-red-500';
      break;
  }
  
  return {
    table,
    date,
    anomalyLevel: item.anomalyLevel,
    anomalyText,
    anomalyColor,
    details: item.details
  };
};

const showTooltip = (data) => {
  if (!data) return;
  
  tooltipData.value = data;
  tooltipVisible.value = true;
  
  // Position tooltip near mouse
  document.addEventListener('mousemove', updateTooltipPosition);
};

const updateTooltipPosition = (e) => {
  tooltipX.value = e.pageX + 10;
  tooltipY.value = e.pageY + 10;
};

const hideTooltip = () => {
  tooltipVisible.value = false;
  document.removeEventListener('mousemove', updateTooltipPosition);
};

const refreshData = () => {
  emit('refresh');
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
};

const formatDateFull = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
};

onMounted(() => {
  // Set up event listeners
});

onUnmounted(() => {
  document.removeEventListener('mousemove', updateTooltipPosition);
});
</script>

<style scoped>
.heatmap-container {
  display: grid;
  width: 100%;
}

.heatmap-header {
  font-size: 0.75rem;
  min-width: 80px;
}

.heatmap-row-header {
  font-size: 0.75rem;
  min-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.heatmap-cell {
  min-width: 24px;
  height: 24px;
  cursor: pointer;
  transition: transform 0.1s ease;
}

.heatmap-cell:hover {
  transform: scale(1.1);
  z-index: 10;
}
</style> 