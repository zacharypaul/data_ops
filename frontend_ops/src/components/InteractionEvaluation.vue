<template>
  <div class="interaction-evaluation bg-gray-950 text-white p-5 rounded-xl border border-gray-800 shadow-lg max-w-6xl w-full mx-auto">
    <h2 class="text-2xl font-semibold mb-5">Interaction Evaluation</h2>
    
    <!-- Metrics Cards with Action Buttons -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6 w-full max-w-4xl mx-auto">
      <!-- Relevance Card -->
      <div class="metric-card group" :class="getMetricCardClass('relevance')">
        <!-- Score Display at Top -->
        <div class="flex flex-col items-center mb-3">
          <span class="font-medium text-base mb-1">Relevance</span>
          <span class="text-xl font-bold" :class="relevanceScore < 70 ? 'text-yellow-400' : relevanceScore < 90 ? 'text-blue-400' : 'text-green-400'">
            {{ relevanceScore }}%
          </span>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-bar-container mb-3">
          <div class="progress-bar" :style="{ width: relevanceScore + '%' }"></div>
        </div>
        
        <!-- Action Button if needed -->
        <div v-if="relevanceScore < 70" class="flex justify-center mt-2">
          <button @click="improveMetric('relevance')" class="action-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V7z" clip-rule="evenodd" />
            </svg>
            Enhance
          </button>
        </div>
      </div>
      
      <!-- Accuracy Card -->
      <div class="metric-card group" :class="getMetricCardClass('accuracy')">
        <!-- Score Display at Top -->
        <div class="flex flex-col items-center mb-3">
          <span class="font-medium text-base mb-1">Accuracy</span>
          <span class="text-xl font-bold" :class="accuracyScore < 70 ? 'text-yellow-400' : accuracyScore < 90 ? 'text-blue-400' : 'text-green-400'">
            {{ accuracyScore }}%
          </span>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-bar-container mb-3">
          <div class="progress-bar" :style="{ width: accuracyScore + '%' }"></div>
        </div>
        
        <!-- Action Button if needed -->
        <div v-if="accuracyScore < 70" class="flex justify-center mt-2">
          <button @click="improveMetric('accuracy')" class="action-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd" />
            </svg>
            Verify
          </button>
        </div>
      </div>
      
      <!-- Helpfulness Card -->
      <div class="metric-card group" :class="getMetricCardClass('helpfulness')">
        <!-- Score Display at Top -->
        <div class="flex flex-col items-center mb-3">
          <span class="font-medium text-base mb-1">Helpfulness</span>
          <span class="text-xl font-bold" :class="helpfulnessScore < 70 ? 'text-yellow-400' : helpfulnessScore < 90 ? 'text-blue-400' : 'text-green-400'">
            {{ helpfulnessScore }}%
          </span>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-bar-container mb-3">
          <div class="progress-bar" :style="{ width: helpfulnessScore + '%' }"></div>
        </div>
        
        <!-- Action Button if needed -->
        <div v-if="helpfulnessScore < 75" class="flex justify-center mt-2">
          <button @click="improveMetric('helpfulness')" class="action-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
            </svg>
            Add Value
          </button>
        </div>
      </div>
      
      <!-- Sentiment Card -->
      <div class="metric-card group">
        <!-- Score Display at Top -->
        <div class="flex flex-col items-center mb-3">
          <span class="font-medium text-base mb-1">Sentiment</span>
          <span class="text-xl font-bold" :class="sentimentScore < 70 ? 'text-yellow-400' : sentimentScore < 90 ? 'text-blue-400' : 'text-green-400'">
            {{ sentimentScore }}%
          </span>
        </div>
        
        <!-- Progress Bar -->
        <div class="progress-bar-container mb-3">
          <div class="progress-bar" :style="{ width: sentimentScore + '%' }"></div>
        </div>
        
        <!-- Action Button if needed -->
        <div v-if="sentimentScore < 75" class="flex justify-center mt-2">
          <button @click="improveMetric('sentiment')" class="action-button">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
            </svg>
            Improve Tone
          </button>
        </div>
      </div>
    </div>
    
    <!-- Auto-apply toggle -->
    <div class="flex items-center justify-end mb-5">
      <span class="text-sm mr-3 text-gray-300">Auto-apply improvements</span>
      <label class="switch">
        <input type="checkbox" v-model="autoApply">
        <span class="slider round"></span>
      </label>
    </div>
    
    <!-- Actionable Suggestions Section -->
    <div class="bg-gray-900/80 border border-gray-700/50 rounded-xl p-5 mb-5 shadow-inner">
      <div class="flex justify-between items-center mb-5">
        <h3 class="text-lg font-medium">Suggested Improvements</h3>
        <button @click="showAddNewImprovement = true" class="primary-button">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Add New Improvement
        </button>
      </div>
      
      <div class="space-y-4">
        <div v-for="(suggestion, index) in improvements" :key="index" 
             class="p-4 bg-gray-800/90 border border-gray-700/50 rounded-lg hover:border-gray-600 transition-colors shadow-sm">
          <p class="text-sm mb-3">{{ suggestion }}</p>
          <div class="flex flex-wrap gap-2 justify-end">
            <button @click="applyImprovement(index)" class="secondary-button bg-blue-600 hover:bg-blue-500">
              Apply
            </button>
            <button @click="editSuggestion(index)" class="secondary-button">
              Edit
            </button>
            <button @click="addToInstructionFeed(index)" class="secondary-button">
              Add to Instructions
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Primary Action Buttons -->
    <div class="flex flex-col sm:flex-row gap-3 justify-end">
      <button class="primary-button-lg">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
        </svg>
        Add All to Instruction Feed
      </button>
      <button class="primary-button-lg bg-gray-700 hover:bg-gray-600">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V8z" clip-rule="evenodd" />
        </svg>
        Export Report
      </button>
    </div>
    
    <!-- Edit Modal -->
    <div v-if="showEditModal" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-medium">Edit Improvement</h3>
          <button @click="showEditModal = false" class="text-gray-400 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <textarea v-model="editedSuggestion" rows="4" class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30 outline-none transition-all"></textarea>
        </div>
        <div class="modal-footer">
          <button @click="showEditModal = false" class="secondary-button-lg">
            Cancel
          </button>
          <button @click="saveEditedSuggestion" class="secondary-button-lg bg-blue-600 hover:bg-blue-500">
            Save Changes
          </button>
        </div>
      </div>
    </div>
    
    <!-- Add New Improvement Modal -->
    <div v-if="showAddNewImprovement" class="modal-backdrop">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="text-lg font-medium">Add New Improvement</h3>
          <button @click="showAddNewImprovement = false" class="text-gray-400 hover:text-white transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <textarea v-model="newImprovement" rows="4" placeholder="Enter a new improvement suggestion..." class="w-full bg-gray-800 border border-gray-700 rounded-lg p-3 text-white focus:border-blue-500 focus:ring-2 focus:ring-blue-500/30 outline-none transition-all"></textarea>
        </div>
        <div class="modal-footer">
          <button @click="showAddNewImprovement = false" class="secondary-button-lg">
            Cancel
          </button>
          <button @click="addNewImprovement" class="secondary-button-lg bg-blue-600 hover:bg-blue-500">
            Add Improvement
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  evaluation: {
    type: Object,
    default: () => ({
      relevance: 92,
      accuracy: 88,
      helpfulness: 95,
      sentiment: 'Positive',
      suggestions: [
        'Consider adding a link to Android permission guide',
        'Reference solution from previous ticket more explicitly'
      ]
    })
  }
});

