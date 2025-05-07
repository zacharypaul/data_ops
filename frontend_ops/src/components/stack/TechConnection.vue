<template>
  <div 
    :class="['tech-connection', getConnectionClass]"
    :style="connectionStyle"
  >
    <div class="connection-line">
      <div class="connection-beam"></div>
      <div class="connection-data-particles" v-if="showDataParticles"></div>
      <div class="connection-endpoints">
        <div class="connection-endpoint start"></div>
        <div class="connection-endpoint end"></div>
      </div>
      <div class="connection-label">
        <span>{{ connection.refreshFrequency?.interval || '24h' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
  connection: {
    type: Object,
    required: true
  }
});

// Get platform-specific colors for the connection
const getConnectionColors = (platform) => {
  switch (platform) {
    case 'snowflake':
      return {
        primary: 'rgba(56, 189, 248, 0.9)',
        secondary: 'rgba(56, 189, 248, 0.3)',
        highlight: 'rgba(56, 189, 248, 1)'
      };
    case 'fabric':
      return {
        primary: 'rgba(45, 212, 191, 0.9)',
        secondary: 'rgba(45, 212, 191, 0.3)',
        highlight: 'rgba(45, 212, 191, 1)'
      };
    case 'powerbi':
      return {
        primary: 'rgba(217, 70, 239, 0.9)',
        secondary: 'rgba(217, 70, 239, 0.3)',
        highlight: 'rgba(217, 70, 239, 1)'
      };
    default:
      return {
        primary: 'rgba(148, 163, 184, 0.9)',
        secondary: 'rgba(148, 163, 184, 0.3)',
        highlight: 'rgba(148, 163, 184, 1)'
      };
  }
};

// Position state
const startPosition = ref({ x: 0, y: 0, z: 0 });
const endPosition = ref({ x: 0, y: 0, z: 0 });
const isVisible = ref(false);

// Determine if we should show data particles based on refresh frequency
const showDataParticles = computed(() => {
  const type = props.connection.refreshFrequency?.type || 'daily';
  // Show for hourly and daily connections
  return ['hourly', 'daily'].includes(type);
});

// Get specific classes for source and target endpoints
const getSourceClass = computed(() => {
  return `source-${props.connection.source.platform}`;
});

const getTargetClass = computed(() => {
  return `target-${props.connection.target.platform}`;
});

