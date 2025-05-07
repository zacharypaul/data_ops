<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-display font-bold">Data Connector Dashboard</h1>
      
      <button 
        @click="refreshDashboard" 
        class="flex items-center space-x-1 px-3 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors"
        :disabled="isLoading"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          class="h-4 w-4" 
          :class="{ 'animate-spin': isLoading }"
          viewBox="0 0 20 20" 
          fill="currentColor"
        >
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
        <span>{{ isLoading ? 'Refreshing...' : 'Refresh' }}</span>
      </button>
    </div>
    
    <!-- Error message -->
    <div v-if="loadingError" class="mb-6 p-4 bg-red-900/30 border border-red-700 rounded-md text-red-200">
      {{ loadingError }}
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading && !metrics.activeConnectors.current" class="flex justify-center py-32">
      <div class="flex flex-col items-center">
        <svg class="animate-spin h-10 w-10 text-primary-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <p class="text-dark-300">Loading dashboard...</p>
      </div>
    </div>
    
    <div v-else>
      <!-- Dashboard Cards Component -->
      <DashboardCards :metrics="metrics" />
      
      <!-- Dashboard Navigation Tabs -->
      <div class="border-b border-dark-700 mb-6">
        <nav class="flex space-x-6">
          <button
            @click="activeTab = 'overview'"
            :class="[
              'py-2 px-1 font-medium text-sm border-b-2 -mb-px transition-colors',
              activeTab === 'overview'
                ? 'border-primary-500 text-primary-400'
                : 'border-transparent text-dark-300 hover:text-white'
            ]"
          >
            Overview
          </button>
          <button
            @click="activeTab = 'trends'"
            :class="[
              'py-2 px-1 font-medium text-sm border-b-2 -mb-px transition-colors',
              activeTab === 'trends'
                ? 'border-primary-500 text-primary-400'
                : 'border-transparent text-dark-300 hover:text-white'
            ]"
          >
            Historical Trends
          </button>
          <button
            @click="activeTab = 'lineage'"
            :class="[
              'py-2 px-1 font-medium text-sm border-b-2 -mb-px transition-colors',
              activeTab === 'lineage'
                ? 'border-primary-500 text-primary-400'
                : 'border-transparent text-dark-300 hover:text-white'
            ]"
          >
            Data Lineage
          </button>
        </nav>
      </div>
      
      <!-- Tab Content -->
      <div v-if="activeTab === 'overview'">
        <!-- Alerts Section Component -->
        <QualityAlerts :alerts="alerts" />
        
        <!-- Connector Health Table Component -->
        <ConnectorTable 
          :connectors="connectors" 
          @refresh-connector="triggerConnectorRefresh"
          @select-connector="selectConnector"
        />
      </div>
      
      <div v-else-if="activeTab === 'trends'">
        <!-- Historical Trends Component -->
        <HistoricalTrends :connector-id="selectedConnectorId" />
      </div>
      
      <div v-else-if="activeTab === 'lineage'">
        <!-- Data Lineage Visualization Component -->
        <DataLineage />
      </div>
  
      <div class="flex justify-end mt-6">
        <button 
          class="btn-primary"
          @click="viewAllConnectors"
        >
          View All Connectors
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DashboardCards from '@/components/dashboard/DashboardCards.vue';
import QualityAlerts from '@/components/dashboard/QualityAlerts.vue';
import ConnectorTable from '@/components/dashboard/ConnectorTable.vue';
import HistoricalTrends from '@/components/dashboard/HistoricalTrends.vue';
import DataLineage from '@/components/dashboard/DataLineage.vue';
import DashboardApi from '@/services/DashboardApi';

// Dashboard state
const isLoading = ref(true);
const loadingError = ref(null);
const selectedConnectorId = ref(null);
const activeTab = ref('overview');

// Dashboard metrics data
const metrics = ref({
  activeConnectors: { current: 0, total: 0, percentage: 0 },
  freshnessScore: { value: 0, percentage: 0 },
  qualityChecks: { passed: 0, total: 0, percentage: 0 },
  pipelineRuntime: { value: 0, unit: 'min', percentage: 0 }
});

// Quality alerts data
const alerts = ref([]);

// Connector data
const connectors = ref([]);

// Methods
const viewAllConnectors = () => {
  console.log('Navigating to all connectors view');
  // Will be implemented for navigation
};

// Select a connector for detailed view
const selectConnector = (connectorId) => {
  selectedConnectorId.value = connectorId;
  // Automatically switch to trends tab when a connector is selected
  activeTab.value = 'trends';
};

// Refresh dashboard data
const refreshDashboard = async () => {
  isLoading.value = true;
  loadingError.value = null;
  
  try {
    await loadDashboardData();
  } catch (error) {
    console.error('Error refreshing dashboard:', error);
    loadingError.value = 'Failed to refresh dashboard data. Please try again.';
  } finally {
    isLoading.value = false;
  }
};

// Load dashboard data from API
const loadDashboardData = async () => {
  try {
    // Load all data in parallel for better performance
    const [metricsData, alertsData, connectorsData] = await Promise.all([
      DashboardApi.getDashboardMetrics(),
      DashboardApi.getQualityAlerts(),
      DashboardApi.getConnectors()
    ]);
    
    // Update the reactive state with the fetched data
    metrics.value = metricsData;
    alerts.value = alertsData;
    connectors.value = connectorsData;
    
  } catch (error) {
    console.error('Error loading dashboard data:', error);
    loadingError.value = 'Failed to load dashboard data. Please try again.';
    throw error;
  }
};

// Trigger data refresh for a specific connector
const triggerConnectorRefresh = async (connectorId) => {
  try {
    const result = await DashboardApi.refreshConnector(connectorId);
    // We could show a success message or update the UI accordingly
    console.log('Refresh triggered:', result);
    
    // Optionally refresh the connector data after a delay
    setTimeout(() => {
      DashboardApi.getConnectors().then(data => {
        connectors.value = data;
      });
    }, 2000);
    
    return result;
  } catch (error) {
    console.error('Error refreshing connector:', error);
    throw error;
  }
};

onMounted(() => {
  console.log('Data Connector Dashboard initialized');
  loadDashboardData().finally(() => {
    isLoading.value = false;
  });
});
</script>

<style scoped>
.btn-primary {
  @apply px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors;
}
</style> 