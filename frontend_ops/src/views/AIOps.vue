<template>
  <div class="w-full mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-6">Generative AI Operations</h1>
    <p class="text-lg mb-8">Design, test, and manage your generative AI applications and LLM-powered services.</p>
    
    <!-- Main tabs -->
    <div class="mb-8 border-b border-dark-700">
      <nav class="flex space-x-8" aria-label="Tabs">
        <button 
          v-for="tab in navigationTabs" 
          :key="tab.id"
          @click="activeNavTab = tab.id"
          :class="[
            'py-3 px-2 border-b-2 font-medium text-sm',
            activeNavTab === tab.id
              ? 'border-primary-500 text-primary-400'
              : 'border-transparent text-dark-400 hover:text-dark-200 hover:border-dark-500'
          ]"
        >
          {{ tab.name }}
        </button>
      </nav>
    </div>
    
    <!-- Dashboard tab content -->
    <div v-if="activeNavTab === 'dashboard'">
      <div class="mb-8">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">Deployed GenAI Applications</h2>
          <button class="btn-primary py-2 px-4 rounded font-medium" @click="openNewAppModal">New Application</button>
        </div>
      </div>
      
      <!-- Deployed Applications Cards -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <AIApplicationCard 
          v-for="app in deployedApps"
          :key="app.id"
          :application="app"
        />
      </div>
    </div>
    
    <!-- Design tab content -->
    <div v-if="activeNavTab === 'design'" class="space-y-8">
      <div class="glass-card p-6">
        <h2 class="text-2xl font-bold mb-6">AI Agent Design Studio</h2>
        
        <!-- Memory System Architecture Diagram -->
        <MemoryArchitectureDiagram />
        
        <!-- Integrated Design and Test Environment -->
        <div class="mt-20">
          <!-- Tab Navigation Within Design Studio -->
          <div class="border-b border-dark-700 mb-6">
            <nav class="flex space-x-4" aria-label="Design Tabs">
              <button 
                v-for="tab in designTabs" 
                :key="tab.id"
                @click="activeDesignTab = tab.id"
                :class="[
                  'py-2 px-3 border-b-2 font-medium text-sm',
                  activeDesignTab === tab.id
                    ? 'border-primary-500 text-primary-400'
                    : 'border-transparent text-dark-400 hover:text-dark-200 hover:border-dark-500'
                ]"
              >
                {{ tab.name }}
              </button>
            </nav>
          </div>
          
          <!-- Memory Configuration Tab -->
          <div v-if="activeDesignTab === 'memory'" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="glass-panel">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Long-Term Memory</h3>
                <div class="flex items-center">
                  <span class="mr-2 text-sm">{{ ltmExpanded ? 'Hide' : 'Show' }} Details</span>
                  <button @click="toggleLtmExpanded" class="p-1 rounded-md bg-dark-700 hover:bg-dark-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" :class="{'rotate-180': !ltmExpanded}">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="ltmExpanded" class="transition-all duration-300">
                <LongTermMemoryConfig :config="memoryConfig.longTerm" @update="updateLongTermMemory" />
              </div>
              <div v-else class="text-sm text-gray-400 mb-2">
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <span class="font-medium">Type:</span> {{ memoryConfig.longTerm.type.replace('_', ' ') }}
                  </div>
                  <div>
                    <span class="font-medium">Model:</span> {{ memoryConfig.longTerm.embeddingModel }}
                  </div>
                  <div>
                    <span class="font-medium">Connections:</span> {{ memoryConfig.longTerm.dataConnections.length }}
                  </div>
                  <div>
                    <span class="font-medium">Status:</span>
                    <span class="text-green-400">{{ memoryConfig.longTerm.enabled ? 'Enabled' : 'Disabled' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="glass-panel">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Short-Term Memory</h3>
                <div class="flex items-center">
                  <span class="mr-2 text-sm">{{ stmExpanded ? 'Hide' : 'Show' }} Details</span>
                  <button @click="toggleStmExpanded" class="p-1 rounded-md bg-dark-700 hover:bg-dark-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" :class="{'rotate-180': !stmExpanded}">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="stmExpanded" class="transition-all duration-300">
                <ShortTermMemoryConfig :config="memoryConfig.shortTerm" @update="updateShortTermMemory" />
              </div>
              <div v-else class="text-sm text-gray-400 mb-2">
                <div class="grid grid-cols-2 gap-2">
                  <div>
                    <span class="font-medium">Context Window:</span> {{ memoryConfig.shortTerm.contextWindow }}
                  </div>
                  <div>
                    <span class="font-medium">Connections:</span> {{ memoryConfig.shortTerm.liveConnections.length }}
                  </div>
                  <div>
                    <span class="font-medium">Status:</span>
                    <span class="text-green-400">{{ memoryConfig.shortTerm.enabled ? 'Enabled' : 'Disabled' }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Memory Inspector Panel from Test Environment -->
            <div class="glass-panel lg:col-span-2">
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-lg font-semibold">Memory Inspector</h3>
                <div class="flex items-center">
                  <span class="mr-2 text-sm">{{ inspectorExpanded ? 'Hide' : 'Show' }} Details</span>
                  <button @click="toggleInspectorExpanded" class="p-1 rounded-md bg-dark-700 hover:bg-dark-600 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" :class="{'rotate-180': !inspectorExpanded}">
                      <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="inspectorExpanded" class="transition-all duration-300">
                <MemoryInspector 
                  :longTermMemory="testEnvironment.longTermMemory"
                  :shortTermMemory="testEnvironment.shortTermMemory"
                  :sessionMemory="testEnvironment.sessionMemory"
                />
              </div>
              <div v-else class="text-sm text-gray-400">
                <p>View and monitor memory contents including long-term, short-term, and session memories.</p>
              </div>
            </div>
          </div>
          
          <!-- System Instructions Tab -->
          <div v-if="activeDesignTab === 'instructions'" class="space-y-6">
            <div class="glass-panel">
              <h3 class="text-lg font-semibold mb-4">System Instructions</h3>
              <SystemInstructionsEditor 
                :instructions="systemInstructions"
                :suggestedChanges="suggestedChanges"
                @update="updateSystemInstructions"
                @apply-changes="applyChanges"
                @select-content="createSuggestionFromSelection"
              />
            </div>
          </div>
          
          <!-- Routing Rules Tab -->
          <div v-if="activeDesignTab === 'routing'" class="space-y-6">
            <div class="glass-panel">
              <h3 class="text-lg font-semibold mb-4">Routing Rules</h3>
              <RoutingRulesEditor :rules="routingRules" @update="updateRoutingRules" />
            </div>
          </div>
          
          <!-- Testing Tab -->
          <div v-if="activeDesignTab === 'testing'" class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Left Column: Memory Insights -->
            <div class="lg:col-span-3">
              <MemoryInsights
                :memory-metrics="{
                  latency: 125,
                  relevance: 92,
                  utilization: 78
                }"
                :active-memory="[
                  { source: 'Product KB', content: 'CloudSync supports automatic file backup every 4 hours.', relevance: 92 },
                  { source: 'Technical Docs', content: 'CloudSync mobile requires background process permissions.', relevance: 78 },
                  { source: 'Customer History', content: 'User previously reported sync issues on mobile app.', relevance: 87 }
                ]"
                :optimization-suggestions="[
                  'Add Android permission guide to knowledge base for improved relevance',
                  'Increase weighting for technical documentation on mobile processes',
                  'Reference solution from previous ticket more explicitly in responses'
                ]"
              />
            </div>
            
            <!-- Middle Column: Chat Session -->
            <div class="lg:col-span-5">
              <div class="glass-panel">
                <h3 class="text-lg font-semibold mb-4 flex items-center justify-between">
                  <span>Chat Session</span>
                  <div class="flex items-center space-x-2">
                    <!-- Account Button -->
                    <div class="icon-wrapper">
                      <AccountDropdown @customer-selected="handleCustomerSelected" @add-customer="handleAddCustomer" />
                    </div>
                    
                    <!-- Contact Button -->
                    <div class="icon-wrapper">
                      <ContactDropdown @contact-selected="handleContactSelected" @create-contact="handleCreateContact" />
                    </div>
                    
                    <!-- Session Button -->
                    <div class="icon-wrapper">
                      <SessionDropdown @session-selected="handleSessionSelected" />
                    </div>
                    
                    <div 
                      v-for="rule in routingRules" 
                      :key="rule.id" 
                      class="tooltip cursor-pointer relative" 
                      :data-tip="`${rule.condition}: ${rule.value}`"
                    >
                      <div 
                        class="p-1.5 rounded-full transition-colors" 
                        :class="[
                          rule.active ? 'bg-dark-700' : 'bg-dark-800/60 border border-dark-600',
                          {
                            'text-amber-400 hover:bg-amber-900/30': rule.condition === 'Time of Day',
                            'text-green-400 hover:bg-green-900/30': rule.condition === 'Day of Week',
                            'text-indigo-400 hover:bg-indigo-900/30': rule.condition === 'User Type'
                          }
                        ]"
                        @click="toggleRuleInfoAndActive(rule.id)"
                      >
                        <svg v-if="rule.condition === 'Time of Day'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                        </svg>
                        <svg v-else-if="rule.condition === 'Day of Week'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                        </svg>
                        <svg v-else-if="rule.condition === 'User Type'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      
                      <!-- Rule Info Popup -->
                      <div 
                        v-if="activeInfoRule === rule.id" 
                        class="absolute right-0 mt-1 w-64 bg-dark-800 border border-dark-600 rounded-md shadow-lg z-10"
                        style="background-color: #1e293b; backdrop-filter: none;"
                        @click.stop
                      >
                        <div class="p-3">
                          <div class="flex justify-between items-center mb-2">
                            <h4 class="text-sm font-medium">Rule Details</h4>
                            <button @click.stop="activeInfoRule = null" class="text-dark-400 hover:text-dark-200">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                              </svg>
                            </button>
                          </div>
                          
                          <div class="space-y-3">
                            <!-- Rule info -->
                            <div>
                              <div class="mb-1 flex items-center">
                                <div class="w-6 h-6 rounded-full flex items-center justify-center mr-2"
                                  :class="{
                                    'bg-amber-700 text-amber-400': rule.condition === 'Time of Day',
                                    'bg-green-700 text-green-400': rule.condition === 'Day of Week',
                                    'bg-indigo-700 text-indigo-400': rule.condition === 'User Type'
                                  }"
                                >
                                  <svg v-if="rule.condition === 'Time of Day'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd" />
                                  </svg>
                                  <svg v-if="rule.condition === 'Day of Week'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                                  </svg>
                                  <svg v-if="rule.condition === 'User Type'" xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812a3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                                  </svg>
                                </div>
                                <div class="text-sm font-medium text-white">{{ rule.condition }}</div>
                              </div>
                              
                              <!-- Editable fields -->
                              <div class="mt-2 space-y-3">
                                <div>
                                  <label class="block text-xs text-dark-400 mb-1">Value</label>
                                  <input 
                                    v-model="rule.value" 
                                    type="text" 
                                    class="w-full bg-dark-700 border border-dark-600 rounded p-1.5 text-xs focus:border-primary-500 focus:outline-none"
                                  />
                                </div>
                                <div>
                                  <label class="block text-xs text-dark-400 mb-1">Action</label>
                                  <input 
                                    v-model="rule.action" 
                                    type="text" 
                                    class="w-full bg-dark-700 border border-dark-600 rounded p-1.5 text-xs focus:border-primary-500 focus:outline-none"
                                  />
                                </div>
                                <div class="flex items-center space-x-2">
                                  <label class="text-xs text-dark-400">Active</label>
                                  <button 
                                    @click.stop="toggleRuleActive(rule.id)" 
                                    :class="[
                                      'w-8 h-4 rounded-full transition-colors',
                                      rule.active ? 'bg-primary-600' : 'bg-dark-600'
                                    ]"
                                  >
                                    <div 
                                      class="w-3 h-3 bg-white rounded-full transform transition-transform" 
                                      :style="{ marginLeft: rule.active ? '18px' : '2px' }"
                                    ></div>
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                          
                          <div class="flex justify-end mt-3">
                            <button 
                              class="text-xs py-1 px-2 bg-dark-700 text-dark-300 rounded hover:bg-dark-600 flex items-center"
                              @click.stop="activeNavTab = 'design'; activeDesignTab = 'routing'; activeInfoRule = null"
                            >
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
                              </svg>
                              Configure All Rules
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </h3>
                <div class="p-4 border border-dark-600 rounded-lg bg-dark-800/50" style="background-color: #1e293b; backdrop-filter: none;">
                  <!-- System prompt instruction -->
                  <div class="mb-4 p-3 bg-dark-700/80 rounded-lg text-dark-300" style="background-color: #1c2536; backdrop-filter: none;">
                    <SimplifiedSystemInstructionsEditor 
                      :instructions="systemInstructions"
                      :suggestedChanges="suggestedChanges"
                      @update="updateSystemInstructions"
                      @apply-changes="applyChanges"
                      @select-content="createSuggestionFromSelection"
                    />
                  </div>
                  
              <ChatInterface 
                :messages="testEnvironment.messages"
                :highlighted-message-id="highlightedMessageId"
                @send-message="sendMessage"
                @select-message="selectMessage"
                @select-content="createSuggestionFromSelection"
              />
                </div>
              </div>
            </div>
            
            <!-- Right Column: Interaction Evaluation -->
            <div class="lg:col-span-4">
              <div class="glass-panel">
                <h3 class="text-lg font-semibold mb-4">Interaction Evaluation</h3>
                <InteractionEvaluation 
                  :evaluation="testEnvironment.evaluation"
                />
              </div>
              
              <!-- Message Flow Diagram in bottom right -->
              <div class="mt-4">
                <MessageFlowDiagram 
                  :selectedMessage="selectedMessageInfo"
                  :messages="testEnvironment.messages"
                  @update-selected-info="updateSelectedMessageInfo"
                  @select-message="selectMessage"
                  @highlight-message="highlightMessage"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Test environment tab content -->
    <div v-if="activeNavTab === 'test'" class="space-y-8">
      <div class="glass-card p-6">
        <h2 class="text-2xl font-bold mb-6">Agent Test Environment</h2>
        
        <div class="grid grid-cols-1 xl:grid-cols-12 gap-8">
          <!-- Memory Inspector Panel -->
          <div class="xl:col-span-3 space-y-4">
            <h3 class="text-xl font-semibold mb-4">Memory Inspector</h3>
            <MemoryInspector 
              :longTermMemory="testEnvironment.longTermMemory"
              :shortTermMemory="testEnvironment.shortTermMemory"
              :sessionMemory="testEnvironment.sessionMemory"
            />
          </div>
          
          <!-- Chat Interface -->
          <div class="xl:col-span-5 space-y-4">
            <h3 class="text-xl font-semibold mb-4">Chat Session</h3>
            <ChatInterface 
              :messages="testEnvironment.messages"
              :highlighted-message-id="highlightedMessageId"
              @send-message="sendMessage"
              @select-message="selectMessage"
              @select-content="createSuggestionFromSelection"
            />
          </div>

          <!-- Evaluation Metrics -->
          <div class="xl:col-span-4 space-y-4">
            <h3 class="text-xl font-semibold mb-4">Interaction Evaluation</h3>
            <InteractionEvaluation 
              :evaluation="testEnvironment.evaluation"
            />
          </div>
        </div>
      </div>
    </div>
    
    <!-- Analysis tab content -->
    <div v-if="activeNavTab === 'analysis'" class="space-y-8">
      <div class="glass-card p-6">
        <h2 class="text-2xl font-bold mb-6">Session Analysis</h2>
        
        <SessionAnalysis 
          :analysis="sessionAnalysis"
        />
      </div>
    </div>
  </div>
  
  <!-- New Application Modal -->
  <NewApplicationModal :show="showNewAppModal" @close="closeNewAppModal" />
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import NewApplicationModal from '../components/NewApplicationModal.vue';
import AIApplicationCard from '../components/AIApplicationCard.vue';
import MemoryArchitectureDiagram from '../components/MemoryArchitectureDiagram.vue';
import LongTermMemoryConfig from '../components/LongTermMemoryConfig.vue';
import ShortTermMemoryConfig from '../components/ShortTermMemoryConfig.vue';
import SystemInstructionsEditor from '../components/SystemInstructionsEditor.vue';
import SimplifiedSystemInstructionsEditor from '../components/SimplifiedSystemInstructionsEditor.vue';
import RoutingRulesEditor from '../components/RoutingRulesEditor.vue';
import MemoryInspector from '../components/MemoryInspector.vue';
import ChatInterface from '../components/ChatInterface.vue';
import InteractionEvaluation from '../components/InteractionEvaluation.vue';
import SessionAnalysis from '../components/SessionAnalysis.vue';
import MemoryInsights from '../components/MemoryInsights.vue';
import MessageFlowDiagram from '../components/MessageFlowDiagram.vue';
import AccountDropdown from '../components/AccountDropdown.vue';
import ContactDropdown from '../components/ContactDropdown.vue';
import SessionDropdown from '../components/SessionDropdown.vue';

