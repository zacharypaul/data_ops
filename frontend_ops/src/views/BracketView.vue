<template>
  <div class="py-8">
    <h1 class="text-3xl font-display font-bold mb-4 text-center">Data Platform Migration Bracket</h1>
    <p class="text-center text-dark-400 mb-8">Compare migration paths from Snowflake to Microsoft Fabric</p>
    
    <!-- Loading state -->
    <div v-if="loading" class="text-center py-10">
      <div class="text-primary-500">Loading connectors...</div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="text-center py-10">
      <div class="text-red-500">{{ error }}</div>
      <button @click="fetchConnectors" class="btn-primary mt-4">Retry</button>
    </div>
    
    <div v-else>
      <!-- Tab Controls -->
      <div class="flex justify-center mb-8">
        <div class="inline-flex rounded-md shadow-sm" role="group">
          <button 
            @click="activeTab = 'full'"
            type="button" 
            :class="`px-5 py-2.5 text-sm font-medium ${activeTab === 'full' ? 'text-white bg-primary-700' : 'text-dark-300 bg-dark-800'} border border-dark-700 rounded-l-lg hover:bg-primary-900/50 focus:z-10 focus:outline-none`"
          >
            Full Migration
          </button>
          <button 
            @click="activeTab = 'partial'"
            type="button" 
            :class="`px-5 py-2.5 text-sm font-medium ${activeTab === 'partial' ? 'text-white bg-accent-700' : 'text-dark-300 bg-dark-800'} border border-dark-700 rounded-r-lg hover:bg-accent-900/50 focus:z-10 focus:outline-none`"
          >
            Partial Migration
          </button>
        </div>
      </div>
      
      <!-- Full Migration Bracket -->
      <div v-if="activeTab === 'full'" class="bracket-container relative">
        <!-- Connector Lines Layer -->
        <div class="connector-container absolute inset-0 z-0" v-if="!loading && !error">
          <!-- Connections are now directly attached to pipeline items -->
        </div>
        
        <!-- Main Bracket Structure -->
        <div class="flex justify-between relative z-10">
          <!-- Snowflake Side (Left) -->
          <div class="w-[42%]">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-display font-bold text-secondary-500">Snowflake/AWS Inventory</h2>
              
              <div class="toggler" @click="toggleConnectionsView">
                <span>{{ showAllConnections ? 'All Connections' : 'Selected Only' }}</span>
                <label class="switch">
                  <input type="checkbox" v-model="showAllConnections">
                  <span class="slider"></span>
                </label>
              </div>
            </div>
            
            <!-- Technology Groups -->
            <div class="space-y-8 mb-8">
              <div 
                v-for="(connectorList, tech) in connectorsByTech" 
                :key="`group-${tech}`" 
                class="bg-dark-800/70 p-4 rounded-lg border border-secondary-700"
              >
                <div class="tech-header" @click="toggleTechActive(tech)">
                  <span 
                    :class="[
                      'status-indicator', 
                      connectorList.every(p => p.active) ? 'active-node' : 'burnt-node'
                    ]"
                  ></span>
                  <h3 class="text-lg font-display font-bold text-secondary-400">{{ tech }}</h3>
                  <div class="tech-controls">
                    <span class="text-xs text-dark-400">{{ connectorList.length }} pipelines</span>
                    <button 
                      class="tech-btn" 
                      @click.stop="selectTechPipelines(tech)"
                      title="Select all pipelines in this group"
                    >
                      Select All
                    </button>
                  </div>
                </div>
                
                <div class="connector-list space-y-2">
                  <div 
                    v-for="connector in connectorList" 
                    :key="`pipe-${connector.name}`"
                    :class="[
                      'pipeline-item', 
                      { 
                        'inactive': !connector.active,
                        'selected': isPipelineSelected(connector)
                      }
                    ]"
                    @click="togglePipelineSelection(connector)"
                    :id="`source-${connector.name}`"
                  >
                    <div class="flex items-center">
                      <span 
                        :class="[
                          'status-indicator', 
                          connector.active ? 'active-node' : 'burnt-node',
                          isPipelineSelected(connector) ? 'selected-node' : ''
                        ]"
                      ></span>
                      <span class="text-sm">{{ connector.name }}</span>
                    </div>
                    
                    <div class="flex items-center">
                      <span class="text-xs bg-dark-700 px-2 py-0.5 rounded text-dark-400 mr-2">
                        {{ connector.owner }}
                      </span>
                      <button 
                        class="p-1 text-dark-400 hover:text-dark-300"
                        @click.stop="togglePipelineActive(connector)"
                        title="Toggle pipeline active state"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                        </svg>
                      </button>
                    </div>
                    
                    <!-- Connection line from pipeline to destination -->
                    <div 
                      v-if="(showAllConnections || isPipelineSelected(connector)) && isValidConnection(connector)"
                      class="connection-line"
                      :class="{ 
                        'inactive': !connector.active,
                        ['beam-' + (connector.refreshFrequency?.interval || 'daily')]: true
                      }"
                    >
                      <div class="connection-beam"></div>
                      <div class="connection-label">
                        {{ connector.refreshFrequency?.interval || 'daily' }}
                      </div>
                      <div class="connection-pulse start" :class="{ 'active-pulse': connector.active }"></div>
                      <div class="connection-pulse end" :class="{ 'active-pulse': connector.active }"></div>
                    </div>
                    
                    <div class="selector-overlay">
                      <button class="action-btn" title="Select pipeline">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Center - Migration Path -->
          <div class="flex flex-col items-center justify-center">
            <div class="glass-effect p-5 rounded-lg border border-gold-500/50 text-center mb-4 z-20 relative">
              <div class="text-xl font-display font-bold text-gold-400 mb-2">Full Migration</div>
              
              <div class="w-14 h-40 my-4 relative">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-full w-full text-gold-500/30" viewBox="0 0 20 20" fill="none" stroke="currentColor">
                  <path d="M1 1 C 10 1, 19 10, 19 19" stroke-width="2" stroke-linecap="round"/>
                </svg>
              </div>
              
              <div class="text-sm text-dark-300">
                Migrating <span class="text-gold-400 font-bold">{{ connectors.length }}</span> pipelines
              </div>
              
              <div class="mt-4 flex justify-center">
                <button 
                  class="px-3 py-1 bg-dark-700 text-dark-300 rounded-full text-xs border border-dark-600 hover:border-dark-500"
                  @click="deselectAllPipelines"
                  v-if="selectedPipelines.length > 0"
                >
                  Clear Selection
                </button>
                <span 
                  v-else
                  class="px-3 py-1 bg-green-900/30 text-green-400 rounded-full text-xs"
                >
                  <span class="status-indicator active-node blink-slow"></span>
                  Select Pipelines
                </span>
              </div>
            </div>
          </div>
          
          <!-- Microsoft Fabric Side (Right) -->
          <div class="w-[42%]">
            <h2 class="text-2xl font-display font-bold mb-6 text-accent-500">Microsoft Fabric Destination</h2>
            
            <!-- Fabric Equivalents -->
            <div class="space-y-8 mb-8">
              <div 
                v-for="(equivalent, tech) in fabricEquivalents" 
                :key="`fabric-${tech}`"
                class="bg-dark-800/70 p-4 rounded-lg border border-accent-700 pulse-animation"
                style="animation-play-state: paused;"
                :style="{
                  'animation-play-state': 
                    (showAllConnections || selectedPipelines.some(p => 
                      techMapping[p.technology] === equivalent.name
                    )) ? 'running' : 'paused'
                }"
                :id="`dest-${tech}`"
              >
                <div class="flex items-center mb-3">
                  <span :class="`status-indicator active-node ${blinkStates[tech]?.blinkClass || 'blink-slow'}`"></span>
                  <h3 class="text-lg font-display font-bold text-accent-400">{{ equivalent.name }}</h3>
                  <span class="ml-auto text-xs px-2 py-1 bg-dark-700 rounded text-accent-300">{{ equivalent.score }}% compatible</span>
                </div>
                
                <div class="p-3 bg-dark-700/50 rounded-lg">
                  <div class="text-sm text-dark-300 mb-2">Receiving from</div>
                  <div class="p-2 bg-dark-800 rounded border border-dark-600 text-sm" :id="`dest-connector-${tech}`">
                    <span v-if="tech.includes('Snowflake ADF')">ADF Pipelines</span>
                    <span v-else-if="tech.includes('Snowflake Airflow')">Airflow DAGs</span>
                    <span v-else-if="tech.includes('Snowflake Fivetran')">Fivetran Connectors</span>
                    <span v-else>Data Warehouse Objects</span>
                    
                    <!-- Connection point for destination -->
                    <div class="connection-point-destination" :class="{ 'active': isConnectionActive(tech) }"></div>
                  </div>
                  
                  <div class="mt-3 flex items-center text-xs">
                    <span class="h-1.5 w-1.5 rounded-full bg-green-400 mr-1.5"></span>
                    <span class="text-green-400">Live</span>
                    <span class="mx-2 text-dark-500">|</span>
                    <span class="text-dark-400">
                      <span v-if="tech.includes('Snowflake')">
                        {{ connectorsByTech[tech]?.filter(c => c.active).length || 0 }} 
                        active of {{ connectorsByTech[tech]?.length || 0 }} pipelines
                      </span>
                      <span v-else>New capability</span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Partial Migration Bracket -->
      <div v-if="activeTab === 'partial'" class="bracket-container">
        <div class="flex justify-between">
          <!-- Snowflake Side (Left) -->
          <div class="w-[45%]">
            <h2 class="text-2xl font-display font-bold mb-6 text-secondary-500 text-center">Retained in Snowflake</h2>
            
            <!-- Components to Retain in Snowflake -->
            <div class="mb-8">
              <div class="bg-dark-800/70 p-6 rounded-lg border border-secondary-700">
                <h3 class="text-xl font-display font-bold mb-4 text-secondary-400">
                  <span class="status-indicator active-node blink-slow"></span>
                  Core Data Platform
                </h3>
                
                <div class="space-y-4">
                  <div class="partial-component snowflake-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">CDP Data Warehouse</span>
                    </div>
                    <div class="component-benefit">Primary Data Store</div>
                  </div>
                  
                  <div class="partial-component snowflake-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">Historical Data</span>
                    </div>
                    <div class="component-benefit">90% Cost Savings vs Migration</div>
                  </div>
                  
                  <div class="partial-component snowflake-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">ETL Processes</span>
                    </div>
                    <div class="component-benefit">Leverages Existing Code</div>
                  </div>
                </div>
                
                <div class="mt-6">
                  <h4 class="text-md font-semibold mb-2 text-secondary-300">Retained Pipelines</h4>
                  <div class="connector-list space-y-1 mt-3">
                    <div 
                      v-for="connector in connectorsByTech['Snowflake ADF']?.slice(0, 2)" 
                      :key="connector.name"
                      class="p-2 rounded border border-dark-600 flex justify-between items-center"
                    >
                      <div class="flex items-center">
                        <span class="status-indicator active-node blink-slow"></span>
                        <span class="text-xs">{{ connector.name }}</span>
                      </div>
                      <span class="text-xs bg-dark-700 px-1.5 py-0.5 rounded text-dark-400">ADF</span>
                    </div>
                    
                    <div 
                      v-for="connector in connectorsByTech['Snowflake Fivetran']?.slice(0, 2)" 
                      :key="connector.name"
                      class="p-2 rounded border border-dark-600 flex justify-between items-center"
                    >
                      <div class="flex items-center">
                        <span class="status-indicator active-node blink-slow"></span>
                        <span class="text-xs">{{ connector.name }}</span>
                      </div>
                      <span class="text-xs bg-dark-700 px-1.5 py-0.5 rounded text-dark-400">Fivetran</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Data Bridge -->
            <div class="data-bridge-section flex justify-end">
              <div class="w-3/4 bg-dark-800/70 p-4 rounded-lg border border-gold-700">
                <h3 class="text-lg font-display font-bold mb-2 text-gold-400">Data Bridge</h3>
                
                <div class="space-y-3">
                  <div class="data-bridge-component migration-path">
                    <div class="flex items-center justify-between">
                      <span class="bridge-name">SnowPipe to OneLake</span>
                      <span class="bridge-direction">→</span>
                    </div>
                  </div>
                  
                  <div class="data-bridge-component migration-path">
                    <div class="flex items-center justify-between">
                      <span class="bridge-name">OneLake References</span>
                      <span class="bridge-direction">←</span>
                    </div>
                  </div>
                  
                  <div class="data-bridge-component migration-path">
                    <div class="flex items-center justify-between">
                      <span class="bridge-name">Metadata Sync</span>
                      <span class="bridge-direction">↔</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Center Column -->
          <div class="flex flex-col items-center justify-center">
            <div class="championship-trophy">
              <div class="migration-arrow text-center mb-4">
                <span class="block text-dark-400 text-sm">Hybrid Approach</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gold-500 rotate-45" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                </svg>
              </div>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-gold-500 pulse-animation" viewBox="0 0 20 20" fill="currentColor">
                <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
              </svg>
            </div>
            <div class="championship-vs mt-4 text-center">
              <span class="text-3xl font-display font-bold text-gold-500">+</span>
              <div class="text-xs text-dark-400 mt-2">Hybrid Platform Strategy</div>
            </div>
            <div class="championship-result mt-4 px-6 py-3 bg-dark-800 rounded-lg">
              <div class="text-sm text-dark-300 text-center mb-1">Best For</div>
              <div class="text-lg font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-secondary-400 via-gold-400 to-accent-400 animate-gradient-x">
                Phased Migration Strategy
              </div>
            </div>
          </div>
          
          <!-- Microsoft Fabric Side (Right) -->
          <div class="w-[45%]">
            <h2 class="text-2xl font-display font-bold mb-6 text-accent-500 text-center">Migrated to Fabric</h2>
            
            <!-- Components to Migrate to Fabric -->
            <div class="mb-8">
              <div class="bg-dark-800/70 p-6 rounded-lg border border-accent-700">
                <h3 class="text-xl font-display font-bold mb-4 text-accent-400">
                  <span class="status-indicator active-node blink-slow"></span>
                  Analytics & Reporting
                </h3>
                
                <div class="space-y-4">
                  <div class="partial-component fabric-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">Power BI Direct Query</span>
                    </div>
                    <div class="component-benefit">Native Integration</div>
                  </div>
                  
                  <div class="partial-component fabric-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">OneLake Analytics</span>
                    </div>
                    <div class="component-benefit">Business User Access</div>
                  </div>
                  
                  <div class="partial-component fabric-component">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-slow"></span>
                      <span class="component-name">Fabric Notebooks</span>
                    </div>
                    <div class="component-benefit">New Analytics</div>
                  </div>
                </div>
                
                <div class="mt-6">
                  <h4 class="text-md font-semibold mb-2 text-accent-300">Migrated Workflows</h4>
                  <div class="connector-list space-y-1 mt-3">
                    <div 
                      v-for="connector in connectorsByTech['Snowflake Airflow']?.slice(0, 4)" 
                      :key="connector.name"
                      class="p-2 rounded border border-dark-600 flex justify-between items-center"
                    >
                      <div class="flex items-center">
                        <span class="status-indicator migrating-node blink-fast"></span>
                        <span class="text-xs">{{ connector.name }}</span>
                      </div>
                      <span class="text-xs bg-dark-700 px-1.5 py-0.5 rounded text-dark-400">Airflow → Pipeline</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- New Fabric Capabilities -->
            <div class="new-capabilities-section">
              <div class="bg-dark-800/70 p-4 rounded-lg border border-accent-700">
                <h3 class="text-lg font-display font-bold mb-2 text-accent-400">New Capabilities</h3>
                
                <div class="space-y-3">
                  <div class="capability-component pulse-animation">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-fast"></span>
                      <span class="capability-name">Real-time Analytics</span>
                    </div>
                  </div>
                  
                  <div class="capability-component pulse-animation" style="animation-delay: 0.5s">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-fast"></span>
                      <span class="capability-name">Copilot Integration</span>
                    </div>
                  </div>
                  
                  <div class="capability-component pulse-animation" style="animation-delay: 1s">
                    <div class="flex items-center">
                      <span class="status-indicator active-node blink-fast"></span>
                      <span class="capability-name">Low-Code Data Prep</span>
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
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

