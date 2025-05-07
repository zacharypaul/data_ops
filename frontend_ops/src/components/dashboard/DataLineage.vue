<template>
  <div class="bg-dark-800/60 rounded-lg p-6 border border-dark-700 mb-8">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-display font-bold">Data Lineage Visualization</h2>
      <div class="flex items-center space-x-3">
        <button 
          @click="toggleView('graph')"
          :class="[
            'px-3 py-1.5 text-sm rounded-md transition-colors',
            view === 'graph' 
              ? 'bg-primary-600 text-white' 
              : 'bg-dark-700 text-dark-300 hover:text-white'
          ]"
        >
          Graph View
        </button>
        <button 
          @click="toggleView('table')"
          :class="[
            'px-3 py-1.5 text-sm rounded-md transition-colors',
            view === 'table' 
              ? 'bg-primary-600 text-white' 
              : 'bg-dark-700 text-dark-300 hover:text-white'
          ]"
        >
          Table View
        </button>
        <div class="relative">
          <select 
            v-model="selectedConnector" 
            class="bg-dark-700/50 border border-dark-600 rounded-md px-3 py-1.5 text-sm appearance-none pr-8 text-white focus:outline-none focus:border-primary-500"
          >
            <option value="all">All Connectors</option>
            <option v-for="connector in connectors" :key="connector.id" :value="connector.id">
              {{ connector.name }}
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

    <!-- Loading State -->
    <div v-if="isLoading" class="h-96 flex items-center justify-center">
      <svg class="animate-spin h-8 w-8 text-primary-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <!-- Graph View -->
    <div v-else-if="view === 'graph'" class="graph-container h-96 relative">
      <!-- New simple graph rendering -->
      <div class="w-full h-full lineage-network" ref="lineageGraphContainer">
        <!-- Nodes will be rendered here -->
        <div v-for="node in filteredConnectors" :key="node.id" 
             class="lineage-node"
             :class="`lineage-node--${getConnectorColor(node.type)}`"
             :style="getNodePosition(node)"
             @click="selectNode(node)">
          <div class="lineage-node__content">
            <div class="lineage-node__label">{{ node.name }}</div>
            <div class="lineage-node__type">{{ node.type }}</div>
          </div>
          <div v-if="node.quality" class="lineage-node__indicator" :class="`status-${node.quality.status || 'green'}`"></div>
        </div>
        
        <!-- Links between nodes -->
        <svg class="lineage-links">
          <g>
            <path v-for="(link, index) in nodeLinks" 
                  :key="index"
                  :d="calculateLinkPath(link)"
                  :class="`link-${getConnectorColor(getLinkSourceType(link))}`"
                  class="lineage-link"
                  marker-end="url(#arrowhead)">
            </path>
          </g>
          <defs>
            <marker id="arrowhead" viewBox="0 0 10 10" refX="5" refY="5"
                    markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 0 L 10 5 L 0 10 z" fill="rgba(255, 255, 255, 0.7)"></path>
            </marker>
          </defs>
        </svg>
      </div>
      
      <!-- Node Details Panel -->
      <div 
        v-if="selectedNode" 
        class="absolute top-3 left-3 p-4 rounded-md shadow-lg max-w-xs node-details"
      >
        <div class="flex justify-between items-start mb-2">
          <h3 class="text-lg font-bold text-white">{{ selectedNode.name }}</h3>
          <button @click="selectedNode = null" class="text-dark-400 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <div class="text-sm mb-3">
          <span :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${getConnectorColor(selectedNode.type)}-600/30 text-${getConnectorColor(selectedNode.type)}-400`">
            {{ selectedNode.type }}
          </span>
        </div>
        
        <div class="space-y-3 text-sm">
          <div v-if="selectedNode.upstream && selectedNode.upstream.length > 0">
            <div class="text-dark-400 mb-1 uppercase text-xs font-medium">Upstream Dependencies:</div>
            <div class="text-white">
              <div v-for="dep in selectedNode.upstream" :key="dep.id" class="flex items-center space-x-1 mb-1">
                <span :class="`w-2 h-2 rounded-full bg-${getConnectorColor(dep.type)}-500`"></span>
                <span>{{ dep.name }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="selectedNode.downstream && selectedNode.downstream.length > 0">
            <div class="text-dark-400 mb-1 uppercase text-xs font-medium">Downstream Dependencies:</div>
            <div class="text-white">
              <div v-for="dep in selectedNode.downstream" :key="dep.id" class="flex items-center space-x-1 mb-1">
                <span :class="`w-2 h-2 rounded-full bg-${getConnectorColor(dep.type)}-500`"></span>
                <span>{{ dep.name }}</span>
              </div>
            </div>
          </div>
          
          <div v-if="selectedNode.lastRefresh">
            <div class="text-dark-400 mb-1 uppercase text-xs font-medium">Last Refresh:</div>
            <div class="text-white">{{ selectedNode.lastRefresh }}</div>
          </div>
          
          <div v-if="selectedNode.quality">
            <div class="text-dark-400 mb-1 uppercase text-xs font-medium">Quality Score:</div>
            <div class="flex items-center">
              <div class="w-24 bg-dark-700 rounded-full h-2 mr-2">
                <div 
                  :class="`h-2 rounded-full bg-${selectedNode.quality.status || 'green'}-500`" 
                  :style="`width: ${selectedNode.quality.value}%`"
                ></div>
              </div>
              <span class="text-white">{{ selectedNode.quality.value }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Table View -->
    <div v-else-if="view === 'table'" class="max-h-96 overflow-y-auto">
      <table class="min-w-full">
        <thead class="bg-dark-700/50 sticky top-0">
          <tr>
            <th class="text-left py-3 px-4 text-dark-400">Connector</th>
            <th class="text-left py-3 px-4 text-dark-400">Type</th>
            <th class="text-left py-3 px-4 text-dark-400">Upstream</th>
            <th class="text-left py-3 px-4 text-dark-400">Downstream</th>
            <th class="text-left py-3 px-4 text-dark-400">Impact Level</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-dark-700">
          <tr 
            v-for="connector in filteredConnectors" 
            :key="connector.id"
            class="hover:bg-dark-700/30 transition-colors"
          >
            <td class="py-3 px-4">{{ connector.name }}</td>
            <td class="py-3 px-4">
              <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${getConnectorColor(connector.type)}-900/30 text-${getConnectorColor(connector.type)}-400`">
                {{ connector.type }}
              </span>
            </td>
            <td class="py-3 px-4">
              <div v-if="connector.upstream && connector.upstream.length > 0" class="flex flex-wrap gap-1">
                <span 
                  v-for="dep in connector.upstream" 
                  :key="dep.id"
                  :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${getConnectorColor(dep.type)}-900/20 text-${getConnectorColor(dep.type)}-400 border border-${getConnectorColor(dep.type)}-900/30`"
                >
                  {{ dep.name }}
                </span>
              </div>
              <span v-else class="text-dark-400">None</span>
            </td>
            <td class="py-3 px-4">
              <div v-if="connector.downstream && connector.downstream.length > 0" class="flex flex-wrap gap-1">
                <span 
                  v-for="dep in connector.downstream" 
                  :key="dep.id"
                  :class="`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-${getConnectorColor(dep.type)}-900/20 text-${getConnectorColor(dep.type)}-400 border border-${getConnectorColor(dep.type)}-900/30`"
                >
                  {{ dep.name }}
                </span>
              </div>
              <span v-else class="text-dark-400">None</span>
            </td>
            <td class="py-3 px-4">
              <span 
                :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getImpactLevelClass(connector)}`"
              >
                {{ getImpactLevel(connector) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Legend -->
    <div class="mt-4 pt-4 border-t border-dark-700 flex flex-wrap gap-4">
      <div class="flex items-center space-x-2">
        <span class="w-3 h-3 rounded-full bg-primary-500"></span>
        <span class="text-sm text-dark-300">Fivetran</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="w-3 h-3 rounded-full bg-accent-500"></span>
        <span class="text-sm text-dark-300">Airflow</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="w-3 h-3 rounded-full bg-secondary-500"></span>
        <span class="text-sm text-dark-300">ADF</span>
      </div>
      <div class="flex items-center space-x-2">
        <span class="w-3 h-3 rounded-full bg-gold-500"></span>
        <span class="text-sm text-dark-300">Lambda</span>
      </div>
      <div class="flex items-center space-x-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-primary-400" viewBox="0 0 24 24" stroke="currentColor" fill="none">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
        </svg>
        <span class="text-sm text-dark-300">Data Flow Direction</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import DashboardApi from '@/services/DashboardApi';
import * as d3 from 'd3';

// Component state
const view = ref('graph');
const isLoading = ref(true);
const connectors = ref([]);
const selectedConnector = ref('all');
const lineageGraphContainer = ref(null);
const selectedNode = ref(null);

// Toggle between graph and table view
const toggleView = (viewType) => {
  view.value = viewType;
};

// Get connector color based on type
const getConnectorColor = (type) => {
  const typeMap = {
    'Fivetran': 'primary',
    'Airflow': 'accent',
    'ADF': 'secondary',
    'Lambda': 'gold'
  };
  
  return typeMap[type] || 'primary';
};

// Get impact level (high, medium, low) based on downstream dependencies
const getImpactLevel = (connector) => {
  if (!connector.downstream || connector.downstream.length === 0) {
    return 'Low';
  }
  
  if (connector.downstream.length > 3) {
    return 'High';
  }
  
  return 'Medium';
};

// Get CSS class for impact level
const getImpactLevelClass = (connector) => {
  const level = getImpactLevel(connector);
  
  if (level === 'High') {
    return 'bg-red-900/30 text-red-400';
  }
  
  if (level === 'Medium') {
    return 'bg-yellow-900/30 text-yellow-400';
  }
  
  return 'bg-green-900/30 text-green-400';
};

// Filtered connectors based on selection
const filteredConnectors = computed(() => {
  if (selectedConnector.value === 'all') {
    return connectors.value;
  }
  
  const selected = connectors.value.find(c => c.id === Number(selectedConnector.value));
  if (!selected) return connectors.value;
  
  // Include the selected connector and its immediate dependencies
  const relatedIds = new Set();
  relatedIds.add(selected.id);
  
  // Add upstream dependencies
  if (selected.upstream) {
    selected.upstream.forEach(dep => relatedIds.add(dep.id));
  }
  
  // Add downstream dependencies
  if (selected.downstream) {
    selected.downstream.forEach(dep => relatedIds.add(dep.id));
  }
  
  return connectors.value.filter(c => relatedIds.has(c.id));
});

// Get links between nodes
const nodeLinks = computed(() => {
  const links = [];
  
  filteredConnectors.value.forEach(source => {
    if (source.downstream) {
      source.downstream.forEach(target => {
        const targetNode = filteredConnectors.value.find(c => c.id === target.id);
        if (targetNode) {
          links.push({
            source: source,
            target: targetNode
          });
        }
      });
    }
  });
  
  return links;
});

// Calculate link path between nodes
const calculateLinkPath = (link) => {
  const sourcePos = getNodeCoordinates(link.source);
  const targetPos = getNodeCoordinates(link.target);
  
  // Calculate curve control point
  const midX = (sourcePos.x + targetPos.x) / 2;
  const midY = (sourcePos.y + targetPos.y) / 2;
  
  // Add slight curve to the path
  return `M ${sourcePos.x} ${sourcePos.y} 
          Q ${midX + 20} ${midY} ${targetPos.x} ${targetPos.y}`;
};

// Get the source type of a link
const getLinkSourceType = (link) => {
  return link.source.type;
};

// Get node position style based on its index
const getNodePosition = (node) => {
  const pos = getNodeCoordinates(node);
  return {
    left: `${pos.x}px`,
    top: `${pos.y}px`
  };
};

// Generate coordinates for nodes in a grid layout
const getNodeCoordinates = (node) => {
  const index = filteredConnectors.value.findIndex(n => n.id === node.id);
  const total = filteredConnectors.value.length;
  
  // Calculate position based on index
  // Use a modified circular layout
  const containerWidth = 700;
  const containerHeight = 400;
  const radius = Math.min(containerWidth, containerHeight) * 0.38;
  const centerX = containerWidth / 2;
  const centerY = containerHeight / 2;
  
  // If very few nodes, arrange them horizontally
  if (total <= 3) {
    const step = containerWidth / (total + 1);
    return {
      x: step * (index + 1),
      y: containerHeight / 2
    };
  }

  // Use circular arrangement for more nodes
  const angle = (index / total) * 2 * Math.PI;
  const x = centerX + radius * Math.cos(angle);
  const y = centerY + radius * Math.sin(angle);
  
  return { x, y };
};

// Select a node
const selectNode = (node) => {
  selectedNode.value = node;
};

// Fetch lineage data
const fetchLineageData = async () => {
  isLoading.value = true;
  
  try {
    const data = await DashboardApi.getConnectorLineage();
    connectors.value = data;
    
    setTimeout(() => {
      isLoading.value = false;
    }, 300);
  } catch (error) {
    console.error('Error fetching lineage data:', error);
    isLoading.value = false;
  }
};

// Initialize
onMounted(() => {
  fetchLineageData();
});
</script>

<style scoped>
.graph-container {
  position: relative;
  border-radius: 0.375rem;
  background-color: rgba(13, 18, 30, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.lineage-network {
  position: relative;
  height: 100%;
  background-color: rgba(13, 18, 30, 0.5);
}

.lineage-node {
  position: absolute;
  transform: translate(-50%, -50%);
  width: 120px;
  height: 60px;
  border-radius: 30px;
  background-color: #111827;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  user-select: none;
  border: 2px solid;
}

.lineage-node__content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: calc(100% - 10px);
  padding: 4px;
}

.lineage-node__label {
  font-weight: 600;
  font-size: 12px;
  line-height: 1.2;
  color: white;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.lineage-node__type {
  font-size: 9px;
  opacity: 0.7;
  color: rgba(255, 255, 255, 0.8);
}

.lineage-node__indicator {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid #111827;
}

.lineage-node--primary {
  border-color: var(--color-primary-500);
  background: linear-gradient(135deg, rgba(76, 85, 201, 0.1), rgba(76, 85, 201, 0.3));
}

.lineage-node--accent {
  border-color: var(--color-accent-500);
  background: linear-gradient(135deg, rgba(224, 77, 194, 0.1), rgba(224, 77, 194, 0.3));
}

.lineage-node--secondary {
  border-color: var(--color-secondary-500);
  background: linear-gradient(135deg, rgba(56, 149, 255, 0.1), rgba(56, 149, 255, 0.3));
}

.lineage-node--gold {
  border-color: var(--color-gold-500);
  background: linear-gradient(135deg, rgba(246, 173, 85, 0.1), rgba(246, 173, 85, 0.3));
}

.lineage-node:hover {
  transform: translate(-50%, -50%) scale(1.05);
  z-index: 20;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
}

.lineage-links {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.lineage-link {
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  opacity: 0.6;
}

.link-primary {
  stroke: var(--color-primary-500);
}

.link-accent {
  stroke: var(--color-accent-500);
}

.link-secondary {
  stroke: var(--color-secondary-500);
}

.link-gold {
  stroke: var(--color-gold-500);
}

.status-green {
  background-color: var(--color-green-500);
}

.status-yellow {
  background-color: var(--color-yellow-500);
}

.status-red {
  background-color: var(--color-red-500);
}

.node-details {
  background-color: rgba(20, 27, 45, 0.85);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
</style> 