// Navigation state
const activeNavTab = ref('design');
const navigationTabs = [
  { id: 'dashboard', name: 'Dashboard' },
  { id: 'design', name: 'Design Studio' },
  { id: 'test', name: 'Test Environment' },
  { id: 'analysis', name: 'Analysis' }
];

// Design Studio sub-tabs
const activeDesignTab = ref('memory');
const designTabs = [
  { id: 'memory', name: 'Memory Configuration' },
  { id: 'instructions', name: 'System Instructions' },
  { id: 'routing', name: 'Routing Rules' },
  { id: 'testing', name: 'Testing' }
];

// Modal state
const showNewAppModal = ref(false);

// Modal methods
const openNewAppModal = () => {
  showNewAppModal.value = true;
};

const closeNewAppModal = () => {
  showNewAppModal.value = false;
};

// Deployed apps data
const deployedApps = ref([
  {
    id: 1,
    name: 'Customer Support AI',
    status: 'Production',
    description: 'AI assistant for customer support inquiries and ticket routing',
    responseTime: '240ms',
    requests: '23,412',
    model: 'GPT-4',
    lastUpdated: '2 days ago'
  },
  {
    id: 2,
    name: 'Content Generator',
    status: 'Staging',
    description: 'Creates marketing content based on product specifications',
    responseTime: '320ms',
    requests: '5,123',
    model: 'GPT-3.5',
    lastUpdated: '1 week ago'
  },
  {
    id: 3,
    name: 'Document Analyzer',
    status: 'Development',
    description: 'Extracts insights and summaries from financial documents',
    responseTime: '450ms',
    requests: '1,240',
    model: 'Llama 2',
    lastUpdated: '3 days ago'
  },
  {
    id: 4,
    name: 'Image Generation API',
    status: 'Production',
    description: 'Creates product images from text descriptions',
    responseTime: '980ms',
    requests: '8,721',
    model: 'DALL-E 3',
    lastUpdated: '5 days ago'
  }
]);