// Update connection positions
const updateConnectionPositions = () => {
  // Get source element
  const sourceElement = document.getElementById(`node-${props.connection.source.platform}-${props.connection.source.id}`);
  // Get target element
  const targetElement = document.getElementById(`node-${props.connection.target.platform}-${props.connection.target.id}`);
  
  if (!sourceElement || !targetElement) {
    isVisible.value = false;
    return;
  }
  
  isVisible.value = true;
  
  // Find the specific connection point elements
  let sourcePoint, targetPoint;
  
  // For output connections from Snowflake or Fabric to PowerBI
  if ((props.connection.source.platform === 'snowflake' || props.connection.source.platform === 'fabric') && 
       props.connection.target.platform === 'powerbi') {
    sourcePoint = sourceElement.querySelector('.output-point');
  }
  // For input connections to PowerBI
  if (props.connection.target.platform === 'powerbi') {
    // Find the correct input point based on source platform
    if (props.connection.source.platform === 'snowflake') {
      targetPoint = targetElement.querySelector('.snowflake-point');
    } else if (props.connection.source.platform === 'fabric') {
      targetPoint = targetElement.querySelector('.fabric-point');
    }
  } else if (props.connection.target.platform === 'fabric') {
    targetPoint = targetElement.querySelector('.input-point');
  }
  
  // Get bounds from specific connection points if available
  const sourceBounds = sourceElement.getBoundingClientRect();
  const targetBounds = targetElement.getBoundingClientRect();
  
  // Calculate source position
  let sourceX, sourceY;
  if (sourcePoint) {
    const sourcePointBounds = sourcePoint.getBoundingClientRect();
    sourceX = sourcePointBounds.left + sourcePointBounds.width / 2;
    sourceY = sourcePointBounds.top + sourcePointBounds.height / 2;
  } else {
    // If connecting to PowerBI, use the bottom center of Snowflake/Fabric nodes
    if (props.connection.target.platform === 'powerbi') {
      sourceX = sourceBounds.left + sourceBounds.width / 2;
      sourceY = sourceBounds.bottom;
    } else {
      sourceX = props.connection.direction === 'forward' ? 
        sourceBounds.right : sourceBounds.left;
      sourceY = sourceBounds.top + sourceBounds.height / 2;
    }
  }
  
  // Calculate target position
  let targetX, targetY;
  if (targetPoint) {
    const targetPointBounds = targetPoint.getBoundingClientRect();
    targetX = targetPointBounds.left + targetPointBounds.width / 2;
    targetY = targetPointBounds.top + targetPointBounds.height / 2;
  } else {
    // If target is PowerBI, connect to top of the element
    if (props.connection.target.platform === 'powerbi') {
      targetX = targetBounds.left + targetBounds.width / 2;
      targetY = targetBounds.top;
    } else {
      targetX = props.connection.direction === 'forward' ? 
        targetBounds.left : targetBounds.right;
      targetY = targetBounds.top + targetBounds.height / 2;
    }
  }
  
  // Get container bounds for relative positioning
  const containerElement = sourceElement.closest('.tech-stack-container');
  const containerBounds = containerElement.getBoundingClientRect();
  
  // Calculate the offset from the container's edge based on 3D transformations
  let sourceZOffset = 0;
  let targetZOffset = 0;
  
  // Add Z-offset for 3D positioning
  if (props.connection.source.platform === 'snowflake') {
    sourceZOffset = 10;
  } else if (props.connection.source.platform === 'fabric') {
    sourceZOffset = 20;
  } else if (props.connection.source.platform === 'powerbi') {
    sourceZOffset = 30;
  }
  
  if (props.connection.target.platform === 'fabric') {
    targetZOffset = 20;
  } else if (props.connection.target.platform === 'powerbi') {
    targetZOffset = 30;
  } else if (props.connection.target.platform === 'snowflake') {
    targetZOffset = 10;
  }
  
  // Convert to relative positions with Z-offset adjustments
  startPosition.value = {
    x: sourceX - containerBounds.left,
    y: sourceY - containerBounds.top,
    z: sourceZOffset
  };
  
  endPosition.value = {
    x: targetX - containerBounds.left,
    y: targetY - containerBounds.top,
    z: targetZOffset
  };
};

// Compute the CSS styles for drawing the connection
const connectionStyle = computed(() => {
  if (!isVisible.value) {
    return { display: 'none' };
  }
  
  const dx = endPosition.value.x - startPosition.value.x;
  const dy = endPosition.value.y - startPosition.value.y;
  const dz = endPosition.value.z - startPosition.value.z;
  const distance = Math.sqrt(dx * dx + dy * dy);
  const angle = Math.atan2(dy, dx) * 180 / Math.PI;
  
  // Calculate 3D perspective based on z-difference
  const perspectiveAngle = Math.atan2(dz, distance) * 180 / Math.PI;
  
  // Add special handling for PowerBI connections
  let transform = `rotate(${angle}deg)`;
  let opacity = 1;
  let zIndex = 5 + Math.min(startPosition.value.z, endPosition.value.z);
  
  // Adjust z-index and transform for connections with z-depth
  if (Math.abs(dz) > 1) {
    // Use more dramatic 3D transformation
    transform += ` perspective(1200px) rotateX(${perspectiveAngle}deg)`;
    
    // Add arc effect based on connection types
    if (props.connection.source.platform === 'snowflake' && props.connection.target.platform === 'powerbi') {
      transform += ' rotateY(8deg) translateZ(20px)';
      zIndex = 15;
    } else if (props.connection.source.platform === 'fabric' && props.connection.target.platform === 'powerbi') {
      transform += ' rotateY(-8deg) translateZ(10px)';
      zIndex = 20;
    } else if (props.connection.source.platform === 'snowflake' && props.connection.target.platform === 'fabric') {
      transform += ' rotateY(5deg) translateZ(15px)';
      zIndex = 10;
    } else if (props.connection.source.platform === 'fabric' && props.connection.target.platform === 'snowflake') {
      transform += ' rotateY(-5deg) translateZ(15px)';
      zIndex = 10;
    }
  }
  
  // Adjust opacity based on refresh frequency
  if (props.connection.refreshFrequency?.type === 'hourly') {
    opacity = 0.95;
  } else if (props.connection.refreshFrequency?.type === 'daily') {
    opacity = 0.9;
  } else {
    opacity = 0.85;
  }
  
  return {
    left: `${startPosition.value.x}px`,
    top: `${startPosition.value.y}px`,
    width: `${distance}px`,
    transform: transform,
    transformOrigin: '0 50%',
    opacity: opacity,
    zIndex: zIndex
  };
});

