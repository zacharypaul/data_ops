<template>
  <div 
    class="bg-dark-800 rounded-lg border border-dark-600 overflow-hidden h-full hover:bg-dark-750 hover:border-blue-500/30 transition-all duration-300"
  >
    <div class="p-5">
      <!-- Header with step icon and title -->
      <div class="flex items-center mb-4">
        <div class="bg-blue-500/20 rounded-full p-2 mr-3">
          <i :class="`fas ${step.icon} text-blue-500 text-lg`"></i>
        </div>
        <h3 class="text-xl font-bold">{{ step.title }}</h3>
      </div>
      
      <!-- Description -->
      <p class="text-gray-300 mb-4">{{ step.description }}</p>
      
      <!-- Key items -->
      <div class="mb-4">
        <h4 class="text-sm uppercase tracking-wider text-gray-400 mb-2">Key Items</h4>
        <ul class="space-y-1">
          <li v-for="(item, i) in step.keyItems" :key="i" 
            class="flex items-start">
            <i class="fas fa-check-circle text-blue-500 mt-1 mr-2 text-sm"></i>
            <span class="text-sm">{{ item }}</span>
          </li>
        </ul>
      </div>
      
      <!-- Time estimate -->
      <div class="mb-4">
        <h4 class="text-sm uppercase tracking-wider text-gray-400 mb-2">Time Estimate</h4>
        <div class="flex items-center">
          <i class="fas fa-clock text-blue-400 mr-2"></i>
          <span class="text-sm">{{ step.timeEstimate }}</span>
        </div>
      </div>
      
      <!-- View details button -->
      <button 
        @click="$emit('view-details', step)"
        class="w-full mt-2 bg-dark-700 hover:bg-blue-600 text-white py-2 px-4 rounded-md transition-colors duration-200"
      >
        View Details
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  step: {
    type: Object,
    required: true
  }
});

defineEmits(['view-details']);
</script> 