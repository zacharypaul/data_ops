<template>
  <div class="tech-stack-container">
    <div class="grid-3d-container">
      <!-- Snowflake Column (Left) -->
      <div class="stack-column snowflake-column">
        <div class="column-header">
          <h2 class="text-2xl font-display font-bold mb-6 text-secondary-500">
            <SnowflakeIcon class="h-6 w-6 inline-block mr-2" />
            Snowflake / AWS
          </h2>
        </div>
        <div class="nodes-container">
          <TechNode 
            v-for="connector in connectors" 
            :key="`snowflake-${connector.name}`"
            :connector="connector"
            :platform="'snowflake'"
            @node-hover="handleNodeHover"
          />
        </div>
      </div>
      
      <!-- Fabric Column (Center) -->
      <div class="stack-column fabric-column">
        <div class="column-header">
          <h2 class="text-2xl font-display font-bold mb-6 text-accent-500">
            <FabricIcon class="h-6 w-6 inline-block mr-2" />
            Microsoft Fabric
          </h2>
        </div>
        <div class="nodes-container">
          <TechNode 
            v-for="connector in connectors" 
            :key="`fabric-${connector.name}`"
            :connector="{ ...connector, platform: 'fabric' }"
            :platform="'fabric'"
            :mapping="getFabricEquivalent(connector)"
            @node-hover="handleNodeHover"
          />
        </div>
      </div>
      
      <!-- PowerBI Column (Right) -->
      <div class="stack-column powerbi-column">
        <div class="column-header">
          <h2 class="text-2xl font-display font-bold mb-6 text-powerbi-500">
            <PowerBIIcon class="h-6 w-6 inline-block mr-2" />
            Power BI Assets
          </h2>
        </div>
        <div class="nodes-container">
          <TechNode 
            v-for="asset in powerBIAssets" 
            :key="`powerbi-${asset.name}`"
            :connector="asset"
            :platform="'powerbi'"
            @node-hover="handleNodeHover"
          />
        </div>
      </div>
    </div>
    
    <!-- Connection Lines Layer -->
    <div class="connections-layer">
      <TechConnection 
        v-for="(connection, index) in activeConnections"
        :key="`connection-${index}`"
        :connection="connection"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import TechNode from './TechNode.vue';
import TechConnection from './TechConnection.vue';
import SnowflakeIcon from './icons/SnowflakeIcon.vue';
import FabricIcon from './icons/FabricIcon.vue';
import PowerBIIcon from './icons/PowerBIIcon.vue';

// State variables
const connectors = ref([]);
const loading = ref(true);
const error = ref(null);
const hoveredNode = ref(null);
const activeConnections = ref([]);

// API URL from environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// Fabric equivalents of Snowflake technologies
const fabricMapping = {
  'Snowflake ADF': 'Data Factory',
  'Snowflake Airflow': 'Fabric Pipelines',
  'Snowflake Fivetran': 'OneLake Ingestion'
};

// Refresh frequency data
const refreshFrequencies = {
  hourly: { speed: 'fast', interval: '1h', duration: 3 },
  daily: { speed: 'medium', interval: '24h', duration: 7 },
  weekly: { speed: 'slow', interval: '7d', duration: 12 }
};

// Generate mock PowerBI assets
const generatePowerBIAssets = (connectors) => {
  const assets = [];
  const assetTypes = ['Dashboard', 'Report', 'Dataset'];
  const departments = ['Sales', 'Marketing', 'Finance', 'Operations', 'Product'];
  
  // Generate 1-3 PowerBI assets per connector
  connectors.forEach(connector => {
    const numAssets = Math.floor(Math.random() * 3) + 1;
    for (let i = 0; i < numAssets; i++) {
      const assetType = assetTypes[Math.floor(Math.random() * assetTypes.length)];
      const department = departments[Math.floor(Math.random() * departments.length)];
      const sourcePlatform = Math.random() > 0.5 ? 'snowflake' : 'fabric';
      
      assets.push({
        name: `${department} ${assetType}`,
        type: assetType,
        department: department,
        sourceConnector: connector.name,
        sourcePlatform: sourcePlatform,
        technology: 'PowerBI',
        refreshFrequency: connector.refreshFrequency || getRandomRefreshFrequency()
      });
    }
  });
  
  return assets;
};

