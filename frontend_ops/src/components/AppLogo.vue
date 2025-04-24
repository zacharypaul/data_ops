<template>
  <div class="logo-container">
    <div class="logo-diagonal">
      <div class="logo-block gold"></div>
      <div class="logo-block primary"></div>
      <div class="logo-block secondary"></div>
      <div class="logo-block accent"></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  expanded: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.logo-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.logo-diagonal {
  position: relative;
  width: 60px;
  height: 40px;
}

.logo-block {
  position: absolute;
  width: 20px;
  height: 16px;
  transform: skew(-25deg);
}

.logo-block.gold {
  background-color: #F5C94C;
  top: 20px;
  left: 0px;
}

.logo-block.primary {
  background-color: #6A38EB;
  top: 0px;
  left: 8px;
}

.logo-block.secondary {
  background-color: #55A0E8;
  top: 20px;
  left: 28px;
}

.logo-block.accent {
  background-color: #50E3C2;
  top: 0px;
  left: 36px;
}
</style> 