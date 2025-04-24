<template>
  <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
    <div class="flex items-center">
      <div class="flex-shrink-0">
        <div :class="[
          'p-3 rounded-md inline-flex items-center justify-center', 
          iconColorClass
        ]">
          <component :is="iconComponent" class="h-6 w-6 text-white" />
        </div>
      </div>
      <div class="ml-5 w-full">
        <div class="flex justify-between items-center w-full">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ title }}</h3>
          <span 
            v-if="showTrend" 
            :class="[
              'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium', 
              trendColorClass
            ]"
          >
            <component :is="trendIconComponent" v-if="trendIcon" class="-ml-0.5 mr-1 h-4 w-4" />
            {{ trend }}
          </span>
        </div>
        <div class="mt-2 flex items-baseline">
          <div v-if="isLoading">
            <div class="h-8 w-24 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
          </div>
          <div v-else-if="error" class="text-red-500 text-sm">{{ error }}</div>
          <div v-else>
            <p class="text-3xl font-semibold text-gray-900 dark:text-white flex items-baseline">
              {{ formattedValue }}
              <span v-if="unit" class="ml-1 text-sm text-gray-500 dark:text-gray-400">{{ unit }}</span>
            </p>
            <p v-if="description" class="mt-1 text-sm text-gray-500 dark:text-gray-400">{{ description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { h, computed } from 'vue';
import {
  ChartBarIcon, 
  CalendarIcon, 
  DatabaseIcon, 
  ExclamationCircleIcon,
  ClockIcon, 
  CheckCircleIcon,
  ArrowSmUpIcon,
  ArrowSmDownIcon
} from '@heroicons/vue/solid';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    default: null
  },
  unit: {
    type: String,
    default: null
  },
  icon: {
    type: String,
    default: 'chart'
  },
  iconColor: {
    type: String,
    default: 'blue'
  },
  trend: {
    type: String,
    default: null
  },
  trendDirection: {
    type: String,
    default: null, // positive, negative, neutral
    validator: (value) => ['positive', 'negative', 'neutral', null].includes(value)
  },
  description: {
    type: String,
    default: null
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: String,
    default: null
  },
  formatter: {
    type: Function,
    default: (value) => value
  },
  showTrend: {
    type: Boolean,
    default: true
  }
});

const iconMap = {
  chart: ChartBarIcon,
  calendar: CalendarIcon,
  database: DatabaseIcon,
  error: ExclamationCircleIcon,
  clock: ClockIcon,
  check: CheckCircleIcon
};

const iconComponent = computed(() => {
  return iconMap[props.icon] || ChartBarIcon;
});

const iconColorClass = computed(() => {
  const colorMap = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    yellow: 'bg-yellow-500',
    purple: 'bg-purple-500',
    indigo: 'bg-indigo-500',
    gray: 'bg-gray-500',
  };
  return colorMap[props.iconColor] || 'bg-blue-500';
});

const trendIconComponent = computed(() => {
  if (props.trendDirection === 'positive') {
    return ArrowSmUpIcon;
  } else if (props.trendDirection === 'negative') {
    return ArrowSmDownIcon;
  }
  return null;
});

const trendIcon = computed(() => {
  return props.trendDirection === 'positive' || props.trendDirection === 'negative';
});

const trendColorClass = computed(() => {
  if (props.trendDirection === 'positive') {
    return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100';
  } else if (props.trendDirection === 'negative') {
    return 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100';
  }
  return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
});

const formattedValue = computed(() => {
  if (props.value === null || props.value === undefined) {
    return '-';
  }
  return props.formatter(props.value);
});
</script> 