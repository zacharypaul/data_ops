<template>
  <div class="tech-stack-3d-container">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
      <div class="loading-text">Loading 3D Visualization...</div>
    </div>
    
    <div class="visualization-header">
      <h2 class="visualization-title">Technology Stack Visualization</h2>
      <div class="visualization-controls">
        <button @click="toggleView" class="control-btn">
          {{ is3DView ? 'Switch to Classic View' : 'Switch to 3D View' }}
        </button>
      </div>
    </div>
    
    <div v-if="is3DView" class="d3-visualization">
      <D3TechGraph 
        :nodes="graphNodes" 
        :connections="graphConnections"
        @nodeSelected="selectNode"
      />
    </div>
    <div v-else class="classic-view">
      <TechStackContainer />
    </div>
    
    <div v-if="selectedNode" class="node-details">
      <div class="details-header">
        <h3>{{ selectedNode.name }}</h3>
        <span class="details-platform">{{ selectedNode.platform }} | {{ selectedNode.technology || 'N/A' }}</span>
      </div>
      <div class="details-content">
        <div v-if="selectedNode.refreshFrequency" class="details-row">
          <span class="details-label">Refresh:</span>
          <span class="details-value">{{ selectedNode.refreshFrequency.interval || 'N/A' }}</span>
        </div>
        <div class="details-row">
          <span class="details-label">Owner:</span>
          <span class="details-value">{{ selectedNode.owner || 'System' }}</span>
        </div>
        <div class="details-connections">
          <span class="details-label">Connections:</span>
          <ul v-if="nodeConnections.length > 0">
            <li v-for="(conn, index) in nodeConnections" :key="index">
              {{ conn.name }} ({{ conn.platform }})
            </li>
          </ul>
          <span v-else class="details-value">No connections</span>
        </div>
      </div>
      <button @click="closeDetails" class="close-btn">×</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import TechStackContainer from './TechStackContainer.vue';
import D3TechGraph from './D3TechGraph.vue';

// State variables
const connectors = ref([]);
const powerBIAssets = ref([]);
const connections = ref([]);
const loading = ref(true);
const error = ref(null);
const is3DView = ref(true);
const selectedNode = ref(null);

// API URL from environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Fetch real data from the backend
const fetchConnectors = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`${API_URL}/connectors`);
    
    // Group connectors by technology
    const groupedConnectors = {};
    response.data.forEach(connector => {
      const tech = connector.technology || 'Unknown';
      if (!groupedConnectors[tech]) {
        groupedConnectors[tech] = [];
      }
      groupedConnectors[tech].push(connector);
    });
    
    // Transform connector data to the format needed for visualization
    connectors.value = [];
    Object.entries(groupedConnectors).forEach(([technology, techConnectors]) => {
      techConnectors.forEach((connector, index) => {
        connectors.value.push({
          id: `snowflake-${connector.name}`,
          name: connector.name,
          technology: connector.technology,
          platform: 'SNOWFLAKE',
          owner: connector.owner,
          techGroup: technology,
          techIndex: index,
          techCount: techConnectors.length,
          refreshFrequency: getRefreshFrequency(connector.technology)
        });
      });
    });
    
    console.log('Fetched connectors:', connectors.value);
    
    // Generate Fabric versions and PowerBI assets
    generateFabricVersions();
    generatePowerBIAssets();
    generateConnections();
    
  } catch (err) {
    console.error('Error fetching connectors:', err);
    error.value = `Failed to fetch data: ${err.message}`;
    
    // Use mock data if API fails
    useMockData();
  } finally {
    loading.value = false;
  }
};

// Create Fabric versions of Snowflake connectors
const generateFabricVersions = () => {
  // For each Snowflake connector, create a Fabric version
  const fabricConnectors = connectors.value
    .filter(conn => conn.platform === 'SNOWFLAKE')
    .map(connector => ({
      id: `fabric-${connector.name}`,
      name: connector.name,
      technology: 'Fabric Service',
      platform: 'FABRIC',
      owner: connector.owner,
      techGroup: connector.techGroup,
      techIndex: connector.techIndex,
      techCount: connector.techCount,
      refreshFrequency: connector.refreshFrequency,
      sourceConnector: connector.id
    }));
  
  // Add Fabric versions to our connectors array
  connectors.value = [...connectors.value, ...fabricConnectors];
};

// Generate PowerBI assets based on connectors and their technologies
const generatePowerBIAssets = () => {
  powerBIAssets.value = [];
  
  // Group connectors by technology for better distribution
  const techGroups = {};
  connectors.value
    .filter(conn => conn.platform === 'SNOWFLAKE' || conn.platform === 'FABRIC')
    .forEach(conn => {
      const key = conn.technology || 'Unknown';
      if (!techGroups[key]) techGroups[key] = [];
      techGroups[key].push(conn);
    });
  
  // Create PowerBI assets for each technology group
  Object.entries(techGroups).forEach(([tech, conns]) => {
    // For each technology, create a balanced number of assets
    conns.forEach((connector, idx) => {
      // Skip some connectors to avoid too many PowerBI assets
      if (idx % 2 !== 0 && connector.platform === 'SNOWFLAKE') return;
      
      const assetType = connector.platform === 'SNOWFLAKE' ? 'Dashboard' : 'Report';
      const refreshFreq = getRefreshFrequency(connector.technology);
      
      powerBIAssets.value.push({
        id: `powerbi-${connector.name}-${connector.platform.toLowerCase()}`,
        name: `${connector.name} ${assetType}`,
        type: `PowerBI ${assetType}`,
        platform: 'POWERBI',
        sourcePlatform: connector.platform,
        sourceConnector: connector.id,
        techGroup: connector.techGroup,
        techIndex: powerBIAssets.value.length,
        owner: connector.owner,
        refreshFrequency: refreshFreq
      });
    });
  });
};

