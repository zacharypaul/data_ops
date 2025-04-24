<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-dark-900 bg-opacity-80 backdrop-blur-sm transition-opacity" aria-hidden="true" @click="closeModal"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

      <div class="inline-block align-bottom bg-gradient-to-br from-dark-800 to-dark-900 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-5xl sm:w-full border border-dark-700">
        <div class="absolute top-0 right-0 pt-4 pr-4">
          <button type="button" class="text-dark-400 hover:text-white focus:outline-none" @click="closeModal">
            <span class="sr-only">Close</span>
            <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <div class="flex items-center mb-6">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mr-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-white">Create New AI Application</h3>
          </div>
          
          <!-- Tabs -->
          <div class="border-b border-dark-700 mb-6">
            <div class="flex -mb-px">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                :class="[
                  'py-3 px-6 font-medium border-b-2 focus:outline-none',
                  activeTab === tab.id 
                    ? 'border-primary-500 text-primary-400' 
                    : 'border-transparent text-dark-400 hover:text-dark-200 hover:border-dark-600'
                ]"
              >
                {{ tab.name }}
              </button>
            </div>
          </div>
          
          <!-- Tab content -->
          <div v-if="activeTab === 'template'" class="mb-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div 
                v-for="template in templates" 
                :key="template.id" 
                class="border border-dark-700 rounded-lg p-4 hover:border-primary-500 cursor-pointer transition-all duration-200 hover:scale-[1.02] hover:shadow-lg"
                :class="{ 'border-primary-500 bg-dark-800': selectedTemplate === template.id }"
                @click="selectedTemplate = template.id"
              >
                <div class="flex items-center mb-3">
                  <div class="w-8 h-8 rounded-md bg-dark-700 flex items-center justify-center mr-3">
                    <span class="text-primary-400" v-html="template.icon"></span>
                  </div>
                  <h4 class="font-medium">{{ template.name }}</h4>
                </div>
                <p class="text-dark-400 text-sm">{{ template.description }}</p>
              </div>
            </div>
          </div>
          
          <div v-else-if="activeTab === 'custom'" class="mb-6">
            <!-- AI Data Flow Builder tool embedded here -->
            <AIDataFlowTool />
          </div>
          
          <div v-else-if="activeTab === 'import'" class="mb-6">
            <div class="border-2 border-dashed border-dark-700 rounded-lg p-8 text-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="mx-auto h-12 w-12 text-dark-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="mt-2 text-sm text-dark-400">
                <span class="font-medium text-primary-400">Click to upload</span> or drag and drop
              </p>
              <p class="text-xs text-dark-500">YAML, JSON or ZIP up to 10MB</p>
            </div>
          </div>
          
          <!-- Actions -->
          <div class="flex justify-end space-x-3">
            <button class="btn-outline py-2 px-4" @click="closeModal">Cancel</button>
            <button 
              class="btn-primary py-2 px-6 flex items-center" 
              :disabled="(activeTab === 'template' && !selectedTemplate)"
            >
              Create
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-2" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import AIDataFlowTool from './AIDataFlowTool.vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close']);

const activeTab = ref('custom');
const selectedTemplate = ref(null);

const tabs = [
  { id: 'template', name: 'Templates' },
  { id: 'custom', name: 'Custom Builder' },
  { id: 'import', name: 'Import' }
];

const templates = [
  { 
    id: 'chatbot', 
    name: 'Customer Support Bot', 
    description: 'AI chatbot for handling customer inquiries with built-in ticket creation.',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" /><path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" /></svg>'
  },
  { 
    id: 'recommender', 
    name: 'Product Recommender', 
    description: 'ML-powered product recommendation system for e-commerce platforms.',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" /></svg>'
  },
  { 
    id: 'document', 
    name: 'Document Analyzer', 
    description: 'AI-powered document analysis for extracting insights and key data points.',
    icon: '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clip-rule="evenodd" /></svg>'
  }
];

const closeModal = () => {
  emit('close');
};
</script>

<style scoped>
.btn-primary {
  background: linear-gradient(135deg, #38bdf8, #818cf8);
  color: white;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.3s;
  border: none;
}

.btn-primary:hover {
  box-shadow: 0 0 15px rgba(56, 189, 248, 0.4);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-outline {
  background: transparent;
  color: #d1d5db;
  border: 1px solid rgba(156, 163, 175, 0.3);
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-outline:hover {
  border-color: rgba(156, 163, 175, 0.5);
  background: rgba(255, 255, 255, 0.05);
}
</style> 