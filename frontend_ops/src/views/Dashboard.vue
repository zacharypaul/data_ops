<template>
  <div>
    <h1 class="text-3xl font-display font-bold mb-6">Data Connector Dashboard</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <!-- Dashboard Cards -->
      <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 hover:border-primary-500 transition-colors shadow-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-dark-300 text-sm font-medium mb-1">Active Connectors</h3>
            <p class="text-2xl font-bold text-white">28<span class="text-sm text-dark-400 ml-1">/32</span></p>
          </div>
          <span class="text-primary-500 p-2 rounded-md bg-primary-500/10 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm11 1H6v8h8V6z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
        <div class="mt-4 h-1 w-full bg-dark-700 rounded-full overflow-hidden">
          <div class="h-full bg-primary-500 rounded-full" style="width: 87%"></div>
        </div>
      </div>

      <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 hover:border-secondary-500 transition-colors shadow-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-dark-300 text-sm font-medium mb-1">Freshness Score</h3>
            <p class="text-2xl font-bold text-white">94<span class="text-sm text-dark-400 ml-1">%</span></p>
          </div>
          <span class="text-secondary-500 p-2 rounded-md bg-secondary-500/10 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
        <div class="mt-4 h-1 w-full bg-dark-700 rounded-full overflow-hidden">
          <div class="h-full bg-secondary-500 rounded-full" style="width: 94%"></div>
        </div>
      </div>

      <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 hover:border-accent-500 transition-colors shadow-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-dark-300 text-sm font-medium mb-1">Quality Checks</h3>
            <p class="text-2xl font-bold text-white">582<span class="text-sm text-dark-400 ml-1">/612</span></p>
          </div>
          <span class="text-accent-500 p-2 rounded-md bg-accent-500/10 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
        <div class="mt-4 h-1 w-full bg-dark-700 rounded-full overflow-hidden">
          <div class="h-full bg-accent-500 rounded-full" style="width: 95%"></div>
        </div>
      </div>

      <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 hover:border-gold-500 transition-colors shadow-lg">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-dark-300 text-sm font-medium mb-1">Avg. Pipeline Runtime</h3>
            <p class="text-2xl font-bold text-white">42<span class="text-sm text-dark-400 ml-1">min</span></p>
          </div>
          <span class="text-gold-500 p-2 rounded-md bg-gold-500/10 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </span>
        </div>
        <div class="mt-4 h-1 w-full bg-dark-700 rounded-full overflow-hidden">
          <div class="h-full bg-gold-500 rounded-full" style="width: 68%"></div>
        </div>
      </div>
    </div>

    <!-- Alerts Section -->
    <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
      <h2 class="text-xl font-display font-bold mb-4">Data Quality Alerts</h2>

      <div class="space-y-4">
        <div class="p-4 rounded-md bg-primary-900/40 border border-primary-700 flex items-center">
          <div class="h-3 w-3 rounded-full bg-primary-500 mr-3"></div>
            <div>
            <h4 class="font-medium text-white">Stale Customer Data</h4>
            <p class="text-sm text-dark-300">Customer data hasn't been updated in the last 48 hours (Fivetran)</p>
              </div>
          <div class="ml-auto">
            <span class="px-2 py-1 text-xs rounded-full bg-primary-900 text-primary-300">WARNING</span>
          </div>
        </div>
        
        <div class="p-4 rounded-md bg-accent-900/40 border border-accent-700 flex items-center">
          <div class="h-3 w-3 rounded-full bg-accent-500 mr-3"></div>
            <div>
            <h4 class="font-medium text-white">Anomaly Detected</h4>
            <p class="text-sm text-dark-300">Orders table row count decreased by 15% (dbt test failure)</p>
              </div>
          <div class="ml-auto">
            <span class="px-2 py-1 text-xs rounded-full bg-accent-900 text-accent-300">CRITICAL</span>
          </div>
        </div>
        
        <div class="p-4 rounded-md bg-gold-900/40 border border-gold-700 flex items-center">
          <div class="h-3 w-3 rounded-full bg-gold-500 mr-3"></div>
            <div>
            <h4 class="font-medium text-white">Schema Change Detected</h4>
            <p class="text-sm text-dark-300">New column added to product_catalog table (Snowflake check)</p>
              </div>
          <div class="ml-auto">
            <span class="px-2 py-1 text-xs rounded-full bg-gold-900 text-gold-300">INFO</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Connector Health Table -->
    <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
      <h2 class="text-xl font-display font-bold mb-4">Top Connectors</h2>
      
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="border-b border-dark-700">
            <tr>
              <th class="text-left py-3 px-4 text-dark-400">Connector</th>
              <th class="text-left py-3 px-4 text-dark-400">Type</th>
              <th class="text-left py-3 px-4 text-dark-400">Last Refresh</th>
              <th class="text-left py-3 px-4 text-dark-400">Freshness</th>
              <th class="text-left py-3 px-4 text-dark-400">Quality</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-700">
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Customer Data</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-900/30 text-primary-400">
                  Fivetran
                </span>
              </td>
              <td class="py-3 px-4">3 hours ago</td>
              <td class="py-3 px-4">
                <div class="w-24 bg-dark-700 rounded-full h-2">
                  <div class="h-2 rounded-full bg-green-500" style="width: 98%"></div>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-400">
                  <span class="w-1.5 h-1.5 mr-1.5 rounded-full bg-green-400"></span>
                  100%
                </span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Sales Transactions</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-accent-900/30 text-accent-400">
                  Airflow
                </span>
              </td>
              <td class="py-3 px-4">30 minutes ago</td>
              <td class="py-3 px-4">
                <div class="w-24 bg-dark-700 rounded-full h-2">
                  <div class="h-2 rounded-full bg-green-500" style="width: 96%"></div>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-400">
                  <span class="w-1.5 h-1.5 mr-1.5 rounded-full bg-green-400"></span>
                  98%
                </span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Product Catalog</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-secondary-900/30 text-secondary-400">
                  ADF
                </span>
              </td>
              <td class="py-3 px-4">2 days ago</td>
              <td class="py-3 px-4">
                <div class="w-24 bg-dark-700 rounded-full h-2">
                  <div class="h-2 rounded-full bg-yellow-500" style="width: 72%"></div>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-900/30 text-yellow-400">
                  <span class="w-1.5 h-1.5 mr-1.5 rounded-full bg-yellow-400"></span>
                  85%
                </span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Marketing Campaigns</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gold-900/30 text-gold-400">
                  Lambda
                </span>
              </td>
              <td class="py-3 px-4">12 hours ago</td>
              <td class="py-3 px-4">
                <div class="w-24 bg-dark-700 rounded-full h-2">
                  <div class="h-2 rounded-full bg-green-500" style="width: 92%"></div>
                </div>
              </td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-400">
                  <span class="w-1.5 h-1.5 mr-1.5 rounded-full bg-green-400"></span>
                  97%
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="flex justify-end">
      <button class="btn-primary">View All Connectors</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Dashboard component with data connector focus
onMounted(() => {
  console.log('Data Connector Dashboard initialized');
});
</script> 