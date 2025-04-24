<template>
  <div class="w-full">
    <h1 class="text-3xl font-bold mb-6">Generative AI Operations</h1>
    <p class="text-lg mb-8">Monitor and manage your generative AI applications and LLM-powered services.</p>
    
    <div class="mb-8">
      <div class="flex justify-between items-center">
        <h2 class="text-2xl font-bold">Deployed GenAI Applications</h2>
        <button class="btn-primary py-2 px-4 rounded font-medium" @click="openNewAppModal">New Application</button>
      </div>
    </div>
    
    <!-- Deployed Applications Cards -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Customer Support AI -->
      <div class="glass-card p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Customer Support AI</h3>
          <span class="px-3 py-1 bg-green-900/50 text-green-400 rounded-full text-sm">Production</span>
        </div>
        <p class="text-gray-300 mb-4">AI assistant for customer support inquiries and ticket routing</p>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div class="text-gray-400 text-sm mb-1">Average Response Time</div>
            <div class="text-xl font-semibold">240ms</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Requests (24h)</div>
            <div class="text-xl font-semibold">23,412</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Base Model</div>
            <div class="text-xl font-semibold">GPT-4</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Last Updated</div>
            <div class="text-xl font-semibold">2 days ago</div>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button class="btn-outline py-1 px-3 text-sm">Monitor</button>
          <button class="btn-outline py-1 px-3 text-sm">Logs</button>
          <button class="btn-outline py-1 px-3 text-sm">Settings</button>
        </div>
      </div>
      
      <!-- Content Generator -->
      <div class="glass-card p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Content Generator</h3>
          <span class="px-3 py-1 bg-purple-900/50 text-purple-400 rounded-full text-sm">Staging</span>
        </div>
        <p class="text-gray-300 mb-4">Creates marketing content based on product specifications</p>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div class="text-gray-400 text-sm mb-1">Average Response Time</div>
            <div class="text-xl font-semibold">320ms</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Requests (24h)</div>
            <div class="text-xl font-semibold">5,123</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Base Model</div>
            <div class="text-xl font-semibold">GPT-3.5</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Last Updated</div>
            <div class="text-xl font-semibold">1 week ago</div>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button class="btn-outline py-1 px-3 text-sm">Monitor</button>
          <button class="btn-outline py-1 px-3 text-sm">Logs</button>
          <button class="btn-outline py-1 px-3 text-sm">Settings</button>
        </div>
      </div>
      
      <!-- Document Analyzer -->
      <div class="glass-card p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Document Analyzer</h3>
          <span class="px-3 py-1 bg-blue-900/50 text-blue-400 rounded-full text-sm">Development</span>
        </div>
        <p class="text-gray-300 mb-4">Extracts insights and summaries from financial documents</p>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div class="text-gray-400 text-sm mb-1">Average Response Time</div>
            <div class="text-xl font-semibold">450ms</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Requests (24h)</div>
            <div class="text-xl font-semibold">1,240</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Base Model</div>
            <div class="text-xl font-semibold">Llama 2</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Last Updated</div>
            <div class="text-xl font-semibold">3 days ago</div>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button class="btn-outline py-1 px-3 text-sm">Monitor</button>
          <button class="btn-outline py-1 px-3 text-sm">Logs</button>
          <button class="btn-outline py-1 px-3 text-sm">Settings</button>
        </div>
      </div>
      
      <!-- Image Generation API -->
      <div class="glass-card p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Image Generation API</h3>
          <span class="px-3 py-1 bg-green-900/50 text-green-400 rounded-full text-sm">Production</span>
        </div>
        <p class="text-gray-300 mb-4">Creates product images from text descriptions</p>
        
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div>
            <div class="text-gray-400 text-sm mb-1">Average Response Time</div>
            <div class="text-xl font-semibold">980ms</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Requests (24h)</div>
            <div class="text-xl font-semibold">8,721</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Base Model</div>
            <div class="text-xl font-semibold">DALL-E 3</div>
          </div>
          <div>
            <div class="text-gray-400 text-sm mb-1">Last Updated</div>
            <div class="text-xl font-semibold">5 days ago</div>
          </div>
        </div>
        
        <div class="flex space-x-2">
          <button class="btn-outline py-1 px-3 text-sm">Monitor</button>
          <button class="btn-outline py-1 px-3 text-sm">Logs</button>
          <button class="btn-outline py-1 px-3 text-sm">Settings</button>
        </div>
      </div>
    </div>
  </div>
  
  <!-- New Application Modal -->
  <NewApplicationModal :show="showNewAppModal" @close="closeNewAppModal" />
</template>

<script setup>
import { ref } from 'vue';
import NewApplicationModal from '../components/NewApplicationModal.vue';

// Modal state
const showNewAppModal = ref(false);

// Modal methods
const openNewAppModal = () => {
  showNewAppModal.value = true;
};

const closeNewAppModal = () => {
  showNewAppModal.value = false;
};

// Component setup
</script>

<style scoped>
.glass-card {
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.btn-primary {
  background-color: rgb(var(--color-primary-600));
  color: white;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: rgb(var(--color-primary-700));
}

.btn-outline {
  border: 1px solid rgb(var(--color-dark-600));
  color: rgb(var(--color-dark-300));
  transition: all 0.2s;
  border-radius: 0.25rem;
}

.btn-outline:hover {
  border-color: rgb(var(--color-dark-500));
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
}
</style> 