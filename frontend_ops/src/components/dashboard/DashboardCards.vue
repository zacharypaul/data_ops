<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
    <!-- Active Connectors Card -->
    <MetricCard 
      title="Active Connectors" 
      :value="metrics.activeConnectors.current" 
      :suffix="`/${metrics.activeConnectors.total}`"
      :percentage="metrics.activeConnectors.percentage"
      icon-type="connectors"
      color-class="primary"
    />

    <!-- Freshness Score Card -->
    <MetricCard 
      title="Freshness Score" 
      :value="metrics.freshnessScore.value" 
      suffix="%"
      :percentage="metrics.freshnessScore.percentage"
      icon-type="freshness"
      color-class="secondary"
    />

    <!-- Quality Checks Card -->
    <MetricCard 
      title="Quality Checks" 
      :value="metrics.qualityChecks.passed" 
      :suffix="`/${metrics.qualityChecks.total}`"
      :percentage="metrics.qualityChecks.percentage"
      icon-type="quality"
      color-class="accent"
    />

    <!-- Pipeline Runtime Card -->
    <MetricCard 
      title="Avg. Pipeline Runtime" 
      :value="metrics.pipelineRuntime.value" 
      :suffix="metrics.pipelineRuntime.unit"
      :percentage="metrics.pipelineRuntime.percentage"
      icon-type="runtime"
      color-class="gold"
    />
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import MetricCard from './MetricCard.vue';

const props = defineProps({
  metrics: {
    type: Object,
    required: true
  }
});
</script> 