// Generate connections between nodes based on a consistent pattern
const generateConnections = () => {
  connections.value = [];
  
  // Create connections from Snowflake to Fabric (all Snowflake nodes connect to their Fabric counterpart)
  connectors.value.forEach(connector => {
    if (connector.platform === 'FABRIC') {
      // Find the source Snowflake connector
      const sourceConnector = connectors.value.find(c => c.id === connector.sourceConnector);
      
      if (sourceConnector) {
        connections.value.push({
          source: sourceConnector.id,
          target: connector.id,
          refreshFrequency: connector.refreshFrequency,
          active: true
        });
      }
    }
  });
  
  // Create connections to PowerBI assets
  powerBIAssets.value.forEach(asset => {
    // Find source connector
    const sourceConnector = connectors.value.find(c => c.id === asset.sourceConnector);
    if (sourceConnector) {
      connections.value.push({
        source: asset.sourceConnector,
        target: asset.id,
        refreshFrequency: asset.refreshFrequency,
        active: true
      });
    }
  });
};

// Get refresh frequency based on technology
const getRefreshFrequency = (technology) => {
  if (!technology) return { type: 'daily', interval: '24h' };
  
  if (technology.includes('Fivetran')) {
    return { type: 'hourly', interval: '1h' };
  } else if (technology.includes('Airflow')) {
    return { type: 'daily', interval: '24h' };
  } else {
    return { type: 'weekly', interval: '7d' };
  }
};

// Use mock data if API fails
const useMockData = () => {
  // Simple mock data for demonstration
  const mockConnectors = [
    { id: 'snowflake-connector1', name: 'Connector 1', technology: 'Snowflake Airflow', platform: 'SNOWFLAKE', owner: 'twks' },
    { id: 'snowflake-connector2', name: 'Connector 2', technology: 'Snowflake Fivetran', platform: 'SNOWFLAKE', owner: 'ind' },
    { id: 'snowflake-connector3', name: 'Connector 3', technology: 'Snowflake ADF', platform: 'SNOWFLAKE', owner: 'zach' }
  ];
  
  connectors.value = mockConnectors.map(conn => ({
    ...conn,
    refreshFrequency: getRefreshFrequency(conn.technology)
  }));
  
  // Generate the rest of the data
  generateFabricVersions();
  generatePowerBIAssets();
  generateConnections();
};

// Transform data for D3 visualization
const graphNodes = computed(() => {
  return [
    ...connectors.value,
    ...powerBIAssets.value
  ];
});

const graphConnections = computed(() => {
  return connections.value;
});

// Select a node for detail view
const selectNode = (node) => {
  selectedNode.value = node;
};

// Get connections for the selected node
const nodeConnections = computed(() => {
  if (!selectedNode.value) return [];
  
  const nodeId = selectedNode.value.id;
  const result = [];
  
  // Find outgoing connections
  connections.value.forEach(conn => {
    if (conn.source === nodeId) {
      const targetNode = graphNodes.value.find(node => node.id === conn.target);
      if (targetNode) {
        result.push({
          name: targetNode.name,
          platform: targetNode.platform,
          direction: 'outgoing'
        });
      }
    }
  });
  
  // Find incoming connections
  connections.value.forEach(conn => {
    if (conn.target === nodeId) {
      const sourceNode = graphNodes.value.find(node => node.id === conn.source);
      if (sourceNode) {
        result.push({
          name: sourceNode.name,
          platform: sourceNode.platform,
          direction: 'incoming'
        });
      }
    }
  });
  
  return result;
});

// Close the details panel
const closeDetails = () => {
  selectedNode.value = null;
};

// Toggle between 3D and classic view
const toggleView = () => {
  is3DView.value = !is3DView.value;
};

// Initialize on mount
onMounted(() => {
  fetchConnectors();
});
</script>

<style scoped>
.tech-stack-3d-container {
  position: relative;
  width: 100%;
  height: 80vh;
  min-height: 600px;
  overflow: hidden;
  background-color: #0f172a;
  border-radius: 0.5rem;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
}

.visualization-header {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  width: calc(100% - 40px);
}

.visualization-title {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.visualization-controls {
  display: flex;
  gap: 1rem;
}

.control-btn {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.control-btn:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
}

.d3-visualization,
.classic-view {
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(15, 23, 42, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 20;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.loading-text {
  color: white;
  font-size: 1.25rem;
}

.node-details {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 300px;
  background-color: rgba(15, 23, 42, 0.8);
  border-radius: 0.5rem;
  padding: 1rem;
  color: white;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.details-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.details-header h3 {
  margin: 0 0 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.details-platform {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.7);
}

.details-content {
  font-size: 0.9rem;
}

.details-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.details-label {
  color: rgba(255, 255, 255, 0.7);
}

.details-value {
  font-weight: 500;
}

.details-connections {
  margin-top: 1rem;
}

.details-connections ul {
  margin-top: 0.5rem;
  padding-left: 1.5rem;
}

.details-connections li {
  margin-bottom: 0.25rem;
}

.close-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  font-size: 1.5rem;
  cursor: pointer;
  line-height: 1;
}

.close-btn:hover {
  color: white;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style> 