<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 24 24" 
    fill="currentColor"
    :width="width" 
    :height="height"
    class="transition-all duration-300">
    <path d="M2 5.5V3.993C2 3.445 2.455 3 2.992 3h18.016c.548 0 .992.456.992.993V5.5H2zM2 8.5v9.007c0 .548.455.993.992.993h18.016c.548 0 .992-.456.992-.993V8.5H2z"/>
    <circle cx="8" cy="6.5" r="1" fill="currentColor"/>
    <circle cx="12" cy="6.5" r="1" fill="currentColor"/>
    <circle cx="16" cy="6.5" r="1" fill="currentColor"/>
    <rect x="5" y="12" width="14" height="2" rx="1" fill="currentColor"/>
    <rect x="5" y="15" width="10" height="2" rx="1" fill="currentColor"/>
  </svg>
</template>

<script setup>
defineProps({
  width: {
    type: [Number, String],
    default: 24
  },
  height: {
    type: [Number, String],
    default: 24
  }
});
</script> 