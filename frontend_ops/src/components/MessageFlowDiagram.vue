<template>
  <div class="message-flow-diagram">
    <div class="flex justify-between items-center mb-3">
      <h3 class="text-lg font-semibold">Message Flow</h3>
      
      <!-- Playback controls -->
      <div class="playback-controls flex items-center space-x-2">
        <button 
          @click="playPrevious" 
          class="playback-btn"
          :disabled="playbackIndex <= 0"
          :class="{'opacity-50 cursor-not-allowed': playbackIndex <= 0}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
            <path d="M9.195 18.44c1.25.713 2.805-.19 2.805-1.629v-2.34l6.945 3.968c1.25.714 2.805-.188 2.805-1.628V8.688c0-1.44-1.555-2.342-2.805-1.628L12 11.03v-2.34c0-1.44-1.555-2.343-2.805-1.629l-7.108 4.062c-1.26.72-1.26 2.536 0 3.256l7.108 4.061z" />
          </svg>
        </button>
        
        <!-- Make play button larger and more obvious -->
        <button 
          @click="togglePlayback" 
          class="playback-btn play-btn"
          :class="{ 'is-playing': isPlaying }"
        >
          <svg v-if="isPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd" d="M6.75 5.25a.75.75 0 01.75-.75H9a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H7.5a.75.75 0 01-.75-.75V5.25zm7.5 0A.75.75 0 0115 4.5h1.5a.75.75 0 01.75.75v13.5a.75.75 0 01-.75.75H15a.75.75 0 01-.75-.75V5.25z" clip-rule="evenodd" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
            <path fill-rule="evenodd" d="M4.5 5.653c0-1.426 1.529-2.33 2.779-1.643l11.54 6.348c1.295.712 1.295 2.573 0 3.285L7.28 19.991c-1.25.687-2.779-.217-2.779-1.643V5.653z" clip-rule="evenodd" />
          </svg>
        </button>
        
        <button 
          @click="playNext" 
          class="playback-btn"
          :disabled="playbackIndex >= totalMessages - 1"
          :class="{'opacity-50 cursor-not-allowed': playbackIndex >= totalMessages - 1}"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
            <path d="M5.055 7.06c-1.25-.714-2.805.189-2.805 1.628v8.123c0 1.44 1.555 2.342 2.805 1.628L12 14.471v2.34c0 1.44 1.555 2.342 2.805 1.628l7.108-4.061c1.26-.72 1.26-2.536 0-3.256L14.805 7.06C13.555 6.346 12 7.25 12 8.688v2.34L5.055 7.06z" />
          </svg>
        </button>

        <div class="px-2 text-xs text-dark-400">
          {{ playbackIndex + 1 }} / {{ totalMessages }}
        </div>
      </div>
    </div>
    
    <div v-if="playbackActive" class="mb-3">
      <div class="timeline-container">
        <div class="timeline-track"></div>
        <div 
          v-for="(dot, index) in totalMessages" 
          :key="index"
          class="timeline-dot"
          :class="{ 'active': index <= playbackIndex, 'current': index === playbackIndex }"
          @click="jumpToMessage(index)"
        ></div>
      </div>
    </div>
    
    <div class="flow-container">
      <!-- Sender section -->
      <div class="flow-section">
        <h4 class="text-sm text-dark-400 mb-2">Sender</h4>
        <div class="icons-container">
          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.role === 'user' }"
            @click="$emit('update-selected-info', { role: 'user' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xs mt-1">User</span>
          </div>

          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.role === 'assistant' }"
            @click="$emit('update-selected-info', { role: 'assistant' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path d="M16.5 7.5h-9v9h9v-9z" />
                <path fill-rule="evenodd" d="M8.25 2.25A.75.75 0 019 3v.75h2.25V3a.75.75 0 011.5 0v.75H15V3a.75.75 0 011.5 0v.75h.75a3 3 0 013 3v.75H21A.75.75 0 0121 9h-.75v2.25H21a.75.75 0 010 1.5h-.75V15H21a.75.75 0 010 1.5h-.75v.75a3 3 0 01-3 3h-.75V21a.75.75 0 01-1.5 0v-.75h-2.25V21a.75.75 0 01-1.5 0v-.75H9V21a.75.75 0 01-1.5 0v-.75h-.75a3 3 0 01-3-3v-.75H3A.75.75 0 013 15h.75v-2.25H3a.75.75 0 010-1.5h.75V9H3a.75.75 0 010-1.5h.75v-.75a3 3 0 013-3h.75V3a.75.75 0 01.75-.75zM6 6.75A.75.75 0 016.75 6h10.5a.75.75 0 01.75.75v10.5a.75.75 0 01-.75.75H6.75a.75.75 0 01-.75-.75V6.75z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xs mt-1">Assistant</span>
          </div>
        </div>
      </div>

      <!-- Arrow between sections -->
      <div class="flow-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </div>

      <!-- Device section -->
      <div class="flow-section">
        <h4 class="text-sm text-dark-400 mb-2">Device</h4>
        <div class="icons-container">
          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.device === 'mobile' }"
            @click="$emit('update-selected-info', { device: 'mobile' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path d="M10.5 18.75a.75.75 0 000 1.5h3a.75.75 0 000-1.5h-3z" />
                <path fill-rule="evenodd" d="M8.625.75A3.375 3.375 0 005.25 4.125v15.75a3.375 3.375 0 003.375 3.375h6.75a3.375 3.375 0 003.375-3.375V4.125A3.375 3.375 0 0015.375.75h-6.75zM7.5 4.125C7.5 3.504 8.004 3 8.625 3H9.75v.375c0 .621.504 1.125 1.125 1.125h2.25c.621 0 1.125-.504 1.125-1.125V3h1.125c.621 0 1.125.504 1.125 1.125v15.75c0 .621-.504 1.125-1.125 1.125h-6.75A1.125 1.125 0 017.5 19.875V4.125z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xs mt-1">Mobile</span>
          </div>

          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.device === 'desktop' }"
            @click="$emit('update-selected-info', { device: 'desktop' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path fill-rule="evenodd" d="M2.25 5.25a3 3 0 013-3h13.5a3 3 0 013 3V15a3 3 0 01-3 3h-3v.257c0 .597.237 1.17.659 1.591l.621.622a.75.75 0 01-.53 1.28h-9a.75.75 0 01-.53-1.28l.621-.622a2.25 2.25 0 00.659-1.59V18h-3a3 3 0 01-3-3V5.25zm1.5 0v9.75c0 .83.67 1.5 1.5 1.5h13.5c.83 0 1.5-.67 1.5-1.5V5.25c0-.83-.67-1.5-1.5-1.5H5.25c-.83 0-1.5.67-1.5 1.5z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xs mt-1">Desktop</span>
          </div>
        </div>
      </div>
      
      <!-- Arrow between sections -->
      <div class="flow-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </div>

      <!-- Modality section -->
      <div class="flow-section">
        <h4 class="text-sm text-dark-400 mb-2">Modality</h4>
        <div class="icons-container">
          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.modality === 'text' }"
            @click="$emit('update-selected-info', { modality: 'text' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path fill-rule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.587 2.674 6.192.232.226.277.428.254.543a3.73 3.73 0 01-.814 1.686.75.75 0 00.44 1.223zM8.25 10.875a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25zM10.875 12a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0zm4.875-1.125a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xs mt-1">Text</span>
          </div>

          <div 
            class="icon-item" 
            :class="{ 'active': selectedMessage.modality === 'speech' }"
            @click="$emit('update-selected-info', { modality: 'speech' })"
          >
            <div class="icon-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
                <path d="M8.25 4.5a3.75 3.75 0 117.5 0v8.25a3.75 3.75 0 11-7.5 0V4.5z" />
                <path d="M6 10.5a.75.75 0 01.75.75v1.5a5.25 5.25 0 1010.5 0v-1.5a.75.75 0 011.5 0v1.5a6.751 6.751 0 01-6 6.709v2.291h3a.75.75 0 010 1.5h-7.5a.75.75 0 010-1.5h3v-2.291a6.751 6.751 0 01-6-6.709v-1.5A.75.75 0 016 10.5z" />
              </svg>
            </div>
            <span class="text-xs mt-1">Speech</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed, watch, onBeforeUnmount, nextTick } from 'vue';

