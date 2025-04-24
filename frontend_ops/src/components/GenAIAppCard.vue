<template>
  <div class="glass-card p-6 mb-4">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-xl font-bold">{{ app.name }}</h3>
        <p class="text-gray-300 text-sm mt-1">{{ app.description }}</p>
      </div>
      <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${statusColors[app.status]}-900 text-${statusColors[app.status]}-300`">
        {{ app.status }}
      </span>
    </div>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
      <div>
        <div class="text-sm text-gray-400">Average Response Time</div>
        <div class="font-semibold">{{ app.responseTime }}ms</div>
      </div>
      <div>
        <div class="text-sm text-gray-400">Requests (24h)</div>
        <div class="font-semibold">{{ app.requests }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-400">Base Model</div>
        <div class="font-semibold">{{ app.model }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-400">Last Updated</div>
        <div class="font-semibold">{{ app.updated }}</div>
      </div>
    </div>
    <div class="flex space-x-2">
      <button class="btn-secondary py-1 px-3 text-sm">Monitor</button>
      <button class="btn-secondary py-1 px-3 text-sm">Logs</button>
      <button class="btn-secondary py-1 px-3 text-sm">Settings</button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  app: {
    type: Object,
    required: true
  },
  statusColors: {
    type: Object,
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

.btn-secondary {
  @apply bg-dark-700 hover:bg-dark-600 text-white rounded-md transition-colors;
}
</style> 