<template>
  <div class="d3-tech-graph" ref="container">
    <div class="graph-legend">
      <div class="legend-section">
        <h3 class="legend-header">Platforms</h3>
        <div class="legend-item">
          <div class="legend-color snowflake-color"></div>
          <div class="legend-label">Snowflake</div>
        </div>
        <div class="legend-item">
          <div class="legend-color fabric-color"></div>
          <div class="legend-label">Fabric</div>
        </div>
        <div class="legend-item">
          <div class="legend-color sqlserver-color"></div>
          <div class="legend-label">SQL Server</div>
        </div>
        <div class="legend-item">
          <div class="legend-color aws-color"></div>
          <div class="legend-label">AWS</div>
        </div>
        <div class="legend-item">
          <div class="legend-color azure-color"></div>
          <div class="legend-label">Azure</div>
        </div>
        <div class="legend-item">
          <div class="legend-color powerbi-color"></div>
          <div class="legend-label">Power BI</div>
        </div>
      </div>
      
      <div class="legend-section">
        <h3 class="legend-header">Technologies</h3>
        <div class="legend-item">
          <div class="legend-tech s3-tech"></div>
          <div class="legend-label">S3</div>
        </div>
        <div class="legend-item">
          <div class="legend-tech blob-tech"></div>
          <div class="legend-label">Azure Blob</div>
        </div>
        <div class="legend-item">
          <div class="legend-tech airflow-tech"></div>
          <div class="legend-label">AWS Airflow</div>
        </div>
        <div class="legend-item">
          <div class="legend-tech dbt-tech"></div>
          <div class="legend-label">Snowflake DBT</div>
        </div>
        <div class="legend-item">
          <div class="legend-tech adf-tech"></div>
          <div class="legend-label">Azure ADF</div>
        </div>
        <div class="legend-item">
          <div class="legend-tech meltano-tech"></div>
          <div class="legend-label">Meltano</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
import * as d3 from 'd3';
import { _3d } from 'd3-3d';

// Define props
const props = defineProps({
  nodes: {
    type: Array,
    default: () => []
  },
  connections: {
    type: Array,
    default: () => []
  }
});

// Define emits
const emit = defineEmits(['nodeSelected']);

// Setup refs
const container = ref(null);
let svg = null;
let width = 0;
let height = 0;
let simulation = null;
let nodes3D = [];
let links3D = [];

// Platform colors
const platformColors = {
  'SNOWFLAKE': '#38bdf8', 
  'FABRIC': '#2dd4bf',
  'POWERBI': '#f59e0b'  // Changed from purple to yellow
};

// Initialize the 3D projection
const d3_3d = _3d()
  .origin([0, 0])
  .scale(400)
  .rotateX(Math.PI/8)
  .rotateY(Math.PI/8);

// Initialize on mount
onMounted(() => {
  nextTick(() => {
    initGraph();
    
    // Add window resize handler
    window.addEventListener('resize', resizeGraph);
  });
});

// Cleanup on unmount
onUnmounted(() => {
  if (simulation) simulation.stop();
  window.removeEventListener('resize', resizeGraph);
});

// Transform data for 3D visualization
const processData = () => {
  nodes3D = props.nodes.map((node, i) => {
    const platformZ = getPlatformZPosition(node.platform, node.technology);
    
    // Index within same platform type - used for better distribution
    const platformNodes = props.nodes.filter(n => n.platform === node.platform);
    const platformIndex = platformNodes.findIndex(n => n.id === node.id);
    const platformCount = platformNodes.length;
    const spreadFactor = platformCount > 1 ? platformIndex / (platformCount - 1) - 0.5 : 0;
    
    // Calculate initial positions
    const initialX = getInitialX(node.platform, platformIndex, platformCount, node);
    const initialY = getInitialY(node.platform, platformIndex, platformCount, node);
    
    // Fix positions for specific platforms
    const fixedX = node.platform === 'POWERBI' || node.platform === 'SNOWFLAKE' || node.platform === 'FABRIC' 
      ? initialX : null;
    const fixedY = node.platform === 'POWERBI' || node.platform === 'SNOWFLAKE' || node.platform === 'FABRIC' 
      ? initialY : null;
    
    return {
      ...node,
      id: node.id || i,
      x: initialX,
      y: initialY,
      z: platformZ,
      fx: fixedX,
      fy: fixedY,
      fz: platformZ
    };
  });
  
  links3D = props.connections
    .filter(conn => {
      const source = nodes3D.find(n => n.id === conn.source);
      const target = nodes3D.find(n => n.id === conn.target);
      return source && target;
    })
    .map(conn => ({
      source: nodes3D.find(n => n.id === conn.source),
      target: nodes3D.find(n => n.id === conn.target),
      active: conn.active || false,
      refreshFrequency: conn.refreshFrequency || { type: 'daily' }
    }));
  
  return { nodes: nodes3D, links: links3D };
};

