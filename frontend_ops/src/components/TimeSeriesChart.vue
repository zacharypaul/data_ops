<template>
  <div class="glass-card p-6 mb-8 relative z-10">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold text-primary-300">Performance Evolution Over Time</h3>
      <button @click="$emit('update:showInfo', !showInfo)" class="text-gray-400 hover:text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
    
    <div v-if="showInfo" class="bg-dark-800 p-4 rounded-md mb-4 text-sm">
      <h4 class="font-semibold text-primary-300 mb-2">Understanding This Chart</h4>
      <p class="mb-2 text-gray-300">This time series visualization tracks model performance across multiple iterations and time periods. Key points:</p>
      <ul class="list-disc pl-5 space-y-1 text-gray-300 mb-3">
        <li><span class="text-purple-400 font-semibold">Model v1 (purple)</span>: Started with lower metrics but shows consistent improvements with occasional plateaus.</li>
        <li><span class="text-green-400 font-semibold">Model v2 (green)</span>: Began development later but quickly outperformed v1, showing the steepest improvement trajectory.</li>
        <li><span class="text-cyan-400 font-semibold">Model v3 (cyan)</span>: The most recent iteration, building on learnings from v1 but taking a different approach than v2.</li>
      </ul>
      <p class="text-gray-300">Higher values indicate better model performance. The <span class="font-semibold">intersection points</span> highlight when one model version surpassed another, suggesting key architectural or hyperparameter improvements.</p>
    </div>
    
    <div class="flex items-center mb-4">
      <div class="mr-4">
        <select v-model="selectedMetric" @change="$emit('update:selectedMetric', selectedMetric)" class="bg-dark-800 border border-dark-600 text-gray-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500">
          <option value="silhouette">Silhouette Score</option>
          <option value="inertia">Inertia</option>
          <option value="runtime">Runtime (s)</option>
        </select>
      </div>
      <div>
        <label class="text-gray-400 mr-2 text-sm">Time Range:</label>
        <select v-model="timeRange" @change="$emit('update:timeRange', timeRange)" class="bg-dark-800 border border-dark-600 text-gray-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-primary-500">
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
        </select>
      </div>
    </div>
    
    <div class="h-80 w-full relative">
      <!-- Time Series Chart -->
      <div class="w-full h-full flex items-center justify-center bg-dark-800 rounded-lg border border-dark-700 relative overflow-hidden">
        <!-- Chart content -->
        <svg class="w-full h-full p-6" viewBox="0 0 1000 400" preserveAspectRatio="none">
          <!-- Background grid -->
          <line x1="80" y1="350" x2="950" y2="350" stroke="#4b5563" stroke-width="1.5" />
          <line x1="80" y1="280" x2="950" y2="280" stroke="#374151" stroke-width="0.5" stroke-dasharray="5,5" />
          <line x1="80" y1="210" x2="950" y2="210" stroke="#374151" stroke-width="0.5" stroke-dasharray="5,5" />
          <line x1="80" y1="140" x2="950" y2="140" stroke="#374151" stroke-width="0.5" stroke-dasharray="5,5" />
          <line x1="80" y1="70" x2="950" y2="70" stroke="#374151" stroke-width="0.5" stroke-dasharray="5,5" />
          
          <line x1="80" y1="50" x2="80" y2="350" stroke="#4b5563" stroke-width="1.5" />
          
          <!-- X-axis labels -->
          <text x="80" y="380" fill="#9ca3af" font-size="12">Oct 15</text>
          <text x="225" y="380" fill="#9ca3af" font-size="12">Oct 17</text>
          <text x="370" y="380" fill="#9ca3af" font-size="12">Oct 19</text>
          <text x="515" y="380" fill="#9ca3af" font-size="12">Oct 21</text>
          <text x="660" y="380" fill="#9ca3af" font-size="12">Oct 23</text>
          <text x="805" y="380" fill="#9ca3af" font-size="12">Oct 25</text>
          
          <!-- Y-axis labels -->
          <text x="50" y="70" fill="#9ca3af" font-size="12" text-anchor="end">0.75</text>
          <text x="50" y="140" fill="#9ca3af" font-size="12" text-anchor="end">0.70</text>
          <text x="50" y="210" fill="#9ca3af" font-size="12" text-anchor="end">0.65</text>
          <text x="50" y="280" fill="#9ca3af" font-size="12" text-anchor="end">0.60</text>
          <text x="50" y="350" fill="#9ca3af" font-size="12" text-anchor="end">0.55</text>
          
          <!-- Model v1 line -->
          <path 
            d="M80,315 L225,245 L370,260 L515,215 L660,190 L805,210 L950,205" 
            stroke="#8b5cf6" 
            stroke-width="3" 
            fill="none" 
            stroke-linejoin="round"
          />
          
          <!-- Model v2 line -->
          <path 
            d="M225,260 L370,215 L515,165 L660,125 L805,95 L950,80" 
            stroke="#10b981" 
            stroke-width="3" 
            fill="none" 
            stroke-linejoin="round"
          />
          
          <!-- Model v3 line -->
          <path 
            d="M370,280 L515,230 L660,200 L805,175 L950,160" 
            stroke="#06b6d4" 
            stroke-width="3" 
            fill="none" 
            stroke-linejoin="round"
          />
          
          <!-- Data points for Model v1 -->
          <circle cx="80" cy="315" r="6" fill="#8b5cf6" />
          <circle cx="225" cy="245" r="6" fill="#8b5cf6" />
          <circle cx="370" cy="260" r="6" fill="#8b5cf6" />
          <circle cx="515" cy="215" r="6" fill="#8b5cf6" />
          <circle cx="660" cy="190" r="6" fill="#8b5cf6" />
          <circle cx="805" cy="210" r="6" fill="#8b5cf6" />
          <circle cx="950" cy="205" r="6" fill="#8b5cf6" />
          
          <!-- Data points for Model v2 -->
          <circle cx="225" cy="260" r="6" fill="#10b981" />
          <circle cx="370" cy="215" r="6" fill="#10b981" />
          <circle cx="515" cy="165" r="6" fill="#10b981" />
          <circle cx="660" cy="125" r="6" fill="#10b981" />
          <circle cx="805" cy="95" r="6" fill="#10b981" />
          <circle cx="950" cy="80" r="6" fill="#10b981" />
          
          <!-- Data points for Model v3 -->
          <circle cx="370" cy="280" r="6" fill="#06b6d4" />
          <circle cx="515" cy="230" r="6" fill="#06b6d4" />
          <circle cx="660" cy="200" r="6" fill="#06b6d4" />
          <circle cx="805" cy="175" r="6" fill="#06b6d4" />
          <circle cx="950" cy="160" r="6" fill="#06b6d4" />
        </svg>
        
        <!-- Legend -->
        <div class="absolute top-4 right-4 bg-dark-900/80 p-2 rounded-md">
          <div class="flex flex-col space-y-2">
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full bg-purple-500 mr-2"></div>
              <span class="text-xs text-gray-300">Model v1</span>
            </div>
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
              <span class="text-xs text-gray-300">Model v2</span>
            </div>
            <div class="flex items-center">
              <div class="w-3 h-3 rounded-full bg-cyan-500 mr-2"></div>
              <span class="text-xs text-gray-300">Model v3</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="mt-4 text-sm text-gray-400">
      <p>Showing {{ selectedMetric === 'silhouette' ? 'Silhouette Score' : selectedMetric === 'inertia' ? 'Inertia' : 'Runtime (s)' }} evolution over time for all experiment iterations. The time-series view helps identify performance trends and model improvements.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  initialMetric: {
    type: String,
    default: 'silhouette'
  },
  initialTimeRange: {
    type: String,
    default: '30d'
  },
  showInfo: {
    type: Boolean,
    default: false
  }
});

const selectedMetric = ref(props.initialMetric);
const timeRange = ref(props.initialTimeRange);

defineEmits(['update:selectedMetric', 'update:timeRange', 'update:showInfo']);
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style> 