<template>
  <div class="dropdown-wrapper relative">
    <button 
      @click.stop="isOpen = !isOpen"
      class="p-1.5 rounded-full transition-colors bg-dark-800/60 border border-dark-600 text-indigo-400 hover:bg-indigo-900/30"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-3.5 w-3.5">
        <path fill-rule="evenodd" d="M10 1a4.5 4.5 0 00-4.5 4.5V9H5a2 2 0 00-2 2v6a2 2 0 002 2h10a2 2 0 002-2v-6a2 2 0 00-2-2h-.5V5.5A4.5 4.5 0 0010 1zm3 8V5.5a3 3 0 10-6 0V9h6z" clip-rule="evenodd" />
      </svg>
    </button>
    
    <!-- Dropdown content -->
    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-1 w-72 bg-dark-800 border border-dark-600 rounded-md shadow-lg z-20"
      style="background-color: #1e293b;"
      @click.stop
    >
      <div class="p-3">
        <div class="flex justify-between items-center mb-3">
          <h4 class="text-sm font-medium">Sessions</h4>
          <button @click.stop="isOpen = false" class="text-dark-400 hover:text-dark-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <!-- Current session -->
        <div class="mb-4">
          <div class="text-xs text-dark-400 mb-1">Current Session</div>
          <div class="bg-dark-700 rounded-md p-3">
            <div class="flex items-center">
              <div class="w-10 h-10 rounded-full bg-indigo-900 flex items-center justify-center flex-shrink-0">
                <span class="text-indigo-300 text-sm">{{ currentSession.contact.charAt(0) }}</span>
              </div>
              <div class="ml-3 flex-grow">
                <div class="text-sm font-medium">{{ currentSession.contact }}</div>
                <div class="text-xs text-dark-400">{{ formatDate(currentSession.date) }}</div>
              </div>
              <div class="flex-shrink-0">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" 
                  :class="currentSession.type === 'call' ? 'bg-green-900/50 text-green-300' : 'bg-blue-900/50 text-blue-300'">
                  <span v-if="currentSession.type === 'call'" class="w-2 h-2 mr-1 rounded-full bg-green-500"></span>
                  <span v-else class="w-2 h-2 mr-1 rounded-full bg-blue-500"></span>
                  {{ currentSession.type === 'call' ? 'Call' : 'Text' }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Previous sessions -->
        <div>
          <div class="text-xs text-dark-400 mb-2">Previous Sessions</div>
          <div class="space-y-2 max-h-60 overflow-y-auto pr-1">
            <div 
              v-for="(session, index) in previousSessions" 
              :key="index"
              @click="selectSession(session.id)"
              class="flex items-center p-2 rounded-md cursor-pointer hover:bg-dark-700"
            >
              <div class="w-8 h-8 rounded-full bg-indigo-900 flex items-center justify-center flex-shrink-0">
                <span class="text-indigo-300 text-xs">{{ session.contact.charAt(0) }}</span>
              </div>
              <div class="ml-3 flex-grow">
                <div class="text-sm">{{ session.contact }}</div>
                <div class="text-xs text-dark-400">{{ formatDate(session.date) }}</div>
              </div>
              <div class="flex-shrink-0">
                <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium" 
                  :class="session.type === 'call' ? 'bg-green-900/50 text-green-300' : 'bg-blue-900/50 text-blue-300'">
                  <span v-if="session.type === 'call'" class="w-2 h-2 mr-1 rounded-full bg-green-500"></span>
                  <span v-else class="w-2 h-2 mr-1 rounded-full bg-blue-500"></span>
                  {{ session.type === 'call' ? 'Call' : 'Text' }}
                </span>
              </div>
            </div>
            
            <div v-if="previousSessions.length === 0" class="text-sm text-dark-400 text-center py-2">
              No previous sessions
            </div>
          </div>
        </div>
        
        <!-- Footer -->
        <div class="pt-3 mt-3 border-t border-dark-700">
          <button class="w-full text-left px-3 py-2 text-sm text-indigo-400 hover:bg-dark-700 rounded-md transition-colors">
            Create New Session
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isOpen = ref(false);

// Mock current session
const currentSession = ref({
  id: 'cs-001',
  contact: 'John Smith',
  date: new Date(),
  type: 'text'
});

// Mock previous sessions - replace with actual data source
const previousSessions = ref([
  { id: 'ps-001', contact: 'Jane Doe', date: new Date(Date.now() - 24 * 60 * 60 * 1000), type: 'call' },
  { id: 'ps-002', contact: 'Robert Johnson', date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), type: 'text' },
  { id: 'ps-003', contact: 'Emily Brown', date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), type: 'call' },
  { id: 'ps-004', contact: 'Michael Wilson', date: new Date(Date.now() - 14 * 24 * 60 * 60 * 1000), type: 'text' }
]);

const formatDate = (date) => {
  const today = new Date();
  const yesterday = new Date(today);
  yesterday.setDate(yesterday.getDate() - 1);
  
  if (date.toDateString() === today.toDateString()) {
    return 'Today, ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else if (date.toDateString() === yesterday.toDateString()) {
    return 'Yesterday, ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else {
    return date.toLocaleDateString([], { month: 'short', day: 'numeric' }) + ', ' + 
           date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }
};

const selectSession = (id) => {
  // Find the session
  const session = previousSessions.value.find(s => s.id === id);
  if (session) {
    // Emit an event to notify parent component
    emit('session-selected', session);
    isOpen.value = false;
  }
};

// Define emits
const emit = defineEmits(['session-selected']);

// Click outside to close dropdown
const clickOutside = (event) => {
  if (isOpen.value && !event.target.closest('.dropdown-wrapper')) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', clickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', clickOutside);
});
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
}
</style> 