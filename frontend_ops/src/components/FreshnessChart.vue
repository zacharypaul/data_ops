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
      <p class="text-gray-600 dark:text-gray-400">No data available for the selected time range</p>
    </div>
    
    <div v-else class="h-64">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed, nextTick } from 'vue';
import Chart from 'chart.js/auto';

const props = defineProps({
  title: {
    type: String,
    default: 'Data Freshness by Source'
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
  timeRange: {
    type: Object,
    default: () => ({})
  },
  chartOptions: {
    type: Object,
    default: () => ({})
  }
});

const emit = defineEmits(['refresh']);
const chartCanvas = ref(null);
let chart = null;

const defaultOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        usePointStyle: true,
        padding: 15,
        boxWidth: 6
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: 'Hours Since Last Update'
      },
      ticks: {
        callback: function(value) {
          return value + 'h';
        }
      }
    },
    x: {
      title: {
        display: true,
        text: 'Source'
      }
    }
  }
};

const mergedOptions = computed(() => {
  return { ...defaultOptions, ...props.chartOptions };
});

const createChart = () => {
  if (!chartCanvas.value || !props.chartData || props.chartData.length === 0) return;
  
  const ctx = chartCanvas.value.getContext('2d');
  
  if (chart) {
    chart.destroy();
  }
  
  // Prepare data for chart
  const labels = props.chartData.map(item => item.source);
  const dataValues = props.chartData.map(item => item.hoursSinceLastUpdate);
  const colors = generateColors(props.chartData.length);
  
  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Hours Since Last Update',
        data: dataValues,
        backgroundColor: colors,
        borderColor: colors,
        borderWidth: 1
      }]
    },
    options: mergedOptions.value
  });
};

const refreshData = () => {
  emit('refresh');
};

// Generate distinct colors for chart
const generateColors = (count) => {
  const baseColors = [
    'rgba(54, 162, 235, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(255, 206, 86, 0.7)',
    'rgba(255, 99, 132, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 159, 64, 0.7)',
    'rgba(199, 199, 199, 0.7)'
  ];
  
  // If we have fewer data points than colors, return a slice of the array
  if (count <= baseColors.length) {
    return baseColors.slice(0, count);
  }
  
  // Otherwise, generate additional colors
  const colors = [...baseColors];
  for (let i = baseColors.length; i < count; i++) {
    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);
    colors.push(`rgba(${r}, ${g}, ${b}, 0.7)`);
  }
  
  return colors;
};

onMounted(() => {
  nextTick(() => {
    createChart();
  });
});

watch(() => props.chartData, () => {
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