<template>
  <div class="flex flex-col h-full">
    <!-- Chat messages container - added padding to ensure messages don't touch the edges -->
    <div class="flex-1 space-y-4 mb-4 max-h-[500px] overflow-y-auto px-3 py-2" ref="chatContainer">
      <div 
        v-for="message in messages" 
        :key="message.id"
        :class="[
          'p-3 rounded-lg transition-all duration-300',
          message.role === 'user' 
            ? 'bg-blue-900/20 text-white ml-auto user-message' 
            : message.role === 'system'
              ? 'bg-dark-700/80 text-dark-300 italic text-sm border border-dark-600'
              : 'bg-dark-800/80 text-white border border-dark-700',
          message.id === highlightedMessageId && 'highlighted-message'
        ]"
        @mouseup="handleSelection"
        @click="$emit('select-message', message)"
      >
        <div v-if="message.role !== 'system'" class="flex items-center mb-1">
          <div 
            class="w-6 h-6 rounded-full flex items-center justify-center mr-2 text-xs"
            :class="message.role === 'user' ? 'bg-blue-700' : 'bg-indigo-700'"
          >
            {{ message.role === 'user' ? 'U' : 'A' }}
          </div>
          <div class="text-xs text-dark-400">
            {{ message.role === 'user' ? 'User' : 'Assistant' }}
          </div>
        </div>
        <div class="whitespace-pre-wrap">{{ message.content }}</div>
      </div>
      
      <div v-if="isTyping" class="bg-dark-800/80 text-white p-3 rounded-lg border border-dark-700">
        <div class="flex items-center">
          <div class="w-6 h-6 rounded-full bg-indigo-700 flex items-center justify-center mr-2 text-xs">A</div>
          <div class="text-xs text-dark-400">Assistant</div>
        </div>
        <div class="mt-2 flex space-x-1">
          <div class="typing-dot"></div>
          <div class="typing-dot animation-delay-200"></div>
          <div class="typing-dot animation-delay-400"></div>
        </div>
      </div>
    </div>
    
    <!-- Input area -->
    <div class="border-t border-dark-700 pt-4">
      <div class="flex space-x-2">
        <div class="flex-1 relative">
          <textarea
            v-model="userInput"
            placeholder="Type your message here..."
            class="w-full bg-dark-700 border border-dark-600 rounded-lg px-4 py-3 focus:outline-none focus:border-primary-500 text-white resize-none"
            rows="2"
            @keydown.enter.prevent="sendMessage"
          ></textarea>
          
          <div class="absolute bottom-2 right-2 flex space-x-1">
            <button class="p-1.5 text-dark-400 hover:text-dark-200 rounded">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M8 4a3 3 0 00-3 3v4a3 3 0 006 0V7a1 1 0 112 0v4a5 5 0 01-10 0V7a5 5 0 0110 0v1.5a1.5 1.5 0 01-3 0V6a1 1 0 012 0v4a3 3 0 01-6 0V7a1 1 0 012 0v4a1 1 0 102 0V7a3 3 0 00-3-3z" clip-rule="evenodd" />
              </svg>
            </button>
            <button class="p-1.5 text-dark-400 hover:text-dark-200 rounded">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        
        <button 
          @click="sendMessage"
          :disabled="!userInput.trim()"
          :class="[
            'px-4 rounded-lg flex items-center justify-center',
            userInput.trim() 
              ? 'bg-primary-600 hover:bg-primary-700 text-white'
              : 'bg-dark-700 text-dark-500 cursor-not-allowed'
          ]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      
      <!-- Chat controls -->
      <div class="flex justify-between items-center mt-3">
        <div class="flex space-x-2">
          <button class="text-xs py-1 px-2 bg-dark-700 text-dark-400 rounded hover:bg-dark-600 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd" />
            </svg>
            Simulated User
          </button>
          <button class="text-xs py-1 px-2 bg-dark-700 text-dark-400 rounded hover:bg-dark-600 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z" />
              <path fill-rule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clip-rule="evenodd" />
            </svg>
            Templates
          </button>
        </div>
        
        <div class="flex space-x-2">
          <button class="text-xs py-1 px-2 bg-red-900/30 text-red-400 rounded hover:bg-red-900/50 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            Clear Chat
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  highlightedMessageId: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['send-message', 'select-content', 'select-message']);

// Local state
const userInput = ref('');
const isTyping = ref(false);
const chatContainer = ref(null);

// Methods
const sendMessage = () => {
  if (!userInput.value.trim()) return;
  
  // Emit the message to parent
  emit('send-message', userInput.value);
  
  // Show typing indicator
  isTyping.value = true;
  setTimeout(() => {
    isTyping.value = false;
  }, 1000);
  
  // Clear input
  userInput.value = '';
};

// Add method to handle text selection and emit selected content
const handleSelection = () => {
  const selection = window.getSelection();
  const selectedText = selection.toString().trim();
  
  if (selectedText) {
    emit('select-content', selectedText);
  }
};

// Enhance the watch function to better handle highlighting
watch(() => props.highlightedMessageId, (newId, oldId) => {
  console.log('Highlighted message ID changed:', oldId, '->', newId);
  
  if (newId) {
    // Use setTimeout to allow Vue to update the DOM first
    setTimeout(() => {
      const highlightedElement = document.querySelector('.highlighted-message');
      if (highlightedElement && chatContainer.value) {
        console.log('Scrolling to highlighted element:', highlightedElement);
        highlightedElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        console.warn('Could not find highlighted element or chat container');
      }
    }, 100);
  }
}, { immediate: true });
</script>

<style scoped>
/* Typing indicator dots */
.typing-dot {
  @apply w-2 h-2 rounded-full bg-primary-500;
  animation: bounce 1.4s infinite;
}

.animation-delay-200 {
  animation-delay: 0.2s;
}

.animation-delay-400 {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

/* Custom scrollbar for chat */
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

/* User message specific styles */
.user-message {
  max-width: 85%; /* Reduced max width to prevent cut-off */
  margin-right: 5px; /* Ensure there's space on the right */
  position: relative;
  width: fit-content; /* Ensure message only takes up needed space */
}

/* Highlighted message */
.highlighted-message {
  box-shadow: 0 0 0 3px rgb(59, 130, 246), 0 0 20px 3px rgba(59, 130, 246, 0.6) !important;
  transform: scale(1.02); /* Slightly reduced scale to prevent overflow */
  z-index: 10;
  position: relative;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.7), 0 0 20px 3px rgba(59, 130, 246, 0.4);
  }
  50% {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 1), 0 0 25px 5px rgba(59, 130, 246, 0.7);
  }
  100% {
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.7), 0 0 20px 3px rgba(59, 130, 246, 0.4);
  }
}
</style> 