// PowerBI assets computed from connectors
const powerBIAssets = computed(() => {
  if (connectors.value.length === 0) return [];
  return generatePowerBIAssets(connectors.value);
});

// Get random refresh frequency
const getRandomRefreshFrequency = () => {
  const frequencies = Object.keys(refreshFrequencies);
  const randomFreq = frequencies[Math.floor(Math.random() * frequencies.length)];
  return {
    ...refreshFrequencies[randomFreq],
    type: randomFreq
  };
};

// Get the Fabric equivalent for a Snowflake connector
const getFabricEquivalent = (connector) => {
  if (!connector || !connector.technology) return '';
  return fabricMapping[connector.technology] || 'Fabric Lakehouse';
};

// Fetch connectors from backend
const fetchConnectors = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`${API_URL}/connectors`);
    connectors.value = response.data;
    
    // Assign simulated refresh frequencies
    connectors.value.forEach(connector => {
      // Randomly assign a refresh frequency for demo purposes
      connector.refreshFrequency = getRandomRefreshFrequency();
    });
    
  } catch (err) {
    console.error('Error fetching connectors:', err);
    error.value = 'Failed to fetch connector data. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Handle node hover event
const handleNodeHover = (nodeData) => {
  hoveredNode.value = nodeData;
  
  if (nodeData) {
    // Generate connections based on the hovered node
    generateConnections(nodeData);
  } else {
    // Clear connections when no node is hovered
    activeConnections.value = [];
  }
};

// Generate connections between platforms based on the hovered node
const generateConnections = (node) => {
  activeConnections.value = [];
  
  if (node.platform === 'snowflake') {
    // Snowflake to Fabric connection
    activeConnections.value.push({
      source: {
        platform: 'snowflake',
        id: node.connector.name
      },
      target: {
        platform: 'fabric',
        id: node.connector.name
      },
      refreshFrequency: node.connector.refreshFrequency,
      direction: 'forward',
      active: true
    });
    
    // Look for PowerBI assets connected to this Snowflake connector
    const connectedAssets = powerBIAssets.value.filter(
      asset => asset.sourceConnector === node.connector.name && asset.sourcePlatform === 'snowflake'
    );
    
    connectedAssets.forEach(asset => {
      activeConnections.value.push({
        source: {
          platform: 'snowflake',
          id: node.connector.name
        },
        target: {
          platform: 'powerbi',
          id: asset.name
        },
        refreshFrequency: asset.refreshFrequency,
        direction: 'forward',
        active: true
      });
    });
  } 
  else if (node.platform === 'fabric') {
    // Fabric to Snowflake connection (backward)
    activeConnections.value.push({
      source: {
        platform: 'snowflake',
        id: node.connector.name
      },
      target: {
        platform: 'fabric',
        id: node.connector.name
      },
      refreshFrequency: node.connector.refreshFrequency,
      direction: 'forward',
      active: true
    });
    
    // Look for PowerBI assets connected to this Fabric connector
    const connectedAssets = powerBIAssets.value.filter(
      asset => asset.sourceConnector === node.connector.name && asset.sourcePlatform === 'fabric'
    );
    
    connectedAssets.forEach(asset => {
      activeConnections.value.push({
        source: {
          platform: 'fabric',
          id: node.connector.name
        },
        target: {
          platform: 'powerbi',
          id: asset.name
        },
        refreshFrequency: asset.refreshFrequency,
        direction: 'forward',
        active: true
      });
    });
  }
  else if (node.platform === 'powerbi') {
    // PowerBI to its source connection
    const asset = node.connector;
    
    activeConnections.value.push({
      source: {
        platform: asset.sourcePlatform,
        id: asset.sourceConnector
      },
      target: {
        platform: 'powerbi',
        id: asset.name
      },
      refreshFrequency: asset.refreshFrequency,
      direction: 'forward',
      active: true
    });
  }
};

onMounted(() => {
  fetchConnectors();
});
</script>

<style scoped>
.tech-stack-container {
  position: relative;
  width: 100%;
  min-height: 800px;
  overflow: hidden;
  perspective: 2000px;
  transform-style: preserve-3d;
  padding: 40px 0;
}

.grid-3d-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
  position: relative;
  z-index: 10;
  transform-style: preserve-3d;
  transform: rotateX(15deg);
}

