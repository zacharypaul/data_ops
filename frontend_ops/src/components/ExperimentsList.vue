<template>
  <div>
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-xl font-bold">Recent Experiments</h3>
      <div class="flex space-x-3">
        <div class="flex items-center bg-dark-800 rounded-lg p-1">
          <button 
            @click="$emit('update:viewMode', 'snapshot')" 
            :class="[
              'px-3 py-1 text-sm rounded-md transition-colors',
              viewMode === 'snapshot' ? 'bg-primary-600 text-white' : 'text-gray-300'
            ]"
          >
            Snapshot
          </button>
          <button 
            @click="$emit('update:viewMode', 'timeseries')" 
            :class="[
              'px-3 py-1 text-sm rounded-md transition-colors',
              viewMode === 'timeseries' ? 'bg-primary-600 text-white' : 'text-gray-300'
            ]"
          >
            Time Series
          </button>
        </div>
        <button @click="$emit('newExperiment')" class="btn-primary py-1 px-3 text-sm">New Experiment</button>
      </div>
    </div>
    
    <!-- Snapshot View -->
    <div v-if="viewMode === 'snapshot'" class="overflow-x-auto">
      <table class="min-w-full divide-y divide-dark-700">
        <thead>
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Name</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Platform</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Model Type</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Created</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Metrics</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-dark-700">
          <tr v-for="(exp, index) in experiments" :key="index" class="hover:bg-dark-800 transition-colors">
            <td class="px-4 py-3 whitespace-nowrap">{{ exp.name }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="`text-${platformColors[exp.platform]}-400`">{{ exp.platform }}</span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap">{{ exp.modelType }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span :class="`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-${statusColors[exp.status]}-900 text-${statusColors[exp.status]}-300`">
                {{ exp.status }}
              </span>
            </td>
            <td class="px-4 py-3 whitespace-nowrap text-gray-400">{{ exp.created }}</td>
            <td class="px-4 py-3 whitespace-nowrap">
              <span class="text-primary-400">{{ exp.metrics }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
defineProps({
  experiments: {
    type: Array,
    required: true
  },
  platformColors: {
    type: Object,
    required: true
  },
  statusColors: {
    type: Object,
    required: true
  },
  viewMode: {
    type: String,
    required: true
  }
});

defineEmits(['update:viewMode', 'newExperiment']);
</script>

<style scoped>
.btn-primary {
  @apply bg-primary-600 hover:bg-primary-700 text-white rounded-md transition-colors;
}
</style> 