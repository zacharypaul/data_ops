<template>
  <div 
    :class="['tech-node', `${platform}-node`, { 'node-active': isActive }]"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    :id="`node-${platform}-${connector.name}`"
  >
    <div class="node-content">
      <div class="node-header">
        <div class="node-icon" :class="`${platform}-icon`">
          <component :is="getIconComponent" class="h-5 w-5" />
        </div>
        <div class="node-title">
          <h3 class="node-name">{{ displayName }}</h3>
          <span class="node-tech">
            {{ displayTechnology }}
          </span>
        </div>
        <div class="node-status">
          <span class="node-status-indicator" :class="getStatusClass">
            <span class="node-frequency">{{ connector.refreshFrequency?.interval || 'N/A' }}</span>
          </span>
        </div>
      </div>
      
      <div class="node-details">
        <div class="node-metadata">
          <div class="metadata-item">
            <span class="metadata-label">Owner:</span>
            <span class="metadata-value">{{ connector.owner || 'System' }}</span>
          </div>
          
          <div v-if="platform === 'fabric'" class="metadata-item">
            <span class="metadata-label">Mapped from:</span>
            <span class="metadata-value">{{ connector.technology || 'Unknown' }}</span>
          </div>
          
          <div v-if="platform === 'powerbi'" class="metadata-item">
            <span class="metadata-label">Source:</span>
            <span class="metadata-value">{{ connector.sourcePlatform === 'fabric' ? 'Fabric' : 'Snowflake' }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Connection point indicators -->
    <div 
      v-if="platform === 'powerbi'"
      class="connection-points input-points"
    >
      <div 
        class="connection-point input-point snowflake-point"
        title="Connection from Snowflake"
      ></div>
      <div 
        class="connection-point input-point fabric-point"
        title="Connection from Fabric"
      ></div>
    </div>
    
    <div 
      v-if="platform !== 'powerbi'"
      class="connection-points output-points"
    >
      <div 
        class="connection-point output-point"
        :class="{ 
          'to-fabric': platform === 'snowflake',
          'to-powerbi': true,
          'to-snowflake': platform === 'fabric'
        }"
      ></div>
    </div>

    <!-- Bottom connection point for connecting to PowerBI -->
    <div 
      v-if="platform !== 'powerbi'" 
      class="connection-points bottom-output-points"
    >
      <div 
        class="connection-point bottom-output-point"
        :class="{ 
          'to-powerbi': true 
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import SnowflakeIcon from './icons/SnowflakeIcon.vue';
import FabricIcon from './icons/FabricIcon.vue';
import PowerBIIcon from './icons/PowerBIIcon.vue';
import AirflowIcon from './icons/AirflowIcon.vue';
import FivetranIcon from './icons/FivetranIcon.vue';
import ADFIcon from './icons/ADFIcon.vue';

