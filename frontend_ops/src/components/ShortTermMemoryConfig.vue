<template>
  <div class="space-y-6 p-4 border border-purple-500/30 rounded-lg bg-dark-800/50">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-md bg-purple-900/50 flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 5a2 2 0 012-2h10a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm11 1H6v8l4-2 4 2V6z" clip-rule="evenodd" />
          </svg>
        </div>
        <h4 class="font-medium">Session Context</h4>
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
      <!-- Context window configuration -->
      <div class="space-y-4">
        <div>
          <label class="text-sm text-dark-300">Context Window Size</label>
          <div class="flex items-center mt-2">
            <input 
              type="range" 
              min="1" 
              max="20" 
              v-model.number="localConfig.contextWindow"
              class="w-full h-2 bg-dark-700 rounded-lg appearance-none cursor-pointer"
            >
            <span class="ml-3 text-sm text-dark-300 w-10">{{ localConfig.contextWindow }}</span>
          </div>
          <div class="text-xs text-dark-400 mt-1">Maximum number of previous interactions to include in short-term memory</div>
        </div>
        
        <div class="mt-6">
          <div class="bg-dark-700 rounded-md p-4 border border-dark-600">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-md bg-purple-900/50 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-400" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
                </svg>
              </div>
              <div>
                <div class="text-sm font-medium">Short-term Memory Structure</div>
                <div class="text-xs text-dark-400">Session context and recent interactions</div>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-5 gap-2 mt-4">
              <div class="md:col-span-3 border border-dark-600 rounded bg-dark-800/50 p-3">
                <div class="text-xs text-purple-400 mb-2">Current Session Context</div>
                <div class="space-y-2">
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full bg-purple-400"></div>
                    <div class="text-xs text-dark-300">Last {{ localConfig.contextWindow }} messages</div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full bg-purple-400"></div>
                    <div class="text-xs text-dark-300">User preferences</div>
                  </div>
                  <div class="flex items-center space-x-2">
                    <div class="w-2 h-2 rounded-full bg-purple-400"></div>
                    <div class="text-xs text-dark-300">Session metadata</div>
                  </div>
                </div>
              </div>
              
              <div class="md:col-span-2 border border-dark-600 rounded bg-dark-800/50 p-3">
                <div class="text-xs text-green-400 mb-2">Live Data Connections</div>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 rounded-full bg-green-400"></div>
                  <div class="text-xs text-dark-300">{{ localConfig.liveConnections.length }} active API connections</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Live API connections -->
      <div class="mt-6 space-y-2">
        <div class="flex justify-between items-center">
          <label class="text-sm text-dark-300">Live API Connections</label>
          <button class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 inline mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Connect
          </button>
        </div>
        
        <div class="space-y-2 max-h-48 overflow-y-auto">
          <div 
            v-for="connection in localConfig.liveConnections" 
            :key="connection.id"
            class="flex items-center justify-between bg-dark-700 rounded-md p-3 border border-dark-600"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-md bg-dark-600 flex items-center justify-center mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM11 12a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
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
      
      <!-- Cross-Memory Integration -->
      <div class="mt-6 space-y-2">
        <div class="flex justify-between items-center">
          <label class="text-sm text-dark-300">Cross-Memory Integration</label>
          <div class="relative inline-block w-10 align-middle select-none">
            <input type="checkbox" checked class="sr-only" />
            <span class="block overflow-hidden h-5 rounded-full bg-green-900/30 cursor-pointer"></span>
          </div>
        </div>
        
        <div class="bg-dark-700/50 rounded-md p-3 border border-dark-600">
          <div class="flex items-center">
            <div class="w-6 h-6 rounded-full bg-green-900/50 flex items-center justify-center mr-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="text-xs text-dark-300">
              Live API connections can access both short-term and long-term memory
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-8 text-dark-400 italic">
      Short-term memory features are disabled
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
  background-color: rgba(168, 85, 247, 0.3);
  border-color: rgba(168, 85, 247, 0.5);
}

input:checked + .slider:before {
  background-color: #a855f7;
  transform: translateX(20px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}

/* Range slider styling */
input[type=range] {
  -webkit-appearance: none;
  height: 8px;
  background: #334155;
  border-radius: 4px;
  background-image: linear-gradient(to right, #a855f7, #a855f7);
  background-size: 50% 100%;
  background-repeat: no-repeat;
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #a855f7;
  cursor: pointer;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

input[type=range]::-webkit-slider-runnable-track {
  -webkit-appearance: none;
  box-shadow: none;
  border: none;
  background: transparent;
}
</style> 