// Memory configuration
const memoryConfig = ref({
  longTerm: {
    enabled: true,
    type: 'vector_database',
    embeddingModel: 'text-embedding-3-large',
    dataConnections: [
      { id: 1, name: 'Product Knowledge Base', type: 'document', status: 'active' },
      { id: 2, name: 'Customer Interactions', type: 'database', status: 'active' },
      { id: 3, name: 'Technical Documentation', type: 'document', status: 'inactive' }
    ]
  },
  shortTerm: {
    enabled: true,
    contextWindow: 10,
    liveConnections: [
      { id: 1, name: 'CRM API', type: 'api', status: 'active' },
      { id: 2, name: 'Order System', type: 'api', status: 'active' }
    ]
  }
});

// System instructions
const systemInstructions = ref(
  `You are a customer support assistant for TechCorp. 
  Your goal is to help users with product issues, answer questions, and create support tickets when necessary.
  
  # Guidelines:
  - Be friendly and professional
  - Ask clarifying questions when needed
  - If you can't resolve an issue, create a support ticket
  - Provide step-by-step troubleshooting when applicable
  
  # Available products:
  - TechWare Pro (software)
  - CloudSync (cloud service)
  - DeviceHub (hardware)
  
  # Support hours:
  - Monday to Friday: 9am to 6pm EST
  - Weekend: Limited support for emergency issues only`
);

