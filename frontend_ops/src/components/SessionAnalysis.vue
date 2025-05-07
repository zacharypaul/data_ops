<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-md bg-primary-900/50 flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-primary-400" viewBox="0 0 20 20" fill="currentColor">
            <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
          </svg>
        </div>
        <h4 class="font-medium">Comprehensive Analysis</h4>
      </div>
      
      <div class="flex space-x-2">
        <button class="text-xs py-1 px-3 bg-dark-700 text-dark-300 rounded hover:bg-dark-600 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
          Export
        </button>
      </div>
    </div>
    
    <!-- Analysis Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Left: Sentiment Analysis -->
      <div class="space-y-4">
        <div class="text-sm font-medium mb-2">Overall Sentiment</div>
        
        <div class="bg-dark-700/50 rounded-lg p-4 border border-dark-600 text-center">
          <div class="inline-flex items-center justify-center w-24 h-24 rounded-full border-4" :class="getSentimentBorderClass()">
            <div class="text-2xl font-semibold" :class="getSentimentTextClass()">{{ analysis.sentiment }}</div>
          </div>
          
          <div class="mt-4">
            <div class="text-xs text-dark-400 mb-1">Customer Satisfaction Score</div>
            <div class="flex items-center justify-center">
              <div 
                v-for="i in 5" 
                :key="i"
                :class="[
                  'w-4 h-4 mx-0.5',
                  i <= getSatisfactionScore() ? 'text-yellow-400' : 'text-dark-600'
                ]"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Middle: Topic Analysis -->
      <div class="space-y-4">
        <div class="text-sm font-medium mb-2">Main Topics</div>
        
        <div class="bg-dark-700/50 rounded-lg p-4 border border-dark-600">
          <div class="space-y-3">
            <div 
              v-for="(topic, index) in analysis.mainTopics" 
              :key="index"
              class="flex items-center"
            >
              <div class="w-2 h-2 rounded-full" :class="getTopicColor(index)"></div>
              <div class="text-sm ml-2">{{ topic }}</div>
            </div>
          </div>
          
          <div class="mt-6">
            <div class="text-xs text-dark-400 mb-2">Entities Mentioned</div>
            <div class="flex flex-wrap gap-2">
              <div 
                v-for="entity in analysis.entities" 
                :key="entity.name"
                class="px-2 py-1 rounded-md text-xs inline-flex items-center space-x-1"
                :class="getEntityClass(entity.type)"
              >
                <span>{{ entity.name }}</span>
                <span class="px-1.5 py-0.5 rounded-full bg-dark-700 text-dark-300 text-xs">{{ entity.mentions }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Right: Improvement Suggestions -->
      <div class="space-y-4">
        <div class="text-sm font-medium mb-2">Suggested Improvements</div>
        
        <div class="bg-dark-700/50 rounded-lg p-4 border border-dark-600">
          <div class="space-y-3 max-h-64 overflow-y-auto">
            <div 
              v-for="(improvement, index) in analysis.suggestedImprovements" 
              :key="index"
              class="flex items-start space-x-2"
            >
              <div class="text-primary-400 mt-0.5">•</div>
              <div class="text-sm">{{ improvement }}</div>
            </div>
            
            <div class="mt-4 pt-4 border-t border-dark-600">
              <button class="w-full text-center text-sm py-1.5 bg-primary-900/30 text-primary-400 rounded hover:bg-primary-900/50 transition">
                Apply Suggestions to Instructions
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Conversation Flow -->
    <div class="mt-8">
      <div class="text-sm font-medium mb-4">Conversation Flow</div>
      
      <div class="bg-dark-700 rounded-lg border border-dark-600 p-5">
        <div class="flex justify-between mb-4">
          <div class="flex items-center space-x-4">
            <div class="space-x-2">
              <span class="inline-block w-3 h-3 rounded-full bg-blue-500"></span>
              <span class="text-xs text-dark-400">User</span>
            </div>
            <div class="space-x-2">
              <span class="inline-block w-3 h-3 rounded-full bg-indigo-500"></span>
              <span class="text-xs text-dark-400">Assistant</span>
            </div>
          </div>
          
          <div class="text-xs text-dark-400">4 message exchanges</div>
        </div>
        
        <!-- Flow chart -->
        <div class="h-32 relative">
          <!-- User messages -->
          <div class="absolute left-0 top-0 w-full h-full">
            <div class="absolute left-[10%] top-[20%] w-2 h-2 bg-blue-500 rounded-full"></div>
            <div class="absolute left-[30%] top-[80%] w-2 h-2 bg-blue-500 rounded-full"></div>
            <div class="absolute left-[70%] top-[40%] w-2 h-2 bg-blue-500 rounded-full"></div>
            <div class="absolute left-[90%] top-[60%] w-2 h-2 bg-blue-500 rounded-full"></div>
          </div>
          
          <!-- Assistant messages -->
          <div class="absolute left-0 top-0 w-full h-full">
            <div class="absolute left-[20%] top-[50%] w-2 h-2 bg-indigo-500 rounded-full"></div>
            <div class="absolute left-[50%] top-[30%] w-2 h-2 bg-indigo-500 rounded-full"></div>
            <div class="absolute left-[80%] top-[20%] w-2 h-2 bg-indigo-500 rounded-full"></div>
          </div>
          
          <!-- Flow lines -->
          <svg class="w-full h-full absolute top-0 left-0">
            <line x1="10%" y1="20%" x2="20%" y2="50%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
            <line x1="20%" y1="50%" x2="30%" y2="80%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
            <line x1="30%" y1="80%" x2="50%" y2="30%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
            <line x1="50%" y1="30%" x2="70%" y2="40%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
            <line x1="70%" y1="40%" x2="80%" y2="20%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
            <line x1="80%" y1="20%" x2="90%" y2="60%" stroke="#4f46e5" stroke-width="1.5" stroke-opacity="0.5" />
          </svg>
          
          <!-- Timeline -->
          <div class="absolute bottom-0 left-0 w-full border-t border-dark-600 pt-1">
            <div class="flex justify-between text-xs text-dark-500">
              <div>Start</div>
              <div>End</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  analysis: {
    type: Object,
    default: () => ({
      sentiment: 'Neutral (0%)',
      mainTopics: [],
      entities: [],
      suggestedImprovements: []
    })
  }
});