const emit = defineEmits(['refresh', 'add-to-instruction-feed', 'apply-suggestion', 'export-report']);

// Reactive state
const autoApply = ref(false);
const improvements = ref([
  'Make the response more direct and concise by removing unnecessary explanations.',
  'Add specific code examples to demonstrate the concept.',
  'Include links to relevant documentation for further reading.'
]);

// Edit modal state
const showEditModal = ref(false);
const currentEditIndex = ref(null);
const editedSuggestion = ref('');

// Add new improvement modal state
const showAddNewImprovement = ref(false);
const newImprovement = ref('');

// Mock metrics for demo
const relevanceScore = ref(65);
const accuracyScore = ref(88);
const helpfulnessScore = ref(72);
const sentimentScore = ref(90);

// Edit suggestion function
function editSuggestion(index) {
  currentEditIndex.value = index;
  editedSuggestion.value = improvements.value[index];
  showEditModal.value = true;
}

// Save edited suggestion
function saveEditedSuggestion() {
  if (currentEditIndex.value !== null) {
    improvements.value[currentEditIndex.value] = editedSuggestion.value;
    showEditModal.value = false;
    currentEditIndex.value = null;
    editedSuggestion.value = '';
  }
}

// Add new improvement
function addNewImprovement() {
  if (newImprovement.value.trim()) {
    improvements.value.push(newImprovement.value);
    newImprovement.value = '';
    showAddNewImprovement.value = false;
  }
}

// Add to instruction feed
function addToInstructionFeed(index) {
  // Implementation would go here
  console.log('Added to instruction feed:', improvements.value[index]);
}

// Apply improvement
function applyImprovement(index) {
  // Implementation would go here
  console.log('Applied improvement:', improvements.value[index]);
}