// Routing rules
const routingRules = ref([
  { id: 1, condition: 'Time of Day', value: 'After Hours', action: 'Use after-hours greeting', active: true },
  { id: 2, condition: 'Day of Week', value: 'Weekend', action: 'Mention limited support', active: false },
  { id: 3, condition: 'User Type', value: 'Premium', action: 'Priority routing', active: true }
]);

// Test environment state
const testEnvironment = ref({
  longTermMemory: [
    { id: 1, source: 'Product KB', content: 'CloudSync supports automatic file backup every 4 hours.', relevance: 0.92 },
    { id: 2, source: 'Customer History', content: 'User previously reported sync issues on mobile app.', relevance: 0.87 },
    { id: 3, source: 'Technical Docs', content: 'CloudSync mobile requires background process permissions.', relevance: 0.78 }
  ],
  shortTermMemory: [
    { id: 1, source: 'CRM API', content: 'Customer tier: Premium', relevance: 0.95 },
    { id: 2, source: 'Order System', content: 'Recent purchase: CloudSync annual plan', relevance: 0.88 }
  ],
  sessionMemory: [
    { id: 1, content: 'User mentioned using Android version 12', source: 'Current Session', relevance: 0.96 }
  ],
  messages: [
    { 
      id: 1, 
      role: 'user', 
      content: 'Hi, my CloudSync mobile app keeps stopping the backup process.',
      device: 'mobile',
      modality: 'text'
    },
    { 
      id: 2, 
      role: 'assistant', 
      content: 'I see you\'re having trouble with CloudSync on your Android 12 device. Since you\'re a Premium customer, I\'ll prioritize this issue. Based on your history, you\'ve had sync issues before. The most common cause is background process permissions. Have you checked if CloudSync has permission to run in the background?',
      device: 'desktop',
      modality: 'text'
    },
    { 
      id: 3, 
      role: 'user', 
      content: 'No, how do I check that?',
      device: 'mobile',
      modality: 'text'
    }
  ],
  evaluation: {
    relevance: 92,
    accuracy: 88,
    helpfulness: 95,
    sentiment: 'Positive',
    suggestions: [
      'Consider adding a link to Android permission guide',
      'Reference solution from previous ticket more explicitly'
    ]
  }
});