const activeTab = ref('full');
const connectors = ref([]);
const loading = ref(true);
const error = ref(null);
const selectedPipelines = ref([]);
const showAllConnections = ref(true); // Toggle between showing all or only selected

// API URL from environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// Refresh frequency data (simulated)
const refreshFrequencies = {
  hourly: { speed: 'fast', interval: '1h', class: 'beam-hourly' },
  daily: { speed: 'medium', interval: '24h', class: 'beam-daily' },
  weekly: { speed: 'slow', interval: '7d', class: 'beam-weekly' }
};

// Fetch connectors from backend
const fetchConnectors = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`${API_URL}/connectors`);
    connectors.value = response.data;
    
    // Assign simulated refresh frequencies
    connectors.value.forEach(connector => {
      // Randomly assign a refresh frequency for demo purposes
      const frequencies = Object.keys(refreshFrequencies);
      const randomFreq = frequencies[Math.floor(Math.random() * frequencies.length)];
      connector.refreshFrequency = refreshFrequencies[randomFreq];
      
      // Active state (initially all active)
      connector.active = true;
    });
    
  } catch (err) {
    console.error('Error fetching connectors:', err);
    error.value = 'Failed to fetch connector data. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Group connectors by technology
const connectorsByTech = computed(() => {
  const groups = {
    'Snowflake ADF': [],
    'Snowflake Airflow': [],
    'Snowflake Fivetran': []
  };
  
  connectors.value.forEach(connector => {
    if (groups[connector.technology]) {
      groups[connector.technology].push(connector);
    }
  });
  
  return groups;
});

// Fabric equivalent technologies
const fabricEquivalents = {
  'Snowflake ADF': { name: 'Data Factory', score: 92, status: 'active' },
  'Snowflake Airflow': { name: 'Fabric Pipelines', score: 94, status: 'active' },
  'Snowflake Fivetran': { name: 'OneLake Ingestion', score: 89, status: 'active' },
  'Data Warehousing': { name: 'Fabric Lakehouse', score: 91, status: 'active' },
  'Analytics': { name: 'Power BI Direct', score: 96, status: 'active' },
  'Data Science': { name: 'Fabric Notebooks', score: 88, status: 'active' }
};

// Computed mapping from source tech to destination tech
const techMapping = computed(() => {
  return {
    'Snowflake ADF': 'Data Factory',
    'Snowflake Airflow': 'Fabric Pipelines',
    'Snowflake Fivetran': 'OneLake Ingestion'
  };
});

// Toggle pipeline selection
const togglePipelineSelection = (pipeline) => {
  const index = selectedPipelines.value.findIndex(p => p.name === pipeline.name);
  if (index === -1) {
    selectedPipelines.value.push(pipeline);
  } else {
    selectedPipelines.value.splice(index, 1);
  }
};

// Toggle pipeline active state
const togglePipelineActive = (pipeline) => {
  pipeline.active = !pipeline.active;
};

// Check if a pipeline is selected
const isPipelineSelected = (pipeline) => {
  return selectedPipelines.value.some(p => p.name === pipeline.name);
};

// Toggle show all connections
const toggleConnectionsView = () => {
  showAllConnections.value = !showAllConnections.value;
};

// Check if a connector has a valid connection mapping
const isValidConnection = (connector) => {
  // A connector is valid if it has a technology that maps to a fabric equivalent
  return connector && connector.technology && techMapping.value[connector.technology];
};

// Get connection class based on refresh frequency
const getConnectionClass = (pipeline) => {
  if (!pipeline.refreshFrequency) return 'beam-daily'; // default
  return pipeline.refreshFrequency.class;
};

// Select all pipelines of a specific technology
const selectTechPipelines = (tech) => {
  const techPipelines = connectorsByTech.value[tech] || [];
  techPipelines.forEach(pipeline => {
    if (!isPipelineSelected(pipeline)) {
      selectedPipelines.value.push(pipeline);
    }
  });
};

// Deselect all pipelines
const deselectAllPipelines = () => {
  selectedPipelines.value = [];
};

// Toggle active state for all pipelines of a tech
const toggleTechActive = (tech) => {
  const techPipelines = connectorsByTech.value[tech] || [];
  // Check if all are active
  const allActive = techPipelines.every(p => p.active);
  // Toggle all to opposite state
  techPipelines.forEach(pipeline => {
    pipeline.active = !allActive;
  });
};

// For blinking/animation effects
const blinkStates = ref({});

const initBlinkStates = () => {
  // Initialize blinking states for nodes
  Object.keys(fabricEquivalents).forEach(key => {
    blinkStates.value[key] = {
      isActive: fabricEquivalents[key].status === 'active',
      blinkClass: 'blink-slow'
    };
  });
  
  // Start animation interval
  setInterval(() => {
    Object.keys(blinkStates.value).forEach(key => {
      if (blinkStates.value[key].isActive) {
        // Randomly change blink speed for active nodes
        blinkStates.value[key].blinkClass = Math.random() > 0.7 ? 'blink-fast' : 'blink-slow';
      }
    });
  }, 3000);
};

onMounted(() => {
  fetchConnectors();
  initBlinkStates();
});

// Add computed property to check if there are any active connections
const hasActiveConnection = computed(() => {
  return Object.values(connectorsByTech.value).some(tech => tech.some(p => p.active));
});

// Add method to determine if a connection is active
const isConnectionActive = (tech) => {
  const techPipelines = connectorsByTech.value[tech] || [];
  return techPipelines.some(p => p.active);
};

// Add method to get technology-specific classes
const getTechClasses = (tech) => {
  return {
    [`tech-${tech.toLowerCase()}`]: true,
    'active': isConnectionActive(tech)
  };
};
</script>

<style scoped>
/* Animation keyframes */
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes beam {
  0% {
    opacity: 0;
    transform: translateX(-100%);
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0;
    transform: translateX(100%);
  }
}

@keyframes nodePulse {
  0% {
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7);
  }
  70% {
    box-shadow: 0 0 0 5px rgba(59, 130, 246, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(59, 130, 246, 0);
  }
}

.bracket-container {
  @apply flex justify-between;
}

.bracket-teams {
  @apply flex flex-col;
}

.bracket-team {
  @apply flex justify-between items-center p-3 rounded-md border border-dark-700;
  background-color: #232B4F; /* dark-800 */
}

.snowflake-team {
  @apply border-secondary-700;
  background-color: rgba(35, 43, 79, 0.8); /* dark-800 with 80% opacity */
}

.snowflake-finalist {
  @apply border-secondary-600;
  background-color: rgba(18, 34, 47, 0.3); /* secondary-900 with 30% opacity */
}

.fabric-team {
  @apply border-accent-700;
  background-color: rgba(35, 43, 79, 0.8); /* dark-800 with 80% opacity */
}

.fabric-finalist {
  @apply border-accent-600;
  background-color: rgba(16, 45, 39, 0.3); /* accent-900 with 30% opacity */
}

.team-name {
  @apply font-medium;
}

.team-score {
  @apply text-sm bg-dark-900 rounded px-2 py-0.5;
}

.glass-effect {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .bracket-container {
    @apply flex-col items-center;
  }
  
  .bracket-container > div {
    @apply w-full max-w-lg mb-8;
  }
}

/* Partial Migration Styles */
.partial-component {
  @apply p-3 rounded border flex justify-between items-center;
}

.snowflake-component {
  @apply border-secondary-700;
  background-color: rgba(18, 34, 47, 0.2); /* secondary-900 with 20% opacity */
}

.fabric-component {
  @apply border-accent-700;
  background-color: rgba(16, 45, 39, 0.2); /* accent-900 with 20% opacity */
}

.component-icon {
  @apply mr-2 text-dark-300;
}

.snowflake-component .component-icon {
  @apply text-secondary-400;
}

.fabric-component .component-icon {
  @apply text-accent-400;
}

.component-name {
  @apply text-sm font-medium;
}

.component-benefit {
  @apply text-xs px-2 py-1 rounded;
}

.snowflake-component .component-benefit {
  @apply text-secondary-300;
  background-color: rgba(35, 68, 93, 0.3); /* secondary-800 with 30% opacity */
}

.fabric-component .component-benefit {
  @apply text-accent-300;
  background-color: rgba(32, 91, 77, 0.3); /* accent-800 with 30% opacity */
}

.data-bridge-component, .capability-component {
  @apply p-2 rounded border border-dark-600;
  background-color: rgba(55, 65, 81, 0.5); /* dark-700 with 50% opacity */
}

.bridge-name, .capability-name {
  @apply text-xs font-medium text-dark-300;
}

.bridge-direction {
  @apply text-xs font-bold text-gold-400;
}

.capability-dot {
  @apply h-2 w-2 rounded-full mr-2;
}

/* Status indicator */
.status-indicator {
  @apply h-2.5 w-2.5 rounded-full inline-block mr-2;
  box-shadow: 0 0 5px currentColor;
}

.active-node {
  @apply text-green-400;
}

.burnt-node {
  @apply text-red-900;
  opacity: 0.6;
}

.migrating-node {
  @apply text-yellow-500;
}

.selected-node {
  @apply text-gold-400;
}

/* Animation classes */
.blink-slow {
  animation: blink 3s infinite;
}

.blink-fast {
  animation: blink 1s infinite;
}

.pulse-animation {
  animation: pulse 2s infinite;
}

/* Status transitions */
.fade-out {
  transition: opacity 0.5s ease-out, filter 0.5s ease-out;
}

.inactive {
  opacity: 0.3;
  filter: grayscale(90%);
}

.active {
  opacity: 1;
  filter: grayscale(0%);
}

/* Connector lines and beams */
.connector-container {
  position: relative;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.connector-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background: #1e293b;
  right: -50%;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
  display: flex;
  align-items: center;
}

.connector-beam {
  position: absolute;
  width: 100%;
  height: 2px;
  top: 0;
  left: 0;
  z-index: 1;
}

.connector-pulse {
  position: absolute;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #64748b;
  z-index: 2;
}

.connector-pulse.start {
  left: -4px;
}

.connector-pulse.end {
  right: -4px;
}

.connector-pulse.active-pulse {
  animation: nodePulse 2s infinite;
}

.connection-label {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.6rem;
  background-color: rgba(15, 23, 42, 0.8);
  border-radius: 4px;
  padding: 2px 6px;
  color: #94a3b8;
  white-space: nowrap;
}

.beam-hourly .connection-beam {
  background: linear-gradient(90deg, transparent, #3b82f6, transparent);
  animation: beam 3s infinite linear;
}

.beam-daily .connection-beam {
  background: linear-gradient(90deg, transparent, #10b981, transparent);
  animation: beam 6s infinite linear;
}

.beam-weekly .connection-beam {
  background: linear-gradient(90deg, transparent, #f59e0b, transparent);
  animation: beam 10s infinite linear;
}

.connection-line.inactive .connection-beam {
  animation-play-state: paused;
  opacity: 0.3;
}

.connection-line.inactive .connection-pulse {
  background: #475569;
}

.pipeline-item {
  @apply p-2.5 rounded border border-dark-600 flex justify-between items-center transition-all duration-300 cursor-pointer;
  background-color: rgba(31, 41, 55, 0.4);
  position: relative;
  z-index: 1;
}

.pipeline-item:hover {
  @apply border-dark-500;
  background-color: rgba(31, 41, 55, 0.7);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.pipeline-item.selected {
  @apply border-gold-600;
  background-color: rgba(153, 109, 51, 0.2);
}

.tech-header {
  @apply flex items-center mb-3 p-2 rounded cursor-pointer transition-all duration-150;
}

.tech-header:hover {
  background-color: rgba(31, 41, 55, 0.4);
}

.tech-controls {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.tech-btn {
  @apply text-xs bg-dark-800 px-2 py-1 rounded border border-dark-600 ml-2 transition-all;
}

.tech-btn:hover {
  @apply border-dark-500 bg-dark-700;
}

.selector-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(31, 41, 55, 0.9);
  z-index: 40;
  border-radius: 0.375rem;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  pointer-events: none;
}

.pipeline-item:hover .selector-overlay {
  opacity: 1;
}

.action-btn {
  @apply text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg text-sm p-1.5 text-center inline-flex items-center;
  margin: 0 0.25rem;
}

.toggler {
  @apply bg-dark-700 rounded-md px-3 py-1 text-xs flex items-center;
  border: 1px solid rgba(148, 163, 184, 0.2);
  transition: all 0.2s ease;
}

.toggler:hover {
  border-color: rgba(148, 163, 184, 0.4);
}

/* Toggle switch */
.switch {
  position: relative;
  display: inline-block;
  width: 38px;
  height: 20px;
  margin-left: 8px;
}

.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #374151;
  transition: .4s;
  border-radius: 20px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #3B82F6;
}

input:focus + .slider {
  box-shadow: 0 0 1px #3B82F6;
}

input:checked + .slider:before {
  transform: translateX(18px);
}

.connector-list {
  max-height: 300px;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.1) transparent;
}

.connector-list::-webkit-scrollbar {
  width: 5px;
}

.connector-list::-webkit-scrollbar-track {
  background: transparent;
}

.connector-list::-webkit-scrollbar-thumb {
  background-color: rgba(255,255,255,0.1);
  border-radius: 20px;
}

/* Make connection lines more visible when selected */
.pipeline-item.selected ~ .connector-line,
.pipeline-item.selected + .connector-line {
  background: rgba(234, 179, 8, 0.2);
  height: 3px;
  z-index: 6;
}

/* Source and destination connection points */
.source-point, .destination-point {
  position: absolute;
  width: 2px;
  height: 2px;
  opacity: 0;
}

.source-point {
  right: -2px;
  top: 50%;
}

.destination-point {
  left: -2px;
  top: 50%;
}

/* Enhanced styles for active connection points */
.connection-point {
  position: absolute;
  width: 12px;  /* Increased from 10px */
  height: 12px;  /* Increased from 10px */
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.8);  /* Increased opacity */
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.8), 0 0 20px rgba(255, 255, 255, 0.4);  /* Enhanced glow */
  z-index: 6;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
}

.connection-point-source {
  right: -6px;  /* Adjusted for new size */
  top: 50%;
  transform: translateY(-50%);
}

.connection-point-destination {
  left: -6px;  /* Adjusted for new size */
  top: 50%;
  transform: translateY(-50%);
}

/* Enhanced styles for active connection points */
.connection-point.active {
  width: 14px;  /* Increased from 12px */
  height: 14px;  /* Increased from 12px */
  background-color: rgba(255, 255, 255, 0.95);  /* Increased opacity */
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.9), 0 0 30px rgba(255, 255, 255, 0.5);  /* Enhanced glow */
}

