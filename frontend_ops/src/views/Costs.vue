<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Cost Management</h1>
      <p class="text-dark-400">Track and optimize expenses across data platforms and pipelines</p>
    </div>

    <!-- Time Range Selector -->
    <div class="flex justify-between items-center mb-6">
      <div class="flex space-x-4">
        <button class="btn-outline py-1.5 px-3">Last 30 days</button>
        <button class="btn-primary py-1.5 px-3">Last Quarter</button>
        <button class="btn-outline py-1.5 px-3">Year to Date</button>
        <button class="btn-outline py-1.5 px-3">Custom Range</button>
      </div>
      <div class="flex space-x-4">
        <select class="bg-dark-800 border border-dark-700 rounded-lg px-4 py-2 focus:outline-none focus:border-primary-500 text-white">
          <option value="">All Platforms</option>
          <option value="snowflake">Snowflake</option>
          <option value="fabric">Microsoft Fabric</option>
          <option value="other">Other Services</option>
        </select>
        <button class="btn-outline py-1.5 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
          </svg>
          Export
        </button>
      </div>
    </div>

    <!-- Cost Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">
      <div class="card-gradient col-span-2">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Total Expenses (QTD)</h3>
        <div class="text-2xl font-bold font-display mb-2">$42,856</div>
        <div class="text-red-400 text-xs">+12% from previous quarter</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Snowflake</h3>
        <div class="text-2xl font-bold font-display mb-2">$28,450</div>
        <div class="text-dark-400 text-xs">66% of total</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Fabric</h3>
        <div class="text-2xl font-bold font-display mb-2">$9,875</div>
        <div class="text-green-400 text-xs">23% of total</div>
      </div>
      
      <div class="card-gradient">
        <h3 class="text-dark-400 text-sm font-medium mb-1">Other</h3>
        <div class="text-2xl font-bold font-display mb-2">$4,531</div>
        <div class="text-dark-400 text-xs">11% of total</div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold">Cost Trends</h3>
          <div class="flex space-x-2">
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Daily</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Weekly</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">Monthly</button>
          </div>
        </div>
        <div class="h-64 bg-dark-700/50 rounded-lg flex items-center justify-center">
          <p class="text-dark-400">[Cost Trend Line Chart - Placeholder]</p>
        </div>
      </div>
      
      <div class="card">
        <div class="flex justify-between items-center mb-4">
          <h3 class="font-bold">Cost Distribution</h3>
          <div class="flex space-x-2">
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">By Platform</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">By Pipeline</button>
            <button class="text-dark-400 hover:text-white px-2 py-1 text-sm">By Type</button>
          </div>
        </div>
        <div class="h-64 bg-dark-700/50 rounded-lg flex items-center justify-center">
          <p class="text-dark-400">[Cost Distribution Pie Chart - Placeholder]</p>
        </div>
      </div>
    </div>

    <!-- Top Expensive Pipelines -->
    <div class="card overflow-hidden mb-8">
      <div class="flex justify-between items-center mb-4 px-6 pt-6">
        <h3 class="font-bold">Top Pipelines by Cost</h3>
        <button class="text-primary-500 hover:text-primary-400 text-sm">View All</button>
      </div>
      <div class="overflow-x-auto">
        <table class="min-w-full">
          <thead class="border-b border-dark-700">
            <tr>
              <th class="text-left py-3 px-4 text-dark-400">Pipeline</th>
              <th class="text-left py-3 px-4 text-dark-400">Platform</th>
              <th class="text-left py-3 px-4 text-dark-400">Cost (QTD)</th>
              <th class="text-left py-3 px-4 text-dark-400">vs. Previous</th>
              <th class="text-left py-3 px-4 text-dark-400">Avg. Per Run</th>
              <th class="text-left py-3 px-4 text-dark-400">Cost Drivers</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-700">
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Customer Data Sync</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-cyan-900/30 text-cyan-400">Snowflake</span>
                </div>
              </td>
              <td class="py-3 px-4 font-medium">$8,540</td>
              <td class="py-3 px-4">
                <span class="text-red-400">+15%</span>
              </td>
              <td class="py-3 px-4">$85</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-dark-700/70">Compute</span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Product Catalog ETL</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-cyan-900/30 text-cyan-400">Snowflake</span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-purple-900/30 text-purple-400">Fabric</span>
                </div>
              </td>
              <td class="py-3 px-4 font-medium">$6,320</td>
              <td class="py-3 px-4">
                <span class="text-green-400">-8%</span>
              </td>
              <td class="py-3 px-4">$58</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-dark-700/70">Storage</span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Financial Reporting</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-cyan-900/30 text-cyan-400">Snowflake</span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-purple-900/30 text-purple-400">Fabric</span>
                </div>
              </td>
              <td class="py-3 px-4 font-medium">$5,920</td>
              <td class="py-3 px-4">
                <span class="text-red-400">+22%</span>
              </td>
              <td class="py-3 px-4">$145</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-dark-700/70">XL Warehouse</span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Marketing Attribution</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-purple-900/30 text-purple-400">Fabric</span>
                </div>
              </td>
              <td class="py-3 px-4 font-medium">$4,780</td>
              <td class="py-3 px-4">
                <span class="text-red-400">+12%</span>
              </td>
              <td class="py-3 px-4">$78</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-dark-700/70">Compute Hours</span>
              </td>
            </tr>
            <tr class="hover:bg-dark-700/30">
              <td class="py-3 px-4">Inventory Forecast</td>
              <td class="py-3 px-4">
                <div class="flex flex-wrap gap-1">
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-cyan-900/30 text-cyan-400">Snowflake</span>
                  <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-purple-900/30 text-purple-400">Fabric</span>
                </div>
              </td>
              <td class="py-3 px-4 font-medium">$3,840</td>
              <td class="py-3 px-4">
                <span class="text-green-400">-5%</span>
              </td>
              <td class="py-3 px-4">$120</td>
              <td class="py-3 px-4">
                <span class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium bg-dark-700/70">ML Compute</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Cost Optimization -->
    <div class="card mb-8">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-bold">Cost Optimization Recommendations</h3>
        <button class="text-primary-500 hover:text-primary-400 text-sm">Apply All</button>
      </div>
      <div class="space-y-4">
        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex items-start">
            <div class="bg-primary-900/30 p-2 rounded mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="flex justify-between">
                <h4 class="font-medium">Resize Snowflake Warehouses for Financial Reporting</h4>
                <span class="text-green-400 font-medium">Save $1,200/mo</span>
              </div>
              <p class="text-dark-400 text-sm mt-1">Usage patterns show the XL warehouse is overprovisioned. Downgrading to L warehouse will maintain performance while reducing costs.</p>
              <div class="mt-3 flex justify-end">
                <button class="text-xs px-3 py-1 bg-primary-900/30 text-primary-400 rounded-md hover:bg-primary-900/50">Apply</button>
              </div>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex items-start">
            <div class="bg-secondary-900/30 p-2 rounded mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-secondary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="flex justify-between">
                <h4 class="font-medium">Optimize Customer Data Storage</h4>
                <span class="text-green-400 font-medium">Save $850/mo</span>
              </div>
              <p class="text-dark-400 text-sm mt-1">Implementing data tiering and archiving for historical customer data older than 12 months will reduce storage costs.</p>
              <div class="mt-3 flex justify-end">
                <button class="text-xs px-3 py-1 bg-secondary-900/30 text-secondary-400 rounded-md hover:bg-secondary-900/50">Apply</button>
              </div>
            </div>
          </div>
        </div>

        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex items-start">
            <div class="bg-accent-900/30 p-2 rounded mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-accent-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="flex justify-between">
                <h4 class="font-medium">Schedule Auto-Suspend for Dev Environments</h4>
                <span class="text-green-400 font-medium">Save $620/mo</span>
              </div>
              <p class="text-dark-400 text-sm mt-1">Development environments are active 24/7 but only used during business hours. Implementing auto-suspend during off-hours.</p>
              <div class="mt-3 flex justify-end">
                <button class="text-xs px-3 py-1 bg-accent-900/30 text-accent-400 rounded-md hover:bg-accent-900/50">Apply</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Budgets Section -->
    <div class="card">
      <div class="flex justify-between items-center mb-4">
        <h3 class="font-bold">Cost Budgets Tracking</h3>
        <button class="text-primary-500 hover:text-primary-400 text-sm">Create Budget</button>
      </div>
      <div class="space-y-4">
        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex justify-between items-center mb-2">
            <h4 class="font-medium">Snowflake Monthly Budget</h4>
            <span class="text-yellow-400 font-medium">$28,450 / $30,000</span>
          </div>
          <div class="w-full bg-dark-700 rounded-full h-2.5 mb-2">
            <div class="bg-yellow-500 h-2.5 rounded-full" style="width: 94.8%"></div>
          </div>
          <div class="flex justify-between text-xs text-dark-400">
            <span>95% utilized</span>
            <span>5 days remaining</span>
          </div>
        </div>

        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex justify-between items-center mb-2">
            <h4 class="font-medium">Microsoft Fabric Quarterly Budget</h4>
            <span class="text-green-400 font-medium">$9,875 / $15,000</span>
          </div>
          <div class="w-full bg-dark-700 rounded-full h-2.5 mb-2">
            <div class="bg-green-500 h-2.5 rounded-full" style="width: 65.8%"></div>
          </div>
          <div class="flex justify-between text-xs text-dark-400">
            <span>66% utilized</span>
            <span>28 days remaining</span>
          </div>
        </div>

        <div class="p-4 rounded-md bg-dark-800/90 border border-dark-700">
          <div class="flex justify-between items-center mb-2">
            <h4 class="font-medium">Annual Data Platform Budget</h4>
            <span class="text-red-400 font-medium">$145,200 / $150,000</span>
          </div>
          <div class="w-full bg-dark-700 rounded-full h-2.5 mb-2">
            <div class="bg-red-500 h-2.5 rounded-full" style="width: 96.8%"></div>
          </div>
          <div class="flex justify-between text-xs text-dark-400">
            <span>97% utilized</span>
            <span>45 days remaining</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// This would normally initialize charts and fetch data from your API
const initCharts = () => {
  // Mock implementation
  console.log('Charts initialized for Cost Management page');
};

onMounted(() => {
  initCharts();
});
</script> 