// Session analysis
const sessionAnalysis = ref({
  sentiment: 'Positive (89%)',
  mainTopics: ['CloudSync', 'Mobile App', 'Permissions', 'Background Sync'],
  entities: [
    { type: 'Product', name: 'CloudSync', mentions: 3 },
    { type: 'OS', name: 'Android', mentions: 2 }
  ],
  suggestedImprovements: [
    'Add more specific Android version troubleshooting steps to knowledge base',
    'Update system prompt with mobile-specific instructions'
  ]
});

// Suggested changes
const suggestedChanges = ref({
  additions: [
    'Add specific instructions for mobile app troubleshooting',
    'Include permission check steps for different OS versions'
  ],
  removals: [],
  modifications: [
    'Clarify weekend support policy to mention response time expectations'
  ]
});

// Update methods
const updateLongTermMemory = (config) => {
  memoryConfig.value.longTerm = config;
};

const updateShortTermMemory = (config) => {
  memoryConfig.value.shortTerm = config;
};

const updateSystemInstructions = (instructions) => {
  systemInstructions.value = instructions;
};

const updateRoutingRules = (rules) => {
  routingRules.value = rules;
};

const applyChanges = () => {
  // Logic to apply suggested changes to system instructions
  console.log("Applying suggested changes to system instructions");
  // Implementation would merge the suggestions into the system instructions
};

