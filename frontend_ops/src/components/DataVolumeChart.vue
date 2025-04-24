<template>
  <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-4 h-full">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h3>
      <div class="flex items-center space-x-2" v-if="showControls">
        <div>
          <select 
            v-model="chartType" 
            class="block w-auto text-sm rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          >
            <option value="area">Area</option>
            <option value="bar">Bar</option>
            <option value="line">Line</option>
          </select>
        </div>
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
      <p class="text-gray-600 dark:text-gray-400">No data volume metrics available for the selected time range</p>
    </div>
    
    <div v-else>
      <div class="mb-4 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div class="text-sm font-medium text-gray-700 dark:text-gray-300">Growth rate:</div>
          <div v-if="growthRate > 0" class="text-sm text-green-600 dark:text-green-400 font-medium flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586l3.293-3.293A1 1 0 0114 7h-2z" clip-rule="evenodd" />
            </svg>
            {{ growthRate.toFixed(2) }}% from previous period
          </div>
          <div v-else-if="growthRate < 0" class="text-sm text-red-600 dark:text-red-400 font-medium flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 13a1 1 0 100 2h5a1 1 0 001-1v-5a1 1 0 10-2 0v2.586l-4.293-4.293a1 1 0 00-1.414 0L8 9.586 3.707 5.293a1 1 0 00-1.414 1.414l5 5a1 1 0 001.414 0L11 9.414l3.293 3.293A1 1 0 0014 13h-2z" clip-rule="evenodd" />
            </svg>
            {{ Math.abs(growthRate.toFixed(2)) }}% from previous period
          </div>
          <div v-else class="text-sm text-gray-600 dark:text-gray-400 font-medium">
            No change from previous period
          </div>
        </div>
        <div class="text-sm text-gray-500 dark:text-gray-400 flex items-center">
          <span class="font-medium">Total:</span>
          <span class="ml-1">{{ formatDataVolume(totalVolume) }}</span>
        </div>
      </div>
      
      <div class="h-64">
        <canvas ref="chartCanvas"></canvas>
      </div>
      
      <div class="mt-3 grid grid-cols-2 md:grid-cols-4 gap-2">
        <div v-for="(source, index) in sources" :key="index" class="flex items-center">
          <span 
            class="inline-block w-3 h-3 mr-2 rounded-full" 
            :style="{ backgroundColor: sourceColors[index % sourceColors.length] }"
          ></span>
          <span class="text-xs text-gray-700 dark:text-gray-300 truncate">{{ source }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  title: {
    type: String,
    default: 'Data Volume Trends'
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
  },
  unit: {
    type: String,
    default: 'rows'
  },
  timeRange: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['refresh']);
const chartCanvas = ref(null);
const chartType = ref('area');
let chart = null;

// Extract sources and dates
const sources = computed(() => {
  const sourcesSet = new Set(props.chartData.map(item => item.source));
  return Array.from(sourcesSet).sort();
});

const dateLabels = computed(() => {
  const uniqueDates = [...new Set(props.chartData.map(item => item.date))];
  return uniqueDates.sort();
});

// Chart colors
const sourceColors = [
  'rgba(59, 130, 246, 0.7)',  // Blue
  'rgba(16, 185, 129, 0.7)',  // Green
  'rgba(245, 158, 11, 0.7)',  // Yellow
  'rgba(239, 68, 68, 0.7)',   // Red
  'rgba(139, 92, 246, 0.7)',  // Purple
  'rgba(14, 165, 233, 0.7)',  // Sky
  'rgba(79, 70, 229, 0.7)',   // Indigo
  'rgba(236, 72, 153, 0.7)',  // Pink
];

// Calculate growth rate
const growthRate = computed(() => {
  if (!props.chartData || props.chartData.length === 0) return 0;
  
  // Group by date and calculate total for each date
  const dateGroups = {};
  
  props.chartData.forEach(item => {
    if (!dateGroups[item.date]) {
      dateGroups[item.date] = 0;
    }
    dateGroups[item.date] += item.value;
  });
  
  const sortedDates = Object.keys(dateGroups).sort();
  
  if (sortedDates.length < 2) return 0;
  
  const currentValue = dateGroups[sortedDates[sortedDates.length - 1]];
  const previousValue = dateGroups[sortedDates[sortedDates.length - 2]];
  
  if (previousValue === 0) return 0;
  
  return ((currentValue - previousValue) / previousValue) * 100;
});

// Calculate total volume
const totalVolume = computed(() => {
  if (!props.chartData || props.chartData.length === 0) return 0;
  
  // Sum values for the most recent date
  const sortedDates = [...new Set(props.chartData.map(item => item.date))].sort();
  const mostRecentDate = sortedDates[sortedDates.length - 1];
  
  return props.chartData
    .filter(item => item.date === mostRecentDate)
    .reduce((total, item) => total + item.value, 0);
});

const formatDataVolume = (value) => {
  if (value >= 1_000_000_000) {
    return `${(value / 1_000_000_000).toFixed(2)}B ${props.unit}`;
  } else if (value >= 1_000_000) {
    return `${(value / 1_000_000).toFixed(2)}M ${props.unit}`;
  } else if (value >= 1_000) {
    return `${(value / 1_000).toFixed(2)}K ${props.unit}`;
  }
  return `${value} ${props.unit}`;
};

const createChart = () => {
  if (!chartCanvas.value || !props.chartData || props.chartData.length === 0) return;
  
  const ctx = chartCanvas.value.getContext('2d');
  
  if (chart) {
    chart.destroy();
  }
  
  // Prepare data for chart
  const datasets = sources.value.map((source, index) => {
    const sourceData = props.chartData.filter(item => item.source === source);
    
    // Create a map of date -> value for this source
    const dataMap = {};
    sourceData.forEach(item => {
      dataMap[item.date] = item.value;
    });
    
    // Create an array of values ordered by date
    const dataPoints = dateLabels.value.map(date => dataMap[date] || 0);
    
    return {
      label: source,
      data: dataPoints,
      backgroundColor: sourceColors[index % sourceColors.length],
      borderColor: sourceColors[index % sourceColors.length].replace('0.7', '1'),
      borderWidth: 1,
      fill: chartType.value === 'area',
      tension: 0.4
    };
  });
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            const value = context.parsed.y;
            label += formatDataVolume(value);
            return label;
          }
        }
      },
      legend: {
        display: false
      }
    },
    scales: {
      x: {
        type: 'category',
        labels: dateLabels.value.map(date => {
          const d = new Date(date);
          return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
        }),
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: true,
        ticks: {
          callback: function(value) {
            return formatDataVolume(value);
          }
        },
        grid: {
          color: 'rgba(160, 174, 192, 0.1)'
        }
      }
    }
  };
  
  chart = new Chart(ctx, {
    type: chartType.value === 'area' ? 'line' : chartType.value,
    data: {
      labels: dateLabels.value,
      datasets: datasets
    },
    options: chartOptions
  });
};

const refreshData = () => {
  emit('refresh');
};

onMounted(() => {
  createChart();
});

watch([() => props.chartData, chartType], () => {
  nextTick(() => {
    createChart();
  });
}, { deep: true });

watch(() => props.timeRange, () => {
  nextTick(() => {
    createChart();
  });
}, { deep: true });
</script> 