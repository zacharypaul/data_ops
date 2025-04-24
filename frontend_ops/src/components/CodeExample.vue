<template>
  <div class="my-4">
    <div class="flex items-center justify-between mb-2">
      <h3 class="font-semibold text-lg">{{ title }}</h3>
      <div class="flex space-x-2">
        <button 
          v-for="(tab, index) in tabs" 
          :key="index" 
          @click="activeTab = index"
          class="px-3 py-1 text-sm rounded-t-md transition-colors duration-200"
          :class="activeTab === index ? 'bg-dark-700 text-white' : 'bg-dark-800 text-gray-400 hover:text-gray-200'"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="relative">
      <pre class="bg-dark-700 text-gray-300 p-4 rounded-md overflow-x-auto"><code>{{ tabs[activeTab].code }}</code></pre>
      
      <button 
        @click="copyCode" 
        class="absolute top-2 right-2 text-gray-400 hover:text-white p-2 rounded"
        :class="copied ? 'text-green-400' : ''"
      >
        <i :class="copied ? 'fas fa-check' : 'fas fa-copy'"></i>
      </button>
    </div>

    <div v-if="tabs[activeTab].description" class="mt-2 text-sm text-gray-400">
      {{ tabs[activeTab].description }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: 'Code Example'
  },
  tabs: {
    type: Array,
    required: true,
    // Each tab should have { label, code, description? }
  }
});

const activeTab = ref(0);
const copied = ref(false);

const copyCode = () => {
  navigator.clipboard.writeText(props.tabs[activeTab.value].code);
  copied.value = true;
  setTimeout(() => {
    copied.value = false;
  }, 2000);
};
</script> 