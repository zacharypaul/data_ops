<template>
  <div class="app min-h-screen bg-app-bg text-white flex flex-col">
    <AppSidebar v-model:sidebarExpanded="sidebarExpanded" />
    
    <div class="flex flex-col min-h-screen" :class="sidebarExpanded ? 'ml-64' : 'ml-16'">
      <AppNavbar class="z-10" />
      
      <main class="flex-1 transition-all duration-300 px-8 py-6">
        <router-view />
      </main>
      
      <footer class="p-4 text-center text-dark-400 text-sm border-t border-dark-700">
        &copy; 2025 Operations Dashboard
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import AppSidebar from './components/AppSidebar.vue';
import AppNavbar from './components/AppNavbar.vue';

const sidebarExpanded = ref(true);
</script>

<style>
:root {
  /* Base Colors */
  --color-primary-50: 239, 246, 255;  /* Lightest blue */
  --color-primary-100: 219, 234, 254;
  --color-primary-200: 191, 219, 254;
  --color-primary-300: 147, 197, 253;
  --color-primary-400: 96, 165, 250;
  --color-primary-500: 59, 130, 246;
  --color-primary-600: 37, 99, 235;
  --color-primary-700: 29, 78, 216;
  --color-primary-800: 30, 64, 175;
  --color-primary-900: 30, 58, 138;  /* Darkest blue */
  
  --color-secondary-500: 99, 102, 241;  /* Indigo */
  --color-accent-500: 236, 72, 153;     /* Pink */
  
  --color-dark-50: 249, 250, 251;
  --color-dark-100: 243, 244, 246;
  --color-dark-200: 229, 231, 235;
  --color-dark-300: 209, 213, 219;
  --color-dark-400: 156, 163, 175;
  --color-dark-500: 107, 114, 128;
  --color-dark-600: 75, 85, 99;
  --color-dark-700: 55, 65, 81;
  --color-dark-800: 31, 41, 55;
  --color-dark-900: 17, 24, 39;
  
  /* UI Colors */
  --color-app-bg: 13, 17, 23;           /* Dark charcoal background */
  --color-sidebar-bg: 22, 27, 34;       /* Slightly lighter for sidebar */
  --color-topbar-bg: 36, 41, 51;        /* Even lighter for top navbar */
  
  --color-success: 34, 197, 94;
  --color-warning: 234, 179, 8;
  --color-danger: 239, 68, 68;
  --color-info: 6, 182, 212;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: rgb(var(--color-app-bg));
  color: rgb(var(--color-dark-300));
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgb(var(--color-dark-800));
}

::-webkit-scrollbar-thumb {
  background: rgb(var(--color-dark-600));
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgb(var(--color-dark-500));
}
</style> 