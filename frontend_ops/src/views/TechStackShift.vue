<template>
  <div class="py-8">
    <h1 class="text-3xl font-display font-bold mb-4 text-center">Tech Stack Shift</h1>
    <p class="text-center text-dark-400 mb-8">Migration path from Snowflake to Microsoft Fabric with PowerBI integrations</p>
    
    <!-- Loading state -->
    <div v-if="loading" class="text-center py-10">
      <div class="text-primary-500">Loading connectors...</div>
    </div>
    
    <!-- Error state -->
    <div v-else-if="error" class="text-center py-10">
      <div class="text-red-500">{{ error }}</div>
      <button @click="fetchConnectors" class="btn-primary mt-4">Retry</button>
    </div>
    
    <div v-else class="stack-shift-container">
      <ThreeDTechStack :connectors="connectors" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ThreeDTechStack from '../components/stack/ThreeDTechStack.vue';
import axios from 'axios';

// Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080';

// State variables
const loading = ref(true);
const error = ref(null);
const connectors = ref([]);

// Fetch connectors data
const fetchConnectors = async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await axios.get(`${API_URL}/connectors`);
    connectors.value = response.data;
  } catch (err) {
    console.error('Error fetching connectors:', err);
    error.value = 'Failed to fetch connector data. Please try again.';
  } finally {
    loading.value = false;
  }
};

// Fetch data on component mount
onMounted(() => {
  fetchConnectors();
});
</script>

<style scoped>
.stack-shift-container {
  width: 100%;
  min-height: 80vh;
  position: relative;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
}

.tech-stack-page {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
  background-color: #0f172a;
  perspective: 1200px;
}

.tech-stack-header {
  margin-bottom: 2rem;
  color: white;
}

.tech-stack-title {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: white;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
}

.tech-stack-description {
  font-size: 1rem;
  color: #cbd5e1;
  max-width: 800px;
}

.tech-stack-visualization {
  position: relative;
  height: calc(100vh - 200px);
  perspective: 2000px;
  transform-style: preserve-3d;
  overflow: visible;
}

/* Loading state */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;
  color: white;
}

.loading-spinner {
  margin-bottom: 1rem;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #38bdf8;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Error state */
.error-container {
  background-color: rgba(239, 68, 68, 0.2);
  border-left: 4px solid rgb(239, 68, 68);
  padding: 1rem;
  margin: 2rem 0;
  color: white;
  border-radius: 0.25rem;
}

/* Legend */
.tech-stack-legend {
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  color: white;
  font-size: 0.875rem;
}

.legend-color {
  width: 20px;
  height: 8px;
  margin-right: 0.5rem;
  border-radius: 4px;
}

.legend-hourly {
  background: linear-gradient(90deg, rgba(74, 222, 128, 0.5), rgba(74, 222, 128, 1));
  box-shadow: 0 0 5px rgba(74, 222, 128, 0.7);
}

.legend-daily {
  background: linear-gradient(90deg, rgba(56, 189, 248, 0.5), rgba(56, 189, 248, 1));
  box-shadow: 0 0 5px rgba(56, 189, 248, 0.7);
}

.legend-weekly {
  background: linear-gradient(90deg, rgba(168, 85, 247, 0.5), rgba(168, 85, 247, 1));
  box-shadow: 0 0 5px rgba(168, 85, 247, 0.7);
}

/* Animation for beam rotation effect */
@keyframes beam-move {
  0% {
    transform: translateX(0%) scaleX(1);
    opacity: 0.7;
  }
  50% {
    transform: translateX(0%) scaleX(1.1);
    opacity: 1;
  }
  100% {
    transform: translateX(0%) scaleX(1);
    opacity: 0.7;
  }
}
</style> 