<template>
  <div class="d3-visualization-container" ref="container">
    <div class="loading-container" v-if="loading">
      <div class="loading-spinner"></div>
      <p>Building 3D visualization...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as d3 from 'd3';
import { _3d } from 'd3-3d';

const props = defineProps({
  connectors: {
    type: Array,
    default: () => []
  },
  powerBIAssets: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  }
});

const container = ref(null);
const loading = ref(true);
let svg = null;
let width = 0;
let height = 0;
let simulation = null;
let nodes = [];
let links = [];
let nodeElements = null;
let linkElements = null;
let projection = null;

// D3 projection setup
const setupProjection = () => {
  projection = _3d()
    .scale(100)
    .origin([width / 2, height / 2])
    .rotateY(Math.PI / 8)
    .rotateX(Math.PI / 16)
    .z(d => d.z);
};

// Initialize the 3D visualization
const initVisualization = () => {
  if (!container.value) return;
  
  // Clear previous visualization
  d3.select(container.value).select('svg').remove();

  // Get container dimensions
  const boundingRect = container.value.getBoundingClientRect();
  width = boundingRect.width;
  height = boundingRect.height || 800;

  // Create SVG container
  svg = d3.select(container.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', [0, 0, width, height])
    .classed('d3-visualization', true);

  // Add a gradient definition for connections
  const defs = svg.append('defs');
  
  // Snowflake gradient
  createGradient(defs, 'snowflake-gradient', '#38BDF8', '#0E203D');
  
  // Fabric gradient
  createGradient(defs, 'fabric-gradient', '#2DD4BF', '#0E3D2A');
  
  // PowerBI gradient
  createGradient(defs, 'powerbi-gradient', '#D946EF', '#3D0E39');

  // Connection gradients
  createGradient(defs, 'snowflake-to-powerbi-gradient', '#38BDF8', '#D946EF');
  createGradient(defs, 'fabric-to-powerbi-gradient', '#2DD4BF', '#D946EF');
  createGradient(defs, 'snowflake-to-fabric-gradient', '#38BDF8', '#2DD4BF');
  createGradient(defs, 'fabric-to-snowflake-gradient', '#2DD4BF', '#38BDF8');

  // Setup 3D projection
  setupProjection();

  // Prepare data
  transformData();

  // Create visualization elements
  createElements();

  // Setup force simulation
  setupSimulation();

  // Start animation cycle
  animate();

  // Set loading to false when completed
  loading.value = false;
};

// Create a gradient definition
const createGradient = (defs, id, startColor, endColor) => {
  const gradient = defs.append('linearGradient')
    .attr('id', id)
    .attr('x1', '0%')
    .attr('y1', '0%')
    .attr('x2', '100%')
    .attr('y2', '100%');

  gradient.append('stop')
    .attr('offset', '0%')
    .attr('stop-color', startColor)
    .attr('stop-opacity', 0.9);

  gradient.append('stop')
    .attr('offset', '100%')
    .attr('stop-color', endColor)
    .attr('stop-opacity', 0.7);
};

// Transform the props data into D3 compatible format
const transformData = () => {
  nodes = [];
  links = [];
  
  // Add Snowflake nodes
  props.connectors.forEach(connector => {
    nodes.push({
      id: `snowflake-${connector.name}`,
      name: connector.name,
      platform: 'snowflake',
      technology: connector.technology || 'Snowflake',
      owner: connector.owner || 'System',
      refreshFrequency: connector.refreshFrequency,
      x: width * 0.25,
      y: height * 0.3 + (nodes.length * 10),
      z: 80
    });
  });
  
  // Add Fabric nodes
  props.connectors.forEach(connector => {
    nodes.push({
      id: `fabric-${connector.name}`,
      name: connector.name,
      platform: 'fabric',
      technology: 'Fabric Service',
      owner: connector.owner || 'System',
      refreshFrequency: connector.refreshFrequency,
      x: width * 0.5,
      y: height * 0.3 + (nodes.length * 10),
      z: 40
    });
  });
  
  // Add PowerBI nodes
  props.powerBIAssets.forEach(asset => {
    nodes.push({
      id: `powerbi-${asset.name}`,
      name: asset.name,
      platform: 'powerbi',
      technology: asset.type || 'PowerBI',
      owner: asset.owner || 'System',
      refreshFrequency: asset.refreshFrequency,
      sourceConnector: asset.sourceConnector,
      sourcePlatform: asset.sourcePlatform,
      x: width * 0.75,
      y: height * 0.7,
      z: 80
    });
  });
  
  // Create connections
  props.connections.forEach(connection => {
    const sourceId = `${connection.source.platform}-${connection.source.id}`;
    const targetId = `${connection.target.platform}-${connection.target.id}`;
    
    // Find source and target nodes
    const source = nodes.find(node => node.id === sourceId);
    const target = nodes.find(node => node.id === targetId);
    
    if (source && target) {
      links.push({
        id: `${sourceId}-to-${targetId}`,
        source,
        target,
        refreshFrequency: connection.refreshFrequency,
        active: connection.active || false
      });
    }
  });
};

// Create the visual elements
const createElements = () => {
  // Create a container for links
  const linksContainer = svg.append('g')
    .attr('class', 'links-container');
  
  // Create links (connections)
  linkElements = linksContainer
    .selectAll('path')
    .data(links)
    .enter()
    .append('path')
    .attr('class', d => `connection-path ${d.source.platform}-to-${d.target.platform}`)
    .attr('id', d => `path-${d.id}`)
    .attr('stroke', d => getConnectionGradient(d))
    .attr('stroke-width', d => getConnectionWidth(d))
    .attr('fill', 'none')
    .attr('opacity', d => d.active ? 0.9 : 0.6)
    .attr('marker-end', 'url(#arrowhead)');
  
  // Add animated particles to active connections
  links.forEach(link => {
    if (link.active && link.refreshFrequency?.type !== 'weekly') {
      addParticles(link);
    }
  });
  
  // Create a container for nodes
  const nodesContainer = svg.append('g')
    .attr('class', 'nodes-container');
  
  // Create nodes (tech stack elements)
  nodeElements = nodesContainer
    .selectAll('g')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', d => `node ${d.platform}-node`)
    .attr('id', d => `node-${d.id}`);
  
  // Add node shapes
  nodeElements
    .append('rect')
    .attr('width', 120)
    .attr('height', 80)
    .attr('rx', 10)
    .attr('ry', 10)
    .attr('fill', d => `url(#${d.platform}-gradient)`)
    .attr('stroke', d => getNodeStrokeColor(d))
    .attr('stroke-width', 1.5)
    .attr('filter', 'url(#glow)');
  
  // Add node labels
  nodeElements
    .append('text')
    .attr('class', 'node-label')
    .attr('x', 60)
    .attr('y', 30)
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'middle')
    .attr('fill', 'white')
    .text(d => d.name);
  
  // Add platform labels
  nodeElements
    .append('text')
    .attr('class', 'platform-label')
    .attr('x', 60)
    .attr('y', 50)
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'middle')
    .attr('fill', 'rgba(255, 255, 255, 0.7)')
    .text(d => d.platform.charAt(0).toUpperCase() + d.platform.slice(1));
  
  // Add filter for glow effect
  const filter = defs.append('filter')
    .attr('id', 'glow')
    .attr('height', '300%')
    .attr('width', '300%')
    .attr('x', '-100%')
    .attr('y', '-100%');
    
  filter.append('feGaussianBlur')
    .attr('stdDeviation', '3')
    .attr('result', 'coloredBlur');
    
  const feMerge = filter.append('feMerge');
  feMerge.append('feMergeNode')
    .attr('in', 'coloredBlur');
  feMerge.append('feMergeNode')
    .attr('in', 'SourceGraphic');

  // Add arrowhead marker for connections
  defs.append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 20)
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'white');

  // Add interaction
  nodeElements.call(
    d3.drag()
      .on('start', dragStarted)
      .on('drag', dragging)
      .on('end', dragEnded)
  );
};

