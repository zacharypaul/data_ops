<template>
  <div>
    <!-- Modal Background -->
    <div 
      v-if="isOpen" 
      class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 flex items-center justify-center overflow-y-auto"
      @click="closeModal"
    >
      <!-- Modal Content -->
      <div 
        class="bg-dark-800 border border-dark-700 rounded-lg shadow-xl max-w-3xl w-full mx-4 max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <!-- Modal Header with Close Button -->
        <div class="flex justify-between items-center border-b border-dark-700 p-4">
          <div class="flex items-center space-x-3">
            <span :class="`text-${connector?.type?.class || 'primary'}-500 p-2 rounded-md bg-${connector?.type?.class || 'primary'}-500/10 flex items-center justify-center`">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm11 1H6v8h8V6z" clip-rule="evenodd" />
              </svg>
            </span>
            <div>
              <h3 class="text-xl font-bold text-white">{{ connector?.name || 'Connector Details' }}</h3>
              <div class="flex items-center text-dark-300 text-sm">
                <span :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${connector?.type?.class || 'primary'}-900/30 text-${connector?.type?.class || 'primary'}-400 mr-2`">
                  {{ connector?.type?.name || 'Unknown' }}
                </span>
                <span>Last updated: {{ connector?.lastRefresh || 'Unknown' }}</span>
              </div>
            </div>
          </div>
          <button
            @click="closeModal"
            class="text-dark-400 hover:text-white p-1"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div v-if="isLoading" class="flex justify-center py-12">
          <div class="flex flex-col items-center">
            <svg class="animate-spin h-10 w-10 text-primary-500 mb-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-dark-300">Loading connector details...</p>
          </div>
        </div>

        <div v-else-if="!connector" class="p-6 text-center text-dark-300">
          Connector details not found
        </div>

        <div v-else class="p-6">
          <!-- Connector Stats -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-dark-700/50 rounded-lg p-4">
              <h4 class="text-dark-300 text-sm mb-1">Source</h4>
              <p class="text-white font-medium">{{ connector.details?.source || 'Unknown' }}</p>
            </div>
            <div class="bg-dark-700/50 rounded-lg p-4">
              <h4 class="text-dark-300 text-sm mb-1">Destination</h4>
              <p class="text-white font-medium">{{ connector.details?.destination || 'Unknown' }}</p>
            </div>
            <div class="bg-dark-700/50 rounded-lg p-4">
              <h4 class="text-dark-300 text-sm mb-1">Schedule</h4>
              <p class="text-white font-medium">{{ connector.details?.schedule || 'Unknown' }}</p>
            </div>
            <div class="bg-dark-700/50 rounded-lg p-4">
              <h4 class="text-dark-300 text-sm mb-1">Owner</h4>
              <p class="text-white font-medium">{{ connector.details?.owner || 'Unknown' }}</p>
            </div>
          </div>

          <!-- Connector Status -->
          <div class="mb-6">
            <h3 class="text-lg font-bold mb-3">Status</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-dark-700/30 rounded-lg p-4">
                <h4 class="text-dark-300 text-sm mb-2">Freshness</h4>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-white text-lg font-bold">{{ connector.freshness?.value }}%</span>
                  <span :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${connector.freshness?.status}-900/30 text-${connector.freshness?.status}-400`">
                    {{ connector.freshness?.status === 'green' ? 'Good' : 'Warning' }}
                  </span>
                </div>
                <div class="h-2 w-full bg-dark-800 rounded-full overflow-hidden">
                  <div 
                    :class="`h-full bg-${connector.freshness?.status}-500 rounded-full`" 
                    :style="`width: ${connector.freshness?.value}%`"
                  ></div>
                </div>
              </div>

              <div class="bg-dark-700/30 rounded-lg p-4">
                <h4 class="text-dark-300 text-sm mb-2">Quality</h4>
                <div class="flex items-center justify-between mb-2">
                  <span class="text-white text-lg font-bold">{{ connector.quality?.value }}%</span>
                  <span :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${connector.quality?.status}-900/30 text-${connector.quality?.status}-400`">
                    {{ connector.quality?.status === 'green' ? 'Good' : 'Warning' }}
                  </span>
                </div>
                <div class="h-2 w-full bg-dark-800 rounded-full overflow-hidden">
                  <div 
                    :class="`h-full bg-${connector.quality?.status}-500 rounded-full`" 
                    :style="`width: ${connector.quality?.value}%`"
                  ></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Recent Runs -->
          <div class="mb-6">
            <h3 class="text-lg font-bold mb-3">Recent Runs</h3>
            <div class="bg-dark-700/30 rounded-lg overflow-hidden">
              <table class="min-w-full">
                <thead class="bg-dark-700/50">
                  <tr>
                    <th class="text-left py-2 px-4 text-dark-400 text-sm">Date</th>
                    <th class="text-left py-2 px-4 text-dark-400 text-sm">Duration</th>
                    <th class="text-left py-2 px-4 text-dark-400 text-sm">Status</th>
                    <th class="text-left py-2 px-4 text-dark-400 text-sm">Rows</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-dark-700/50">
                  <tr class="hover:bg-dark-700/20">
                    <td class="py-2 px-4 text-white">Today, 10:45 AM</td>
                    <td class="py-2 px-4 text-white">12m 30s</td>
                    <td class="py-2 px-4">
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-400">
                        Success
                      </span>
                    </td>
                    <td class="py-2 px-4 text-white">10,432</td>
                  </tr>
                  <tr class="hover:bg-dark-700/20">
                    <td class="py-2 px-4 text-white">Yesterday, 11:30 PM</td>
                    <td class="py-2 px-4 text-white">15m 05s</td>
                    <td class="py-2 px-4">
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-900/30 text-green-400">
                        Success
                      </span>
                    </td>
                    <td class="py-2 px-4 text-white">10,428</td>
                  </tr>
                  <tr class="hover:bg-dark-700/20">
                    <td class="py-2 px-4 text-white">Yesterday, 5:30 PM</td>
                    <td class="py-2 px-4 text-white">14m 45s</td>
                    <td class="py-2 px-4">
                      <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-900/30 text-red-400">
                        Failed
                      </span>
                    </td>
                    <td class="py-2 px-4 text-white">8,327</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-end space-x-3 border-t border-dark-700 pt-4">
            <button class="px-4 py-2 border border-dark-600 bg-dark-700 hover:bg-dark-600 text-white rounded-md transition-colors">
              View Configuration
            </button>
            <button 
              @click="refreshConnector"
              class="flex items-center space-x-2 px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors"
              :disabled="isRefreshing"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="h-4 w-4" 
                :class="{ 'animate-spin': isRefreshing }"
                viewBox="0 0 20 20" 
                fill="currentColor"
              >
                <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
              </svg>
              <span>{{ isRefreshing ? 'Refreshing...' : 'Refresh Now' }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, ref, defineEmits, watch } from 'vue';
import DashboardApi from '@/services/DashboardApi';

const props = defineProps({
  connectorId: {
    type: [Number, null],
    default: null
  },
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'refresh']);

const connector = ref(null);
const isLoading = ref(false);
const isRefreshing = ref(false);

const closeModal = () => {
  emit('close');
};

const loadConnectorDetails = async () => {
  if (!props.connectorId) return;
  
  isLoading.value = true;
  
  try {
    connector.value = await DashboardApi.getConnectorDetails(props.connectorId);
  } catch (error) {
    console.error('Error loading connector details:', error);
  } finally {
    isLoading.value = false;
  }
};

const refreshConnector = async () => {
  if (isRefreshing.value || !connector.value) return;
  
  isRefreshing.value = true;
  
  try {
    const result = await DashboardApi.refreshConnector(connector.value.id);
    console.log('Refresh triggered:', result);
    
    // Emit refresh event to parent
    emit('refresh', connector.value.id);
    
    // Reload connector details after a delay
    setTimeout(async () => {
      await loadConnectorDetails();
      isRefreshing.value = false;
    }, 2000);
    
  } catch (error) {
    console.error('Error refreshing connector:', error);
    isRefreshing.value = false;
  }
};

// Watch for changes to connector ID or open state
watch(() => [props.connectorId, props.isOpen], async ([newId, newIsOpen]) => {
  if (newIsOpen && newId) {
    await loadConnectorDetails();
  }
}, { immediate: true });
</script> 