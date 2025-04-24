<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Data Quality Observability</h1>
      <p class="text-dark-400">Monitor connector freshness, data quality checks, and pipeline health</p>
    </div>

    <!-- Time Range Selector -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex space-x-4">
        <button class="btn-outline py-1.5 px-3">Last 24 hours</button>
        <button class="btn-outline py-1.5 px-3">Last 7 days</button>
        <button class="btn-primary py-1.5 px-3">Last 30 days</button>
        <button class="btn-outline py-1.5 px-3">Custom Range</button>
      </div>
      <button class="btn-outline py-1.5 flex items-center" @click="refreshData">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Refresh Data
      </button>
    </div>

    <!-- Data Quality Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Connector Health</h3>
        <div class="text-2xl font-bold font-display mb-2">92%</div>
        <div class="text-green-400 text-xs">+3% from last period</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Freshness Score</h3>
        <div class="text-2xl font-bold font-display mb-2">87%</div>
        <div class="text-yellow-400 text-xs">-2% from last period</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Quality Tests</h3>
        <div class="text-2xl font-bold font-display mb-2">562/583</div>
        <div class="text-green-400 text-xs">96.4% pass rate</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Avg Latency</h3>
        <div class="text-2xl font-bold font-display mb-2">13.5 min</div>
        <div class="text-green-400 text-xs">-2.1 min from last period</div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold">Data Freshness by Source</h3>
          <div class="flex space-x-2">
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Airflow</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Fivetran</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">ADF</button>
          </div>
        </div>
        <div class="h-64 bg-dark-700/50 rounded-lg flex items-center justify-center">
          <p class="text-dark-400">[Freshness Trend Chart - Placeholder]</p>
        </div>
      </div>
      
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold">Data Quality by Table</h3>
          <div class="flex space-x-2">
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Row Counts</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Schema</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Nulls</button>
          </div>
        </div>
        <div class="h-64 bg-dark-700/50 rounded-lg flex items-center justify-center">
          <p class="text-dark-400">[Quality Test Results Chart - Placeholder]</p>
        </div>
      </div>
    </div>

    <!-- Anomaly Detection Heatmap -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-6">Anomaly Detection</h2>
      <AnomalyHeatmapChart 
        :chart-data="anomalyData" 
        :loading="loading" 
        :error="error"
        @refresh="refreshAnomalyData"
      />
    </div>

    <!-- Schema Change Timeline -->
    <div class="mb-8">
      <h2 class="text-xl font-bold mb-6">Schema Change History</h2>
      <SchemaChangeTimeline 
        :timeline-data="schemaChangeData" 
        :loading="loading" 
        :error="error"
        @refresh="refreshSchemaChanges"
      />
    </div>

    <!-- Test Results Table -->
    <div class="mb-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">Recent Quality Test Results</h2>
        <div class="flex space-x-4">
          <select v-model="statusFilter" class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-1.5 focus:outline-none focus:border-primary-500 text-white text-sm">
            <option value="all">All Status</option>
            <option value="failed">Failed</option>
            <option value="warning">Warning</option>
            <option value="passed">Passed</option>
          </select>
        </div>
      </div>

      <TestResultsTable 
        :test-results="filteredTestResults" 
        :loading="loading" 
        :error="error"
        @refresh="refreshTestResults"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import SchemaChangeTimeline from '../components/SchemaChangeTimeline.vue';
import TestResultsTable from '../components/TestResultsTable.vue';
import AnomalyHeatmapChart from '../components/AnomalyHeatmapChart.vue';
import AIDataFlowTool from '../components/AIDataFlowTool.vue';

// State
const loading = ref(false);
const error = ref('');
const statusFilter = ref('all');

// Mock data
const testResults = ref([
  {
    id: 1,
    status: 'passed',
    table: 'customer_orders',
    test: 'not_null_id',
    timestamp: '2025-08-15T14:32:10',
    description: 'Checks that the id column in customer_orders table is not null'
  },
  {
    id: 2,
    status: 'warning',
    table: 'product_inventory',
    test: 'row_count_deviation',
    timestamp: '2025-08-15T14:31:45',
    description: 'Checks that row count has not decreased by more than 10%'
  },
  {
    id: 3,
    status: 'failed',
    table: 'transactions',
    test: 'referential_integrity',
    timestamp: '2025-08-15T14:30:22',
    description: 'Checks referential integrity between transactions and customers'
  },
  {
    id: 4,
    status: 'passed',
    table: 'marketing_campaigns',
    test: 'freshness_check',
    timestamp: '2025-08-15T14:29:18',
    description: 'Checks that data is no more than 24 hours old'
  },
  {
    id: 5,
    status: 'passed',
    table: 'financial_data',
    test: 'schema_changes',
    timestamp: '2025-08-15T14:28:04',
    description: 'Validates schema has not changed unexpectedly'
  }
]);

