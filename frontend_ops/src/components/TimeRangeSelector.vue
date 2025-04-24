<template>
  <div class="flex flex-col w-full">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h2>
      <div class="inline-flex shadow-sm rounded-md">
        <button
          v-for="option in timeRangeOptions" 
          :key="option.value"
          @click="selectTimeRange(option.value)"
          :class="[
            'relative inline-flex items-center px-4 py-2 text-sm font-medium',
            option.value === modelValue 
              ? 'bg-blue-600 text-white' 
              : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600',
            getButtonPositionClass(option.value)
          ]"
        >
          {{ option.label }}
        </button>
      </div>
    </div>
    <div v-if="showCustomRange" class="flex items-center space-x-4 mb-4">
      <div class="relative">
        <input
          type="date"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          v-model="customStartDate"
          :max="currentDate"
        />
      </div>
      <span class="text-gray-500 dark:text-gray-400">to</span>
      <div class="relative">
        <input
          type="date"
          class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          v-model="customEndDate"
          :max="currentDate"
          :min="customStartDate"
        />
      </div>
      <button
        @click="applyCustomRange"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        Apply
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  title: {
    type: String,
    default: 'Time Range'
  },
  customOptions: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:modelValue', 'range-changed']);

const timeRangeOptions = computed(() => {
  const defaultOptions = [
    { label: 'Last 24h', value: '24h' },
    { label: 'Last 7d', value: '7d' },
    { label: '30 days', value: '30d' },
    { label: 'Custom', value: 'custom' }
  ];
  
  return props.customOptions.length > 0 ? props.customOptions : defaultOptions;
});

const showCustomRange = computed(() => props.modelValue === 'custom');
const customStartDate = ref(formatDate(new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)));
const customEndDate = ref(formatDate(new Date()));
const currentDate = computed(() => formatDate(new Date()));

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function selectTimeRange(range) {
  emit('update:modelValue', range);
  
  if (range !== 'custom') {
    let endDate = new Date();
    let startDate;
    
    switch (range) {
      case '24h':
        startDate = new Date(endDate.getTime() - 24 * 60 * 60 * 1000);
        break;
      case '7d':
        startDate = new Date(endDate.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '30d':
        startDate = new Date(endDate.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      default:
        if (range.match(/^\d+[dhm]$/)) {
          const value = parseInt(range);
          const unit = range.slice(-1);
          let milliseconds = 0;
          
          if (unit === 'h') milliseconds = value * 60 * 60 * 1000;
          else if (unit === 'd') milliseconds = value * 24 * 60 * 60 * 1000;
          else if (unit === 'm') milliseconds = value * 30 * 24 * 60 * 60 * 1000; // approximate months
          
          startDate = new Date(endDate.getTime() - milliseconds);
        } else {
          startDate = new Date(endDate.getTime() - 7 * 24 * 60 * 60 * 1000); // default to 7d
        }
    }
    
    emitRangeChanged(startDate, endDate);
  }
}

function applyCustomRange() {
  if (customStartDate.value && customEndDate.value) {
    const startDate = new Date(customStartDate.value);
    const endDate = new Date(customEndDate.value);
    
    // Set end date to end of day
    endDate.setHours(23, 59, 59, 999);
    
    emitRangeChanged(startDate, endDate);
  }
}

function emitRangeChanged(startDate, endDate) {
  emit('range-changed', {
    startDate,
    endDate,
    range: props.modelValue
  });
}

function getButtonPositionClass(value) {
  const index = timeRangeOptions.value.findIndex(option => option.value === value);
  const total = timeRangeOptions.value.length;
  
  if (total === 1) return 'rounded-md';
  if (index === 0) return 'rounded-l-md';
  if (index === total - 1) return 'rounded-r-md';
  return '-ml-px';
}

// Initialize with the current time range on component creation
watch(() => props.modelValue, (newValue) => {
  selectTimeRange(newValue);
}, { immediate: true });
</script> 