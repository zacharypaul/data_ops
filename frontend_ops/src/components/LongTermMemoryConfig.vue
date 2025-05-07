<template>
  <div class="space-y-6 p-4 border border-blue-500/30 rounded-lg bg-dark-800/50">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-md bg-blue-900/50 flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
            <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM14 11a1 1 0 011 1v1h1a1 1 0 110 2h-1v1a1 1 0 11-2 0v-1h-1a1 1 0 110-2h1v-1a1 1 0 011-1z" />
          </svg>
        </div>
        <h4 class="font-medium">Vector Embeddings</h4>
      </div>
      <div class="flex items-center">
        <span class="text-sm text-dark-400 mr-2">Enable</span>
        <label class="switch">
          <input type="checkbox" v-model="localConfig.enabled">
          <span class="slider round"></span>
        </label>
      </div>
    </div>
    
    <div v-if="localConfig.enabled">
      <!-- Embedding model selection -->
      <div class="space-y-2">
        <label class="text-sm text-dark-300">Embedding Model</label>
        <select 
          v-model="localConfig.embeddingModel" 
          class="w-full bg-dark-700 border border-dark-600 rounded-md p-2.5 focus:outline-none focus:border-blue-500"
        >
          <option value="text-embedding-3-large">text-embedding-3-large (OpenAI)</option>
          <option value="text-embedding-3-small">text-embedding-3-small (OpenAI)</option>
          <option value="all-mpnet-base-v2">all-mpnet-base-v2 (HuggingFace)</option>
          <option value="e5-large-v2">e5-large-v2 (Microsoft)</option>
        </select>
      </div>
      
      <!-- Embedding creation process -->
      <div class="mt-6 space-y-4">
        <div class="flex justify-between items-center">
          <label class="text-sm text-dark-300">Embedding Process</label>
          <button class="text-xs py-1 px-2 bg-blue-900/30 text-blue-400 rounded hover:bg-blue-900/50 transition">
            Advanced Settings
          </button>
        </div>
        
        <div class="bg-dark-700 rounded-md p-4 border border-dark-600">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-dark-600 flex items-center justify-center mr-3 text-blue-400">1</div>
            <div>
              <div class="text-sm font-medium">Data Ingestion</div>
              <div class="text-xs text-dark-400">Source data from knowledge bases &amp; documents</div>
            </div>
          </div>
          
          <div class="ml-4 pl-4 border-l border-dark-600">
            <svg class="w-4 h-8 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
          
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-dark-600 flex items-center justify-center mr-3 text-blue-400">2</div>
            <div>
              <div class="text-sm font-medium">Chunking &amp; Preprocessing</div>
              <div class="text-xs text-dark-400">Split texts into optimal chunks with metadata</div>
            </div>
          </div>
          
          <div class="ml-4 pl-4 border-l border-dark-600">
            <svg class="w-4 h-8 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
          
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-dark-600 flex items-center justify-center mr-3 text-blue-400">3</div>
            <div>
              <div class="text-sm font-medium">Vector Generation</div>
              <div class="text-xs text-dark-400">Create embeddings using {{ localConfig.embeddingModel }}</div>
            </div>
          </div>
          
          <div class="ml-4 pl-4 border-l border-dark-600">
            <svg class="w-4 h-8 text-dark-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
            </svg>
          </div>
          
          <div class="flex items-center">
            <div class="w-8 h-8 rounded-full bg-dark-600 flex items-center justify-center mr-3 text-blue-400">4</div>
            <div>
              <div class="text-sm font-medium">Vector Index Storage</div>
              <div class="text-xs text-dark-400">Store in database for similarity search</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Data connections -->
      <div class="mt-6 space-y-2">
        <div class="flex justify-between items-center">
          <label class="text-sm text-dark-300">Data Connections</label>
          <button class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Add
          </button>
        </div>
        
        <div class="space-y-2 max-h-48 overflow-y-auto">
          <div 
            v-for="connection in localConfig.dataConnections" 
            :key="connection.id"
            class="flex items-center justify-between bg-dark-700 rounded-md p-3 border border-dark-600"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-md bg-dark-600 flex items-center justify-center mr-3">
                <svg v-if="connection.type === 'document'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" />
                </svg>
                <svg v-else-if="connection.type === 'database'" xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                  <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                  <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2h-2.22l.123.489.804.804A1 1 0 0113 18H7a1 1 0 01-.707-1.707l.804-.804L7.22 15H5a2 2 0 01-2-2V5zm5.771 7H5V5h10v7H8.771z" clip-rule="evenodd" />
                </svg>
              </div>
              <div>
                <div class="text-sm font-medium">{{ connection.name }}</div>
                <div class="text-xs text-dark-400">{{ connection.type }}</div>
              </div>
            </div>
            <div>
              <span 
                class="px-2 py-1 rounded-full text-xs"
                :class="connection.status === 'active' ? 'bg-green-900/30 text-green-400' : 'bg-dark-600 text-dark-400'"
              >
                {{ connection.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-8 text-dark-400 italic">
      Long-term memory features are disabled
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  config: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['update']);

// Create a local copy of the config
const localConfig = ref({ ...props.config });

// Watch for changes to local config and emit updates
watch(localConfig, (newConfig) => {
  emit('update', newConfig);
}, { deep: true });

// Watch for parent config changes
watch(() => props.config, (newConfig) => {
  localConfig.value = { ...newConfig };
}, { deep: true });
</script>

<style scoped>
/* Toggle switch styling */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
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
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  transition: .3s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 2px;
  background-color: #64748b;
  transition: .3s;
}

input:checked + .slider {
  background-color: rgba(59, 130, 246, 0.3);
  border-color: rgba(59, 130, 246, 0.5);
}

input:checked + .slider:before {
  background-color: #3b82f6;
  transform: translateX(20px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}
</style> 