// Get initial X position based on platform and metadata
const getInitialX = (platform, index, total, metadata = {}) => {
  const centerX = width * 0.5;
  const techType = metadata.technology || '';
  
  switch(platform) {
    case 'SNOWFLAKE': {
      // Position Snowflake nodes in a horizontal line at the top
      // Distribute nodes evenly across the width
      const spacing = (width * 0.7) / (total + 1);
      return (width * 0.15) + spacing * (index + 1);
    }
    case 'FABRIC': {
      // Position Fabric nodes in a horizontal line at the bottom
      // Distribute nodes evenly across the width
      const spacing = (width * 0.7) / (total + 1);
      return (width * 0.15) + spacing * (index + 1);
    }
    case 'POWERBI': {
      // Position PowerBI in a fixed column on the right side
      return width * 0.85; // Fixed position on the right side
    }
    default:
      return centerX;
  }
};

// Get initial Y position based on platform and metadata
const getInitialY = (platform, index, total, metadata = {}) => {
  const centerY = height * 0.5;
  
  switch(platform) {
    case 'SNOWFLAKE': {
      // Position Snowflake nodes at the top
      return height * 0.15; // Fixed position at the top
    }
    case 'FABRIC': {
      // Position Fabric nodes at the bottom
      return height * 0.85; // Fixed position at the bottom
    }
    case 'POWERBI': {
      // Position PowerBI nodes in an evenly spaced column
      // Distribute nodes evenly between top and bottom
      const spacing = height / (total + 1);
      return spacing * (index + 1);
    }
    default:
      return centerY;
  }
};

// Get Z position based on platform and technology
const getPlatformZPosition = (platform, technology = '') => {
  // Base Z position by platform
  let baseZ = 0;
  switch(platform) {
    case 'SNOWFLAKE': baseZ = -20; break;
    case 'FABRIC': baseZ = 20; break;
    case 'POWERBI': baseZ = 40; break;
  }
  
  // Add technology-specific offsets for visual separation
  if (technology.includes('Fivetran')) {
    return baseZ + 5;
  } else if (technology.includes('Airflow')) {
    return baseZ;
  } else if (technology.includes('ADF')) {
    return baseZ - 5;
  }
  
  return baseZ;
};

