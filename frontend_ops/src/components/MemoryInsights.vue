<template>
  <div class="space-y-6">
    <!-- Actionable Insights Panel -->
    <div class="glass-panel">
      <div class="flex justify-between items-center mb-4">
        <h3 class="text-lg font-semibold flex items-center">
          <span class="mr-2">Conversation Assistant</span>
          <div class="info-tooltip">
            <button @click="togglePerformanceMetrics" class="tooltip-btn">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 text-blue-400">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd" />
              </svg>
            </button>
            <!-- Performance Metrics Popup -->
            <div v-if="showPerformanceMetrics" class="tooltip-content performance-metrics">
              <div class="tooltip-header flex justify-between items-center">
                <h4 class="font-medium">Memory Pull Performance</h4>
                <button @click="togglePerformanceMetrics" class="text-dark-400 hover:text-dark-200">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4">
                    <path d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z" />
                  </svg>
                </button>
              </div>
              <div class="space-y-3 mt-2">
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Retrieval Latency</span>
                    <span class="text-green-400">{{ memoryMetrics.latency }}ms</span>
                  </div>
                  <div class="w-full bg-dark-700 rounded-full h-1.5">
                    <div class="bg-green-500 h-1.5 rounded-full" :style="{ width: `${Math.min(100, 100 - (memoryMetrics.latency / 2))}%` }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Relevance Score</span>
                    <span class="text-green-400">{{ memoryMetrics.relevance }}%</span>
                  </div>
                  <div class="w-full bg-dark-700 rounded-full h-1.5">
                    <div class="bg-green-500 h-1.5 rounded-full" :style="{ width: `${memoryMetrics.relevance}%` }"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between text-sm mb-1">
                    <span>Memory Utilization</span>
                    <span class="text-yellow-400">{{ memoryMetrics.utilization }}%</span>
                  </div>
                  <div class="w-full bg-dark-700 rounded-full h-1.5">
                    <div class="bg-yellow-500 h-1.5 rounded-full" :style="{ width: `${memoryMetrics.utilization}%` }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </h3>
        <div class="flex items-center space-x-2">
          <span class="text-xs py-1 px-2 bg-blue-900/30 text-blue-400 rounded flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5 mr-1">
              <path fill-rule="evenodd" d="M1 4a1 1 0 011-1h16a1 1 0 011 1v8a1 1 0 01-1 1H2a1 1 0 01-1-1V4zm12 4a3 3 0 11-6 0 3 3 0 016 0zM4 9a1 1 0 100-2 1 1 0 000 2zm13-1a1 1 0 11-2 0 1 1 0 012 0zM1.75 14.5a.75.75 0 000 1.5c4.417 0 8.693.603 12.749 1.73 1.111.309 2.251-.512 2.251-1.696v-.784a.75.75 0 00-1.5 0v.784a.272.272 0 01-.35.25A49.043 49.043 0 001.75 14.5z" clip-rule="evenodd" />
            </svg>
            AI Assistant Active
          </span>
        </div>
      </div>

      <!-- Context-aware suggestions -->
      <div class="mb-4">
        <h4 class="text-sm font-medium text-dark-300 mb-2">User Intent Analysis</h4>
        <div class="bg-dark-800/40 rounded p-3 border border-dark-700 text-sm">
          <p class="text-white">User is having trouble with <span class="text-blue-400">CloudSync mobile app backup process</span> on <span class="text-blue-400">Android 12</span>.</p>
          <div class="mt-2 flex items-center text-green-400 text-xs">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4 mr-1">
              <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clip-rule="evenodd" />
            </svg>
            Intent identified with 92% confidence
          </div>
        </div>
      </div>

      <!-- Action buttons -->
      <div class="space-y-3">
        <button @click="insertSolution('permissions')" class="action-button">
          <div class="action-icon bg-indigo-900/30 text-indigo-400">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
              <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 01-9.201 2.466l-.312-.311h2.433a.75.75 0 000-1.5H3.989a.75.75 0 00-.75.75v4.242a.75.75 0 001.5 0v-2.43l.31.31a7 7 0 0011.712-3.138.75.75 0 00-1.449-.39zm1.23-3.723a.75.75 0 00.219-.53V2.929a.75.75 0 00-1.5 0V5.36l-.31-.31A7 7 0 003.239 8.188a.75.75 0 101.448.389A5.5 5.5 0 0113.89 6.11l.311.31h-2.432a.75.75 0 000 1.5h4.243a.75.75 0 00.53-.219z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="text-sm font-medium">Insert Android 12 Permission Guide</div>
            <div class="text-xs text-dark-400">Step-by-step instructions for checking background permissions</div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 text-dark-500">
            <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
          </svg>
        </button>

        <button @click="insertSolution('reference')" class="action-button">
          <div class="action-icon bg-green-900/30 text-green-400">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
              <path d="M10.75 16.82A7.462 7.462 0 0115 15.5c.71 0 1.396.098 2.046.282A.75.75 0 0018 15.06v-11a.75.75 0 00-.546-.721A9.006 9.006 0 0015 3a8.963 8.963 0 00-4.25 1.065V16.82zM9.25 4.065A8.963 8.963 0 005 3c-.85 0-1.673.118-2.454.339A.75.75 0 002 4.06v11a.75.75 0 00.954.721A7.506 7.506 0 015 15.5c1.579 0 3.042.487 4.25 1.32V4.065z" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="text-sm font-medium">Reference Previous Solution</div>
            <div class="text-xs text-dark-400">Include solution from user's previous sync issue ticket</div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 text-dark-500">
            <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
          </svg>
        </button>

        <button @click="insertSolution('backup')" class="action-button">
          <div class="action-icon bg-amber-900/30 text-amber-400">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
              <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 01-9.201 2.466l-.312-.311h2.433a.75.75 0 000-1.5H3.989a.75.75 0 00-.75.75v4.242a.75.75 0 001.5 0v-2.43l.31.31a7 7 0 0011.712-3.138.75.75 0 00-1.449-.39zm1.23-3.723a.75.75 0 00.219-.53V2.929a.75.75 0 00-1.5 0V5.36l-.31-.31A7 7 0 003.239 8.188a.75.75 0 101.448.389A5.5 5.5 0 0113.89 6.11l.311.31h-2.432a.75.75 0 000 1.5h4.243a.75.75 0 00.53-.219z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="flex-1">
            <div class="text-sm font-medium">Add Manual Backup Instructions</div>
            <div class="text-xs text-dark-400">Alternative method if background sync continues to fail</div>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 text-dark-500">
            <path fill-rule="evenodd" d="M5 10a.75.75 0 01.75-.75h6.638L10.23 7.29a.75.75 0 111.04-1.08l3.5 3.25a.75.75 0 010 1.08l-3.5 3.25a.75.75 0 11-1.04-1.08l2.158-1.96H5.75A.75.75 0 015 10z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>

      <!-- Agentic context panel -->
      <div class="mt-4 pt-4 border-t border-dark-700">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-sm font-medium text-dark-300">Active Memory Context</h4>
          <button @click="refreshActiveMemory" class="text-xs py-1 px-2 bg-dark-700 text-dark-400 rounded hover:bg-dark-600 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3.5 h-3.5 mr-1">
              <path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 01-9.201 2.466l-.312-.311h2.433a.75.75 0 000-1.5H3.989a.75.75 0 00-.75.75v4.242a.75.75 0 001.5 0v-2.43l.31.31a7 7 0 0011.712-3.138.75.75 0 00-1.449-.39zm1.23-3.723a.75.75 0 00.219-.53V2.929a.75.75 0 00-1.5 0V5.36l-.31-.31A7 7 0 003.239 8.188a.75.75 0 101.448.389A5.5 5.5 0 0113.89 6.11l.311.31h-2.432a.75.75 0 000 1.5h4.243a.75.75 0 00.53-.219z" clip-rule="evenodd" />
            </svg>
            Refresh
          </button>
        </div>
        
        <div v-for="(item, index) in activeMemory" :key="index" :class="['memory-item', { 'focused': index === 2 }]">
          <div class="memory-source">{{ item.source }}</div>
          <div class="memory-content">{{ item.content }}</div>
          <div class="memory-relevance">{{ item.relevance }}%</div>
        </div>
      </div>
    </div>

    <!-- Keep the existing Memory Optimization Suggestions -->
    <div class="glass-panel">
      <div class="flex items-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 text-amber-400 mr-2">
          <path d="M10 1a6 6 0 00-6 6v1.351A5.998 5.998 0 010 13.236l1.821.688-.62 1.693A.75.75 0 002.043 17H3.75a.75.75 0 00.75-.75h10.939a.75.75 0 00.75.75h1.707a.75.75 0 00.842-1.045L17.818 15a5.998 5.998 0 00-4-11.236V7a4 4 0 11-8 0V3.764A5.954 5.954 0 0110 1zm2 13.264V13a2 2 0 11-4 0v1.264a3.025 3.025 0 002 0z" />
        </svg>
        <h3 class="text-lg font-semibold">Memory Optimization Suggestions</h3>
      </div>
      
      <ul class="space-y-3">
        <li v-for="(suggestion, index) in optimizationSuggestions" :key="index" class="flex">
          <span class="text-amber-400 mr-2">•</span>
          <span>{{ suggestion }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';

const props = defineProps({
  memoryMetrics: {
    type: Object,
    default: () => ({
      latency: 125,
      relevance: 92,
      utilization: 78
    })
  },
  activeMemory: {
    type: Array,
    default: () => []
  },
  optimizationSuggestions: {
    type: Array,
    default: () => []
  }
});

// State management
const showPerformanceMetrics = ref(false);

// Methods
const togglePerformanceMetrics = () => {
  showPerformanceMetrics.value = !showPerformanceMetrics.value;
};

const refreshActiveMemory = () => {
  // Emit event to refresh memory context
  console.log('Refreshing memory context');
};

const insertSolution = (type) => {
  // Emit event to insert appropriate solution text into chat
  console.log(`Inserting ${type} solution into chat`);
  
  let solutionText = '';
  
  switch(type) {
    case 'permissions':
      solutionText = `To check background permissions on Android 12:
1. Go to Settings > Apps > CloudSync
2. Tap "Battery"
3. Select "Unrestricted" to allow background activity
4. Return to the previous screen
5. Tap "Permissions" > "Background process" and enable it`;
      break;
    case 'reference':
      solutionText = `I see this is similar to your previous sync issue last month. The solution that worked then was to clear the app's cache. Let's try that:
1. Go to Settings > Apps > CloudSync
2. Tap "Storage & cache"
3. Tap "Clear cache"
4. Restart the app and try backing up again`;
      break;
    case 'backup':
      solutionText = `If automatic backups continue to fail, you can try a manual backup:
1. Open CloudSync app
2. Tap the menu (3 lines) in top-left
3. Select "Backup now"
4. Choose "Manual backup"
5. Select the files you want to back up
6. Tap "Start backup"`;
      break;
  }
  
  // Event would be emitted here to send this text to the chat interface
};
</script>

<style scoped>
.glass-panel {
  background-color: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(71, 85, 105, 0.25);
  backdrop-filter: blur(8px);
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.info-tooltip {
  position: relative;
  display: inline-block;
}

.tooltip-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  transition: all 0.2s;
}

.tooltip-btn:hover {
  background-color: rgba(59, 130, 246, 0.1);
}

.tooltip-content {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
  width: 260px;
  background-color: rgba(30, 41, 59, 0.95);
  border: 1px solid rgba(71, 85, 105, 0.4);
  border-radius: 0.5rem;
  padding: 1rem;
  z-index: 50;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  backdrop-filter: blur(16px);
  animation: fadeIn 0.2s ease-out;
}

.tooltip-header {
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(71, 85, 105, 0.4);
}

.action-button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0.75rem;
  border-radius: 0.5rem;
  background-color: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(71, 85, 105, 0.25);
  text-align: left;
  transition: all 0.2s;
}

.action-button:hover {
  background-color: rgba(55, 65, 81, 0.6);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.action-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  margin-right: 0.75rem;
}

.memory-item {
  display: grid;
  grid-template-columns: 1fr 3fr 40px;
  gap: 0.5rem;
  padding: 0.5rem;
  margin-bottom: 0.25rem;
  border-radius: 0.25rem;
  background-color: rgba(30, 41, 59, 0.3);
  font-size: 0.75rem;
  transition: all 0.2s;
}

.memory-item.focused {
  background-color: rgba(59, 130, 246, 0.2);
  border-left: 2px solid rgb(59, 130, 246);
}

.memory-source {
  color: rgba(156, 163, 175, 1);
}

.memory-content {
  color: rgba(229, 231, 235, 1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.memory-relevance {
  text-align: right;
  color: rgba(156, 163, 175, 1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style> 