// Add selectedMessageInfo to store the current message's metadata
const selectedMessageInfo = ref({
  role: 'user',
  device: 'mobile',
  modality: 'text'
});

// Update selected message info method
const updateSelectedMessageInfo = (info) => {
  selectedMessageInfo.value = { ...selectedMessageInfo.value, ...info };
};

// Method to handle message selection
const selectMessage = (message) => {
  // Extract metadata from message or use defaults
  const messageInfo = {
    role: message.role || 'user',
    device: message.device || 'mobile',
    modality: message.modality || 'text'
  };
  selectedMessageInfo.value = messageInfo;
};

// Update the sendMessage method to also set the selected message
const sendMessage = (message) => {
  // Add user message
  const newMessageId = testEnvironment.value.messages.length + 1;
  const userMessage = {
    id: newMessageId,
    role: 'user',
    content: message,
    device: 'mobile', // Default device for user
    modality: 'text'  // Default modality
  };
  
  testEnvironment.value.messages.push(userMessage);
  
  // Update selected message info to the user message
  updateSelectedMessageInfo({
    role: 'user',
    device: 'mobile',
    modality: 'text'
  });
  
  // Simulate assistant response after a short delay
  setTimeout(() => {
    const assistantMessage = {
      id: testEnvironment.value.messages.length + 1,
      role: 'assistant',
      content: 'This is a simulated response based on your message: "' + message + '". In a real implementation, this would call the AI model with the current context.',
      device: 'desktop', // Default device for assistant
      modality: 'text'   // Default modality
    };
    
    testEnvironment.value.messages.push(assistantMessage);
    
    // Update selected message info to the assistant response
    updateSelectedMessageInfo({
      role: 'assistant',
      device: 'desktop',
      modality: 'text'
    });
    
    // Update the evaluation metrics
    testEnvironment.value.evaluation = {
      relevance: Math.floor(Math.random() * 20) + 80,
      accuracy: Math.floor(Math.random() * 20) + 80,
      helpfulness: Math.floor(Math.random() * 20) + 80,
      sentiment: Math.random() > 0.7 ? 'Positive' : 'Neutral',
      suggestions: [
        'Consider providing more detailed response',
        'Reference relevant knowledge base articles'
      ]
    };
  }, 1000);
};