const schemaChangeData = ref([
  {
    id: 1,
    table: 'customer_orders',
    timestamp: '2025-08-10T09:15:30',
    changeType: 'added',
    field: 'customer_segment',
    dataType: 'VARCHAR(50)',
    description: 'Added customer segment field for marketing analytics'
  },
  {
    id: 2,
    table: 'product_inventory',
    timestamp: '2025-08-12T11:22:45',
    changeType: 'modified',
    field: 'price',
    oldValue: 'DECIMAL(8,2)',
    newValue: 'DECIMAL(10,2)',
    description: 'Expanded price precision to accommodate international currencies'
  },
  {
    id: 3,
    table: 'transactions',
    timestamp: '2025-08-14T15:07:12',
    changeType: 'added',
    field: 'payment_processor',
    dataType: 'VARCHAR(100)',
    description: 'Added payment processor tracking for financial reporting'
  },
  {
    id: 4,
    table: 'customer_orders',
    timestamp: '2025-08-15T10:33:18',
    changeType: 'removed',
    field: 'legacy_id',
    dataType: 'INTEGER',
    description: 'Removed deprecated legacy identifier'
  }
]);

const anomalyData = ref([
  {
    table: 'customer_orders',
    date: '2025-08-10',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'customer_orders',
    date: '2025-08-11',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'customer_orders',
    date: '2025-08-12',
    anomalyLevel: 1,
    details: 'Slight increase in NULL values'
  },
  {
    table: 'customer_orders',
    date: '2025-08-13',
    anomalyLevel: 2,
    details: 'Row count dropped by 15%'
  },
  {
    table: 'customer_orders',
    date: '2025-08-14',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'product_inventory',
    date: '2025-08-10',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'product_inventory',
    date: '2025-08-11',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'product_inventory',
    date: '2025-08-12',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'product_inventory',
    date: '2025-08-13',
    anomalyLevel: 3,
    details: 'Schema change detected with no notification'
  },
  {
    table: 'product_inventory',
    date: '2025-08-14',
    anomalyLevel: 2,
    details: 'Data pattern change in price column'
  },
  {
    table: 'transactions',
    date: '2025-08-10',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  },
  {
    table: 'transactions',
    date: '2025-08-11',
    anomalyLevel: 1,
    details: 'Unusual transaction volume pattern'
  },
  {
    table: 'transactions',
    date: '2025-08-12',
    anomalyLevel: 1,
    details: 'Continued unusual transaction pattern'
  },
  {
    table: 'transactions',
    date: '2025-08-13',
    anomalyLevel: 0,
    details: 'Pattern returned to normal'
  },
  {
    table: 'transactions',
    date: '2025-08-14',
    anomalyLevel: 0,
    details: 'No anomalies detected'
  }
]);

// Computed
const filteredTestResults = computed(() => {
  if (statusFilter.value === 'all') {
    return testResults.value;
  }
  return testResults.value.filter(result => result.status === statusFilter.value);
});

// Methods
const initCharts = () => {
  // Mock implementation
  console.log('Charts initialized for Data Quality Observability page');
};

const refreshData = () => {
  refreshTestResults();
  refreshSchemaChanges();
  refreshAnomalyData();
};

const refreshTestResults = () => {
  loading.value = true;
  error.value = '';
  
  // This would be a real API call in a production app
  setTimeout(() => {
    loading.value = false;
    // mock updated data
    console.log('Test results refreshed');
  }, 1000);
};

const refreshSchemaChanges = () => {
  loading.value = true;
  error.value = '';
  
  // This would be a real API call in a production app
  setTimeout(() => {
    loading.value = false;
    // mock updated data
    console.log('Schema changes refreshed');
  }, 1000);
};

const refreshAnomalyData = () => {
  loading.value = true;
  error.value = '';
  
  // This would be a real API call in a production app
  setTimeout(() => {
    loading.value = false;
    // mock updated data
    console.log('Anomaly data refreshed');
  }, 1000);
};

onMounted(() => {
  initCharts();
});
</script> 