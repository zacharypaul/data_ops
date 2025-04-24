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
          />
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute right-3 top-2.5 text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
        <select class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white">
          <option value="">All Categories</option>
          <option value="ingestion">Ingestion</option>
          <option value="transformation">Transformation</option>
        </select>
        <select class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white">
          <option value="">All Platforms</option>
          <option value="snowflake">Snowflake</option>
          <option value="fabric">Microsoft Fabric</option>
          <option value="both">Dual Platform</option>
        </select>
      </div>
      <button class="btn-primary">+ Add Pipeline</button>
    </div>

    <!-- Inventory Table -->
    <div class="card overflow-hidden mb-8">
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="border-b border-dark-700">
            <tr>
              <th class="text-left py-3 px-4 text-dark-400">Name</th>
              <th class="text-left py-3 px-4 text-dark-400">Type</th>
              <th class="text-left py-3 px-4 text-dark-400">Technologies</th>
              <th class="text-left py-3 px-4 text-dark-400">Status</th>
              <th class="text-left py-3 px-4 text-dark-400">Last Run</th>
              <th class="text-left py-3 px-4 text-dark-400">Avg. Duration</th>
              <th class="text-left py-3 px-4 text-dark-400">Data Sync</th>
              <th class="text-left py-3 px-4 text-dark-400">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-700">
            <tr v-for="(pipeline, index) in pipelines" :key="index" class="hover:bg-dark-700/30">
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
                <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${pipeline.statusClass}`">
                  <span :class="`w-1.5 h-1.5 mr-1.5 rounded-full ${pipeline.dotClass}`"></span>
                  {{ pipeline.status }}
                </span>
              </td>
              <td class="py-3 px-4">{{ pipeline.lastRun }}</td>
              <td class="py-3 px-4">
                <div class="w-36 bg-dark-700 rounded-full h-2">
                  <div :class="`h-2 rounded-full ${pipeline.durationClass}`" :style="{ width: `${pipeline.durationPercentage}%` }"></div>
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
                  <button class="p-1 hover:text-secondary-500">
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
    <div class="flex justify-between items-center">
      <div class="text-dark-400">Showing 1-10 of 16 pipelines</div>
      <div class="flex space-x-2">
        <button class="btn-outline py-1.5 px-3">Previous</button>
        <button class="btn-primary py-1.5 px-3">Next</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const getSyncStatusClass = (status) => {
  if (status === 'Match') return 'bg-green-900/30 text-green-400';
  if (status === 'Partial') return 'bg-yellow-900/30 text-yellow-400';
  return 'bg-red-900/30 text-red-400';
};

const pipelines = ref([
  {
    name: 'Customer Data Sync',
    type: 'Ingestion',
    typeClass: 'bg-primary-900/30 text-primary-400',
    technologies: [
      { name: 'Airflow Meltano', class: 'bg-blue-900/30 text-blue-400' },
      { name: 'Snowflake', class: 'bg-cyan-900/30 text-cyan-400' }
    ],
    status: 'Running',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '10 min ago',
    duration: '45 min / 60 min',
    durationPercentage: 75,
    durationClass: 'bg-yellow-500',
    dataSync: {
      rowCount: 'Match',
      columnCount: 'Match',
      dateRange: 'Match'
    }
  },
  {
    name: 'Product Catalog ETL',
    type: 'Ingestion',
    typeClass: 'bg-primary-900/30 text-primary-400',
    technologies: [
      { name: 'Fivetran', class: 'bg-indigo-900/30 text-indigo-400' },
      { name: 'Snowflake', class: 'bg-cyan-900/30 text-cyan-400' },
      { name: 'Fabric', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Completed',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '2 hrs ago',
    duration: '18 min / 30 min',
    durationPercentage: 60,
    durationClass: 'bg-green-500',
    dataSync: {
      rowCount: 'Match',
      columnCount: 'Partial',
      dateRange: 'Match'
    }
  },
  {
    name: 'Sales Analytics',
    type: 'Transformation',
    typeClass: 'bg-accent-900/30 text-accent-400',
    technologies: [
      { name: 'Snowflake dbt', class: 'bg-cyan-900/30 text-cyan-400' }
    ],
    status: 'Completed',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '3 hrs ago',
    duration: '12 min / 20 min',
    durationPercentage: 60,
    durationClass: 'bg-green-500',
    dataSync: null
  },
  {
    name: 'Marketing Attribution',
    type: 'Transformation',
    typeClass: 'bg-accent-900/30 text-accent-400',
    technologies: [
      { name: 'Fabric PowerBI', class: 'bg-purple-900/30 text-purple-400' },
      { name: 'Snowflake', class: 'bg-cyan-900/30 text-cyan-400' }
    ],
    status: 'Failed',
    statusClass: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    dotClass: 'bg-red-400',
    lastRun: '6 hrs ago',
    duration: '35 min / 25 min',
    durationPercentage: 140,
    durationClass: 'bg-red-500',
    dataSync: {
      rowCount: 'Mismatch',
      columnCount: 'Partial',
      dateRange: 'Mismatch'
    }
  },
  {
    name: 'Log Data Collection',
    type: 'Ingestion',
    typeClass: 'bg-primary-900/30 text-primary-400',
    technologies: [
      { name: 'AWS Lambda', class: 'bg-orange-900/30 text-orange-400' }
    ],
    status: 'Idle',
    statusClass: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    dotClass: 'bg-blue-400',
    lastRun: '1 day ago',
    duration: '5 min / 10 min',
    durationPercentage: 50,
    durationClass: 'bg-green-500',
    dataSync: null
  },
  {
    name: 'Financial Reporting',
    type: 'Transformation',
    typeClass: 'bg-accent-900/30 text-accent-400',
    technologies: [
      { name: 'Snowflake Notebooks', class: 'bg-cyan-900/30 text-cyan-400' },
      { name: 'Fabric', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Scheduled',
    statusClass: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    dotClass: 'bg-yellow-400',
    lastRun: '1 day ago',
    duration: '40 min / 45 min',
    durationPercentage: 89,
    durationClass: 'bg-yellow-500',
    dataSync: {
      rowCount: 'Match',
      columnCount: 'Match',
      dateRange: 'Partial'
    }
  },
  {
    name: 'Inventory Forecast',
    type: 'Transformation',
    typeClass: 'bg-accent-900/30 text-accent-400',
    technologies: [
      { name: 'Snowflake Airflow', class: 'bg-cyan-900/30 text-cyan-400' },
      { name: 'Fabric ML', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Running',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '30 min ago',
    duration: '50 min / 60 min',
    durationPercentage: 83,
    durationClass: 'bg-yellow-500',
    dataSync: {
      rowCount: 'Match',
      columnCount: 'Match',
      dateRange: 'Match'
    }
  },
  {
    name: 'User Activity Data',
    type: 'Ingestion',
    typeClass: 'bg-primary-900/30 text-primary-400',
    technologies: [
      { name: 'Airflow Custom', class: 'bg-blue-900/30 text-blue-400' },
      { name: 'Snowflake', class: 'bg-cyan-900/30 text-cyan-400' },
      { name: 'Fabric', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Paused',
    statusClass: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
    dotClass: 'bg-orange-400',
    lastRun: '2 days ago',
    duration: '30 min / 35 min',
    durationPercentage: 86,
    durationClass: 'bg-yellow-500',
    dataSync: {
      rowCount: 'Partial',
      columnCount: 'Partial',
      dateRange: 'Match'
    }
  },
  {
    name: 'Customer 360',
    type: 'Transformation',
    typeClass: 'bg-accent-900/30 text-accent-400',
    technologies: [
      { name: 'Fabric Notebooks', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Completed',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '12 hrs ago',
    duration: '15 min / 20 min',
    durationPercentage: 75,
    durationClass: 'bg-yellow-500',
    dataSync: null
  },
  {
    name: 'Social Media Ingest',
    type: 'Ingestion',
    typeClass: 'bg-primary-900/30 text-primary-400',
    technologies: [
      { name: 'Azure Data Factory', class: 'bg-blue-900/30 text-blue-400' },
      { name: 'Fabric', class: 'bg-purple-900/30 text-purple-400' }
    ],
    status: 'Completed',
    statusClass: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    dotClass: 'bg-green-400',
    lastRun: '4 hrs ago',
    duration: '8 min / 15 min',
    durationPercentage: 53,
    durationClass: 'bg-green-500',
    dataSync: null
  }
]);
</script> 