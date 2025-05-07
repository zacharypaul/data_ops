<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Pipeline Management</h1>
      <p class="text-dark-400">Track and manage your data ingestion and transformation pipelines across platforms</p>
    </div>

    <!-- Actions -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex space-x-4">
        <div class="relative">
          <input 
            type="text"
            placeholder="Search pipelines..."
            class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 pr-10 focus:outline-none focus:border-primary-500 text-white w-80"
            v-model="searchQuery"
          />
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute right-3 top-2.5 text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select 
          class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white"
          v-model="selectedType"
        >
          <option value="">All Categories</option>
          <option value="ingestion">Ingestion</option>
          <option value="transformation">Transformation</option>
          <option value="orchestration">Orchestration</option>
          <option value="staging">File Staging</option>
          <option value="visualization">Visualization</option>
        </select>
        <select 
          class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white"
          v-model="selectedPlatform"
        >
          <option value="">All Platforms</option>
          <option value="snowflake">Snowflake</option>
          <option value="fabric">Fabric</option>
          <option value="sqlserver">SQL Server</option>
          <option value="aws">AWS</option>
          <option value="azure">Azure</option>
          <option value="powerbi">Power BI</option>
        </select>
        <select 
          class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white"
          v-model="selectedTechnology"
        >
          <option value="">All Technologies</option>
          <option value="S3">S3</option>
          <option value="Blob">Azure Blob</option>
          <option value="Airflow">AWS Airflow</option>
          <option value="Meltano">Meltano</option>
          <option value="DBT">Snowflake DBT</option>
          <option value="Snowpark">Snowflake Snowpark</option>
          <option value="ADF">Azure ADF</option>
          <option value="PowerBI">Power BI</option>
        </select>
      </div>
      <button class="btn-primary">+ Add Pipeline</button>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-10">
      <div class="text-primary-500">Loading connectors...</div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="text-center py-10">
      <div class="text-red-500">{{ error }}</div>
      <button @click="fetchConnectors" class="btn-primary mt-4">Retry</button>
    </div>

    <!-- Inventory Table -->
    <div v-else class="card overflow-hidden mb-8">
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="border-b border-dark-700">
            <tr>
              <th class="text-left py-3 px-4 text-dark-400">Name</th>
              <th class="text-left py-3 px-4 text-dark-400">Type</th>
              <th class="text-left py-3 px-4 text-dark-400">Technologies</th>
              <th class="text-left py-3 px-4 text-dark-400">Owner</th>
              <th class="text-left py-3 px-4 text-dark-400">Status</th>
              <th class="text-left py-3 px-4 text-dark-400">Last Run</th>
              <th class="text-left py-3 px-4 text-dark-400">Avg. Duration</th>
              <th class="text-left py-3 px-4 text-dark-400">Data Sync</th>
              <th class="text-left py-3 px-4 text-dark-400">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-700">
            <tr v-for="(pipeline, index) in paginatedPipelines" :key="index" class="hover:bg-dark-700/30">
              <td class="py-3 px-4">{{ pipeline.name }}</td>
              <td class="py-3 px-4">
                <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${pipeline.typeClass}`">
                  {{ pipeline.type }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span v-for="tech in pipeline.technologies" :key="tech.name" 
                    :class="`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium ${tech.class}`">
                    {{ tech.name }}
                  </span>
                </div>
              </td>
              <td class="py-3 px-4">
                <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getOwnerClass(pipeline.owner)}`">
                  {{ pipeline.owner }}
                </span>
              </td>
              <td class="py-3 px-4">
                <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${pipeline.statusClass}`">
                  <span :class="`w-1.5 h-1.5 mr-1.5 rounded-full ${pipeline.dotClass}`"></span>
                  {{ pipeline.status }}
                </span>
              </td>
              <td class="py-3 px-4">{{ pipeline.lastRun }}</td>
              <td class="py-3 px-4">
                <div class="w-36 bg-dark-700 rounded-full h-2 relative overflow-hidden">
                  <div :class="`h-2 rounded-full ${pipeline.durationClass}`" :style="{ width: `${Math.min(pipeline.durationPercentage, 100)}%` }"></div>
                </div>
                <div class="text-xs text-dark-400 mt-1">{{ pipeline.duration }}</div>
              </td>
              <td class="py-3 px-4">
                <div v-if="pipeline.dataSync" class="flex flex-col space-y-2">
                  <div class="flex items-center space-x-2">
                    <span :class="`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium ${getSyncStatusClass(pipeline.dataSync.rowCount)}`">
                      <span class="mr-1">Rows:</span> {{ pipeline.dataSync.rowCount }}
                    </span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span :class="`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium ${getSyncStatusClass(pipeline.dataSync.columnCount)}`">
                      <span class="mr-1">Columns:</span> {{ pipeline.dataSync.columnCount }}
                    </span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span :class="`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium ${getSyncStatusClass(pipeline.dataSync.dateRange)}`">
                      <span class="mr-1">Date Range:</span> {{ pipeline.dataSync.dateRange }}
                    </span>
                  </div>
                </div>
                <div v-else class="text-dark-400 text-xs italic">
                  Single platform
                </div>
              </td>
              <td class="py-3 px-4">
                <div class="flex space-x-2">
                  <button class="p-1 hover:text-primary-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button class="p-1 hover:text-secondary-500" @click="editPipeline(pipeline)">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button class="p-1 hover:text-accent-500">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="!loading && !error" class="flex justify-between items-center">
      <div class="text-dark-400">Showing {{ startIndex + 1 }}-{{ endIndex }} of {{ pipelines.length }} pipelines</div>
      <div class="flex space-x-2">
        <button 
          class="btn-outline py-1.5 px-3" 
          :disabled="currentPage === 1"
          @click="currentPage--"
        >Previous</button>
        <button 
          class="btn-primary py-1.5 px-3" 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
        >Next</button>
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-dark-900/80 flex items-center justify-center z-50">
      <div class="bg-dark-800 rounded-lg p-6 w-full max-w-md">
        <h2 class="text-xl font-semibold mb-4">Edit Pipeline</h2>
        
        <div v-if="formError" class="bg-red-900/30 text-red-400 p-3 rounded-md mb-4">
          {{ formError }}
        </div>
        
        <div class="mb-4">
          <label class="block text-dark-300 mb-2">Name</label>
          <input 
            type="text" 
            v-model="editedPipeline.name"
            class="w-full bg-dark-700 border border-dark-600 rounded-md p-2 focus:outline-none focus:border-primary-500"
          />
        </div>
        
        <div class="mb-4">
          <label class="block text-dark-300 mb-2">Type</label>
          <select 
            v-model="editedPipeline.type"
            class="w-full bg-dark-700 border border-dark-600 rounded-md p-2 focus:outline-none focus:border-primary-500"
          >
            <option value="ingestion">Ingestion</option>
            <option value="transformation">Transformation</option>
            <option value="orchestration">Orchestration</option>
            <option value="staging">File Staging</option>
            <option value="visualization">Visualization</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-dark-300 mb-2">Primary Category</label>
          <select 
            v-model="editedPipeline.primaryCategory"
            class="w-full bg-dark-700 border border-dark-600 rounded-md p-2 focus:outline-none focus:border-primary-500"
            @change="updateAvailableTechnologiesForCategory"
          >
            <option value="all">All Categories</option>
            <option value="staging">File Staging</option>
            <option value="warehouse">Data Warehouse</option>
            <option value="orchestration">Orchestration</option>
            <option value="visualization">Visualization</option>
          </select>
        </div>
        
        <div class="mb-4">
          <label class="block text-dark-300 mb-2">Owner</label>
          <select 
            v-model="editedPipeline.owner"
            class="w-full bg-dark-700 border border-dark-600 rounded-md p-2 focus:outline-none focus:border-primary-500"
          >
            <option value="twks">twks</option>
            <option value="ind">ind</option>
            <option value="zach">zach</option>
            <option value="other">other</option>
          </select>
        </div>
        
        <div class="mb-6">
          <label class="block text-dark-300 mb-2">Technologies</label>
          <div class="space-y-2 bg-dark-700 border border-dark-600 rounded-md p-3">
            <div 
              v-for="tech in filteredAvailableTechnologies" 
              :key="tech.id"
              class="flex items-center"
            >
              <label class="flex items-center space-x-2 cursor-pointer">
                <input 
                  type="checkbox" 
                  :checked="isTechnologySelected(tech.name)" 
                  @change="toggleTechnology(tech.name)"
                  class="rounded text-primary-500 focus:ring-primary-500 bg-dark-600 border-dark-500"
                />
                <span>{{ tech.name }}</span>
              </label>
            </div>
          </div>
          <p class="mt-1 text-xs text-dark-400">Select at least one technology. The first selected technology will be the primary one.</p>
        </div>
        
        <div class="flex justify-end space-x-3">
          <button 
            @click="cancelEdit"
            class="px-4 py-2 border border-dark-600 rounded-md hover:bg-dark-700"
          >
            Cancel
          </button>
          <button 
            @click="saveEditedPipeline"
            class="px-4 py-2 bg-primary-500 text-white rounded-md hover:bg-primary-600"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';

// Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';
const ITEMS_PER_PAGE = 10;

// State variables
const connectors = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const selectedType = ref('');
const selectedTechnology = ref('');
const selectedPlatform = ref('');
const currentPage = ref(1);

// Add new data properties for edit modal
const showEditModal = ref(false);
const editedPipeline = ref(null);
const formError = ref('');
const availableTechnologies = [
  // File staging
  { id: 's3', name: 'S3', type: 'staging', platform: 'aws' },
  { id: 'blob', name: 'Azure Blob', type: 'staging', platform: 'azure' },
  
  // Data warehouses
  { id: 'snowflake', name: 'Snowflake', type: 'warehouse', platform: 'snowflake' },
  { id: 'fabric', name: 'Fabric', type: 'warehouse', platform: 'fabric' },
  { id: 'sqlserver', name: 'SQL Server', type: 'warehouse', platform: 'sqlserver' },
  
  // Orchestration
  { id: 'airflow', name: 'AWS Airflow', type: 'orchestration', platform: 'aws' },
  { id: 'meltano', name: 'Meltano', type: 'orchestration', platform: 'aws' },
  { id: 'dbt', name: 'Snowflake DBT', type: 'orchestration', platform: 'snowflake' },
  { id: 'snowpark', name: 'Snowflake Snowpark', type: 'orchestration', platform: 'snowflake' },
  { id: 'adf', name: 'Azure ADF', type: 'orchestration', platform: 'azure' },
  
  // Visualization
  { id: 'powerbi', name: 'Power BI', type: 'visualization', platform: 'powerbi' },
];

// Status and styling utilities
const getSyncStatusClass = (status) => {
  if (status === 'Match') return 'bg-green-900/30 text-green-400';
  if (status === 'Partial') return 'bg-yellow-900/30 text-yellow-400';
  return 'bg-red-900/30 text-red-400';
};

// Generate random status and metrics for each connector
const generateRandomStatusAndMetrics = (connector) => {
  const statuses = ['Running', 'Completed', 'Failed', 'Idle', 'Scheduled', 'Paused'];
  const syncStatuses = ['Match', 'Partial', 'Mismatch'];
  
  // Determine the type based on the connector's category from CSV
  let connectorType = connector.type;
  
  // If we have a category field, use that for more accurate classification
  if (connector.category) {
    if (connector.category === 'orchestration') {
      connectorType = 'Orchestration';
    } else if (connector.category === 'ingestion') {
      connectorType = 'Ingestion';
    } else if (connector.category === 'staging') {
      connectorType = 'File Staging';
    } else if (connector.category === 'visualization') {
      connectorType = 'Visualization';
    }
  }
  
  const randomStatus = statuses[Math.floor(Math.random() * statuses.length)];
  
  // Create technologies array
  const technologies = [];
  
  // Add the main technology
  const mainTech = { 
    name: connector.technology, 
    class: '' 
  };
  
  // Get platform from CSV or extract from technology
  const platform = connector.platform || '';
  const tech = connector.technology?.toLowerCase() || '';
  
  // Assign color classes based on technology groups
  if (platform === 'aws' || tech.includes('airflow') || tech.includes('meltano')) {
    mainTech.class = 'bg-blue-900/30 text-blue-400';
  } else if (platform === 'snowflake' || tech.includes('snowflake') || tech.includes('dbt') || tech.includes('snowpark')) {
    mainTech.class = 'bg-cyan-900/30 text-cyan-400';
  } else if (platform === 'azure' || tech.includes('adf') || tech.includes('blob')) {
    mainTech.class = 'bg-orange-900/30 text-orange-400';
  } else if (tech.includes('s3')) {
    mainTech.class = 'bg-yellow-900/30 text-yellow-400';
  } else if (platform === 'powerbi' || platform === 'fabric' || tech.includes('powerbi') || tech.includes('fabric')) {
    mainTech.class = 'bg-purple-900/30 text-purple-400';
  } else if (platform === 'sqlserver' || tech.includes('sqlserver')) {
    mainTech.class = 'bg-indigo-900/30 text-indigo-400';
  } else {
    mainTech.class = 'bg-gray-900/30 text-gray-400';
  }
  
  technologies.push(mainTech);
  
  // Add secondary technology if it exists in the CSV
  if (connector.secondary_tech && connector.secondary_tech !== '') {
    let secondaryClass = 'bg-gray-900/30 text-gray-400';
    
    if (connector.secondary_tech === 'meltano') {
      secondaryClass = 'bg-green-900/30 text-green-400';
    } else if (connector.secondary_tech === 'snowpark') {
      secondaryClass = 'bg-cyan-900/30 text-cyan-400';
    } else if (connector.secondary_tech === 's3') {
      secondaryClass = 'bg-yellow-900/30 text-yellow-400';
    } else if (connector.secondary_tech === 'blob') {
      secondaryClass = 'bg-orange-900/30 text-orange-400';
    } else if (connector.secondary_tech === 'custom_scripts') {
      secondaryClass = 'bg-gray-900/30 text-gray-400';
    }
    
    technologies.push({
      name: connector.secondary_tech.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      class: secondaryClass
    });
  }
  
  // Add warehouse/destination if it exists in the CSV
  if (connector.warehouse && connector.warehouse !== '') {
    let warehouseClass = 'bg-gray-900/30 text-gray-400';
    
    if (connector.warehouse === 'snowflake') {
      warehouseClass = 'bg-cyan-900/30 text-cyan-400';
    } else if (connector.warehouse === 'fabric') {
      warehouseClass = 'bg-purple-900/30 text-purple-400';
    } else if (connector.warehouse === 'sqlserver') {
      warehouseClass = 'bg-indigo-900/30 text-indigo-400';
    }
    
    technologies.push({
      name: connector.warehouse.charAt(0).toUpperCase() + connector.warehouse.slice(1),
      class: warehouseClass
    });
  }
  
  // Type styling
  let typeClass = 'bg-primary-900/30 text-primary-400';
  if (connectorType === 'Transformation') {
    typeClass = 'bg-accent-900/30 text-accent-400';
  } else if (connectorType === 'Orchestration') {
    typeClass = 'bg-blue-900/30 text-blue-400';
  } else if (connectorType === 'File Staging') {
    typeClass = 'bg-yellow-900/30 text-yellow-400';
  } else if (connectorType === 'Visualization') {
    typeClass = 'bg-purple-900/30 text-purple-400';
  }
  
  // Status styling
  let statusClass = 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
  let dotClass = 'bg-blue-400';
  
  if (randomStatus === 'Running') {
    statusClass = 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
    dotClass = 'bg-green-400';
  } else if (randomStatus === 'Completed') {
    statusClass = 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400';
    dotClass = 'bg-green-400';
  } else if (randomStatus === 'Failed') {
    statusClass = 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400';
    dotClass = 'bg-red-400';
  } else if (randomStatus === 'Scheduled') {
    statusClass = 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400';
    dotClass = 'bg-yellow-400';
  } else if (randomStatus === 'Paused') {
    statusClass = 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400';
    dotClass = 'bg-orange-400';
  } else if (randomStatus === 'Idle') {
    statusClass = 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400';
    dotClass = 'bg-blue-400';
  }
  
  // Duration metrics
  const actualDuration = Math.floor(Math.random() * 60) + 5; // 5-65 min
  const targetDuration = Math.floor(Math.random() * 40) + 20; // 20-60 min
  const durationPercentage = Math.min(Math.round((actualDuration / targetDuration) * 100), 150);
  
  let durationClass = 'bg-green-500';
  if (durationPercentage > 90) durationClass = 'bg-yellow-500';
  if (durationPercentage > 110) durationClass = 'bg-red-500';
  
  // Data sync metrics
  let dataSync = null;
  
  // Add data sync info for cross-platform integrations
  if (connector.warehouse && 
      ((connector.platform && connector.platform !== connector.warehouse) || 
       (connector.technology && !connector.technology.toLowerCase().includes(connector.warehouse)))) {
    dataSync = {
      rowCount: syncStatuses[Math.floor(Math.random() * syncStatuses.length)],
      columnCount: syncStatuses[Math.floor(Math.random() * syncStatuses.length)],
      dateRange: syncStatuses[Math.floor(Math.random() * syncStatuses.length)]
    };
  }
  
  // Last run time
  const times = ['10 min ago', '30 min ago', '1 hr ago', '2 hrs ago', '4 hrs ago', '1 day ago'];
  const randomTimeIndex = Math.floor(Math.random() * times.length);
  
  return {
    name: connector.name,
    type: connectorType,
    typeClass,
    technologies: technologies,
    owner: connector.owner || 'twks',
    platform: connector.platform || '',
    category: connector.category || '',
    warehouse: connector.warehouse || '',
    secondary_tech: connector.secondary_tech || '',
    status: randomStatus,
    statusClass,
    dotClass,
    lastRun: times[randomTimeIndex],
    duration: `${actualDuration} min / ${targetDuration} min`,
    durationPercentage,
    durationClass,
    dataSync
  };
};

// Fetch connectors from backend
const fetchConnectors = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`${API_URL}/connectors`);
    
    // Map the connector data with random status and metrics
    connectors.value = response.data.map(connector => generateRandomStatusAndMetrics(connector));
    
  } catch (err) {
    console.error('Error fetching connectors:', err);
    error.value = 'Failed to fetch connector data. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Filtered pipelines based on search and filters
const filteredPipelines = computed(() => {
  let results = connectors.value;
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    results = results.filter(p => 
      p.name.toLowerCase().includes(query) || 
      p.technologies.some(t => t.name.toLowerCase().includes(query))
    );
  }
  
  // Apply type filter
  if (selectedType.value) {
    results = results.filter(p => p.type.toLowerCase().includes(selectedType.value.toLowerCase()));
  }
  
  // Apply platform filter
  if (selectedPlatform.value) {
    results = results.filter(p => 
      p.technologies.some(t => t.name.toLowerCase().includes(selectedPlatform.value.toLowerCase()))
    );
  }
  
  // Apply technology filter
  if (selectedTechnology.value) {
    results = results.filter(p => 
      p.technologies.some(t => t.name.includes(selectedTechnology.value))
    );
  }
  
  return results;
});

// Pagination computed properties
const pipelines = computed(() => filteredPipelines.value);

const totalPages = computed(() => Math.ceil(pipelines.value.length / ITEMS_PER_PAGE));

const startIndex = computed(() => (currentPage.value - 1) * ITEMS_PER_PAGE);

const endIndex = computed(() => {
  const end = startIndex.value + ITEMS_PER_PAGE;
  return end > pipelines.value.length ? pipelines.value.length : end;
});

const paginatedPipelines = computed(() => {
  return pipelines.value.slice(startIndex.value, endIndex.value);
});

// Reset pagination when filters change
const resetPagination = () => {
  currentPage.value = 1;
};

// Watch for filter changes to reset pagination
watch([searchQuery, selectedType, selectedTechnology, selectedPlatform], resetPagination);

// Add new methods for edit functionality
const editPipeline = (pipeline) => {
  // Extract all technologies from the pipeline
  const technologies = pipeline.technologies.map(tech => tech.name);
  
  // Determine primary category based on type
  let primaryCategory = 'all';
  if (pipeline.type === 'File Staging') primaryCategory = 'staging';
  else if (pipeline.type === 'Orchestration') primaryCategory = 'orchestration';
  else if (pipeline.type === 'Visualization') primaryCategory = 'visualization';
  else if (technologies.some(t => t.includes('Snowflake') || t.includes('Fabric') || t.includes('SQL Server'))) {
    primaryCategory = 'warehouse';
  }
  
  // Make a copy of the pipeline to edit
  editedPipeline.value = {
    name: pipeline.name,
    type: pipeline.type.toLowerCase(),
    technologies: technologies,
    owner: pipeline.owner || 'twks',
    primaryCategory: primaryCategory,
    originalName: pipeline.name // Keep track of original name for update
  };
  showEditModal.value = true;
};

const saveEditedPipeline = async () => {
  formError.value = '';
  
  if (!editedPipeline.value.name || !editedPipeline.value.type || 
      editedPipeline.value.technologies.length === 0 || !editedPipeline.value.owner) {
    formError.value = 'All fields are required. At least one technology must be selected.';
    return;
  }
  
  try {
    // Get the platform and category from the primary technology
    const primaryTech = editedPipeline.value.technologies[0];
    const techInfo = availableTechnologies.find(t => t.name === primaryTech);
    
    // Get the secondary technology if available (any tech that's not primary and not a warehouse)
    const secondaryTechs = editedPipeline.value.technologies.filter(t => 
      t !== primaryTech && 
      !['Snowflake', 'Fabric', 'SQL Server'].includes(t)
    );
    const secondaryTech = secondaryTechs.length > 0 ? secondaryTechs[0].toLowerCase().replace(' ', '_') : '';
    
    // Get the warehouse if available (look for Snowflake, Fabric, or SQL Server)
    const warehouseTechs = editedPipeline.value.technologies.filter(t => 
      ['Snowflake', 'Fabric', 'SQL Server'].includes(t)
    );
    const warehouse = warehouseTechs.length > 0 ? warehouseTechs[0].toLowerCase() : '';
    
    // Format the data for the backend with all the new fields
    const backendData = {
      name: editedPipeline.value.name,
      type: editedPipeline.value.type,
      technology: primaryTech,
      owner: editedPipeline.value.owner,
      category: techInfo?.type || editedPipeline.value.type.toLowerCase(),
      platform: techInfo?.platform || '',
      secondary_tech: secondaryTech,
      warehouse: warehouse === 'sql server' ? 'sqlserver' : warehouse,
      originalName: editedPipeline.value.originalName
    };
    
    const response = await axios.put(`${API_URL}/connectors`, backendData);
    
    // Close modal
    showEditModal.value = false;
    
    // Refresh data
    await fetchConnectors();
    
  } catch (err) {
    console.error('Error updating pipeline:', err);
    formError.value = 'Failed to update pipeline. Please try again.';
  }
};

// Technology selection helpers
const isTechnologySelected = (technology) => {
  return editedPipeline.value && editedPipeline.value.technologies.includes(technology);
};

const toggleTechnology = (technology) => {
  if (!editedPipeline.value) return;
  
  const index = editedPipeline.value.technologies.indexOf(technology);
  if (index === -1) {
    // Add technology
    editedPipeline.value.technologies.push(technology);
  } else {
    // Remove technology if it's not the last one
    if (editedPipeline.value.technologies.length > 1) {
      editedPipeline.value.technologies.splice(index, 1);
    }
  }
};

const cancelEdit = () => {
  showEditModal.value = false;
  editedPipeline.value = null;
  formError.value = '';
};

// Helper function for owner styling
const getOwnerClass = (owner) => {
  if (owner === 'twks') return 'bg-green-900/30 text-green-400';
  if (owner === 'ind') return 'bg-blue-900/30 text-blue-400';
  if (owner === 'zach') return 'bg-purple-900/30 text-purple-400';
  return 'bg-gray-900/30 text-gray-400';
};

// Technology filtering by category
const filteredAvailableTechnologies = computed(() => {
  if (!editedPipeline.value || editedPipeline.value.primaryCategory === 'all') {
    return availableTechnologies;
  }
  
  return availableTechnologies.filter(tech => 
    tech.type === editedPipeline.value.primaryCategory
  );
});

// Update pipeline edit methods
const updateAvailableTechnologiesForCategory = () => {
  // Reset technologies if changing categories
  if (editedPipeline.value) {
    const currentTechnologies = [...editedPipeline.value.technologies];
    const keptTechnologies = currentTechnologies.filter(tech => {
      const matchingTech = availableTechnologies.find(t => t.name === tech);
      return matchingTech && (matchingTech.type === editedPipeline.value.primaryCategory || editedPipeline.value.primaryCategory === 'all');
    });
    
    editedPipeline.value.technologies = keptTechnologies.length ? keptTechnologies : [];
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchConnectors();
});
</script> 