// Get CSS class based on refresh frequency and direction
const getConnectionClass = computed(() => {
  if (!props.connection.refreshFrequency) {
    return 'frequency-daily';
  }
  
  const type = props.connection.refreshFrequency.type || 'daily';
  const sourcePlatform = props.connection.source.platform;
  const targetPlatform = props.connection.target.platform;
  const active = props.connection.active ? 'active' : '';
  
  return [
    `frequency-${type}`,
    `source-${sourcePlatform}`,
    `target-${targetPlatform}`,
    props.connection.direction || 'forward',
    active
  ].join(' ');
});

// Set up watchers, resize observer and animation frame
let resizeObserver = null;
let animationFrameId = null;

// Create and clean up the resize observer
const setupResizeObserver = () => {
  if (typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(() => {
      updateConnectionPositions();
    });
    
    const container = document.querySelector('.tech-stack-container');
    if (container) {
      resizeObserver.observe(container);
    }
  }
};

// Update on scroll
const handleScroll = () => {
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId);
  }
  
  animationFrameId = window.requestAnimationFrame(() => {
    updateConnectionPositions();
  });
};

// Initialize and clean up
onMounted(() => {
  // Wait for DOM to be fully rendered
  setTimeout(() => {
    updateConnectionPositions();
    setupResizeObserver();
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', updateConnectionPositions);
  }, 200);
});

onUnmounted(() => {
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
  
  window.removeEventListener('scroll', handleScroll);
  window.removeEventListener('resize', updateConnectionPositions);
  
  if (animationFrameId) {
    window.cancelAnimationFrame(animationFrameId);
  }
});

// Watch for changes in connection data
watch(() => props.connection, () => {
  updateConnectionPositions();
}, { deep: true });
</script>

<style scoped>
.tech-connection {
  position: absolute;
  height: 2px;
  pointer-events: none;
  z-index: 5;
  transform-style: preserve-3d;
}

.connection-line {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: visible;
  background-color: rgba(255, 255, 255, 0.1);
  transform-style: preserve-3d;
}

.connection-beam {
  position: absolute;
  top: -5px;
  left: 0;
  width: 100%;
  height: 12px;
  overflow: hidden;
  opacity: 0.95;
  transform-style: preserve-3d;
  filter: blur(0.5px);
}

.connection-beam::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100px;
  width: 100px;
  height: 100%;
  border-radius: 4px;
  animation: beam 2.5s infinite linear;
  box-shadow: 0 0 22px 5px rgba(255, 255, 255, 0.7);
  transform-style: preserve-3d;
}

/* Platform-specific beam styles */
.source-snowflake .connection-beam::after {
  box-shadow: 0 0 22px 5px rgba(56, 189, 248, 0.8);
  background: linear-gradient(90deg, 
    rgba(56, 189, 248, 0) 0%, 
    rgba(56, 189, 248, 0.7) 50%, 
    rgba(56, 189, 248, 0) 100%
  );
}

.source-fabric .connection-beam::after {
  box-shadow: 0 0 22px 5px rgba(45, 212, 191, 0.8);
  background: linear-gradient(90deg, 
    rgba(45, 212, 191, 0) 0%, 
    rgba(45, 212, 191, 0.7) 50%, 
    rgba(45, 212, 191, 0) 100%
  );
}

.source-powerbi .connection-beam::after {
  box-shadow: 0 0 22px 5px rgba(217, 70, 239, 0.8);
  background: linear-gradient(90deg, 
    rgba(217, 70, 239, 0) 0%, 
    rgba(217, 70, 239, 0.7) 50%, 
    rgba(217, 70, 239, 0) 100%
  );
}

/* Active connection states */
.active .connection-beam::after {
  animation-duration: 1.5s;
  box-shadow: 0 0 30px 6px rgba(255, 255, 255, 0.9);
  filter: blur(0.3px);
}