const props = defineProps({
  connector: {
    type: Object,
    required: true
  },
  platform: {
    type: String,
    required: true,
    validator: (value) => ['snowflake', 'fabric', 'powerbi'].includes(value)
  },
  mapping: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['node-hover']);

const isActive = ref(false);

// Get the icon component based on technology and platform
const getIconComponent = computed(() => {
  if (props.platform === 'snowflake') {
    if (props.connector.technology === 'Snowflake ADF') return ADFIcon;
    if (props.connector.technology === 'Snowflake Airflow') return AirflowIcon;
    if (props.connector.technology === 'Snowflake Fivetran') return FivetranIcon;
    return SnowflakeIcon;
  }
  else if (props.platform === 'fabric') {
    return FabricIcon;
  }
  else if (props.platform === 'powerbi') {
    return PowerBIIcon;
  }
  
  return SnowflakeIcon; // Default fallback
});

// Get display name based on platform
const displayName = computed(() => {
  if (props.platform === 'fabric') {
    return props.connector.name; // Same name as the source
  }
  
  return props.connector.name;
});

// Get display technology based on platform
const displayTechnology = computed(() => {
  if (props.platform === 'snowflake') {
    return props.connector.technology || 'Snowflake';
  }
  else if (props.platform === 'fabric') {
    return props.mapping || 'Fabric Service';
  }
  else if (props.platform === 'powerbi') {
    return props.connector.type || 'PowerBI';
  }
  
  return 'Unknown';
});

// Get status class based on refresh frequency
const getStatusClass = computed(() => {
  if (!props.connector.refreshFrequency) return 'status-unknown';
  
  const type = props.connector.refreshFrequency.type || 'daily';
  
  if (type === 'hourly') return 'status-hourly';
  if (type === 'daily') return 'status-daily';
  if (type === 'weekly') return 'status-weekly';
  
  return 'status-unknown';
});

// Handle mouse enter event
const handleMouseEnter = () => {
  isActive.value = true;
  emit('node-hover', { 
    connector: props.connector,
    platform: props.platform,
    element: `node-${props.platform}-${props.connector.name}`
  });
};

// Handle mouse leave event
const handleMouseLeave = () => {
  isActive.value = false;
  emit('node-hover', null);
};
</script>

<style scoped>
.tech-node {
  position: relative;
  border-radius: 0.5rem;
  padding: 0.75rem;
  transition: all 0.3s ease;
  cursor: pointer;
  overflow: hidden;
  transform-style: preserve-3d;
  transform: translateZ(10px);
  box-shadow: 0 8px 16px -6px rgba(0, 0, 0, 0.3);
}

.node-content {
  position: relative;
  z-index: 2;
  transform-style: preserve-3d;
}

.snowflake-node {
  background-color: rgba(14, 32, 61, 0.5);
  border: 1px solid rgba(56, 189, 248, 0.3);
}

.snowflake-node::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(56, 189, 248, 0.05) 0%, rgba(14, 32, 61, 0.05) 100%);
  z-index: 1;
}

.snowflake-node:hover, .snowflake-node.node-active {
  background-color: rgba(14, 32, 61, 0.8);
  border-color: rgba(56, 189, 248, 0.6);
  transform: translateZ(25px) scale(1.03);
  box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.4), 0 0 15px rgba(56, 189, 248, 0.3);
}

.fabric-node {
  background-color: rgba(14, 61, 42, 0.5);
  border: 1px solid rgba(45, 212, 191, 0.3);
}

.fabric-node::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(45, 212, 191, 0.05) 0%, rgba(14, 61, 42, 0.05) 100%);
  z-index: 1;
}

.fabric-node:hover, .fabric-node.node-active {
  background-color: rgba(14, 61, 42, 0.8);
  border-color: rgba(45, 212, 191, 0.6);
  transform: translateZ(25px) scale(1.03);
  box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.4), 0 0 15px rgba(45, 212, 191, 0.3);
}

.powerbi-node {
  background-color: rgba(61, 14, 57, 0.5);
  border: 1px solid rgba(217, 70, 239, 0.3);
}

.powerbi-node::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(217, 70, 239, 0.05) 0%, rgba(61, 14, 57, 0.05) 100%);
  z-index: 1;
}

.powerbi-node:hover, .powerbi-node.node-active {
  background-color: rgba(61, 14, 57, 0.8);
  border-color: rgba(217, 70, 239, 0.6);
  transform: translateZ(25px) scale(1.03);
  box-shadow: 0 12px 20px -8px rgba(0, 0, 0, 0.4), 0 0 15px rgba(217, 70, 239, 0.3);
}

.node-header {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  transform-style: preserve-3d;
}

.node-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 0.5rem;
  margin-right: 0.75rem;
  transform: translateZ(5px);
  box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.2);
}

.snowflake-icon {
  background-color: rgba(14, 165, 233, 0.2);
  color: rgb(56, 189, 248);
}

.fabric-icon {
  background-color: rgba(20, 184, 166, 0.2);
  color: rgb(45, 212, 191);
}

.powerbi-icon {
  background-color: rgba(192, 38, 211, 0.2);
  color: rgb(217, 70, 239);
}

.node-title {
  flex: 1;
  transform-style: preserve-3d;
  transform: translateZ(7px);
}

.node-name {
  font-size: 0.9rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.node-tech {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.6);
}

.node-status {
  display: flex;
  align-items: center;
  transform: translateZ(8px);
}

.node-status-indicator {
  display: inline-block;
  font-size: 0.65rem;
  padding: 0.15rem 0.4rem;
  border-radius: 1rem;
  font-weight: 500;
  box-shadow: 0 3px 6px -2px rgba(0, 0, 0, 0.2);
}