// Initialize the 3D graph
const initGraph = () => {
  if (!container.value) return;
  
  // Clear any existing visualization
  d3.select(container.value).select('svg').remove();
  
  // Get container dimensions
  width = container.value.clientWidth;
  height = container.value.clientHeight || 600;
  
  // Create SVG element
  svg = d3.select(container.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', [0, 0, width, height]);
  
  // Add defs for gradients and filters
  const defs = createDefs();
  
  // Process data for visualization
  const data = processData();
  
  // Create the force simulation with stronger positioning forces
  simulation = d3.forceSimulation(data.nodes)
    .force('link', d3.forceLink(data.links).id(d => d.id).distance(d => {
      // Longer distances between different platforms
      if (d.source.platform !== d.target.platform) {
        return 200; // Increased for better separation
      }
      if (d.source.technology !== d.target.technology) {
        return 150; // Medium distance between different technologies
      }
      return 100; // Shorter distances within same platform and technology
    }))
    .force('charge', d3.forceManyBody().strength(d => {
      // Reduce the effect of charge on fixed nodes
      if (d.platform === 'SNOWFLAKE' || d.platform === 'FABRIC' || d.platform === 'POWERBI') {
        return -20; // Much weaker repulsion for fixed nodes
      }
      return -120; // Normal repulsion for other nodes
    }))
    .force('x', d3.forceX(d => {
      // Get counts by platform and technology
      const techNodes = data.nodes.filter(n => 
        n.platform === d.platform && 
        (n.technology === d.technology || n.techGroup === d.techGroup)
      );
      const platformIndex = techNodes.findIndex(n => n.id === d.id);
      const platformCount = techNodes.length;
      
      return getInitialX(d.platform, platformIndex, platformCount, d);
    }).strength(d => {
      // Fixed nodes should have zero x force
      if (d.platform === 'SNOWFLAKE' || d.platform === 'FABRIC' || d.platform === 'POWERBI') {
        return 0;
      }
      return 0.8; // Normal strength for other nodes
    }))
    .force('y', d3.forceY(d => {
      // Get counts by platform and technology
      const techNodes = data.nodes.filter(n => 
        n.platform === d.platform && 
        (n.technology === d.technology || n.techGroup === d.techGroup)
      );
      const platformIndex = techNodes.findIndex(n => n.id === d.id);
      const platformCount = techNodes.length;
      
      return getInitialY(d.platform, platformIndex, platformCount, d);
    }).strength(d => {
      // Fixed nodes should have zero y force
      if (d.platform === 'SNOWFLAKE' || d.platform === 'FABRIC' || d.platform === 'POWERBI') {
        return 0;
      } 
      return 0.8; // Normal strength for other nodes
    }))
    .force('collide', d3.forceCollide(40)) // Increased node separation
    .on('tick', ticked);
  
  // Let simulation cool down before interaction
  simulation.alpha(0.9).alphaDecay(0.02); // Slower decay for better settlement
  
  // Heat simulation for a bit then let it stabilize
  setTimeout(() => {
    // Keep stronger forces to maintain cluster formation
    simulation.force('charge').strength(-80);
    simulation.force('x').strength(0.6);
    simulation.force('y').strength(0.6);
    simulation.alphaTarget(0).alphaDecay(0.02);
  }, 2000);
  
  // Create the links
  const link = svg.append('g')
    .attr('class', 'links')
    .selectAll('path')
    .data(data.links)
    .enter().append('path')
    .attr('class', d => `link ${d.active ? 'active-link' : 'inactive-link'}`)
    .attr('stroke', d => {
      if (!d.active) return '#555';
      // Use platform-specific colors for links
      if (d.source.platform === 'POWERBI' || d.target.platform === 'POWERBI') {
        return 'url(#powerbi-gradient)';
      } else if (d.source.platform === 'FABRIC' || d.target.platform === 'FABRIC') {
        return 'url(#fabric-gradient)';
      }
      return 'url(#snowflake-gradient)';
    })
    .attr('stroke-width', d => getLinkWidth(d))
    .attr('stroke-opacity', d => d.active ? 0.8 : 0.3)
    .attr('fill', 'none')
    .attr('filter', d => d.active ? 'url(#glow)' : null)
    .attr('data-id', d => `${d.source.id}-${d.target.id}`); // Add data-id for particle animation
  
  // Add particles to active links
  data.links.forEach(link => {
    if (link.active) {
      addParticles(link);
    }
  });
  
  // Create the node groups
  const node = svg.append('g')
    .attr('class', 'nodes')
    .selectAll('.node')
    .data(data.nodes)
    .enter().append('g')
    .attr('class', d => `node node-${d.platform.toLowerCase()}`)
    .on('click', (event, d) => {
      // Prevent event propagation to avoid layout disruption
      event.stopPropagation();
      emit('nodeSelected', d);
    })
    .call(d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended));
  
  // Add node shapes with platform-specific styling
  node.each(function(d) {
    const g = d3.select(this);
    
    if (d.platform === 'POWERBI') {
      // Square shape for PowerBI nodes
      g.append('rect')
        .attr('width', 50)  // Larger square
        .attr('height', 50)
        .attr('x', -25)     // Center the square
        .attr('y', -25)
        .attr('rx', 5)      // Slightly rounded corners
        .attr('ry', 5)
        .attr('fill', `url(#${d.platform.toLowerCase()}-gradient)`)
        .attr('stroke', '#92400e')
        .attr('stroke-width', 2)
        .attr('filter', 'url(#glow)');
    } else if (d.platform === 'SNOWFLAKE') {
      // Add an invisible larger circle for better click target
      g.append('circle')
        .attr('r', 35)
        .attr('fill', 'rgba(0,0,0,0)')  // Transparent
        .attr('class', 'click-target');

      // Snowflake shape - larger and more visible
      const snowflakePath = createSnowflakePath(30); // Increased from 25
      g.append('path')
        .attr('d', snowflakePath)
        .attr('fill', `url(#${d.platform.toLowerCase()}-gradient)`)
        .attr('stroke', '#0c4a6e')
        .attr('stroke-width', 2.5)  // Thicker stroke
        .attr('filter', 'url(#snowflake-glow)');  // Special glow filter
    } else {
      // Circles for Fabric platform
      g.append('circle')
        .attr('r', d => {
          // Slightly different sizes based on technology
          if (d.technology && d.technology.includes('Fivetran')) {
            return 27; // Slightly larger
          } else if (d.technology && d.technology.includes('ADF')) {
            return 23; // Slightly smaller
          }
          return 25; // Default size
        })
        .attr('fill', d => `url(#${d.platform.toLowerCase()}-gradient)`)
        .attr('stroke', d => {
          // Different stroke colors based on technology
          if (d.technology && d.technology.includes('Fivetran')) {
            return '#94a3b8'; // Slate color for Fivetran
          } else if (d.technology && d.technology.includes('Airflow')) {
            return '#818cf8'; // Indigo color for Airflow
          } else if (d.technology && d.technology.includes('ADF')) {
            return '#fb923c'; // Orange color for ADF
          }
          return platformColors[d.platform] || '#fff';
        })
        .attr('stroke-width', d => d.technology && d.technology.includes('Fivetran') ? 3 : 2)
        .attr('filter', 'url(#glow)');
    }
  });
  
  // Add node labels
  node.append('text')
    .attr('class', 'node-label')
    .attr('dy', d => d.platform === 'POWERBI' ? 45 : 40)  // Lower position for PowerBI labels
    .attr('text-anchor', 'middle')
    .attr('fill', 'white')
    .text(d => {
      // Shorten long names
      if (d.name.length > 15) {
        return d.name.substring(0, 13) + '...';
      }
      return d.name;
    })
    .attr('pointer-events', 'none'); // Prevent label from capturing events
  
  // Setup rotation control
  setupRotationControl();
};

