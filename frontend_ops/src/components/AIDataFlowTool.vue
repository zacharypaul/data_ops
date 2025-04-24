<template>
  <div class="flow-tool-container">
    <div class="flow-tool-header">
      <h3 class="text-xl font-bold text-primary-400">AI Data Flow Builder</h3>
      <p class="text-dark-400">Create intelligent data pipelines with automated evaluation</p>
    </div>
    
    <div class="flow-tool-card">
      <div class="glassmorphic-panel">
        <div class="source-section">
          <h4 class="panel-title">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
              <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
              <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
            </svg>
            Data Sources
          </h4>
          <div class="data-sources-grid">
            <div class="data-source-item" :class="{ active: selectedSources.includes('snowflake') }" @click="toggleSource('snowflake')">
              <div class="source-icon snowflake-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 3v18M3 12h18M4.5 4.5l15 15M19.5 4.5l-15 15" />
                </svg>
              </div>
              <span>Snowflake</span>
            </div>
            <div class="data-source-item" :class="{ active: selectedSources.includes('fabric') }" @click="toggleSource('fabric')">
              <div class="source-icon fabric-icon">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" />
                </svg>
              </div>
              <span>Fabric</span>
            </div>
          </div>
          
          <div class="mt-4" v-if="selectedSources.length > 0">
            <div class="flex justify-between items-center mb-2">
              <h5 class="text-sm font-medium text-dark-300">Available Data Points</h5>
              <button @click="fetchDataPoints" class="text-xs text-primary-400 hover:text-primary-300 flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                </svg>
                Refresh
              </button>
            </div>
            
            <div class="data-points-container relative">
              <div v-if="loadingDataPoints" class="absolute inset-0 flex items-center justify-center bg-dark-800 bg-opacity-75 z-10 rounded">
                <div class="animate-spin h-5 w-5 border-2 border-primary-500 rounded-full border-t-transparent"></div>
              </div>
              
              <div class="search-container mb-2">
                <input 
                  type="text" 
                  placeholder="Search data points..." 
                  v-model="dataPointsSearch"
                  class="w-full bg-dark-700 border border-dark-600 rounded px-3 py-1.5 text-sm"
                />
              </div>
              
              <div class="data-points-list max-h-60 overflow-y-auto pr-1 custom-scrollbar">
                <div 
                  v-for="point in filteredDataPoints" 
                  :key="point.id"
                  class="data-point-item"
                  :class="{ 'selected': selectedDataPoints.includes(point.id) }"
                  @click="toggleDataPoint(point.id)"
                >
                  <div class="flex items-center">
                    <input 
                      type="checkbox" 
                      :checked="selectedDataPoints.includes(point.id)" 
                      @click.stop
                      class="mr-2 accent-primary-500"
                    />
                    <div class="flex-1">
                      <div class="font-medium text-sm">{{ point.name }}</div>
                      <div class="text-xs text-dark-400">{{ point.table }}</div>
                    </div>
                    <div class="flex flex-col items-end">
                      <span class="text-xs text-dark-300">Refresh: {{ point.refreshRate }}</span>
                      <span 
                        class="text-xs px-1.5 py-0.5 rounded-full mt-1" 
                        :class="getRefreshStatusClass(point.lastRefreshed)"
                      >
                        {{ getRefreshStatus(point.lastRefreshed) }}
                      </span>
                    </div>
                  </div>
                </div>
                
                <div v-if="filteredDataPoints.length === 0" class="p-3 text-center text-dark-400 text-sm">
                  No data points found. Try adjusting your search.
                </div>
              </div>
              
              <div class="selected-count mt-2 text-xs text-right text-dark-400">
                {{ selectedDataPoints.length }} data point(s) selected
              </div>
            </div>
          </div>
        </div>
        
        <div class="workflow-section">
          <h4 class="panel-title">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm11 1H6v8l4-2 4 2V6z" clip-rule="evenodd" />
            </svg>
            Context Parameters
          </h4>
          <div class="context-inputs">
            <div class="input-group">
              <label>Business Context</label>
              <input type="text" placeholder="e.g., Sales forecasting, Customer segmentation" />
            </div>
            <div class="input-group">
              <label>Time Frame</label>
              <input type="text" placeholder="e.g., Last 30 days, Q1 2025" />
            </div>
            <div class="input-group">
              <label>Evaluation Metrics</label>
              <select>
                <option value="">Select metrics</option>
                <option>Accuracy</option>
                <option>F1 Score</option>
                <option>MAE</option>
                <option>Precision/Recall</option>
              </select>
            </div>
            
            <div class="mt-4 border-t border-dark-700 pt-4">
              <div class="flex items-center">
                <input type="checkbox" id="generate-sop" v-model="generateSOP" class="mr-2" />
                <label for="generate-sop" class="text-sm font-medium cursor-pointer select-none">Generate Standard Operating Procedure</label>
              </div>
              
              <div v-if="generateSOP" class="mt-3 space-y-3">
                <div class="input-group">
                  <label>SOP Template</label>
                  <select v-model="sopTemplate">
                    <option value="default">Default Template</option>
                    <option value="detailed">Detailed Analysis</option>
                    <option value="quickstart">Quick Start Guide</option>
                    <option value="custom">Custom Template</option>
                  </select>
                </div>
                
                <div class="input-group">
                  <label>Target Audience</label>
                  <select v-model="sopAudience">
                    <option value="technical">Technical Team</option>
                    <option value="business">Business Users</option>
                    <option value="executive">Executive Leadership</option>
                    <option value="mixed">Mixed Audience</option>
                  </select>
                </div>
                
                <div class="input-group">
                  <label>Key Process Goals</label>
                  <textarea 
                    placeholder="Describe the main goals this SOP should address..."
                    class="w-full bg-dark-700 border border-dark-600 rounded px-3 py-2 text-sm h-20"
                    v-model="sopGoals"
                  ></textarea>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="feedback-loop-section">
          <h4 class="panel-title">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
            Feedback Loop Configuration
          </h4>
          <div class="loop-options">
            <div class="loop-option">
              <input type="checkbox" id="auto-retrain" v-model="feedbackOptions.autoRetrain" />
              <label for="auto-retrain">Auto-retrain on drift</label>
            </div>
            <div class="loop-option">
              <input type="checkbox" id="human-review" v-model="feedbackOptions.humanReview" />
              <label for="human-review">Human review for low confidence</label>
            </div>
            <div class="loop-option">
              <input type="checkbox" id="performance-alerts" v-model="feedbackOptions.performanceAlerts" />
              <label for="performance-alerts">Performance degradation alerts</label>
            </div>
            
            <div class="mt-4 pt-4 border-t border-dark-700">
              <h5 class="text-sm font-medium mb-2">Refresh Rate Monitoring</h5>
              <div class="loop-option">
                <input type="checkbox" id="refresh-alerts" v-model="feedbackOptions.refreshAlerts" />
                <label for="refresh-alerts">Alert on stale data</label>
              </div>
              
              <div class="input-group mt-2" v-if="feedbackOptions.refreshAlerts">
                <label class="text-xs">Staleness Threshold</label>
                <div class="flex items-center space-x-2">
                  <input 
                    type="number" 
                    min="1" 
                    v-model="refreshThreshold.value" 
                    class="w-20 bg-dark-700 border border-dark-600 rounded px-2 py-1 text-sm"
                  />
                  <select 
                    v-model="refreshThreshold.unit" 
                    class="bg-dark-700 border border-dark-600 rounded px-2 py-1 text-sm"
                  >
                    <option value="minutes">Minutes</option>
                    <option value="hours">Hours</option>
                    <option value="days">Days</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="selectedDataPoints.length > 0" class="data-preview-container mb-6">
        <h4 class="text-sm font-medium text-dark-300 mb-3">Selected Data Points Preview</h4>
        <div class="data-preview bg-dark-800/50 p-4 rounded-lg border border-dark-700">
          <div class="data-flow-diagram">
            <div class="space-y-2">
              <div 
                v-for="id in selectedDataPoints" 
                :key="id" 
                class="data-node flex items-center p-2 rounded bg-dark-700/70 border border-dark-600"
              >
                <span class="w-2 h-2 rounded-full mr-2" :class="getSourceColor(getDataPointById(id)?.source)"></span>
                <span class="text-sm">{{ getDataPointById(id)?.name }}</span>
                <span class="text-xs ml-auto text-dark-400">{{ getDataPointById(id)?.refreshRate }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="flow-actions">
        <button class="btn-outline pulse-btn" @click="importTemplate">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zM6.293 6.707a1 1 0 010-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L11 5.414V13a1 1 0 11-2 0V5.414L7.707 6.707a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
          Import Template
        </button>
        <button class="glow-btn" @click="buildFlow" :disabled="!canBuildFlow">
          Build Flow
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- SOP Viewer -->
    <div v-if="generatedSOP" class="mt-8">
      <h3 class="text-xl font-bold text-primary-400 mb-4">Generated Standard Operating Procedure</h3>
      <SOPViewer 
        :sopDocument="generatedSOP" 
        @export="handleSOPExport" 
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import sopService from '../services/sopService';
import SOPViewer from './SOPViewer.vue';

const selectedSources = ref([]);
const selectedDataPoints = ref([]);
const dataPointsSearch = ref('');
const loadingDataPoints = ref(false);

const generateSOP = ref(false);
const sopTemplate = ref('default');
const sopAudience = ref('technical');
const sopGoals = ref('');

const feedbackOptions = ref({
  autoRetrain: true,
  humanReview: false,
  performanceAlerts: true,
  refreshAlerts: false
});

const refreshThreshold = ref({
  value: 24,
  unit: 'hours'
});

const dataPoints = ref([
  { 
    id: 'sf1', 
    name: 'Monthly Sales', 
    table: 'SALES.MONTHLY_SUMMARY', 
    refreshRate: 'Daily at 2AM', 
    lastRefreshed: new Date(Date.now() - 6 * 3600000),
    source: 'snowflake' 
  },
  { 
    id: 'sf2', 
    name: 'Customer Demographics', 
    table: 'CUSTOMERS.DEMOGRAPHICS', 
    refreshRate: 'Weekly on Sunday', 
    lastRefreshed: new Date(Date.now() - 2 * 86400000),
    source: 'snowflake' 
  },
  { 
    id: 'sf3', 
    name: 'Product Inventory', 
    table: 'PRODUCTS.INVENTORY', 
    refreshRate: 'Every 3 hours', 
    lastRefreshed: new Date(Date.now() - 4 * 3600000),
    source: 'snowflake' 
  },
  { 
    id: 'fb1', 
    name: 'Customer Sentiment', 
    table: 'ANALYTICS.SENTIMENT', 
    refreshRate: 'Daily at 5AM', 
    lastRefreshed: new Date(Date.now() - 23 * 3600000),
    source: 'fabric' 
  },
  { 
    id: 'fb2', 
    name: 'Marketing Campaign Results', 
    table: 'MARKETING.CAMPAIGNS', 
    refreshRate: 'Bi-weekly', 
    lastRefreshed: new Date(Date.now() - 8 * 86400000),
    source: 'fabric' 
  },
  { 
    id: 'fb3', 
    name: 'Website Traffic', 
    table: 'ANALYTICS.TRAFFIC', 
    refreshRate: 'Hourly', 
    lastRefreshed: new Date(Date.now() - 30 * 60000),
    source: 'fabric' 
  }
]);

const filteredDataPoints = computed(() => {
  if (!dataPointsSearch.value) {
    return dataPoints.value.filter(point => 
      selectedSources.value.includes(point.source)
    );
  }
  
  const search = dataPointsSearch.value.toLowerCase();
  return dataPoints.value.filter(point => 
    selectedSources.value.includes(point.source) && 
    (point.name.toLowerCase().includes(search) || 
     point.table.toLowerCase().includes(search))
  );
});

const canBuildFlow = computed(() => {
  return selectedDataPoints.value.length > 0;
});

const toggleSource = (source) => {
  if (selectedSources.value.includes(source)) {
    selectedSources.value = selectedSources.value.filter(s => s !== source);
    selectedDataPoints.value = selectedDataPoints.value.filter(id => {
      const point = getDataPointById(id);
      return point && point.source !== source;
    });
  } else {
    selectedSources.value.push(source);
  }
};

const toggleDataPoint = (id) => {
  if (selectedDataPoints.value.includes(id)) {
    selectedDataPoints.value = selectedDataPoints.value.filter(p => p !== id);
  } else {
    selectedDataPoints.value.push(id);
  }
};

const getDataPointById = (id) => {
  return dataPoints.value.find(point => point.id === id);
};

const getRefreshStatus = (lastRefreshed) => {
  const now = new Date();
  const diff = now - lastRefreshed;
  const hoursDiff = diff / (1000 * 60 * 60);
  
  if (hoursDiff < 1) return 'Recent';
  if (hoursDiff < 24) return 'Today';
  if (hoursDiff < 48) return 'Yesterday';
  return 'Stale';
};

const getRefreshStatusClass = (lastRefreshed) => {
  const now = new Date();
  const diff = now - lastRefreshed;
  const hoursDiff = diff / (1000 * 60 * 60);
  
  if (hoursDiff < 1) return 'bg-green-900/30 text-green-400';
  if (hoursDiff < 24) return 'bg-blue-900/30 text-blue-400';
  if (hoursDiff < 48) return 'bg-yellow-900/30 text-yellow-400';
  return 'bg-red-900/30 text-red-400';
};

const getSourceColor = (source) => {
  if (source === 'snowflake') return 'bg-blue-400';
  if (source === 'fabric') return 'bg-purple-400';
  return 'bg-gray-400';
};

const fetchDataPoints = async () => {
  if (selectedSources.value.length === 0) return;
  
  loadingDataPoints.value = true;
  
  try {
    await new Promise(resolve => setTimeout(resolve, 800));
    
    console.log("Fetched data points for sources:", selectedSources.value);
    
  } catch (error) {
    console.error("Error fetching data points:", error);
  } finally {
    loadingDataPoints.value = false;
  }
};

const importTemplate = () => {
  console.log("Import template clicked");
};

const generatedSOP = ref(null);
const isGeneratingSOP = ref(false);

const buildFlow = async () => {
  try {
    console.log("Building flow with data points:", selectedDataPoints.value);
    
    if (generateSOP.value) {
      isGeneratingSOP.value = true;
      
      try {
        const selectedPointsData = selectedDataPoints.value.map(id => {
          const point = getDataPointById(id);
          return {
            id: point.id,
            name: point.name,
            table: point.table,
            refreshRate: point.refreshRate,
            source: point.source,
            lastRefreshed: point.lastRefreshed instanceof Date 
              ? point.lastRefreshed.toISOString() 
              : point.lastRefreshed
          };
        });
        
        const sopData = {
          dataPoints: selectedPointsData,
          template: sopTemplate.value,
          audience: sopAudience.value,
          goals: sopGoals.value
        };
        
        console.log("Generating SOP with config:", sopData);
        
        const sopResult = await sopService.generateSOP(sopData);
        
        generatedSOP.value = sopResult;
        console.log("Generated SOP:", generatedSOP.value);
        
      } catch (error) {
        console.error("Error generating SOP:", error);
      } finally {
        isGeneratingSOP.value = false;
      }
    }
    
    console.log("Flow configuration:", {
      dataPoints: selectedDataPoints.value.map(id => getDataPointById(id)),
      feedbackOptions: feedbackOptions.value,
      refreshThreshold: refreshThreshold.value,
      generateSOP: generateSOP.value
    });
  } catch (error) {
    console.error("Error building flow:", error);
  }
};

const handleSOPExport = (exportInfo) => {
  console.log(`SOP exported: ${exportInfo.format}`, exportInfo);
};

watch(selectedSources, (newSources) => {
  if (newSources.length > 0) {
    fetchDataPoints();
  }
});

onMounted(() => {
  // Any initialization code
});
</script>

<style scoped>
.flow-tool-container {
  margin-bottom: 2rem;
  animation: fadeIn 0.6s ease-out;
}

.flow-tool-header {
  margin-bottom: 1rem;
}

.flow-tool-card {
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
  border-radius: 1rem;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.glassmorphic-panel {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.source-section, .workflow-section, .feedback-loop-section {
  background: rgba(30, 41, 59, 0.4);
  border-radius: 0.75rem;
  padding: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.panel-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 1rem;
  color: rgba(219, 234, 254, 0.9);
  display: flex;
  align-items: center;
}

.data-sources-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.data-source-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgba(30, 41, 59, 0.4);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.data-source-item:hover {
  background: rgba(56, 189, 248, 0.1);
  transform: translateY(-2px);
}

.data-source-item.active {
  background: rgba(56, 189, 248, 0.15);
  border-color: rgba(56, 189, 248, 0.4);
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.3);
}

.source-icon {
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.5rem;
  color: #38bdf8;
}

.data-points-container {
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 0.5rem;
  background: rgba(15, 23, 42, 0.5);
  padding: 0.75rem;
}

.data-point-item {
  padding: 0.5rem;
  border-radius: 0.375rem;
  margin-bottom: 0.5rem;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.data-point-item:hover {
  background: rgba(55, 65, 81, 0.5);
}

.data-point-item.selected {
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.3);
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: rgba(219, 234, 254, 0.7);
}

.input-group input, .input-group select {
  width: 100%;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  color: white;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.input-group input:focus, .input-group select:focus {
  outline: none;
  border-color: rgba(56, 189, 248, 0.5);
  box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.2);
}

.loop-options {
  display: grid;
  gap: 0.75rem;
}

.loop-option {
  display: flex;
  align-items: center;
}

.loop-option input[type="checkbox"] {
  margin-right: 0.5rem;
  appearance: none;
  width: 1rem;
  height: 1rem;
  border-radius: 0.25rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: rgba(15, 23, 42, 0.6);
  position: relative;
  cursor: pointer;
}

.loop-option input[type="checkbox"]:checked {
  background: #38bdf8;
  border-color: #38bdf8;
}

.loop-option input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 0.75rem;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.flow-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.glow-btn {
  background: linear-gradient(135deg, #38bdf8, #818cf8);
  color: white;
  padding: 0.5rem 1.25rem;
  border-radius: 0.375rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  border: none;
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
  position: relative;
  overflow: hidden;
}

.glow-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.glow-btn:not(:disabled)::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
}

.glow-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.6);
}

.glow-btn:not(:disabled):hover::before {
  opacity: 1;
  animation: rotate 4s linear infinite;
}

.pulse-btn {
  background: transparent;
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  padding: 0.5rem 1.25rem;
  border-radius: 0.375rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.pulse-btn:hover {
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.5);
}

.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(56, 189, 248, 0.3) rgba(15, 23, 42, 0.3);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(56, 189, 248, 0.3);
  border-radius: 3px;
}

.data-preview-container {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 1024px) {
  .glassmorphic-panel {
    grid-template-columns: 1fr;
  }
}
</style> 