.connection-point-source.active {
  right: -7px;  /* Adjusted for new size */
}

.connection-point-destination.active {
  left: -7px;  /* Adjusted for new size */
}

/* Platform-specific connection point colors */
.tech-powerbi .connection-point {
  background-color: rgba(242, 201, 76, 0.9);  /* Enhanced PowerBI yellow */
  box-shadow: 0 0 10px rgba(242, 201, 76, 0.8), 0 0 20px rgba(242, 201, 76, 0.4);
}

.tech-snowflake .connection-point {
  background-color: rgba(42, 171, 238, 0.9);  /* Enhanced Snowflake blue */
  box-shadow: 0 0 10px rgba(42, 171, 238, 0.8), 0 0 20px rgba(42, 171, 238, 0.4);
}

.tech-fabric .connection-point {
  background-color: rgba(111, 76, 255, 0.9);  /* Enhanced Fabric purple */
  box-shadow: 0 0 10px rgba(111, 76, 255, 0.8), 0 0 20px rgba(111, 76, 255, 0.4);
}

/* Enhanced active connection points for each platform */
.tech-powerbi .connection-point.active {
  box-shadow: 0 0 15px rgba(242, 201, 76, 0.9), 0 0 30px rgba(242, 201, 76, 0.5);
}

.tech-snowflake .connection-point.active {
  box-shadow: 0 0 15px rgba(42, 171, 238, 0.9), 0 0 30px rgba(42, 171, 238, 0.5);
}

.tech-fabric .connection-point.active {
  box-shadow: 0 0 15px rgba(111, 76, 255, 0.9), 0 0 30px rgba(111, 76, 255, 0.5);
}

/* Add pulse effect for more visual appeal on active destination points */
@keyframes pulse {
  0% {
    transform: translateY(-50%) scale(1);
    opacity: 1;
  }
  50% {
    transform: translateY(-50%) scale(1.3);
    opacity: 0.7;
  }
  100% {
    transform: translateY(-50%) scale(1);
    opacity: 1;
  }
}

.connection-point-destination.active {
  animation: pulse 2s infinite ease-in-out;
}

.stack-section {
  margin-top: 2rem;
  padding: 1rem;
}

.stack-container {
  width: 100%;
  height: 700px;
  margin-top: 1rem;
  border-radius: 0.5rem;
  overflow: hidden;
}
</style> 