// Create SVG defs with gradients and filters
const createDefs = () => {
  const defs = svg.append('defs');
  
  // Create platform gradients
  createGradient(defs, 'snowflake-gradient', '#5ebafc', '#0c4a6e'); // Brighter blue for snowflake
  createGradient(defs, 'fabric-gradient', platformColors.FABRIC, '#064e3b');
  createGradient(defs, 'powerbi-gradient', platformColors.POWERBI, '#92400e');
  
  // Create link gradients
  createGradient(defs, 'active-link-gradient', '#ffffff', '#38bdf8');
  
  // Create glow filter
  const filter = defs.append('filter')
    .attr('id', 'glow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%');
    
  filter.append('feGaussianBlur')
    .attr('stdDeviation', '3')
    .attr('result', 'blur');
    
  filter.append('feComposite')
    .attr('in', 'SourceGraphic')
    .attr('in2', 'blur')
    .attr('operator', 'over');

  // Create stronger glow filter for snowflakes
  const snowflakeFilter = defs.append('filter')
    .attr('id', 'snowflake-glow')
    .attr('x', '-50%')
    .attr('y', '-50%')
    .attr('width', '200%')
    .attr('height', '200%');
    
  snowflakeFilter.append('feGaussianBlur')
    .attr('stdDeviation', '5')  // Stronger blur
    .attr('result', 'blur');
    
  snowflakeFilter.append('feComposite')
    .attr('in', 'SourceGraphic')
    .attr('in2', 'blur')
    .attr('operator', 'over');
  
  return defs;
};

// Create a linear gradient
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

// Get link width based on refresh frequency
const getLinkWidth = (link) => {
  if (!link.refreshFrequency) return 2;
  
  switch (link.refreshFrequency.type) {
    case 'hourly': return 4;
    case 'daily': return 3;
    case 'weekly': return 2;
    default: return 2;
  }
};