// Expanded state
const ltmExpanded = ref(false);
const stmExpanded = ref(false);
const inspectorExpanded = ref(false);
const showRoutingRulesDropdown = ref(false);
const activeInfoRule = ref(null);

// Toggle methods
const toggleLtmExpanded = () => {
  ltmExpanded.value = !ltmExpanded.value;
};

const toggleStmExpanded = () => {
  stmExpanded.value = !stmExpanded.value;
};

const toggleInspectorExpanded = () => {
  inspectorExpanded.value = !inspectorExpanded.value;
};

// New method to toggle rule active state
const toggleRuleActive = (ruleId) => {
  const rule = routingRules.value.find(r => r.id === ruleId);
  if (rule) {
    rule.active = !rule.active;
  }
};

// Method to handle both info display and click outside
const toggleRuleInfoAndActive = (ruleId) => {
  if (activeInfoRule.value === ruleId) {
    activeInfoRule.value = null; // Close if clicking same rule
  } else {
    activeInfoRule.value = ruleId; // Open new info panel
  }
};

// Initialize selected message on component mount
onMounted(() => {
  // Set up click outside handler for rules info panel
  document.addEventListener('click', (event) => {
    // Close info panel when clicking outside
    if (activeInfoRule.value !== null && !event.target.closest('.tooltip')) {
      activeInfoRule.value = null;
    }
  });
  
  // Initialize selectedMessageInfo with the last message data
  if (testEnvironment.value.messages.length > 0) {
    const lastMessage = testEnvironment.value.messages[testEnvironment.value.messages.length - 1];
    selectMessage(lastMessage);
  }
});