.status-hourly {
  background-color: rgba(74, 222, 128, 0.2);
  color: rgb(74, 222, 128);
}

.status-daily {
  background-color: rgba(56, 189, 248, 0.2);
  color: rgb(56, 189, 248);
}

.status-weekly {
  background-color: rgba(168, 85, 247, 0.2);
  color: rgb(168, 85, 247);
}

.status-unknown {
  background-color: rgba(148, 163, 184, 0.2);
  color: rgb(148, 163, 184);
}

.node-details {
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.node-metadata {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.metadata-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
}

.metadata-label {
  color: rgba(255, 255, 255, 0.5);
}

.metadata-value {
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Connection points */
.connection-points {
  position: absolute;
  width: 10px;
  height: 20px;
  z-index: 5;
}

.input-points {
  left: -5px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
}

.output-points {
  right: -5px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-around;
}

.bottom-output-points {
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  height: 10px;
  width: 20px;
}

.connection-point {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  z-index: 5;
  transform-style: preserve-3d;
  transition: all 0.2s ease;
}

.input-point {
  transform: translateZ(5px);
}

.output-point {
  transform: translateZ(5px);
}

.bottom-output-point {
  transform: translateZ(5px);
}

/* Special styling for PowerBI input points */
.snowflake-point {
  margin-bottom: 6px;
  background-color: rgb(56, 189, 248);
  box-shadow: 0 0 6px rgba(56, 189, 248, 0.7);
}

.fabric-point {
  background-color: rgb(45, 212, 191);
  box-shadow: 0 0 6px rgba(45, 212, 191, 0.7);
}

/* Custom connection point colors by platform */
.snowflake-node .connection-point {
  background-color: rgb(56, 189, 248);
  box-shadow: 0 0 6px rgba(56, 189, 248, 0.7);
}

.fabric-node .connection-point {
  background-color: rgb(45, 212, 191);
  box-shadow: 0 0 6px rgba(45, 212, 191, 0.7);
}

.powerbi-node .connection-point {
  background-color: rgb(217, 70, 239);
  box-shadow: 0 0 6px rgba(217, 70, 239, 0.7);
}

/* Output point destination indicators */
.to-powerbi {
  background: rgb(217, 70, 239) !important;
  box-shadow: 0 0 6px rgba(217, 70, 239, 0.7) !important;
}

.to-fabric {
  background: rgb(45, 212, 191) !important;
  box-shadow: 0 0 6px rgba(45, 212, 191, 0.7) !important;
}

.to-snowflake {
  background: rgb(56, 189, 248) !important;
  box-shadow: 0 0 6px rgba(56, 189, 248, 0.7) !important;
}

/* Active node states */
.node-active .connection-point {
  animation: connection-pulse 1.5s infinite;
  width: 12px;
  height: 12px;
  box-shadow: 0 0 15px 5px rgba(255, 255, 255, 0.4);
}

/* Add a subtle ambient glow to active nodes */
.node-active::after {
  content: '';
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border-radius: 0.75rem;
  z-index: -1;
  opacity: 0;
  animation: node-glow 2s ease-in-out infinite;
}

.snowflake-node.node-active::after {
  box-shadow: 0 0 25px 5px rgba(56, 189, 248, 0.3);
  background: radial-gradient(circle at center, rgba(56, 189, 248, 0.1) 0%, transparent 70%);
}

.fabric-node.node-active::after {
  box-shadow: 0 0 25px 5px rgba(45, 212, 191, 0.3);
  background: radial-gradient(circle at center, rgba(45, 212, 191, 0.1) 0%, transparent 70%);
}

.powerbi-node.node-active::after {
  box-shadow: 0 0 25px 5px rgba(217, 70, 239, 0.3);
  background: radial-gradient(circle at center, rgba(217, 70, 239, 0.1) 0%, transparent 70%);
}

@keyframes node-glow {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.8;
  }
}

@keyframes connection-pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.8), 0 0 10px 2px rgba(255, 255, 255, 0.5);
  }
  70% {
    box-shadow: 0 0 0 15px rgba(255, 255, 255, 0), 0 0 10px 2px rgba(255, 255, 255, 0.5);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0), 0 0 10px 2px rgba(255, 255, 255, 0.5);
  }
}
</style> 