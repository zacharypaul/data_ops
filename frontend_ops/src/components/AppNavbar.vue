<template>
  <header class="topbar">
    <div class="container mx-auto px-6 py-4">
      <nav class="flex items-center justify-between">
        <div class="flex-1"></div>

        <!-- The Desktop Navigation section is removed -->

        <div class="flex items-center space-x-8">
          <!-- Status Button -->
          <div class="relative">
            <button 
              @click="statusDropdownOpen = !statusDropdownOpen" 
              class="system-status-btn flex items-center px-3 py-1.5 rounded-md text-white font-medium shadow-lg hover:bg-green-700 transition-all"
            >
              <span class="mr-2">All Systems Operational</span>
              <span class="inline-block w-2 h-2 rounded-full bg-green-300 animate-pulse"></span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
            
            <!-- Status Dropdown -->
            <div 
              v-if="statusDropdownOpen" 
              class="status-dropdown absolute right-0 mt-2 w-64 border border-dark-700 rounded-md shadow-lg z-20"
              v-click-outside="closeStatusDropdown"
            >
              <div class="p-3 border-b border-dark-700 solid-bg">
                <h3 class="text-sm font-semibold text-white">System Status</h3>
                <p class="text-xs text-gray-400">Last updated: 5 minutes ago</p>
              </div>
              
              <div class="p-3 solid-bg">
                <ul class="space-y-2">
                  <li class="flex justify-between items-center">
                    <span class="text-sm text-gray-300">Data Pipelines</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium solid-status-pill bg-green-100 text-green-800">
                      <span class="w-1.5 h-1.5 mr-1 rounded-full bg-green-600"></span>
                      Operational
                    </span>
                  </li>
                  <li class="flex justify-between items-center">
                    <span class="text-sm text-gray-300">API Services</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium solid-status-pill bg-green-100 text-green-800">
                      <span class="w-1.5 h-1.5 mr-1 rounded-full bg-green-600"></span>
                      Operational
                    </span>
                  </li>
                  <li class="flex justify-between items-center">
                    <span class="text-sm text-gray-300">ML Services</span>
                    <span class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium solid-status-pill bg-green-100 text-green-800">
                      <span class="w-1.5 h-1.5 mr-1 rounded-full bg-green-600"></span>
                      Operational
                    </span>
                  </li>
                </ul>
              </div>
              
              <div class="p-3 border-t border-dark-700 solid-bg">
                <a href="#" class="text-xs text-primary-400 hover:text-primary-300 flex items-center justify-center">
                  View detailed status page
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 ml-1" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </a>
              </div>
            </div>
          </div>
          
          <!-- Login/Logout Button -->
          <div class="relative">
            <button 
              @click="authDropdownOpen = !authDropdownOpen" 
              class="text-gray-300 hover:text-white p-1.5 rounded-md hover:bg-dark-700 transition-colors"
              aria-label="Authentication"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
              </svg>
            </button>
            
            <!-- Auth Dropdown -->
            <div 
              v-if="authDropdownOpen" 
              class="absolute right-0 mt-2 w-56 bg-dark-800 border border-dark-700 rounded-md shadow-lg z-20"
              v-click-outside="closeAuthDropdown"
            >
              <div class="p-3 border-b border-dark-700">
                <h3 class="text-sm font-semibold text-white">AWS Cognito</h3>
                <p class="text-xs text-gray-400">Manage your authentication</p>
              </div>
              
              <div class="py-1">
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  Sign In
                </a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  Sign Out
                </a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  Manage Account
                </a>
              </div>
            </div>
          </div>
          
          <!-- User Profile -->
          <div class="relative">
            <button 
              @click="profileDropdownOpen = !profileDropdownOpen" 
              class="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium border-2 border-dark-700 hover:border-primary-500 transition-all focus:outline-none focus:ring-2 focus:ring-primary-500"
              aria-label="User profile"
            >
              ZP
            </button>
            
            <!-- Profile Dropdown -->
            <div 
              v-if="profileDropdownOpen" 
              class="absolute right-0 mt-2 w-64 bg-dark-800 border border-dark-700 rounded-md shadow-lg z-20"
              v-click-outside="closeProfileDropdown"
            >
              <div class="p-4 border-b border-dark-700">
                <div class="flex items-center">
                  <div class="w-12 h-12 rounded-full bg-primary-600 flex items-center justify-center text-white font-medium mr-3">ZP</div>
                  <div>
                    <div class="text-sm font-medium text-white">Zach Paul</div>
                    <div class="text-xs text-gray-400">zach.paul@example.com</div>
                    <div class="text-xs text-green-400 mt-1">Admin</div>
                  </div>
                </div>
              </div>
              
              <div class="py-1">
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  Your Profile
                </a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  Account Settings
                </a>
                <a href="#" class="block px-4 py-2 text-sm text-gray-300 hover:bg-dark-700 hover:text-white">
                  API Access
                </a>
              </div>
              
              <div class="py-1 border-t border-dark-700">
                <a href="#" class="block px-4 py-2 text-sm text-red-400 hover:bg-dark-700 hover:text-red-300">
                  Sign Out
                </a>
              </div>
            </div>
          </div>
          
          <!-- Mobile menu button -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden text-dark-300 hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path v-if="mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </nav>
    </div>

    <!-- Mobile Navigation is removed -->
  </header>
</template>

<script setup>
import { ref } from 'vue';

const mobileMenuOpen = ref(false);
const statusDropdownOpen = ref(false);
const authDropdownOpen = ref(false);
const profileDropdownOpen = ref(false);

const closeStatusDropdown = () => {
  statusDropdownOpen.value = false;
};

const closeAuthDropdown = () => {
  authDropdownOpen.value = false;
};

const closeProfileDropdown = () => {
  profileDropdownOpen.value = false;
};
</script>

<style scoped>
/* Styles for the navbar */
.topbar {
  background-color: var(--topbar-bg);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.system-status-btn {
  background-color: #16a34a !important; /* Solid green-600 color */
  opacity: 1 !important;
}

.status-dropdown {
  background-color: #111827 !important; /* Dark-800 solid color */
  opacity: 1 !important;
  backdrop-filter: none !important;
}

.status-dropdown * {
  opacity: 1 !important;
}

.status-dropdown .bg-dark-900\/40 {
  background-color: #0f172a !important; /* Dark-900 solid color */
  opacity: 1 !important;
}

/* Ensure footer section is also solid */
.status-dropdown div[class*="border-t"] {
  background-color: #0f172a !important;
  opacity: 1 !important;
}

.solid-bg {
  background-color: #111827 !important; 
  opacity: 1 !important;
  backdrop-filter: none !important;
}

.solid-status-pill {
  background-color: #d1fae5 !important; /* Solid green-100 */
  opacity: 1 !important;
}

/* Fix for all status indicators in dropdown */
.status-dropdown .rounded-full {
  opacity: 1 !important;
}

.bg-green-600 {
  background-color: #16a34a !important;
  opacity: 1 !important;
}
</style> 