// Extract sentiment score from string like "Positive (89%)"
const getSentimentScore = () => {
  const scoreMatch = props.analysis.sentiment.match(/\((\d+)%\)/);
  if (scoreMatch && scoreMatch[1]) {
    return Math.round(parseInt(scoreMatch[1]) / 20); // Convert to 1-5 scale
  }
  return 3; // Default to neutral
};

// Methods for sentiment styling
const getSentimentBorderClass = () => {
  if (props.analysis.sentiment.includes('Positive')) {
    return 'border-green-500';
  }
  if (props.analysis.sentiment.includes('Negative')) {
    return 'border-red-500';
  }
  return 'border-gray-500';
};

const getSentimentTextClass = () => {
  if (props.analysis.sentiment.includes('Positive')) {
    return 'text-green-400';
  }
  if (props.analysis.sentiment.includes('Negative')) {
    return 'text-red-400';
  }
  return 'text-gray-400';
};

// Topic color based on index
const getTopicColor = (index) => {
  const colors = [
    'bg-primary-500',
    'bg-indigo-500',
    'bg-cyan-500',
    'bg-green-500',
    'bg-yellow-500',
    'bg-orange-500',
    'bg-red-500',
    'bg-pink-500',
    'bg-purple-500'
  ];
  
  return colors[index % colors.length];
};

// Entity styling based on type
const getEntityClass = (type) => {
  switch(type) {
    case 'Product':
      return 'bg-blue-900/30 text-blue-400';
    case 'OS':
      return 'bg-purple-900/30 text-purple-400';
    case 'Person':
      return 'bg-green-900/30 text-green-400';
    case 'Feature':
      return 'bg-yellow-900/30 text-yellow-400';
    default:
      return 'bg-dark-600 text-dark-300';
  }
};
</script>

<style scoped>
/* Custom scrollbar for containers */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(15, 23, 42, 0.3);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(71, 85, 105, 0.5);
  border-radius: 10px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(71, 85, 105, 0.8);
}
</style> 