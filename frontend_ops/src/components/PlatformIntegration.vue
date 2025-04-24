<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Platform Integration</h2>
    <p class="mb-6">Connect your ML Ops platform with data warehouses, compute resources, and deployment targets.</p>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
      <div v-for="(integration, index) in integrations" :key="index" class="glass-card p-5">
        <h3 class="text-xl font-bold mb-4">{{ integration.name }} Integration</h3>
        <p class="text-gray-300 mb-4">{{ integration.description }}</p>
        <div class="flex items-center space-x-2 mb-4" :class="`text-${integration.status.color}-400`">
          <svg v-if="integration.status.value === 'connected'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
          </svg>
          <svg v-else-if="integration.status.value === 'partial'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v3a1 1 0 11-2 0v-3a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <span>{{ integration.status.label }}</span>
        </div>
        <button class="btn-primary py-1.5 px-3">{{ integration.status.value === 'not-connected' ? 'Connect' : 'Configure' }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  integrations: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.btn-primary {
  @apply bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors;
}
</style> 