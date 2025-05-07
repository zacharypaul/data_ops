<template>
  <div class="space-y-6">
    <!-- Memory tabs -->
    <div class="flex space-x-1 border-b border-dark-700">
      <button 
        v-for="tab in memoryTabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="[
          'py-2 px-3 text-xs font-medium border-b-2',
          activeTab === tab.id 
            ? 'border-primary-500 text-primary-400' 
            : 'border-transparent text-dark-400 hover:text-dark-200 hover:border-dark-600'
        ]"
      >
        {{ tab.name }}
      </button>
    </div>
    
    <!-- Long-term memory tab content -->
    <div v-if="activeTab === 'longTerm'" class="space-y-4">
      <div v-if="longTermMemory.length === 0" class="text-center py-6 text-dark-400">
        No long-term memory records found
      </div>
      
      <div v-else class="space-y-3 max-h-96 overflow-y-auto pr-2">
        <div 
          v-for="item in longTermMemory" 
          :key="item.id"
          class="border border-dark-600 rounded-lg p-3 hover:border-blue-500/30 transition"
        >
          <div class="flex justify-between mb-2">
            <div class="text-sm font-medium text-blue-400">{{ item.source }}</div>
            <div class="text-xs text-dark-400">Relevance: {{ (item.relevance * 100).toFixed(0) }}%</div>
          </div>
          <div class="text-sm">{{ item.content }}</div>
        </div>
      </div>
      
      <div class="text-xs text-dark-400 p-2 border border-dark-600 rounded bg-dark-700/50">
        Long-term memory stores persistent knowledge across multiple sessions using vector embeddings
      </div>
    </div>
    
    <!-- Short-term memory tab content -->
    <div v-else-if="activeTab === 'shortTerm'" class="space-y-4">
      <div v-if="shortTermMemory.length === 0" class="text-center py-6 text-dark-400">
        No short-term memory records found
      </div>
      
      <div v-else class="space-y-3 max-h-96 overflow-y-auto pr-2">
        <div 
          v-for="item in shortTermMemory" 
          :key="item.id"
          class="border border-dark-600 rounded-lg p-3 hover:border-purple-500/30 transition"
        >
          <div class="flex justify-between mb-2">
            <div class="text-sm font-medium text-purple-400">{{ item.source }}</div>
            <div class="text-xs text-dark-400">Relevance: {{ (item.relevance * 100).toFixed(0) }}%</div>
          </div>
          <div class="text-sm">{{ item.content }}</div>
        </div>
      </div>
      
      <div class="text-xs text-dark-400 p-2 border border-dark-600 rounded bg-dark-700/50">
        Short-term memory contains information from the current conversation context and recent API calls
      </div>
    </div>
    
    <!-- Session memory tab content -->
    <div v-else-if="activeTab === 'session'" class="space-y-4">
      <div v-if="sessionMemory.length === 0" class="text-center py-6 text-dark-400">
        No session memory records found
      </div>
      
      <div v-else class="space-y-3 max-h-96 overflow-y-auto pr-2">
        <div 
          v-for="item in sessionMemory" 
          :key="item.id"
          class="border border-dark-600 rounded-lg p-3 hover:border-green-500/30 transition"
        >
          <div class="flex justify-between mb-2">
            <div class="text-sm font-medium text-green-400">{{ item.source }}</div>
            <div class="text-xs text-dark-400">Relevance: {{ (item.relevance * 100).toFixed(0) }}%</div>
          </div>
          <div class="text-sm">{{ item.content }}</div>
        </div>
      </div>
      
      <div class="text-xs text-dark-400 p-2 border border-dark-600 rounded bg-dark-700/50">
        Session memory contains information extracted from the current conversation
      </div>
    </div>
    
    <!-- Memory search -->
    <div class="relative">
      <input 
        type="text" 
        placeholder="Search across memory..."
        class="w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-2 pr-10 focus:outline-none focus:border-primary-500 text-sm"
      >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 absolute right-3 top-2.5 text-dark-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
    
    <!-- Memory refresh controls -->
    <div class="flex justify-between items-center">
      <div class="text-xs text-dark-400">Last updated: 2 minutes ago</div>
      <button class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
        </svg>
        Refresh
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  longTermMemory: {
    type: Array,
    default: () => []
  },
  shortTermMemory: {
    type: Array,
    default: () => []
  },
  sessionMemory: {
    type: Array,
    default: () => []
  }
});

// Memory tab state
const activeTab = ref('longTerm');
const memoryTabs = [
  { id: 'longTerm', name: 'Long-Term Memory' },
  { id: 'shortTerm', name: 'Short-Term Memory' },
  { id: 'session', name: 'Session Memory' }
];
</script>

<style scoped>
/* Custom scrollbar for memory containers */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(71, 85, 105, 0.5);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(71, 85, 105, 0.8);
}
</style> 