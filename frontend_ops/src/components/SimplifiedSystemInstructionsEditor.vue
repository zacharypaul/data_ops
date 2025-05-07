<template>
  <div class="space-y-4">
    <div class="flex justify-between items-center">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-md bg-indigo-900/50 flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h8a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3 1h6v4H5V6zm6 6H5v2h6v-2z" clip-rule="evenodd" />
            <path d="M15 7h1a2 2 0 012 2v5.5a1.5 1.5 0 01-3 0V7z" />
          </svg>
        </div>
        <h4 class="font-medium">System Instructions</h4>
      </div>
      
      <div class="flex space-x-2">
        <button @click="toggleDiffView" class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path d="M5 4a1 1 0 00-2 0v7.268a2 2 0 000 3.464V16a1 1 0 102 0v-1.268a2 2 0 000-3.464V4zM11 4a1 1 0 10-2 0v1.268a2 2 0 000 3.464V16a1 1 0 102 0V8.732a2 2 0 000-3.464V4zM16 3a1 1 0 011 1v7.268a2 2 0 010 3.464V16a1 1 0 11-2 0v-1.268a2 2 0 010-3.464V4a1 1 0 011-1z" />
          </svg>
          {{ showDiffView ? 'Hide Diff' : 'Show Diff' }}
        </button>
        
        <button 
          v-if="hasSuggestedChanges" 
          @click="applyChanges" 
          class="text-xs py-1 px-2 bg-indigo-900/30 text-indigo-400 rounded hover:bg-indigo-900/50 transition flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
          </svg>
          Apply Suggestions
        </button>
      </div>
    </div>
    
    <div v-if="showDiffView && hasSuggestedChanges" class="bg-dark-700 rounded-lg p-4 border border-indigo-500/30">
      <div class="text-sm font-medium mb-3 text-indigo-400">Suggested Changes</div>
      
      <div class="space-y-3">
        <!-- Additions Section (GitHub-style) -->
        <div v-if="suggestedChanges.additions && suggestedChanges.additions.length > 0" class="border border-dark-600 rounded-md overflow-hidden">
          <div class="text-xs font-medium bg-dark-800 px-3 py-2 border-b border-dark-600 flex justify-between items-center">
            <span>Add specific instructions for mobile app troubleshooting</span>
            <div class="flex items-center space-x-2">
              <button class="text-xs py-0.5 px-1.5 bg-dark-700 text-dark-300 rounded hover:bg-dark-600">View</button>
              <button @click="applyAddition(0)" class="text-xs py-0.5 px-1.5 bg-green-900/30 text-green-400 rounded hover:bg-green-900/50">Apply</button>
            </div>
          </div>
          
          <div class="text-sm font-mono">
            <div class="bg-dark-900/50 px-3 py-1 border-b border-dark-600 text-dark-400">
              <span class="select-none mr-1">@@ -16,6 +16,12 @@</span> Guidelines
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">16</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"> - Provide step-by-step troubleshooting when applicable</div>
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">17</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">- For mobile app issues, check these steps first:</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">  1. Verify app is updated to latest version</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">  2. Check device storage space</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">  3. Restart the app and device</span></div>
            </div>
          </div>
        </div>

        <!-- Permissions Addition (GitHub-style) -->
        <div v-if="suggestedChanges.additions && suggestedChanges.additions.length > 1" class="border border-dark-600 rounded-md overflow-hidden">
          <div class="text-xs font-medium bg-dark-800 px-3 py-2 border-b border-dark-600 flex justify-between items-center">
            <span>Include permission check steps for different OS versions</span>
            <div class="flex items-center space-x-2">
              <button class="text-xs py-0.5 px-1.5 bg-dark-700 text-dark-300 rounded hover:bg-dark-600">View</button>
              <button @click="applyAddition(1)" class="text-xs py-0.5 px-1.5 bg-green-900/30 text-green-400 rounded hover:bg-green-900/50">Apply</button>
            </div>
          </div>
          
          <div class="text-sm font-mono">
            <div class="bg-dark-900/50 px-3 py-1 border-b border-dark-600 text-dark-400">
              <span class="select-none mr-1">@@ -25,6 +25,14 @@</span> Products
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">25</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"> - DeviceHub (hardware)</div>
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">26</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400"># Permission Checks:</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">- Android: Settings > Apps > CloudSync > Permissions</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">- iOS: Settings > Privacy > CloudSync</span></div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> <span class="text-green-400">- Windows: System Tray > CloudSync > Settings > Permissions</span></div>
            </div>
          </div>
        </div>
        
        <!-- Modifications (GitHub-style) -->
        <div v-if="suggestedChanges.modifications && suggestedChanges.modifications.length > 0" class="border border-dark-600 rounded-md overflow-hidden">
          <div class="text-xs font-medium bg-dark-800 px-3 py-2 border-b border-dark-600 flex justify-between items-center">
            <span>Clarify weekend support policy to mention response time expectations</span>
            <div class="flex items-center space-x-2">
              <button class="text-xs py-0.5 px-1.5 bg-dark-700 text-dark-300 rounded hover:bg-dark-600">View</button>
              <button @click="applyModification(0)" class="text-xs py-0.5 px-1.5 bg-yellow-900/30 text-yellow-400 rounded hover:bg-yellow-900/50">Apply</button>
            </div>
          </div>
          
          <div class="text-sm font-mono">
            <div class="bg-dark-900/50 px-3 py-1 border-b border-dark-600 text-dark-400">
              <span class="select-none mr-1">@@ -28,5 +28,5 @@</span> Support hours
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">28</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"> # Support hours:</div>
            </div>
            <div class="flex">
              <div class="text-xs text-dark-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">29</div>
              <div class="px-3 py-1 text-dark-300 w-full bg-dark-800/30"> - Monday to Friday: 9am to 6pm EST</div>
            </div>
            <div class="flex bg-red-900/20">
              <div class="text-xs text-red-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">-</div>
              <div class="px-3 py-1 text-red-400 w-full bg-dark-800/30"> - Weekend: Limited support for emergency issues only</div>
            </div>
            <div class="flex bg-green-900/20">
              <div class="text-xs text-green-500 select-none px-2 py-1 text-right w-10 border-r border-dark-700 bg-dark-800/50">+</div>
              <div class="px-3 py-1 text-green-400 w-full bg-dark-800/30"> - Weekend: Limited support for emergency issues only (response within 4-6 hours)</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="relative">
      <textarea 
        v-model="localInstructions"
        class="w-full h-80 bg-dark-700 border border-dark-600 rounded-lg p-4 font-mono text-sm focus:outline-none focus:border-indigo-500"
        placeholder="Enter system instructions here..."
        @input="updateInstructions"
      ></textarea>
      
      <div class="absolute top-2 right-2 flex space-x-1">
        <button class="p-1 bg-dark-800/80 text-dark-400 hover:text-dark-200 rounded">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
          </svg>
        </button>
        <button class="p-1 bg-dark-800/80 text-dark-400 hover:text-dark-200 rounded">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
        </button>
        <button class="p-1 bg-dark-800/80 text-dark-400 hover:text-dark-200 rounded">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  instructions: {
    type: String,
    required: true
  },
  suggestedChanges: {
    type: Object,
    default: () => ({ additions: [], removals: [], modifications: [] })
  }
});