// Add animated particles to a connection
const addParticles = (link) => {
  const numParticles = link.refreshFrequency?.type === 'hourly' ? 5 : 3;
  
  for (let i = 0; i < numParticles; i++) {
    const delay = i * (1000 / numParticles);
    
    svg.append('circle')
      .attr('class', 'connection-particle')
      .attr('r', 3)
      .attr('fill', getParticleColor(link))
      .attr('opacity', 0.8)
      .attr('filter', 'url(#glow)')
      .call(animateParticle, link, delay);
  }
};

// Animate a particle along a path
const animateParticle = (particle, link, delay) => {
  function repeat() {
    const pathNode = document.getElementById(`path-${link.id}`);
    if (!pathNode) return;
    
    const pathLength = pathNode.getTotalLength();
    
    particle
      .attr('opacity', 0)
      .transition()
      .delay(delay)
      .duration(0)
      .attr('opacity', 0.8)
      .transition()
      .duration(link.refreshFrequency?.type === 'hourly' ? 2000 : 3000)
      .ease(d3.easeLinear)
      .attrTween('transform', () => {
        return (t) => {
          const point = pathNode.getPointAtLength(t * pathLength);
          return `translate(${point.x}, ${point.y})`;
        };
      })
      .on('end', repeat);
  }
  
  repeat();
};

// Get appropriate gradient for a connection
const getConnectionGradient = (connection) => {
  const source = connection.source.platform;
  const target = connection.target.platform;
  
  if (source === 'snowflake' && target === 'powerbi') {
    return 'url(#snowflake-to-powerbi-gradient)';
  } else if (source === 'fabric' && target === 'powerbi') {
    return 'url(#fabric-to-powerbi-gradient)';
  } else if (source === 'snowflake' && target === 'fabric') {
    return 'url(#snowflake-to-fabric-gradient)';
  } else if (source === 'fabric' && target === 'snowflake') {
    return 'url(#fabric-to-snowflake-gradient)';
  }
  
  return 'rgba(255, 255, 255, 0.5)';
};