// Method to create suggestions from selected content
const createSuggestionFromSelection = (selectedText) => {
  if (!selectedText) return;
  
  // Create new suggestion
  const newSuggestion = {
    type: 'modification',
    content: selectedText,
    source: 'conversation'
  };
  
  // Add to suggested changes
  if (!suggestedChanges.value.modifications) {
    suggestedChanges.value.modifications = [];
  }
  
  suggestedChanges.value.modifications.push(selectedText);
  
  // Provide visual feedback
  console.log('Created suggestion from selected text:', selectedText);
};

// Add computed property to get active routing rules
const activeRoutingRules = computed(() => {
  return routingRules.value.filter(rule => rule.active);
});

// Add highlightedMessageId to track the currently highlighted message
const highlightedMessageId = ref(null);

// Method to handle message highlighting
const highlightMessage = (messageId) => {
  console.log('Highlighting message in chat:', messageId);
  highlightedMessageId.value = messageId;
  
  // Find the message element in the DOM and make sure it's visible
  setTimeout(() => {
    const messageElement = document.querySelector(`.highlighted-message`);
    if (messageElement) {
      console.log('Found highlighted message element, scrolling into view');
      messageElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      console.warn('Could not find highlighted message element in DOM');
    }
  }, 50);
  
  // Clear highlight after a short delay for visual effect
  setTimeout(() => {
    highlightedMessageId.value = null;
  }, 5000);
};

// Add new methods in script section:
const handleAccountOption = (optionId) => {
  console.log('Account option selected:', optionId);
};

const handleSignOut = () => {
  console.log('Sign out requested');
};

const handleCustomerSelected = (customer) => {
  console.log('Customer selected:', customer);
};

const handleAddCustomer = () => {
  console.log('Add new customer requested');
};

const handleContactSelected = (contactId) => {
  console.log('Contact selected:', contactId);
};

const handleCreateContact = () => {
  console.log('Create new contact requested');
};

const handleSessionSelected = (session) => {
  console.log('Session selected:', session);
};
</script>

<style scoped>
.glass-card {
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.3);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.glass-panel {
  background-color: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(71, 85, 105, 0.25);
  backdrop-filter: blur(8px);
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.2s ease;
}

.glass-panel:hover {
  background-color: rgba(30, 41, 59, 0.5);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
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

.icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Override dropdown buttons styles to match icon buttons */
.icon-wrapper :deep(.dropdown-wrapper button) {
  background: transparent;
  border: none;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  padding: 1.5px;
}

.icon-wrapper :deep(.dropdown-wrapper) {
  width: 100%;
  height: 100%;
}

/* Position dropdowns properly */
.icon-wrapper :deep(.dropdown-wrapper button) {
  background-color: rgba(30, 41, 59, 0.6);
  border: 1px solid #475569;
}

.icon-wrapper :deep(.dropdown-wrapper button:hover) {
  background-color: rgba(79, 70, 229, 0.2);
}
</style> 