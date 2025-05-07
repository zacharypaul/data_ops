<template>
  <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-xl font-display font-bold">Top Connectors</h2>
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search connectors..." 
            class="bg-dark-700/50 border border-dark-600 rounded-md px-3 py-1.5 text-sm w-48 pl-8 text-white focus:outline-none focus:border-primary-500"
          />
          <svg 
            class="absolute left-2.5 top-2 h-4 w-4 text-dark-400" 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path 
              fill-rule="evenodd" 
              d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" 
              clip-rule="evenodd" 
            />
          </svg>
        </div>
        <div class="relative">
          <select 
            v-model="selectedType"
            class="bg-dark-700/50 border border-dark-600 rounded-md px-3 py-1.5 text-sm appearance-none pr-8 text-white focus:outline-none focus:border-primary-500"
          >
            <option value="all">All Types</option>
            <option 
              v-for="type in connectorTypes.filter(t => t !== 'all')" 
              :key="type" 
              :value="type.toLowerCase()"
            >
              {{ type }}
            </option>
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
      </div>
    </div>
    
    <div v-if="filteredConnectors.length === 0" class="text-center py-12 text-dark-300">
      No connectors found matching your search criteria
    </div>
    
    <div v-else class="overflow-x-auto">
      <table class="min-w-full">
        <thead class="border-b border-dark-700">
          <tr>
            <th class="text-left py-3 px-4 text-dark-400">Connector</th>
            <th class="text-left py-3 px-4 text-dark-400">Type</th>
            <th class="text-left py-3 px-4 text-dark-400">Last Refresh</th>
            <th class="text-left py-3 px-4 text-dark-400">Freshness</th>
            <th class="text-left py-3 px-4 text-dark-400">Quality</th>
            <th class="text-left py-3 px-4 text-dark-400 w-24">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-dark-700">
          <tr 
            v-for="connector in filteredConnectors" 
            :key="connector.id"
            class="hover:bg-dark-700/30 transition-colors cursor-pointer"
            @click="openConnectorDetails(connector)"
          >
            <td class="py-3 px-4">{{ connector.name }}</td>
            <td class="py-3 px-4">
              <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${connector.type.class}-900/30 text-${connector.type.class}-400`">
                {{ connector.type.name }}
              </span>
            </td>
            <td class="py-3 px-4">{{ connector.lastRefresh }}</td>
            <td class="py-3 px-4">
              <div class="w-24 bg-dark-700 rounded-full h-2">
                <div 
                  :class="`h-2 rounded-full bg-${connector.freshness.status}-500`" 
                  :style="`width: ${connector.freshness.value}%`"
                ></div>
              </div>
            </td>
            <td class="py-3 px-4">
              <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${connector.quality.status}-900/30 text-${connector.quality.status}-400`">
                <span :class="`w-1.5 h-1.5 mr-1.5 rounded-full bg-${connector.quality.status}-400`"></span>
                {{ connector.quality.value }}%
              </span>
            </td>
            <td class="py-3 px-4 flex items-center space-x-2" @click.stop>
              <button 
                @click="refreshConnector(connector)"
                :disabled="isRefreshing[connector.id]"
                :class="`text-${isRefreshing[connector.id] ? 'primary-400' : 'dark-300'} hover:text-white transition-colors`"
                title="Refresh connector"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5" 
                  :class="{ 'animate-spin': isRefreshing[connector.id] }"
                  viewBox="0 0 20 20" 
                  fill="currentColor"
                >
                  <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
                </svg>
              </button>
              <button 
                @click="openConnectorDetails(connector)"
                class="text-dark-300 hover:text-white transition-colors"
                title="View details"
              >
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  class="h-5 w-5" 
                  viewBox="0 0 20 20" 
                  fill="currentColor"
                >
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                </svg>
              </button>
              <button class="text-dark-300 hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="filteredConnectors.length > 0" class="flex justify-between items-center mt-4">
      <div class="text-sm text-dark-300">
        Showing <span class="font-medium text-white">{{ filteredConnectors.length }}</span> of {{ connectors.length }} connectors
      </div>
      <div class="flex space-x-1">
        <button class="px-2 py-1 rounded bg-dark-700 text-dark-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
        <button class="px-2 py-1 rounded bg-primary-600 text-white">1</button>
        <button class="px-2 py-1 rounded bg-dark-700 text-dark-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Connector Detail Modal -->
    <ConnectorDetail
      :connector-id="selectedConnectorId"
      :is-open="isModalOpen"
      @close="closeConnectorModal"
      @refresh="handleModalRefresh"
    />
  </div>
</template>

<script setup>
import { defineProps, ref, computed, defineEmits } from 'vue';
import ConnectorDetail from './ConnectorDetail.vue';

const props = defineProps({
  connectors: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['refresh-connector', 'select-connector']);

// Search and filtering functionality
const searchQuery = ref('');
const selectedType = ref('all');
const isRefreshing = ref({});

// Modal state
const isModalOpen = ref(false);
const selectedConnectorId = ref(null);

// Filter the connectors based on search query and type filter
const filteredConnectors = computed(() => {
  return props.connectors.filter(connector => {
    const matchesSearch = connector.name.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesType = selectedType.value === 'all' || 
                        connector.type.name.toLowerCase() === selectedType.value.toLowerCase();
    return matchesSearch && matchesType;
  });
});

// Get unique connector types for the filter dropdown
const connectorTypes = computed(() => {
  const types = new Set(props.connectors.map(c => c.type.name));
  return ['all', ...Array.from(types)];
});

// Handle connector refresh
const refreshConnector = async (connector) => {
  if (isRefreshing.value[connector.id]) return;
  
  try {
    isRefreshing.value[connector.id] = true;
    await emit('refresh-connector', connector.id);
  } catch (error) {
    console.error(`Error refreshing connector ${connector.id}:`, error);
  } finally {
    // After a delay, set refreshing state back to false
    setTimeout(() => {
      isRefreshing.value[connector.id] = false;
    }, 2000);
  }
};

// Open connector details modal
const openConnectorDetails = (connector) => {
  selectedConnectorId.value = connector.id;
  isModalOpen.value = true;
  emit('select-connector', connector.id);
};

// Close connector details modal
const closeConnectorModal = () => {
  isModalOpen.value = false;
  // Optionally clear the selected connector after a delay for better UX
  setTimeout(() => {
    selectedConnectorId.value = null;
  }, 300);
};

// Handle refresh from modal
const handleModalRefresh = (connectorId) => {
  emit('refresh-connector', connectorId);
};
</script> 