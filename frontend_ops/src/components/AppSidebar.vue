<!-- AppSidebar.vue -->
<template>
  <aside
    class="fixed top-0 left-0 h-full transition-all duration-300 flex flex-col z-20"
    :class="[
      sidebarExpanded ? 'w-64' : 'w-16',
      'bg-sidebar'
    ]"
  >
    <!-- Logo section (fixed size regardless of sidebar state) -->
    <div class="h-16 relative border-b border-dark-700">
      <!-- Logo container - positioned absolutely -->
      <div class="absolute top-4 left-4 flex items-center">
        <img src="../assets/hyimg.jpeg" class="h-8 w-8 rounded-md shadow-lg" alt="Logo" />
        <span v-if="sidebarExpanded" class="ml-3 font-semibold text-lg gradient-text">Data Operations</span>
      </div>
      
      <!-- Toggle button -->
      <button 
        v-if="sidebarExpanded" 
        class="absolute top-5 right-3 text-dark-400 hover:text-white" 
        @click="toggleSidebar"
      >
        <!-- Chevron Left Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button 
        v-else
        class="absolute top-5 right-3 text-dark-400 hover:text-white" 
        @click="toggleSidebar"
      >
        <!-- Chevron Right Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <!-- Navigation Links -->
    <nav class="flex-1 py-4 overflow-y-auto">
      <div v-if="!sidebarExpanded" class="flex justify-center">
        <NavCircles />
      </div>
      <ul v-else class="space-y-1 px-2">
        <li v-for="item in navItems" :key="item.path">
          <router-link 
            :to="item.path"
            class="flex items-center px-2 py-2 rounded-md transition-colors duration-200"
            :class="[
              $route.path === item.path ? 
                'bg-teal-600 text-white' : 
                'text-dark-300 hover:bg-dark-700 hover:text-white'
            ]"
          >
            <span class="h-5 w-5 flex-shrink-0" v-html="item.icon"></span>
            <span class="ml-3">{{ item.name }}</span>
          </router-link>
        </li>
      </ul>
    </nav>

    <!-- Settings Section -->
    <div class="p-2 border-t border-dark-700">
      <div class="relative">
        <button 
          @click="settingsDropdownOpen = !settingsDropdownOpen" 
          class="w-full flex items-center px-2 py-2 rounded-md transition-colors duration-200 text-dark-300 hover:bg-dark-700 hover:text-white"
        >
          <!-- Settings/Cog Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span v-if="sidebarExpanded" class="ml-3">Settings</span>
          <svg v-if="sidebarExpanded && settingsDropdownOpen" xmlns="http://www.w3.org/2000/svg" class="ml-auto h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
          </svg>
          <svg v-if="sidebarExpanded && !settingsDropdownOpen" xmlns="http://www.w3.org/2000/svg" class="ml-auto h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Settings Dropdown Menu -->
        <div 
          v-if="sidebarExpanded && settingsDropdownOpen" 
          class="mt-1 py-1 bg-dark-800 rounded-md shadow-lg"
        >
          <a href="#" class="block px-4 py-2 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
            Account Settings
          </a>
          <a href="#" class="block px-4 py-2 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
            API Keys
          </a>
          <a href="#" class="block px-4 py-2 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
            Preferences
          </a>
          <a href="#" class="block px-4 py-2 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
            Notifications
          </a>
          
          <!-- Team Members Section -->
          <div class="border-t border-dark-700 mt-1 pt-1">
            <div class="px-4 py-1 text-xs font-medium text-dark-400">Team Members</div>
            
            <!-- Internal Employees -->
            <div class="px-4 py-1 mt-1">
              <div class="text-xs font-medium text-dark-500">Internal</div>
              <div class="ml-2">
                <a href="#" class="block px-2 py-1 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
                  Sarah Johnson
                </a>
                <a href="#" class="block px-2 py-1 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
                  Michael Chen
                </a>
                <a href="#" class="block px-2 py-1 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
                  Alex Rodriguez
                </a>
              </div>
            </div>
            
            <!-- Contractors -->
            <div class="px-4 py-1 mt-1">
              <div class="text-xs font-medium text-dark-500">Contractors</div>
              <div class="ml-2">
                <a href="#" class="block px-2 py-1 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
                  Priya Patel
                </a>
                <a href="#" class="block px-2 py-1 text-sm text-dark-300 hover:bg-dark-700 hover:text-white">
                  Robert Kim
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import NavCircles from './NavCircles.vue';

// Props
const props = defineProps({
  sidebarExpanded: {
    type: Boolean,
    default: true
  }
});

// Emits
const emit = defineEmits(['update:sidebarExpanded']);

// State
const route = useRoute();
const settingsDropdownOpen = ref(false);

// Navigation items with inline SVG icons
const navItems = [
  { 
    name: 'Dashboard', 
    path: '/', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>` 
  },
  { 
    name: 'Inventory', 
    path: '/inventory', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>` 
  },
  { 
    name: 'Observability', 
    path: '/observability', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>` 
  },
  { 
    name: 'ML Ops', 
    path: '/mlops', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
          </svg>` 
  },
  { 
    name: 'AI Ops', 
    path: '/aiops', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>` 
  },
  { 
    name: 'Platform Bracket', 
    path: '/bracket', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
          </svg>` 
  },
  { 
    name: 'Tech Stack Shift', 
    path: '/tech-stack-shift', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          </svg>` 
  },
  { 
    name: 'Costs', 
    path: '/costs', 
    icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>` 
  }
];

// Methods
const toggleSidebar = () => {
  emit('update:sidebarExpanded', !props.sidebarExpanded);
  if (!props.sidebarExpanded) {
    settingsDropdownOpen.value = false;
  }
};
</script>

<style scoped>
.bg-sidebar {
  background-color: rgb(10, 15, 35); /* Deep navy blue matching the main app background */
}

.router-link-active {
  background-color: rgb(13, 148, 136); /* Teal-600 color that matches the greenish color from the logo */
  color: white;
}

/* Animated gradient text */
.gradient-text {
  background: linear-gradient(90deg, 
    #f0b53f, /* yellow/gold */
    #4d7bf3, /* blue */
    #8b5cf6, /* purple */
    #06b6d4, /* cyan/teal */
    #f0b53f  /* repeat first color to make the transition smooth */
  );
  background-size: 200% 100%;
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  animation: gradient-shift 4s linear infinite;
  text-shadow: 
    0 0 10px rgba(255, 255, 255, 0.2),
    0 0 20px rgba(255, 255, 255, 0.1);
  position: relative;
  font-weight: bold;
  letter-spacing: 0.5px;
  overflow: hidden;
}

/* Replace the sparkle overlay with a cleaner pulse effect */
.gradient-text::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.4) 0%,
    transparent 70%
  );
  opacity: 0;
  animation: pulse 2s ease-in-out infinite;
  pointer-events: none;
}

@keyframes gradient-shift {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

@keyframes pulse {
  0% { opacity: 0; transform: scale(0.8); }
  50% { opacity: 0.3; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.2); }
}
</style> 