.stack-column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background-color: rgba(15, 23, 42, 0.3);
  border-radius: 1rem;
  padding: 1.5rem;
  backdrop-filter: blur(4px);
  position: relative;
  transition: all 0.5s ease;
  transform-style: preserve-3d;
  box-shadow: 0 20px 30px -15px rgba(2, 6, 23, 0.3);
}

.snowflake-column {
  background-color: rgba(14, 32, 61, 0.3);
  border: 1px solid rgba(56, 189, 248, 0.2);
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.1), 0 20px 30px -15px rgba(2, 6, 23, 0.5);
  transform: translateZ(80px) translateX(-30px) rotateY(-15deg);
  z-index: 20;
}

.fabric-column {
  background-color: rgba(14, 61, 42, 0.3);
  border: 1px solid rgba(45, 212, 191, 0.2);
  box-shadow: 0 0 15px rgba(45, 212, 191, 0.1), 0 20px 30px -15px rgba(2, 6, 23, 0.5);
  transform: translateZ(40px);
  z-index: 10;
}

.powerbi-column {
  background-color: rgba(61, 14, 57, 0.3);
  border: 1px solid rgba(217, 70, 239, 0.2);
  box-shadow: 0 0 15px rgba(217, 70, 239, 0.1), 0 20px 30px -15px rgba(2, 6, 23, 0.5);
  transform: translateZ(80px) translateX(30px) rotateY(15deg);
  z-index: 20;
}

.column-header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
  margin-bottom: 1rem;
  transform-style: preserve-3d;
}

.column-header h2 {
  transform: translateZ(10px);
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.nodes-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  overflow-y: auto;
  max-height: 700px;
  padding-right: 0.5rem;
  transform-style: preserve-3d;
}

.nodes-container::-webkit-scrollbar {
  width: 6px;
}

.nodes-container::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.nodes-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.nodes-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

.connections-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 5;
  transform-style: preserve-3d;
}

/* Add text color for PowerBI */
:root {
  --color-powerbi-500: rgb(217, 70, 239);
  --color-powerbi-400: rgb(232, 121, 249);
}

.text-powerbi-500 {
  color: var(--color-powerbi-500);
}

/* Column hover effects for 3D feel */
.stack-column:hover {
  transform: translateZ(100px) scale(1.03);
  z-index: 30;
}

.snowflake-column:hover {
  transform: translateZ(100px) translateX(-30px) rotateY(-8deg) scale(1.03);
  box-shadow: 0 0 25px rgba(56, 189, 248, 0.2), 0 30px 40px -20px rgba(2, 6, 23, 0.5);
}

.fabric-column:hover {
  transform: translateZ(100px) scale(1.03);
  box-shadow: 0 0 25px rgba(45, 212, 191, 0.2), 0 30px 40px -20px rgba(2, 6, 23, 0.5);
}

.powerbi-column:hover {
  transform: translateZ(100px) translateX(30px) rotateY(8deg) scale(1.03);
  box-shadow: 0 0 25px rgba(217, 70, 239, 0.2), 0 30px 40px -20px rgba(2, 6, 23, 0.5);
}

/* Add a subtle ambient animation to all columns */
@keyframes float {
  0% {
    transform: translateZ(80px) translateY(0px);
  }
  50% {
    transform: translateZ(80px) translateY(-5px);
  }
  100% {
    transform: translateZ(80px) translateY(0px);
  }
}

.snowflake-column {
  animation: float 8s ease-in-out infinite;
}

.fabric-column {
  animation: float 8s ease-in-out infinite;
  animation-delay: 2s;
}

.powerbi-column {
  animation: float 8s ease-in-out infinite;
  animation-delay: 4s;
}
</style> 