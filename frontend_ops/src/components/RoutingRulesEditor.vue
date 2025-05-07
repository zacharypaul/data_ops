<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <div class="flex items-center">
        <div class="w-8 h-8 rounded-md bg-orange-900/50 flex items-center justify-center mr-3">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-orange-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
          </svg>
        </div>
        <h4 class="font-medium">Dynamic Routing Rules</h4>
      </div>
      
      <button class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Add Rule
      </button>
    </div>
    
    <!-- Rules table -->
    <div class="bg-dark-700 rounded-lg overflow-hidden border border-dark-600">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-dark-600">
          <thead>
            <tr>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase tracking-wider">
                Condition
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase tracking-wider">
                Value
              </th>
              <th scope="col" class="px-4 py-3 text-left text-xs font-medium text-dark-400 uppercase tracking-wider">
                Action
              </th>
              <th scope="col" class="px-4 py-3 text-xs font-medium text-dark-400 uppercase tracking-wider text-right">
                Controls
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-dark-600">
            <tr v-for="rule in localRules" :key="rule.id" class="hover:bg-dark-700/50">
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-sm font-medium">{{ rule.condition }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-sm">
                  <span 
                    class="px-2 py-1 rounded-full text-xs"
                    :class="getValueClass(rule.condition)"
                  >
                    {{ rule.value }}
                  </span>
                </div>
              </td>
              <td class="px-4 py-3">
                <div class="text-sm">{{ rule.action }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex justify-end space-x-2">
                  <button class="p-1 text-dark-400 hover:text-dark-200 rounded">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                  </button>
                  <button class="p-1 text-dark-400 hover:text-red-400 rounded">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Time and Day Configuration -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
      <!-- Time of Day Rules -->
      <div class="space-y-4">
        <div class="flex items-center">
          <div class="w-6 h-6 rounded-full bg-orange-900/50 flex items-center justify-center mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-orange-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
            </svg>
          </div>
          <h4 class="text-sm font-medium">Time of Day Rules</h4>
        </div>
        
        <div class="space-y-3 p-4 bg-dark-700/50 rounded-lg border border-dark-600">
          <div class="flex items-center justify-between">
            <div class="text-sm">Business Hours</div>
            <div class="flex items-center space-x-2">
              <input 
                type="time" 
                value="09:00" 
                class="bg-dark-700 border border-dark-600 rounded p-1 text-xs w-24"
              >
              <span class="text-dark-400">to</span>
              <input 
                type="time" 
                value="17:00" 
                class="bg-dark-700 border border-dark-600 rounded p-1 text-xs w-24"
              >
            </div>
          </div>
          
          <div class="flex items-center justify-between mt-2">
            <div class="text-sm">After Hours</div>
            <div class="text-xs text-dark-400">All other times</div>
          </div>
          
          <div class="mt-3">
            <div class="text-xs text-dark-400 mb-2">Time Zone</div>
            <select class="w-full bg-dark-700 border border-dark-600 rounded p-2 text-sm focus:outline-none focus:border-orange-500">
              <option>Eastern Time (ET)</option>
              <option>Central Time (CT)</option>
              <option>Mountain Time (MT)</option>
              <option>Pacific Time (PT)</option>
              <option>UTC</option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Day of Week Rules -->
      <div class="space-y-4">
        <div class="flex items-center">
          <div class="w-6 h-6 rounded-full bg-orange-900/50 flex items-center justify-center mr-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-orange-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
            </svg>
          </div>
          <h4 class="text-sm font-medium">Day of Week Rules</h4>
        </div>
        
        <div class="space-y-3 p-4 bg-dark-700/50 rounded-lg border border-dark-600">
          <div class="text-xs text-dark-400 mb-2">Business Days</div>
          <div class="flex flex-wrap gap-2">
            <div 
              v-for="day in days" 
              :key="day.code"
              :class="[
                'rounded-full py-1 px-3 text-xs cursor-pointer transition',
                day.selected ? 'bg-orange-900/30 text-orange-400' : 'bg-dark-700 text-dark-400 hover:bg-dark-600'
              ]"
              @click="toggleDay(day)"
            >
              {{ day.name }}
            </div>
          </div>
          
          <div class="mt-4">
            <div class="flex items-center">
              <input type="checkbox" id="weekend-support" class="rounded text-orange-500 focus:ring-orange-500 bg-dark-800 border-dark-700">
              <label for="weekend-support" class="ml-2 text-sm text-dark-300">Limited Weekend Support</label>
            </div>
            <div class="text-xs text-dark-400 mt-1">
              Special routing for Saturday and Sunday
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  rules: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update']);

// Create a local copy of the rules
const localRules = ref([...props.rules]);

// Days of week
const days = ref([
  { name: 'Mon', code: 'monday', selected: true },
  { name: 'Tue', code: 'tuesday', selected: true },
  { name: 'Wed', code: 'wednesday', selected: true },
  { name: 'Thu', code: 'thursday', selected: true },
  { name: 'Fri', code: 'friday', selected: true },
  { name: 'Sat', code: 'saturday', selected: false },
  { name: 'Sun', code: 'sunday', selected: false }
]);

// Methods
const toggleDay = (day) => {
  day.selected = !day.selected;
};

const getValueClass = (condition) => {
  switch(condition) {
    case 'Time of Day':
      return 'bg-blue-900/30 text-blue-400';
    case 'Day of Week':
      return 'bg-green-900/30 text-green-400';
    case 'User Type':
      return 'bg-purple-900/30 text-purple-400';
    default:
      return 'bg-dark-600 text-dark-400';
  }
};

// Watch for parent props changes
watch(() => props.rules, (newRules) => {
  localRules.value = [...newRules];
});
</script>

<style scoped>
/* Custom checkbox styling same as in SystemInstructionsEditor */
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
  background-color: rgba(249, 115, 22, 0.8);
  border-color: rgba(249, 115, 22, 0.5);
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

/* Time input styling */
input[type="time"] {
  color: #e2e8f0;
  font-size: 12px;
}

input[type="time"]::-webkit-calendar-picker-indicator {
  filter: invert(0.7);
  opacity: 0.6;
}
</style> 