// Improve specific metric
function improveMetric(metric) {
  let improvementText = '';
  
  switch(metric) {
    case 'relevance':
      improvementText = 'Make the response more focused on addressing the specific user query.';
      break;
    case 'accuracy':
      improvementText = 'Verify the factual accuracy of the information provided.';
      break;
    case 'helpfulness':
      improvementText = 'Add more practical examples and actionable advice.';
      break;
    case 'sentiment':
      improvementText = 'Adjust the tone to be more encouraging and supportive.';
      break;
  }
  
  if (improvementText) {
    improvements.value.push(improvementText);
  }
}

// Get metric card class based on score
function getMetricCardClass(metric) {
  let score;
  
  switch(metric) {
    case 'relevance':
      score = relevanceScore.value;
      break;
    case 'accuracy':
      score = accuracyScore.value;
      break;
    case 'helpfulness':
      score = helpfulnessScore.value;
      break;
    default:
      return '';
  }
  
  if (score < 50) {
    return 'border-red-600/30 bg-red-900/20';
  } else if (score < 70) {
    return 'border-yellow-600/30 bg-yellow-900/20';
  } else if (score < 90) {
    return 'border-blue-600/30 bg-blue-900/20';
  } else {
    return 'border-green-600/30 bg-green-900/20';
  }
}
</script>

<style scoped>
.interaction-evaluation {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.metric-card {
  @apply p-4 bg-gray-900 border border-gray-800 rounded-lg relative transition-all duration-200 ease-in-out;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  min-width: 135px;
  max-width: 180px;
  margin: 0 auto;
}

.metric-card:hover {
  @apply transform translate-y-[-2px] border-opacity-100;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
}

.progress-bar-container {
  @apply w-full h-2 bg-gray-800 rounded-full overflow-hidden;
}

.progress-bar {
  @apply h-full rounded-full transition-all duration-500 ease-out;
  background: linear-gradient(90deg, #4ade80 0%, #3b82f6 50%, #eab308 100%);
  animation: shimmer 2s infinite linear;
  background-size: 200% 100%;
}

@keyframes shimmer {
  0% {
    background-position: 100% 0;
  }
  100% {
    background-position: 0 0;
  }
}

.tooltip {
  @apply relative cursor-help inline-flex items-center;
}

.tooltip-text {
  @apply absolute z-10 invisible opacity-0 w-52 bg-gray-800 text-xs text-white rounded-md p-2 bottom-full left-1/2 transform -translate-x-1/2 mb-1 shadow-lg transition-all duration-300;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}

.tooltip:hover .tooltip-text {
  @apply visible opacity-100;
}

/* Button styles */
.action-button {
  @apply text-xs px-2.5 py-1.5 bg-gray-800 hover:bg-gray-700 rounded flex items-center gap-1.5 transition-all duration-200 font-medium;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.action-button:hover {
  @apply transform translate-y-[-1px];
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
}

.primary-button {
  @apply text-xs px-3.5 py-2 bg-blue-600 hover:bg-blue-500 rounded-md transition-all duration-200 flex items-center gap-1.5 font-medium;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.primary-button:hover {
  @apply transform translate-y-[-1px];
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
}

.primary-button-lg {
  @apply px-4 py-2.5 bg-blue-600 hover:bg-blue-500 rounded-md transition-all duration-200 flex items-center justify-center gap-2 font-medium;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.primary-button-lg:hover {
  @apply transform translate-y-[-1px];
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.25);
}

.secondary-button {
  @apply text-xs px-2.5 py-1.5 bg-gray-700 hover:bg-gray-600 rounded transition-all duration-200 font-medium;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.secondary-button:hover {
  @apply transform translate-y-[-1px];
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
}

.secondary-button-lg {
  @apply px-4 py-2.5 bg-gray-700 hover:bg-gray-600 rounded-md transition-all duration-200 font-medium;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.secondary-button-lg:hover {
  @apply transform translate-y-[-1px];
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.25);
}

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 22px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #374151;
  transition: .4s;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 2px;
  bottom: 2px;
  background-color: white;
  transition: .4s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}

input:checked + .slider {
  background-color: #3b82f6;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
}

input:checked + .slider:before {
  transform: translateX(22px);
}

.slider.round {
  border-radius: 22px;
}

.slider.round:before {
  border-radius: 50%;
}

/* Modal styles */
.modal-backdrop {
  @apply fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4;
  animation: fadeIn 0.2s ease-out;
}

.modal-content {
  @apply bg-gray-900 border border-gray-800 rounded-lg shadow-xl w-full max-w-md overflow-hidden;
  animation: slideUp 0.3s ease-out;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
}

.modal-header {
  @apply flex justify-between items-center p-4 border-b border-gray-800;
}

.modal-body {
  @apply p-4;
}

.modal-footer {
  @apply flex justify-end gap-3 p-4 border-t border-gray-800;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(20px);
  }
  to { 
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .metric-card {
    @apply p-3;
  }
  
  .tooltip-text {
    @apply w-40;
  }
}
</style> 