// Get appropriate particle color for a connection
const getParticleColor = (connection) => {
  const source = connection.source.platform;
  
  if (source === 'snowflake') {
    return '#38BDF8';
  } else if (source === 'fabric') {
    return '#2DD4BF';
  } else if (source === 'powerbi') {
    return '#D946EF';
  }
  
  return 'white';
};

// Get connection width based on refresh frequency
const getConnectionWidth = (connection) => {
  if (!connection.refreshFrequency) return 2;
  
  const type = connection.refreshFrequency.type || 'daily';
  
  if (type === 'hourly') return 4;
  if (type === 'daily') return 3;
  if (type === 'weekly') return 2;
  
  return 2;
};

// Get stroke color for nodes
const getNodeStrokeColor = (node) => {
  if (node.platform === 'snowflake') {
    return '#38BDF8';
  } else if (node.platform === 'fabric') {
    return '#2DD4BF';
  } else if (node.platform === 'powerbi') {
    return '#D946EF';
  }
  
  return 'white';
};

// Setup the force simulation for node positioning
const setupSimulation = () => {
  simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(200))
    .force('charge', d3.forceManyBody().strength(-300))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('x', d3.forceX().strength(0.1).x(d => {
      if (d.platform === 'snowflake') return width * 0.25;
      if (d.platform === 'fabric') return width * 0.5;
      if (d.platform === 'powerbi') return width * 0.75;
      return width * 0.5;
    }))
    .force('y', d3.forceY().strength(0.1).y(d => {
      if (d.platform === 'powerbi') return height * 0.7;
      return height * 0.3;
    }))
    .force('collision', d3.forceCollide().radius(60))
    .on('tick', ticked);
};

// Force simulation tick handler
const ticked = () => {
  // Update node positions
  nodeElements.attr('transform', d => {
    const projected = projection([{x: d.x, y: d.y, z: d.z}])[0];
    return `translate(${projected.projected.x - 60}, ${projected.projected.y - 40})`;
  });
  
  // Update link paths
  linkElements.attr('d', d => {
    const sourceProjected = projection([{x: d.source.x, y: d.source.y, z: d.source.z}])[0];
    const targetProjected = projection([{x: d.target.x, y: d.target.y, z: d.target.z}])[0];
    
    const sx = sourceProjected.projected.x;
    const sy = sourceProjected.projected.y;
    const tx = targetProjected.projected.x;
    const ty = targetProjected.projected.y;
    
    const dx = tx - sx;
    const dy = ty - sy;
    const dr = Math.sqrt(dx * dx + dy * dy) * 2;
    
    return `M${sx},${sy}A${dr},${dr} 0 0,1 ${tx},${ty}`;
  });
};

// Drag handlers
const dragStarted = (event, d) => {
  if (!event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
};

const dragging = (event, d) => {
  d.fx = event.x;
  d.fy = event.y;
};

const dragEnded = (event, d) => {
  if (!event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
};

// Animation function for continuous rotation
const animate = () => {
  const rotationSpeed = 0.001;
  
  // Update the projection with rotation
  projection.rotateY(projection.rotateY() + rotationSpeed);
  
  // Update positions
  ticked();
  
  // Request next frame
  requestAnimationFrame(animate);
};

// Resize handler
const handleResize = () => {
  if (container.value) {
    initVisualization();
  }
};

// Watch for data changes
watch(() => props.connectors, () => {
  if (container.value) {
    initVisualization();
  }
}, { deep: true });

watch(() => props.powerBIAssets, () => {
  if (container.value) {
    initVisualization();
  }
}, { deep: true });

watch(() => props.connections, () => {
  if (container.value) {
    initVisualization();
  }
}, { deep: true });

// Initialize on mount
onMounted(() => {
  window.addEventListener('resize', handleResize);
  initVisualization();
});

// Cleanup on unmount
onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (simulation) {
    simulation.stop();
  }
});
</script>

<style scoped>
.d3-visualization-container {
  width: 100%;
  height: 800px;
  background-color: #0f172a;
  border-radius: 1rem;
  position: relative;
  overflow: hidden;
}

.loading-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(15, 23, 42, 0.8);
  z-index: 100;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

:deep(.d3-visualization) {
  background-color: transparent;
}

:deep(.node) {
  cursor: pointer;
  transition: transform 0.3s ease;
}

:deep(.node:hover) {
  transform: scale(1.1);
}

:deep(.node-label) {
  font-weight: bold;
  font-size: 12px;
  pointer-events: none;
}

:deep(.platform-label) {
  font-size: 10px;
  pointer-events: none;
}

:deep(.connection-path) {
  stroke-linecap: round;
  filter: drop-shadow(0 0 3px rgba(255, 255, 255, 0.3));
}

:deep(.connection-particle) {
  pointer-events: none;
}

/* Snowflake specific styles */
:deep(.snowflake-node rect) {
  filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.4));
}

/* Fabric specific styles */
:deep(.fabric-node rect) {
  filter: drop-shadow(0 0 8px rgba(45, 212, 191, 0.4));
}

/* PowerBI specific styles */
:deep(.powerbi-node rect) {
  filter: drop-shadow(0 0 8px rgba(217, 70, 239, 0.4));
}
</style> 