.active.source-snowflake .connection-beam::after {
  box-shadow: 0 0 30px 6px rgba(56, 189, 248, 0.95);
  background: linear-gradient(90deg, 
    rgba(56, 189, 248, 0) 0%, 
    rgba(56, 189, 248, 0.9) 50%, 
    rgba(56, 189, 248, 0) 100%
  );
}

.active.source-fabric .connection-beam::after {
  box-shadow: 0 0 30px 6px rgba(45, 212, 191, 0.95);
  background: linear-gradient(90deg, 
    rgba(45, 212, 191, 0) 0%, 
    rgba(45, 212, 191, 0.9) 50%, 
    rgba(45, 212, 191, 0) 100%
  );
}

.active.source-powerbi .connection-beam::after {
  box-shadow: 0 0 30px 6px rgba(217, 70, 239, 0.95);
  background: linear-gradient(90deg, 
    rgba(217, 70, 239, 0) 0%, 
    rgba(217, 70, 239, 0.9) 50%, 
    rgba(217, 70, 239, 0) 100%
  );
}

.active .connection-line {
  background-color: rgba(255, 255, 255, 0.25);
}

.active .connection-endpoint {
  transform: scale(1.2) translateZ(5px);
  transition: transform 0.3s ease;
}

/* Frequency-based beam variations */
.frequency-hourly .connection-beam::after {
  animation-duration: 1.5s;
  width: 120px;
  left: -120px;
}

.frequency-daily .connection-beam::after {
  animation-duration: 2.5s;
}

.frequency-weekly .connection-beam::after {
  animation-duration: 4s;
  opacity: 0.85;
}

/* Add a 3D glow effect to active connections */
.active .connection-beam {
  filter: blur(0.3px);
}

.active .connection-beam::before {
  content: '';
  position: absolute;
  top: -3px;
  left: 0;
  right: 0;
  height: 18px;
  border-radius: 9px;
  background: transparent;
  z-index: -1;
  animation: beam-glow 2s infinite ease-in-out;
  opacity: 0.4;
}

.active.source-snowflake .connection-beam::before {
  box-shadow: 0 0 15px 3px rgba(56, 189, 248, 0.6);
}

.active.source-fabric .connection-beam::before {
  box-shadow: 0 0 15px 3px rgba(45, 212, 191, 0.6);
}

.active.source-powerbi .connection-beam::before {
  box-shadow: 0 0 15px 3px rgba(217, 70, 239, 0.6);
}

@keyframes beam-glow {
  0%, 100% {
    opacity: 0.4;
  }
  50% {
    opacity: 0.7;
  }
}

/* Animation keyframes */
@keyframes beam {
  0% {
    left: -100px;
  }
  100% {
    left: 100%;
  }
}

@keyframes particles {
  0% {
    left: -10px;
  }
  100% {
    left: 100%;
  }
}

/* 3D enhancements for connection endpoints */
.connection-endpoints {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.connection-endpoint {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: white;
  box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.8);
  transform-style: preserve-3d;
  transform: translateZ(5px);
  filter: blur(0.2px);
}

.start {
  left: -6px;
  top: -6px;
}

.end {
  right: -6px;
  top: -6px;
}

/* Source-specific endpoint styling */
.source-snowflake .start {
  background-color: rgba(56, 189, 248, 1);
  box-shadow: 0 0 10px 2px rgba(56, 189, 248, 0.8);
}

.source-fabric .start {
  background-color: rgba(45, 212, 191, 1);
  box-shadow: 0 0 10px 2px rgba(45, 212, 191, 0.8);
}

.source-powerbi .start {
  background-color: rgba(217, 70, 239, 1);
  box-shadow: 0 0 10px 2px rgba(217, 70, 239, 0.8);
}

/* Target-specific endpoint styling */
.target-powerbi .end {
  background-color: rgba(217, 70, 239, 1);
  box-shadow: 0 0 10px 2px rgba(217, 70, 239, 0.8);
}

.target-fabric .end {
  background-color: rgba(45, 212, 191, 1);
  box-shadow: 0 0 10px 2px rgba(45, 212, 191, 0.8);
}

.target-snowflake .end {
  background-color: rgba(56, 189, 248, 1);
  box-shadow: 0 0 10px 2px rgba(56, 189, 248, 0.8);
}

.connection-label {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%) translateZ(10px);
  color: white;
  font-size: 11px;
  background-color: rgba(30, 41, 59, 0.8);
  padding: 2px 6px;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(2px);
}
</style> 