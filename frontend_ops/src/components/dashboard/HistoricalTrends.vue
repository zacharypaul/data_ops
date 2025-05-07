<template>
  <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-display font-bold">Historical Trends</h2>
      <div class="flex items-center space-x-3">
        <div class="relative">
          <select 
            v-model="timeRange" 
            class="bg-dark-700/50 border border-dark-600 rounded-md px-3 py-1.5 text-sm appearance-none pr-8 text-white focus:outline-none focus:border-primary-500"
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
          <svg 
            class="absolute right-2.5 top-2 h-4 w-4 text-dark-400 pointer-events-none" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fill-rule="evenodd" 
              d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" 
              clip-rule="evenodd" 
            />
          </svg>
        </div>
        <div class="flex space-x-1 bg-dark-700/50 rounded-md p-1">
          <button 
            v-for="metric in availableMetrics" 
            :key="metric.id"
            @click="toggleMetric(metric.id)"
            :class="[
              'px-2 py-1 text-xs rounded-md transition-colors',
              selectedMetrics.includes(metric.id) 
                ? `bg-${metric.color}-600/80 text-white` 
                : 'bg-transparent text-dark-300 hover:text-white'
            ]"
          >
            {{ metric.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Chart Container -->
    <div class="h-80 w-full relative">
      <!-- Loading State -->
      <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center">
        <svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>

      <!-- No Data State -->
      <div v-else-if="!hasData" class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-dark-500 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <p class="text-dark-400">No trend data available for the selected time range</p>
        </div>
      </div>

      <!-- Simple Chart View -->
      <div v-else class="h-full w-full">
        <div class="flex items-end justify-between h-64 w-full border-b border-dark-700 relative">
          <!-- Y-axis labels -->
          <div class="absolute left-0 top-0 bottom-0 w-12 flex flex-col justify-between text-right pr-2 text-xs text-dark-400">
            <span>100</span>
            <span>75</span>
            <span>50</span>
            <span>25</span>
            <span>0</span>
          </div>
          
          <!-- Chart bars container -->
          <div class="flex items-end justify-between flex-1 h-full ml-12">
            <div 
              v-for="(dataPoint, index) in chartData" 
              :key="index" 
              class="flex flex-col items-center justify-end h-full px-1"
              :style="{ width: `${100 / chartData.length}%` }"
            >
              <!-- Bars for each metric -->
              <div 
                v-for="metric in selectedMetrics" 
                :key="metric"
                class="relative mx-0.5"
                :style="{
                  height: `${(dataPoint[metric] / maxValue) * 100}%`,
                  width: '8px',
                  backgroundColor: getMetricColor(metric),
                  marginBottom: metric === selectedMetrics[0] ? '0' : '-8px',
                  zIndex: getMetricZIndex(metric)
                }"
              >
                <div 
                  v-if="index === hoveredIndex"
                  class="absolute -top-7 left-1/2 transform -translate-x-1/2 bg-dark-800 px-2 py-1 rounded text-xs whitespace-nowrap"
                >
                  {{ dataPoint[metric] }}
                </div>
              </div>
              
              <!-- X-axis label -->
              <div 
                class="text-xs text-dark-400 mt-2 transform -rotate-45 origin-top-left whitespace-nowrap"
                style="font-size: 10px;"
              >
                {{ formatDate(chartData[index].timestamp, timeRange) }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Legend -->
        <div class="flex justify-center mt-4 space-x-4">
          <div 
            v-for="metric in availableMetrics.filter(m => selectedMetrics.includes(m.id))" 
            :key="metric.id"
            class="flex items-center"
          >
            <span 
              class="inline-block w-3 h-3 mr-1 rounded-sm" 
              :style="{ backgroundColor: `var(--color-${metric.color}-500)` }"
            ></span>
            <span class="text-xs text-dark-300">{{ metric.label }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Insights Panel -->
    <div v-if="insights.length > 0" class="mt-6 pt-4 border-t border-dark-700">
      <h3 class="text-base font-bold mb-3 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-1 text-primary-400" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
        Key Insights
      </h3>
      <div class="space-y-2">
        <div 
          v-for="(insight, index) in insights" 
          :key="index"
          class="flex items-start space-x-2 text-sm"
        >
          <span :class="`text-${insight.type}-500`">
            <svg v-if="insight.trend === 'up'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 7a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0V8.414l-4.293 4.293a1 1 0 01-1.414 0L8 10.414l-4.293 4.293a1 1 0 01-1.414-1.414l5-5a1 1 0 011.414 0L11 10.586 14.586 7H12z" clip-rule="evenodd" />
            </svg>
            <svg v-else-if="insight.trend === 'down'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12 13a1 1 0 100 2h5a1 1 0 001-1v-5a1 1 0 10-2 0v2.586l-4.293-4.293a1 1 0 00-1.414 0L8 9.586l-4.293-4.293a1 1 0 00-1.414 1.414l5 5a1 1 0 001.414 0L11 9.414 14.586 13H12z" clip-rule="evenodd" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </span>
          <span class="text-dark-200">{{ insight.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import DashboardApi from '@/services/DashboardApi';

const props = defineProps({
  connectorId: {
    type: [String, Number],
    default: null
  }
});

// Chart state
const isLoading = ref(true);
const hasData = ref(true);
const timeRange = ref('7d');
const hoveredIndex = ref(null);

// Available metrics
const availableMetrics = [
  { id: 'freshness', label: 'Freshness', color: 'primary' },
  { id: 'quality', label: 'Quality', color: 'accent' },
  { id: 'runtime', label: 'Runtime', color: 'gold' },
  { id: 'volume', label: 'Data Volume', color: 'secondary' }
];

// Selected metrics
const selectedMetrics = ref(['freshness', 'quality']);

// Insights generated from the data
const insights = ref([]);

// Chart data
const chartData = ref([]);
const maxValue = ref(100);

// Toggle a metric
const toggleMetric = (metricId) => {
  if (selectedMetrics.value.includes(metricId)) {
    // Don't allow deselecting all metrics
    if (selectedMetrics.value.length > 1) {
      selectedMetrics.value = selectedMetrics.value.filter(id => id !== metricId);
    }
  } else {
    selectedMetrics.value.push(metricId);
  }
};

// Get mocked trend data for demonstration
const getTrendData = async () => {
  isLoading.value = true;
  
  try {
    // In a real app, this would be an API call with timeRange and connectorId
    const response = await DashboardApi.getTrendData(timeRange.value, props.connectorId);
    
    if (response && response.series && response.series.length > 0) {
      // Transform the data for our simple chart
      transformChartData(response);
      hasData.value = true;
      
      // Generate insights based on the data
      if (response.insights) {
        insights.value = response.insights;
      }
    } else {
      hasData.value = false;
    }
  } catch (error) {
    console.error('Error fetching trend data:', error);
    hasData.value = false;
  } finally {
    isLoading.value = false;
  }
};

// Transform data for chart
const transformChartData = (data) => {
  const transformed = [];
  const seriesMap = {};
  
  // Create a map of series by id
  data.series.forEach(series => {
    seriesMap[series.id] = series;
  });
  
  // Build data points
  for (let i = 0; i < data.timestamps.length; i++) {
    const point = {
      timestamp: data.timestamps[i]
    };
    
    // Add value for each series
    availableMetrics.forEach(metric => {
      if (seriesMap[metric.id]) {
        point[metric.id] = seriesMap[metric.id].data[i];
      } else {
        point[metric.id] = 0;
      }
    });
    
    transformed.push(point);
  }
  
  chartData.value = transformed;
  
  // Calculate max value for scaling
  let max = 0;
  availableMetrics.forEach(metric => {
    if (seriesMap[metric.id]) {
      const seriesMax = Math.max(...seriesMap[metric.id].data);
      if (seriesMax > max) max = seriesMax;
    }
  });
  
  maxValue.value = max;
};

// Format date based on time range
const formatDate = (timestamp, range) => {
  const date = new Date(timestamp);
  
  if (range === '24h') {
    return date.getHours().toString().padStart(2, '0') + ':00';
  } else if (range === '7d') {
    return date.getDate() + '/' + (date.getMonth() + 1);
  } else {
    return date.getDate() + '/' + (date.getMonth() + 1);
  }
};

// Get color for a metric
const getMetricColor = (metricId) => {
  const metric = availableMetrics.find(m => m.id === metricId);
  return metric ? `var(--color-${metric.color}-500)` : 'var(--color-primary-500)';
};

// Get z-index for a metric to control overlap
const getMetricZIndex = (metricId) => {
  return selectedMetrics.value.indexOf(metricId) + 1;
};

// Watch for changes that require a data refresh
watch([timeRange, props.connectorId], () => {
  getTrendData();
});

// Initial data fetch
onMounted(() => {
  getTrendData();
});
</script> 