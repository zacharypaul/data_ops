<template>
  <div class="mb-8">
    <nav class="glass-card p-2 flex space-x-1 rounded-xl">
      <button 
        v-for="(tab, index) in tabs" 
        :key="index"
        @click="$emit('update:activeTab', tab.id)"
        :class="[
          'px-4 py-2 text-sm rounded-lg transition-colors',
          activeTab === tab.id 
            ? 'bg-primary-600 text-white' 
            : 'text-gray-300 hover:text-white hover:bg-dark-700'
        ]"
      >
        {{ tab.name }}
      </button>
    </nav>
  </div>
</template>

<script setup>
defineProps({
  tabs: {
    type: Array,
    required: true
  },
  activeTab: {
    type: String,
    required: true
  }
});

defineEmits(['update:activeTab']);
</script>

<style scoped>
.glass-card {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
</style> 