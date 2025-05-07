<template>
  <div class="dropdown-wrapper relative">
    <button 
      @click.stop="isOpen = !isOpen"
      class="p-1.5 rounded-full transition-colors bg-dark-800/60 border border-dark-600 text-indigo-400 hover:bg-indigo-900/30"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="h-3.5 w-3.5">
        <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
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
          <h4 class="text-sm font-medium">Customer Accounts</h4>
          <button @click.stop="isOpen = false" class="text-dark-400 hover:text-dark-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <!-- Active customer -->
        <div class="flex items-center mb-4 p-3 bg-dark-700 rounded-md">
          <div class="w-10 h-10 rounded-full bg-blue-900 flex items-center justify-center flex-shrink-0">
            <span class="text-blue-300 text-sm">{{ activeCustomer.initial }}</span>
          </div>
          <div class="ml-3">
            <div class="text-sm font-medium">{{ activeCustomer.name }}</div>
            <div class="text-xs text-dark-400">{{ activeCustomer.email }}</div>
          </div>
        </div>
        
        <!-- Customer list -->
        <div class="space-y-1 max-h-60 overflow-y-auto">
          <button 
            v-for="customer in customers" 
            :key="customer.id"
            @click="selectCustomer(customer.id)"
            class="w-full text-left px-3 py-2 text-sm rounded-md hover:bg-dark-700 flex items-center"
            :class="{'bg-indigo-900/30 border border-indigo-800': customer.id === activeCustomer.id}"
          >
            <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 mr-2"
              :class="getCustomerBgColor(customer.tier)">
              <span class="text-sm">{{ customer.initial }}</span>
            </div>
            <div>
              <div>{{ customer.name }}</div>
              <div class="text-xs text-dark-400">{{ customer.tier }} tier</div>
            </div>
          </button>
        </div>
        
        <!-- Footer - New customer -->
        <div class="pt-3 mt-3 border-t border-dark-700">
          <button 
            @click="addNewCustomer" 
            class="w-full text-left px-3 py-2 text-sm text-primary-400 hover:bg-dark-700 rounded-md transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
            </svg>
            Add New Customer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const isOpen = ref(false);

// Mock customer data - business accounts
const customers = [
  {
    id: 1,
    name: 'Acme Corp',
    email: 'accounts@acmecorp.com',
    tier: 'Premium',
    initial: 'A'
  },
  {
    id: 2,
    name: 'Stellar Dynamics',
    email: 'info@stellardynamics.com',
    tier: 'Standard',
    initial: 'S'
  },
  {
    id: 3,
    name: 'Momentum Tech',
    email: 'support@momentumtech.com',
    tier: 'Enterprise',
    initial: 'M'
  },
  {
    id: 4,
    name: 'Orbit Solutions',
    email: 'contact@orbitsolutions.com',
    tier: 'Premium',
    initial: 'O'
  },
  {
    id: 5,
    name: 'Radiant Systems',
    email: 'help@radiantsystems.com',
    tier: 'Standard',
    initial: 'R'
  }
];

const activeCustomer = ref(customers[4]); // Radiant Systems is active by default

const getCustomerBgColor = (tier) => {
  switch(tier) {
    case 'Premium':
      return 'bg-amber-900 text-amber-300';
    case 'Enterprise':
      return 'bg-indigo-900 text-indigo-300';
    case 'Standard':
    default:
      return 'bg-blue-900 text-blue-300';
  }
};

const selectCustomer = (id) => {
  const customer = customers.find(c => c.id === id);
  if (customer) {
    activeCustomer.value = customer;
    emit('customer-selected', customer);
    isOpen.value = false;
  }
};

const addNewCustomer = () => {
  emit('add-customer');
  isOpen.value = false;
};

// Define emits
const emit = defineEmits(['customer-selected', 'add-customer']);

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