<template>
  <div class="dropdown-wrapper relative">
    <button 
      @click.stop="isOpen = !isOpen"
      class="p-1.5 rounded-full transition-colors bg-dark-800/60 border border-dark-600 text-indigo-400 hover:bg-indigo-900/30"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-3.5 w-3.5">
        <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
      </svg>
    </button>
    
    <!-- Dropdown content -->
    <div 
      v-if="isOpen" 
      class="absolute right-0 mt-1 w-64 bg-dark-800 border border-dark-600 rounded-md shadow-lg z-20"
      style="background-color: #1e293b;"
      @click.stop
    >
      <div class="p-3">
        <div class="flex justify-between items-center mb-3">
          <h4 class="text-sm font-medium">Contacts</h4>
          <button @click.stop="isOpen = false" class="text-dark-400 hover:text-dark-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <!-- Current contact info if any -->
        <div v-if="currentContact" class="mb-4 p-3 bg-dark-700 rounded-md">
          <div class="text-sm font-medium mb-1">Current Contact</div>
          <div class="flex items-center">
            <div class="w-8 h-8 rounded-full bg-indigo-900 flex items-center justify-center flex-shrink-0">
              <span class="text-indigo-300 text-xs">{{ currentContact.name.charAt(0) }}</span>
            </div>
            <div class="ml-2">
              <div class="text-sm font-medium">{{ currentContact.name }}</div>
              <div class="text-xs text-dark-400">{{ currentContact.type }}</div>
            </div>
          </div>
        </div>
        
        <!-- Contact filters -->
        <div class="space-y-1">
          <div class="text-xs text-dark-400 mb-1 px-1">Select Contact</div>
          
          <!-- All contacts option -->
          <button 
            @click="selectContact('all')"
            class="w-full text-left px-3 py-2 text-sm rounded-md hover:bg-dark-700 flex items-center" 
            :class="{'bg-indigo-900/30 text-indigo-300': selectedContactFilter === 'all'}"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
            </svg>
            All contacts
          </button>
          
          <button 
            v-for="contact in contacts" 
            :key="contact.id"
            @click="selectContact(contact.id)"
            class="w-full text-left px-3 py-2 text-sm rounded-md hover:bg-dark-700 flex items-center"
            :class="{'bg-indigo-900/30 text-indigo-300': selectedContactFilter === contact.id}"
          >
            <div class="w-6 h-6 rounded-full bg-indigo-900/50 flex items-center justify-center mr-2 flex-shrink-0">
              <span class="text-indigo-300 text-xs">{{ contact.name.charAt(0) }}</span>
            </div>
            <div>
              <div class="font-medium">{{ contact.name }}</div>
              <div class="text-xs text-dark-400">{{ contact.type }}</div>
            </div>
          </button>
        </div>
        
        <!-- Footer - Add new contact -->
        <div class="pt-3 mt-3 border-t border-dark-700">
          <button 
            @click="createNewContact" 
            class="w-full text-left px-3 py-2 text-sm text-indigo-400 hover:bg-dark-700 rounded-md transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Add new contact
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isOpen = ref(false);
const selectedContactFilter = ref('all');

// Mock current contact - replace with actual data
const currentContact = ref({
  id: '1',
  name: 'Jane Smith',
  type: 'Customer'
});

// Mock contacts data - replace with actual data
const contacts = ref([
  { id: '1', name: 'Jane Smith', type: 'Customer' },
  { id: '2', name: 'Mark Johnson', type: 'Supplier' },
  { id: '3', name: 'Alice Wong', type: 'Partner' },
  { id: '4', name: 'David Brown', type: 'Customer' }
]);

const selectContact = (contactId) => {
  selectedContactFilter.value = contactId;
  emit('contact-selected', contactId);
  isOpen.value = false;
};

const createNewContact = () => {
  emit('create-contact');
  isOpen.value = false;
};

// Define emits
const emit = defineEmits(['contact-selected', 'create-contact']);

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