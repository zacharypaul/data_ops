<template>
  <div class="glass-card p-6">
    <h2 class="text-xl font-bold mb-4">{{ title }}</h2>
    <p class="text-gray-300 mb-4">{{ description }}</p>
    <div class="text-accent-400 font-semibold">{{ stats }}</div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  stats: {
    type: String,
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
</style> 