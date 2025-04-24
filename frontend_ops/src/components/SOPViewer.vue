<template>
  <div v-if="sopDocument" class="sop-viewer">
    <div class="sop-header">
      <h2 class="text-2xl font-bold">{{ sopDocument.title }}</h2>
      <p class="text-dark-400 mt-1">{{ sopDocument.summary }}</p>
      <div class="audience-tag mt-2 inline-block px-3 py-1 rounded-full text-sm bg-dark-700 text-dark-300">
        {{ sopDocument.audience }}
      </div>
    </div>
    
    <div class="sop-actions mt-4 mb-6 flex space-x-3">
      <button @click="exportSOP('pdf')" class="action-button">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v3.586l-1.293-1.293a1 1 0 10-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L11 11.586V8z" clip-rule="evenodd" />
        </svg>
        Export as PDF
      </button>
      <button @click="exportSOP('md')" class="action-button">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
        </svg>
        Export as Markdown
      </button>
      <button @click="printSOP" class="action-button">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M5 4v3H4a2 2 0 00-2 2v3a2 2 0 002 2h1v2a2 2 0 002 2h6a2 2 0 002-2v-2h1a2 2 0 002-2V9a2 2 0 00-2-2h-1V4a2 2 0 00-2-2H7a2 2 0 00-2 2zm8 0H7v3h6V4zm0 8H7v4h6v-4z" clip-rule="evenodd" />
        </svg>
        Print
      </button>
    </div>
    
    <div class="sop-content">
      <div class="sop-summary-box mb-6 p-4 rounded-lg bg-dark-800 border border-dark-700">
        <div class="summary-stats grid grid-cols-2 gap-4">
          <div>
            <div class="text-sm text-dark-400 mb-1">Total Data Points</div>
            <div class="text-xl font-bold">{{ sopDocument.dataPointsSummary.totalPoints }}</div>
          </div>
          <div v-for="(count, source) in sopDocument.dataPointsSummary.bySource" :key="source">
            <div class="text-sm text-dark-400 mb-1">{{ capitalize(source) }} Points</div>
            <div class="text-xl font-bold">{{ count }}</div>
          </div>
        </div>
      </div>
      
      <div v-for="(section, index) in sopDocument.sections" :key="index" class="sop-section mb-8">
        <h3 class="text-xl font-bold mb-3 text-primary-400">{{ section.title }}</h3>
        <div class="markdown-content" v-html="renderMarkdown(section.content)"></div>
      </div>
    </div>
  </div>
  
  <div v-else class="sop-placeholder p-8 text-center text-dark-400 border border-dashed border-dark-700 rounded-lg">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-4 text-dark-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
    <p class="text-lg mb-2">No SOP Document Generated</p>
    <p class="text-sm max-w-md mx-auto">Select data points and configure parameters in the AI Data Flow Builder to generate a Standard Operating Procedure document.</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';
import { marked } from 'marked';
import DOMPurify from 'dompurify';
import sopService from '../services/sopService';

const props = defineProps({
  sopDocument: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['export']);

// Render markdown to HTML
const renderMarkdown = (markdown) => {
  if (!markdown) return '';
  // Convert markdown to HTML and sanitize to prevent XSS
  const html = marked(markdown);
  return DOMPurify.sanitize(html);
};

// Capitalize first letter of a string
const capitalize = (str) => {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
};

// Export SOP document
const exportSOP = async (format) => {
  try {
    if (!props.sopDocument) return;
    
    const result = await sopService.exportSOP(props.sopDocument, format);
    console.log('Export result:', result);
    
    // In a real implementation, this would handle the downloaded file
    // For now, just emit an event that parent components can listen to
    emit('export', { format, success: true });
    
  } catch (error) {
    console.error('Error exporting document:', error);
    emit('export', { format, success: false, error });
  }
};

// Print SOP document
const printSOP = () => {
  window.print();
};
</script>

<style scoped>
.sop-viewer {
  margin-bottom: 2rem;
  animation: fadeIn 0.6s ease-out;
}

.action-button {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #d1d5db;
  transition: all 0.2s;
}

.action-button:hover {
  background-color: rgba(55, 65, 81, 0.5);
  border-color: rgba(71, 85, 105, 0.5);
  transform: translateY(-1px);
}

.markdown-content {
  line-height: 1.6;
  color: #e2e8f0;
}

.markdown-content :deep(h2) {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 1.5rem 0 1rem;
  color: #38bdf8;
}

.markdown-content :deep(h3) {
  font-size: 1.125rem;
  font-weight: 600;
  margin: 1.25rem 0 0.75rem;
  color: #e2e8f0;
}

.markdown-content :deep(p) {
  margin-bottom: 1rem;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

.markdown-content :deep(li) {
  margin-bottom: 0.5rem;
}

.markdown-content :deep(pre) {
  background-color: rgba(15, 23, 42, 0.6);
  padding: 1rem;
  border-radius: 0.375rem;
  margin: 1rem 0;
  overflow-x: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.markdown-content :deep(code) {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  padding: 0.125rem 0.25rem;
  background-color: rgba(15, 23, 42, 0.6);
  border-radius: 0.25rem;
}

.markdown-content :deep(blockquote) {
  border-left: 4px solid rgba(71, 85, 105, 0.5);
  padding-left: 1rem;
  margin: 1rem 0;
  color: #94a3b8;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media print {
  .sop-actions {
    display: none;
  }
  
  .sop-content {
    color: black;
  }
  
  .markdown-content :deep(*) {
    color: black;
  }
  
  .markdown-content :deep(h2) {
    color: #0284c7;
  }
  
  .markdown-content :deep(h3) {
    color: #111827;
  }
}
</style> 