<template>
  <div class="glass-card p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-bold">{{ application.name }}</h3>
      <span 
        class="px-3 py-1 rounded-full text-sm"
        :class="statusClass"
      >{{ application.status }}</span>
    </div>
    <p class="text-gray-300 mb-4">{{ application.description }}</p>
    
    <div class="grid grid-cols-2 gap-4 mb-4">
      <div>
        <div class="text-gray-400 text-sm mb-1">Average Response Time</div>
        <div class="text-xl font-semibold">{{ application.responseTime }}</div>
      </div>
      <div>
        <div class="text-gray-400 text-sm mb-1">Requests (24h)</div>
        <div class="text-xl font-semibold">{{ application.requests }}</div>
      </div>
      <div>
        <div class="text-gray-400 text-sm mb-1">Base Model</div>
        <div class="text-xl font-semibold">{{ application.model }}</div>
      </div>
      <div>
        <div class="text-gray-400 text-sm mb-1">Last Updated</div>
        <div class="text-xl font-semibold">{{ application.lastUpdated }}</div>
      </div>
    </div>
    
    <div class="flex space-x-2">
      <button class="btn-outline py-1 px-3 text-sm">Monitor</button>
      <button class="btn-outline py-1 px-3 text-sm">Logs</button>
      <button class="btn-outline py-1 px-3 text-sm">Settings</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  application: {
    type: Object,
    required: true
  }
});

const statusClass = computed(() => {
  switch(props.application.status) {
    case 'Production':
      return 'bg-green-900/50 text-green-400';
    case 'Staging':
      return 'bg-purple-900/50 text-purple-400';
    case 'Development':
      return 'bg-blue-900/50 text-blue-400';
    default:
      return 'bg-gray-900/50 text-gray-400';
  }
});
</script>

<style scoped>
.glass-card {
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.btn-outline {
  border: 1px solid rgb(var(--color-dark-600));
  color: rgb(var(--color-dark-300));
  transition: all 0.2s;
  border-radius: 0.25rem;
}

.btn-outline:hover {
  border-color: rgb(var(--color-dark-500));
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
}
</style> 