const props = defineProps({
  selectedMessage: {
    type: Object,
    default: () => ({
      role: 'user',
      device: 'mobile',
      modality: 'text'
    })
  },
  messages: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update-selected-info', 'select-message', 'highlight-message']);

// Playback state
const playbackActive = ref(false);
const isPlaying = ref(false);
const playbackIndex = ref(0);
const playbackInterval = ref(null);
const playbackSpeed = ref(1500); // ms between messages

// Computed properties
const totalMessages = computed(() => props.messages.length);
const currentMessage = computed(() => {
  if (props.messages.length > 0 && playbackIndex.value >= 0 && playbackIndex.value < props.messages.length) {
    return props.messages[playbackIndex.value];
  }
  return null;
});

// Methods for playback
const togglePlayback = () => {
  console.log('Toggle playback, current state:', isPlaying.value);
  playbackActive.value = true;
  isPlaying.value = !isPlaying.value;
  
  if (isPlaying.value) {
    console.log('Starting playback');
    startPlayback();
  } else {
    console.log('Stopping playback');
    stopPlayback();
  }
};

const startPlayback = () => {
  // Clear any existing interval to prevent duplicates
  stopPlayback();
  
  console.log('Starting playback from index:', playbackIndex.value);
  
  // First highlight the current message immediately
  updateSelectedMessage();
  
  // Then set up the interval for subsequent messages
  playbackInterval.value = setInterval(() => {
    console.log('Playback interval triggered');
    
    if (playbackIndex.value < totalMessages.value - 1) {
      playbackIndex.value++;
      console.log('Moving to next message, index:', playbackIndex.value);
      
      // Force Vue to update before trying to highlight the message
      nextTick(() => {
        updateSelectedMessage();
      });
    } else {
      console.log('Reached end of messages, stopping playback');
      stopPlayback();
    }
  }, playbackSpeed.value);
};

const stopPlayback = () => {
  console.log('Stopping playback, clearing interval:', playbackInterval.value);
  isPlaying.value = false;
  
  if (playbackInterval.value) {
    clearInterval(playbackInterval.value);
    playbackInterval.value = null;
  }
};

const playNext = () => {
  if (playbackIndex.value < totalMessages.value - 1) {
    playbackIndex.value++;
    updateSelectedMessage();
    playbackActive.value = true;
  }
};

const playPrevious = () => {
  if (playbackIndex.value > 0) {
    playbackIndex.value--;
    updateSelectedMessage();
    playbackActive.value = true;
  }
};

const jumpToMessage = (index) => {
  playbackIndex.value = index;
  updateSelectedMessage();
  playbackActive.value = true;
};

const updateSelectedMessage = () => {
  if (!props.messages || props.messages.length === 0) {
    console.warn('No messages available to highlight');
    return;
  }
  
  if (playbackIndex.value >= 0 && playbackIndex.value < props.messages.length) {
    const message = props.messages[playbackIndex.value];
    console.log('Updating selected message:', message);
    
    // Update the selected message info for the flow diagram
    const messageInfo = {
      role: message.role || 'user',
      device: message.device || 'mobile',
      modality: message.modality || 'text'
    };
    
    emit('select-message', message);
    
    // Explicitly emit highlight-message event with the message ID
    if (typeof message.id === 'number') {
      console.log('Emitting highlight-message event with ID:', message.id);
      emit('highlight-message', message.id);
    } else {
      console.warn('Message ID is not a number:', message.id);
    }
  } else {
    console.warn('Invalid playback index:', playbackIndex.value, 'for messages length:', props.messages.length);
  }
};

// Clean up interval on component unmount
onBeforeUnmount(() => {
  if (playbackInterval.value) {
    clearInterval(playbackInterval.value);
  }
});

// Initialize playback index when messages change
watch(() => props.messages, (newMessages) => {
  if (newMessages.length > 0 && playbackIndex.value >= newMessages.length) {
    playbackIndex.value = newMessages.length - 1;
  }
}, { deep: true });
</script>

<style scoped>
.message-flow-diagram {
  background-color: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(71, 85, 105, 0.25);
  backdrop-filter: blur(8px);
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.flow-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.flow-section {
  flex: 1;
}

.icons-container {
  display: flex;
  justify-content: space-evenly;
  gap: 1rem;
}

.icon-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-wrapper {
  background-color: rgba(30, 41, 59, 0.6);
  border-radius: 9999px;
  padding: 0.5rem;
  color: rgba(156, 163, 175, 1);
  transition: all 0.2s ease;
}

.icon-item:hover .icon-wrapper {
  background-color: rgba(55, 65, 81, 0.8);
  color: rgba(209, 213, 219, 1);
}

.icon-item.active .icon-wrapper {
  background-color: rgba(59, 130, 246, 0.2);
  border: 2px solid rgb(59, 130, 246);
  color: rgb(59, 130, 246);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.4);
}

.flow-arrow {
  color: rgba(156, 163, 175, 0.6);
  margin: 0 0.5rem;
  display: flex;
  align-items: center;
}

/* Playback controls */
.playback-controls {
  display: flex;
  align-items: center;
}

.playback-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(30, 41, 59, 0.6);
  color: rgba(156, 163, 175, 1);
  border-radius: 9999px;
  padding: 0.5rem;
  transition: all 0.2s ease;
}

.playback-btn:hover:not(:disabled) {
  background-color: rgba(55, 65, 81, 0.8);
  color: rgba(209, 213, 219, 1);
}

/* Enhanced play button */
.play-btn {
  background-color: rgba(37, 99, 235, 0.3);
  padding: 0.6rem;
  color: rgba(191, 219, 254, 1);
  box-shadow: 0 0 8px rgba(37, 99, 235, 0.2);
  transition: all 0.3s ease;
}

.play-btn:hover {
  background-color: rgba(37, 99, 235, 0.5);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 0 12px rgba(37, 99, 235, 0.4);
}

.play-btn.is-playing {
  background-color: rgba(220, 38, 38, 0.3);
  color: rgba(252, 165, 165, 1);
  animation: pulse-play 2s infinite;
}

.play-btn.is-playing:hover {
  background-color: rgba(220, 38, 38, 0.5);
}

@keyframes pulse-play {
  0% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.4);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(220, 38, 38, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(220, 38, 38, 0);
  }
}

/* Timeline */
.timeline-container {
  position: relative;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
}

.timeline-track {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background-color: rgba(71, 85, 105, 0.5);
  transform: translateY(-50%);
}

.timeline-dot {
  position: relative;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: rgba(71, 85, 105, 0.7);
  cursor: pointer;
  z-index: 1;
  transition: all 0.2s ease;
}

.timeline-dot.active {
  background-color: rgb(59, 130, 246);
}

.timeline-dot.current {
  background-color: rgb(59, 130, 246);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
  transform: scale(1.2);
}
</style> 