// Add animated particles to links
const addParticles = (link) => {
  const particleCount = link.refreshFrequency?.type === 'hourly' ? 5 : 3;
  
  for (let i = 0; i < particleCount; i++) {
    svg.append('circle')
      .datum(link)
      .attr('class', 'particle')
      .attr('r', 3)
      .attr('fill', platformColors[link.source.platform] || '#ffffff')
      .style('filter', 'url(#glow)')
      .style('opacity', 0.7);
  }
};

// Setup rotation control for 3D effect
const setupRotationControl = () => {
  let startX = 0;
  let startY = 0;
  let rotationX = Math.PI/8;
  let rotationY = Math.PI/8;
  let isDraggingScene = false;
  
  // Add a transparent overlay for scene rotation that doesn't conflict with nodes
  const rotationControl = svg.append('rect')
    .attr('class', 'rotation-control')
    .attr('width', width)
    .attr('height', height)
    .attr('fill', 'transparent')
    .style('cursor', 'move')
    .call(d3.drag()
      .on('start', (event) => {
        // Only start rotation if not interacting with a node
        if (event.sourceEvent.target.classList.contains('rotation-control')) {
          isDraggingScene = true;
          startX = event.x;
          startY = event.y;
          
          // Pause simulation during rotation to prevent jitter
          simulation.alpha(0).stop();
        }
      })
      .on('drag', (event) => {
        if (!isDraggingScene) return;
        
        const dx = event.x - startX;
        const dy = event.y - startY;
        
        // Use smaller rotation increments for smoother effect
        rotationY += dx * 0.005;
        rotationX += dy * 0.005;
        
        // Update the 3D projection
        d3_3d.rotateX(rotationX).rotateY(rotationY);
        
        // Update positions without simulation
        ticked();
        
        startX = event.x;
        startY = event.y;
      })
      .on('end', () => {
        isDraggingScene = false;
        
        // Restart simulation at very low alpha to minimize disruption
        simulation.alpha(0.1).restart();
        simulation.alphaTarget(0);
      })
    );
    
  // Ensure nodes are above the rotation control for interaction
  svg.selectAll('.nodes').raise();
};

// Simulation tick function
function ticked() {
  // Project the 3D points to 2D
  const projectedNodes = d3_3d(nodes3D);
  
  // Update node positions
  svg.selectAll('.node')
    .attr('transform', (d, i) => {
      // Apply 3D projection
      const x = d.x;
      const y = d.y;
      const z = d.z || 0;
      
      // Scale based on z position for pseudo-3D effect
      const scale = 1 + (z / 500);
      
      return `translate(${x}, ${y}) scale(${scale})`;
    });
  
  // Update link paths
  svg.selectAll('.link')
    .attr('d', (d) => {
      const sourceX = d.source.x;
      const sourceY = d.source.y;
      const targetX = d.target.x;
      const targetY = d.target.y;
      
      // Calculate path with arc for 3D effect
      const dx = targetX - sourceX;
      const dy = targetY - sourceY;
      const dr = Math.sqrt(dx * dx + dy * dy) * 1.5;
      
      // Add 3D perspective effect based on z positions
      const sourceZ = d.source.z || 0;
      const targetZ = d.target.z || 0;
      const zDiff = Math.abs(targetZ - sourceZ);
      
      // More curved for larger z differences
      const curveFactor = 0.5 + (zDiff / 200);
      
      return `M ${sourceX} ${sourceY} A ${dr * curveFactor} ${dr * curveFactor} 0 0 1 ${targetX} ${targetY}`;
    });
  
  // Update particles
  svg.selectAll('.particle')
    .each(function(d) {
      if (!d) return; // Skip if data is undefined
      
      const selector = `.link[data-id="${d.source.id}-${d.target.id}"]`;
      const path = svg.select(selector);
      
      if (!path.empty()) {
        const pathNode = path.node();
        // Only proceed if we can get path length
        if (pathNode && typeof pathNode.getTotalLength === 'function') {
          const pathLength = pathNode.getTotalLength();
          
          // Calculate particle position along the path
          const offset = (Date.now() % 3000) / 3000 * pathLength;
          try {
            const point = pathNode.getPointAtLength(offset);
            
            d3.select(this)
              .attr('cx', point.x)
              .attr('cy', point.y);
          } catch (e) {
            // If point calculation fails, hide the particle
            d3.select(this).style('opacity', 0);
          }
        }
      }
    });
}

