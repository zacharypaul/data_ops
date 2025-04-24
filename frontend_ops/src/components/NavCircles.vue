<template>
  <div class="flex flex-col space-y-6 items-center py-4">
    <router-link
      v-for="(item, index) in navItems"
      :key="index"
      :to="item.path"
      class="w-14 h-14 rounded-full flex items-center justify-center cursor-pointer transition-all duration-300 hover:scale-110"
      :style="{ backgroundColor: item.color }"
      :class="[
        $route.path === item.path ? 'ring-2 ring-white ring-offset-2 ring-offset-dark-900' : ''
      ]"
    >
      <span class="circle-number">{{ index + 1 }}</span>
    </router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// Navigation items with colors
const navItems = [
  { 
    name: 'Infrastructure Setup', 
    path: '/infrastructure', 
    color: '#8b5cf6' // Purple
  },
  { 
    name: 'Data Pipeline', 
    path: '/data-pipeline', 
    color: '#3b82f6' // Blue
  },
  { 
    name: 'Model Development', 
    path: '/model-development', 
    color: '#4ade80' // Green
  },
  { 
    name: 'CI/CD Pipeline', 
    path: '/cicd', 
    color: '#e97f11' // Orange
  },
  { 
    name: 'Model Monitoring', 
    path: '/monitoring', 
    color: '#ef4444' // Red
  },
  { 
    name: 'Governance & Security', 
    path: '/governance', 
    color: '#10b981' // Teal
  }
];
</script>

<style scoped>
/* Shadow and glow effect for the circles */
.router-link-active {
  box-shadow: 0 0 15px rgba(255, 255, 255, 0.2);
}

.circle-number {
  color: white;
  font-weight: 800;
  font-size: 1.5rem;
  text-shadow: 
    0 1px 2px rgba(0, 0, 0, 0.6),
    0 0 5px rgba(0, 0, 0, 0.4);
  position: relative;
  z-index: 10;
  letter-spacing: -0.5px;
}

/* Add a hover effect for the numbers */
.w-14:hover .circle-number {
  transform: scale(1.1);
  text-shadow: 
    0 1px 3px rgba(0, 0, 0, 0.8),
    0 0 8px rgba(255, 255, 255, 0.4);
}
</style> 