const emit = defineEmits(['update', 'apply-changes', 'select-content']);

// Local state
const localInstructions = ref(props.instructions);
const showDiffView = ref(false);

// Computed properties
const hasSuggestedChanges = computed(() => {
  const { additions = [], removals = [], modifications = [] } = props.suggestedChanges;
  return additions.length > 0 || removals.length > 0 || modifications.length > 0;
});

// Methods
const updateInstructions = () => {
  emit('update', localInstructions.value);
};

const toggleDiffView = () => {
  showDiffView.value = !showDiffView.value;
};

const applyChanges = () => {
  emit('apply-changes');
};

const applyAddition = (index) => {
  // This would normally apply just this specific addition
  console.log(`Applying addition at index ${index}`);
  emit('apply-changes');
};

const applyModification = (index) => {
  // This would normally apply just this specific modification
  console.log(`Applying modification at index ${index}`);
  emit('apply-changes');
};

// Watch for parent props changes
watch(() => props.instructions, (newValue) => {
  localInstructions.value = newValue;
});
</script>

<style scoped>
textarea {
  resize: none;
  line-height: 1.5;
}

/* Custom checkbox styling */
input[type="checkbox"] {
  appearance: none;
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 4px;
  background-color: rgba(30, 41, 59, 0.5);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

input[type="checkbox"]:checked {
  background-color: rgba(79, 70, 229, 0.8);
  border-color: rgba(79, 70, 229, 0.5);
}

input[type="checkbox"]:checked::after {
  content: '';
  width: 4px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  position: relative;
  top: -1px;
}
</style> 