// Drag handlers
function dragstarted(event, d) {
  // Use a very low alpha target to minimize disruption
  if (!event.active) simulation.alphaTarget(0.1).restart();
  
  // Only allow dragging for non-fixed nodes
  if (d.platform !== 'SNOWFLAKE' && d.platform !== 'FABRIC' && d.platform !== 'POWERBI') {
    d.fx = d.x;
    d.fy = d.y;
  }
  
  // Stop propagation to prevent svg drag handler from firing
  event.sourceEvent.stopPropagation();
}

function dragged(event, d) {
  // Only allow dragging horizontally for snowflake and fabric nodes
  if (d.platform === 'SNOWFLAKE') {
    // Only allow horizontal movement within bounds
    d.fx = Math.max(width * 0.1, Math.min(width * 0.9, event.x));
    // Keep fixed vertical position
    d.fy = height * 0.15;
  } else if (d.platform === 'FABRIC') {
    // Only allow horizontal movement within bounds
    d.fx = Math.max(width * 0.1, Math.min(width * 0.9, event.x));
    // Keep fixed vertical position
    d.fy = height * 0.85;
  } else if (d.platform === 'POWERBI') {
    // Don't allow movement for PowerBI nodes
    d.fx = width * 0.85;
  } else {
    // Full movement for other nodes
    d.fx = event.x;
    d.fy = event.y;
  }
}

function dragended(event, d) {
  // Quickly cool down simulation
  if (!event.active) simulation.alphaTarget(0);
  
  // Keep fixed positions for all platform nodes
  if (d.platform === 'SNOWFLAKE') {
    // Keep snowflake nodes in their horizontal line
    d.fy = height * 0.15;
    // Horizontal position from where they were dragged
    d.fx = Math.max(width * 0.1, Math.min(width * 0.9, d.x));
  } else if (d.platform === 'FABRIC') {
    // Keep fabric nodes in their horizontal line
    d.fy = height * 0.85;
    // Horizontal position from where they were dragged
    d.fx = Math.max(width * 0.1, Math.min(width * 0.9, d.x));
  } else if (d.platform === 'POWERBI') {
    // Ensure PowerBI nodes stay in their column on the right
    d.fx = width * 0.85;
  } else {
    d.fx = null;
    d.fy = null;
  }
}

// Handle window resizing
const resizeGraph = () => {
  if (svg && container.value) {
    const width = container.value.clientWidth;
    const height = container.value.clientHeight;
    
    svg.attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height]);
  }
};

// Watch for changes in props
watch(() => props.nodes, () => {
  if (simulation) {
    simulation.stop();
    d3.select(container.value).select('svg').remove();
    initGraph();
  }
}, { deep: true });

watch(() => props.connections, () => {
  if (simulation) {
    simulation.stop();
    d3.select(container.value).select('svg').remove();
    initGraph();
  }
}, { deep: true });

// Function to create a snowflake path
const createSnowflakePath = (size) => {
  // Increase size parameter for better visibility
  const innerRadius = size * 0.5;  // Increased from 0.4
  const outerRadius = size * 1.2;  // Increased by 20%

  // Create 6 spokes for the snowflake
  let path = '';
  
  // Main spokes
  for (let i = 0; i < 6; i++) {
    const angle = (Math.PI / 3) * i;
    const x1 = Math.sin(angle) * innerRadius;
    const y1 = Math.cos(angle) * innerRadius;
    const x2 = Math.sin(angle) * outerRadius;
    const y2 = Math.cos(angle) * outerRadius;
    
    // Main line - make thicker
    path += ` M ${x1},${y1} L ${x2},${y2}`;
    
    // Add smaller branches at 60 degree angles
    const branch1Angle = angle + Math.PI / 6;
    const branch2Angle = angle - Math.PI / 6;
    const branchLength = size * 0.4;  // Increased from 0.3
    
    // Position branches at 70% of the main spoke length
    const branchX = Math.sin(angle) * (outerRadius * 0.7);
    const branchY = Math.cos(angle) * (outerRadius * 0.7);
    
    const branch1X = branchX + Math.sin(branch1Angle) * branchLength;
    const branch1Y = branchY + Math.cos(branch1Angle) * branchLength;
    const branch2X = branchX + Math.sin(branch2Angle) * branchLength;
    const branch2Y = branchY + Math.cos(branch2Angle) * branchLength;
    
    path += ` M ${branchX},${branchY} L ${branch1X},${branch1Y}`;
    path += ` M ${branchX},${branchY} L ${branch2X},${branch2Y}`;
  }
  
  // Add a center circle - larger
  path += ` M 0,${-innerRadius * 0.8} A ${innerRadius * 0.8} ${innerRadius * 0.8} 0 1 1 0,${innerRadius * 0.8} A ${innerRadius * 0.8} ${innerRadius * 0.8} 0 1 1 0,${-innerRadius * 0.8}`;
  
  return path;
};
</script>

<style scoped>
.d3-tech-graph {
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #1e293b, #0f172a);
  border-radius: 0.5rem;
  overflow: hidden;
  position: relative;
}

/* Legend styles */
.graph-legend {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(15, 23, 42, 0.7);
  padding: 10px 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(4px);
  z-index: 10;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.legend-header {
  color: white;
  font-size: 0.85rem;
  font-weight: 500;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
}

.legend-label {
  color: white;
  font-size: 0.85rem;
}

.snowflake-color {
  background: linear-gradient(135deg, #38bdf8, #0c4a6e);
}

.fabric-color {
  background: linear-gradient(135deg, #2dd4bf, #064e3b);
}

.powerbi-color {
  background: linear-gradient(135deg, #f59e0b, #92400e);
}

.sqlserver-color {
  background: linear-gradient(135deg, #6366f1, #4338ca);
}

.aws-color {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.azure-color {
  background: linear-gradient(135deg, #0ea5e9, #0369a1);
}

.s3-tech {
  background: linear-gradient(135deg, #f59e0b, #f59e0b);
}

.blob-tech {
  background: linear-gradient(135deg, #0ea5e9, #0ea5e9);
}

.dbt-tech {
  background: linear-gradient(135deg, #06b6d4, #06b6d4);
}

.meltano-tech {
  background: linear-gradient(135deg, #22c55e, #22c55e);
}

.fivetran-tech {
  background: linear-gradient(135deg, #94a3b8, #94a3b8);
}

.airflow-tech {
  background: linear-gradient(135deg, #818cf8, #818cf8);
}

.adf-tech {
  background: linear-gradient(135deg, #fb923c, #fb923c);
}

.legend-tech {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  box-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(0, 0, 0, 0.3);
}

:deep(.node) {
  cursor: pointer;
  transition: transform 0.2s ease-out;
  /* Remove the hover effect from the node group itself */
}

/* Apply hover effect only to the circle inside the node, not the entire group */
:deep(.node circle) {
  transition: stroke-width 0.2s ease, filter 0.2s ease;
}

:deep(.node:hover circle) {
  stroke-width: 3;
  /* Scale only the circle, not the group containing position data */
  filter: brightness(1.2) drop-shadow(0 0 8px currentColor);
}

:deep(.node-label) {
  font-weight: 500;
  font-size: 0.8rem;
  pointer-events: none;
  text-shadow: 0 0 5px rgba(0, 0, 0, 0.8);
}

:deep(.node-snowflake circle) {
  filter: drop-shadow(0 0 8px rgba(56, 189, 248, 0.5));
}

:deep(.node-fabric circle) {
  filter: drop-shadow(0 0 8px rgba(45, 212, 191, 0.5));
}

:deep(.node-powerbi circle) {
  filter: drop-shadow(0 0 8px rgba(245, 158, 11, 0.5)); /* Updated to yellow glow */
}

:deep(.active-link) {
  stroke-dasharray: 5;
  animation: dash 15s linear infinite;
}

:deep(.particle) {
  pointer-events: none;
}

@keyframes dash {
  to {
    stroke-dashoffset: 1000;
  }
}
</style> 