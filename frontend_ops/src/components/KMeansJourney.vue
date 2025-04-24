<template>
  <div class="bg-dark-800 rounded-lg p-6 mb-8">
    <!-- Tab Navigation -->
    <div class="flex border-b border-gray-700 mb-8 overflow-x-auto">
      <button 
        class="px-6 py-3 font-medium text-sm transition-colors duration-200"
        :class="activeTab === 'kmeans' ? 'text-blue-400 border-b-2 border-blue-500' : 'text-gray-400 hover:text-gray-300'"
        @click="activeTab = 'kmeans'">
        K-means
      </button>
      <button 
        class="px-6 py-3 font-medium text-sm transition-colors duration-200"
        :class="activeTab === 'randomforest' ? 'text-blue-400 border-b-2 border-blue-500' : 'text-gray-400 hover:text-gray-300'"
        @click="activeTab = 'randomforest'">
        Random Forest
      </button>
      <button 
        class="px-6 py-3 font-medium text-sm transition-colors duration-200"
        :class="activeTab === 'gradient' ? 'text-blue-400 border-b-2 border-blue-500' : 'text-gray-400 hover:text-gray-300'"
        @click="activeTab = 'gradient'">
        Gradient Descent
      </button>
      <button 
        class="px-6 py-3 font-medium text-sm transition-colors duration-200"
        :class="activeTab === 'neural' ? 'text-blue-400 border-b-2 border-blue-500' : 'text-gray-400 hover:text-gray-300'"
        @click="activeTab = 'neural'">
        Neural Networks
      </button>
      <button 
        class="px-6 py-3 font-medium text-sm transition-colors duration-200"
        :class="activeTab === 'xgboost' ? 'text-blue-400 border-b-2 border-blue-500' : 'text-gray-400 hover:text-gray-300'"
        @click="activeTab = 'xgboost'">
        XGBoost
      </button>
    </div>
    
    <!-- K-means Tab Content -->
    <div v-if="activeTab === 'kmeans'">
      <h3 class="text-xl font-bold mb-4">K-means Model Development Journey</h3>
      <p class="mb-12">Follow this iterative workflow to develop, deploy and continuously improve your K-means clustering models.</p>
      
      <div class="flex flex-wrap justify-center">
        <!-- Circular diagram section -->
        <div class="relative w-full md:w-7/12 mx-auto" style="height: 600px; max-width: 600px;">
          <!-- Center circle -->
          <div class="absolute" style="left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 20;">
            <div class="bg-blue-800 rounded-full h-32 w-32 flex items-center justify-center border-2 border-blue-500 shadow-glow">
              <div class="text-center">
                <div class="text-blue-200 font-bold text-lg">K-means</div>
                <div class="text-xs text-blue-300">Continuous</div>
                <div class="text-xs text-blue-300">Improvement</div>
                <div class="text-xs text-blue-300">Cycle</div>
              </div>
            </div>
          </div>
          
          <!-- Step nodes -->
          <div v-for="(step, index) in kmeansSteps" :key="index" class="absolute transition-transform duration-200"
               :style="getNodePosition(index, kmeansSteps.length)"
               :class="{'z-30': activeStep === index, 'z-20': true, 'scale-105': activeStep === index}">
            <div class="bg-dark-700 rounded-lg p-3 border border-gray-600 cursor-pointer shadow-md w-44 hover:translate-y-[-2px] transition-all"
                 :class="{'border-blue-500 border-2': activeStep === index}"
                 @click="activeStep = index"
                 style="pointer-events: auto;">
              <div class="mb-1 flex items-center">
                <div class="bg-blue-800 text-blue-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">{{ index + 1 }}</div>
                <div class="font-bold text-sm">{{ step.title }}</div>
              </div>
              <p class="text-xs text-gray-400">{{ step.shortDesc }}</p>
            </div>
          </div>
          
          <!-- SVG for connections -->
          <svg class="absolute left-0 top-0 w-full h-full" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" style="z-index: 5; pointer-events: none;">
            <!-- Main circle -->
            <circle :cx="centerX" :cy="centerY" r="200" fill="none" stroke="#2d3748" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- Connection paths -->
            <g v-for="(step, index) in kmeansSteps" :key="`path-${index}`">
              <path 
                :d="getPathToNextNode(index, kmeansSteps.length)" 
                fill="none" 
                :stroke="activeStep === index ? '#3b82f6' : '#3b82f680'" 
                :stroke-width="activeStep === index ? 3 : 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="activeStep === index ? '0' : '5,5'"
                marker-end="url(#arrow-marker)"
              />
            </g>
            
            <!-- Arrow marker definition -->
            <defs>
              <marker id="arrow-marker" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
                <path d="M0,0 L0,8 L10,4 z" fill="#3b82f6" />
              </marker>
            </defs>
          </svg>
        </div>
        
        <!-- Right side detail panel -->
        <div class="w-full md:w-4/12 pl-0 md:pl-4">
          <div class="bg-dark-900 rounded-lg border border-dark-600 p-5 shadow-lg">
            <div class="flex items-start">
              <div class="bg-blue-800 text-blue-200 rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold mr-3 flex-shrink-0">{{ activeStep + 1 }}</div>
              <div>
                <h4 class="font-bold text-blue-300 mb-2 text-lg">{{ kmeansSteps[activeStep].title }}</h4>
                <p class="text-gray-300 mb-4">{{ kmeansSteps[activeStep].description }}</p>
                
                <ul class="mb-6 space-y-2">
                  <li v-for="(point, i) in kmeansSteps[activeStep].details" :key="i" class="flex items-start">
                    <span class="text-blue-400 mr-2 mt-1">•</span>
                    <span class="text-gray-300">{{ point }}</span>
                  </li>
                </ul>
                
                <div class="flex mt-4 text-sm">
                  <div class="bg-blue-900/30 border border-blue-800 rounded px-3 py-1 mr-3">
                    <span class="text-blue-400 font-medium">Time:</span>
                    <span class="text-gray-300 ml-1">{{ kmeansSteps[activeStep].time }}</span>
                  </div>
                  <div class="bg-blue-900/30 border border-blue-800 rounded px-3 py-1 flex-grow">
                    <span class="text-blue-400 font-medium">Output:</span>
                    <span class="text-gray-300 ml-1">{{ kmeansSteps[activeStep].output }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Random Forest Tab Content -->
    <div v-if="activeTab === 'randomforest'">
      <h3 class="text-xl font-bold mb-4">Random Forest Model Development Journey</h3>
      <p class="mb-12">Follow this iterative workflow to develop, deploy and continuously improve your Random Forest models for classification and regression tasks.</p>
      
      <div class="flex flex-wrap justify-center">
        <!-- Circular diagram section -->
        <div class="relative w-full md:w-7/12 mx-auto" style="height: 600px; max-width: 600px;">
          <!-- Center circle -->
          <div class="absolute" style="left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 20;">
            <div class="bg-green-800 rounded-full h-32 w-32 flex items-center justify-center border-2 border-green-500 shadow-glow-green">
              <div class="text-center">
                <div class="text-green-200 font-bold text-lg">Random</div>
                <div class="text-xs text-green-300">Forest</div>
                <div class="text-xs text-green-300">Development</div>
                <div class="text-xs text-green-300">Cycle</div>
              </div>
            </div>
          </div>
          
          <!-- Step nodes -->
          <div v-for="(step, index) in rfSteps" :key="index" class="absolute transition-transform duration-200"
               :style="getNodePosition(index, rfSteps.length)"
               :class="{'z-30': rfActiveStep === index, 'z-20': true, 'scale-105': rfActiveStep === index}">
            <div class="bg-dark-700 rounded-lg p-3 border border-gray-600 cursor-pointer shadow-md w-44 hover:translate-y-[-2px] transition-all"
                 :class="{'border-green-500 border-2': rfActiveStep === index}"
                 @click="rfActiveStep = index"
                 style="pointer-events: auto;">
              <div class="mb-1 flex items-center">
                <div class="bg-green-800 text-green-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">{{ index + 1 }}</div>
                <div class="font-bold text-sm">{{ step.title }}</div>
              </div>
              <p class="text-xs text-gray-400">{{ step.shortDesc }}</p>
            </div>
          </div>
          
          <!-- SVG for connections -->
          <svg class="absolute left-0 top-0 w-full h-full" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" style="z-index: 5; pointer-events: none;">
            <!-- Main circle -->
            <circle :cx="centerX" :cy="centerY" r="200" fill="none" stroke="#2d3748" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- Connection paths -->
            <g v-for="(step, index) in rfSteps" :key="`path-${index}`">
              <path 
                :d="getPathToNextNode(index, rfSteps.length)" 
                fill="none" 
                :stroke="rfActiveStep === index ? '#22c55e' : '#22c55e80'" 
                :stroke-width="rfActiveStep === index ? 3 : 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="rfActiveStep === index ? '0' : '5,5'"
                marker-end="url(#arrow-marker-green)"
              />
            </g>
            
            <!-- Arrow marker definition -->
            <defs>
              <marker id="arrow-marker-green" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
                <path d="M0,0 L0,8 L10,4 z" fill="#22c55e" />
              </marker>
            </defs>
          </svg>
        </div>
        
        <!-- Right side detail panel -->
        <div class="w-full md:w-4/12 pl-0 md:pl-4">
          <div class="bg-dark-900 rounded-lg border border-dark-600 p-5 shadow-lg">
            <div class="flex items-start">
              <div class="bg-green-800 text-green-200 rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold mr-3 flex-shrink-0">{{ rfActiveStep + 1 }}</div>
              <div>
                <h4 class="font-bold text-green-300 mb-2 text-lg">{{ rfSteps[rfActiveStep].title }}</h4>
                <p class="text-gray-300 mb-4">{{ rfSteps[rfActiveStep].description }}</p>
                
                <ul class="mb-6 space-y-2">
                  <li v-for="(point, i) in rfSteps[rfActiveStep].details" :key="i" class="flex items-start">
                    <span class="text-green-400 mr-2 mt-1">•</span>
                    <span class="text-gray-300">{{ point }}</span>
                  </li>
                </ul>
                
                <div class="flex mt-4 text-sm">
                  <div class="bg-green-900/30 border border-green-800 rounded px-3 py-1 mr-3">
                    <span class="text-green-400 font-medium">Time:</span>
                    <span class="text-gray-300 ml-1">{{ rfSteps[rfActiveStep].time }}</span>
                  </div>
                  <div class="bg-green-900/30 border border-green-800 rounded px-3 py-1 flex-grow">
                    <span class="text-green-400 font-medium">Output:</span>
                    <span class="text-gray-300 ml-1">{{ rfSteps[rfActiveStep].output }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Gradient Descent Tab Content -->
    <div v-if="activeTab === 'gradient'">
      <h3 class="text-xl font-bold mb-4">Gradient Descent Optimization Journey</h3>
      <p class="mb-12">Follow this iterative workflow to implement and optimize gradient descent algorithms for various machine learning tasks.</p>
      
      <div class="flex flex-wrap justify-center">
        <!-- Circular diagram section -->
        <div class="relative w-full md:w-7/12 mx-auto" style="height: 600px; max-width: 600px;">
          <!-- Center circle -->
          <div class="absolute" style="left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 20;">
            <div class="bg-purple-800 rounded-full h-32 w-32 flex items-center justify-center border-2 border-purple-500 shadow-glow-purple">
              <div class="text-center">
                <div class="text-purple-200 font-bold text-lg">Gradient</div>
                <div class="text-xs text-purple-300">Descent</div>
                <div class="text-xs text-purple-300">Optimization</div>
                <div class="text-xs text-purple-300">Cycle</div>
              </div>
            </div>
          </div>
          
          <!-- Step nodes -->
          <div v-for="(step, index) in gdSteps" :key="index" class="absolute transition-transform duration-200"
               :style="getNodePosition(index, gdSteps.length)"
               :class="{'z-30': gdActiveStep === index, 'z-20': true, 'scale-105': gdActiveStep === index}">
            <div class="bg-dark-700 rounded-lg p-3 border border-gray-600 cursor-pointer shadow-md w-44 hover:translate-y-[-2px] transition-all"
                 :class="{'border-purple-500 border-2': gdActiveStep === index}"
                 @click="gdActiveStep = index"
                 style="pointer-events: auto;">
              <div class="mb-1 flex items-center">
                <div class="bg-purple-800 text-purple-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">{{ index + 1 }}</div>
                <div class="font-bold text-sm">{{ step.title }}</div>
              </div>
              <p class="text-xs text-gray-400">{{ step.shortDesc }}</p>
            </div>
          </div>
          
          <!-- SVG for connections -->
          <svg class="absolute left-0 top-0 w-full h-full" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" style="z-index: 5; pointer-events: none;">
            <!-- Main circle -->
            <circle :cx="centerX" :cy="centerY" r="200" fill="none" stroke="#2d3748" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- Connection paths -->
            <g v-for="(step, index) in gdSteps" :key="`path-${index}`">
              <path 
                :d="getPathToNextNode(index, gdSteps.length)" 
                fill="none" 
                :stroke="gdActiveStep === index ? '#a855f7' : '#a855f780'" 
                :stroke-width="gdActiveStep === index ? 3 : 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="gdActiveStep === index ? '0' : '5,5'"
                marker-end="url(#arrow-marker-purple)"
              />
            </g>
            
            <!-- Arrow marker definition -->
            <defs>
              <marker id="arrow-marker-purple" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
                <path d="M0,0 L0,8 L10,4 z" fill="#a855f7" />
              </marker>
            </defs>
          </svg>
        </div>
        
        <!-- Right side detail panel -->
        <div class="w-full md:w-4/12 pl-0 md:pl-4">
          <div class="bg-dark-900 rounded-lg border border-dark-600 p-5 shadow-lg">
            <div class="flex items-start">
              <div class="bg-purple-800 text-purple-200 rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold mr-3 flex-shrink-0">{{ gdActiveStep + 1 }}</div>
              <div>
                <h4 class="font-bold text-purple-300 mb-2 text-lg">{{ gdSteps[gdActiveStep].title }}</h4>
                <p class="text-gray-300 mb-4">{{ gdSteps[gdActiveStep].description }}</p>
                
                <ul class="mb-6 space-y-2">
                  <li v-for="(point, i) in gdSteps[gdActiveStep].details" :key="i" class="flex items-start">
                    <span class="text-purple-400 mr-2 mt-1">•</span>
                    <span class="text-gray-300">{{ point }}</span>
                  </li>
                </ul>
                
                <div class="flex mt-4 text-sm">
                  <div class="bg-purple-900/30 border border-purple-800 rounded px-3 py-1 mr-3">
                    <span class="text-purple-400 font-medium">Time:</span>
                    <span class="text-gray-300 ml-1">{{ gdSteps[gdActiveStep].time }}</span>
                  </div>
                  <div class="bg-purple-900/30 border border-purple-800 rounded px-3 py-1 flex-grow">
                    <span class="text-purple-400 font-medium">Output:</span>
                    <span class="text-gray-300 ml-1">{{ gdSteps[gdActiveStep].output }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Neural Networks Tab Content -->
    <div v-if="activeTab === 'neural'">
      <h3 class="text-xl font-bold mb-4">Neural Network Development Journey</h3>
      <p class="mb-12">Follow this iterative workflow to design, train and deploy deep learning neural network models.</p>
      
      <div class="flex flex-wrap justify-center">
        <!-- Circular diagram section -->
        <div class="relative w-full md:w-7/12 mx-auto" style="height: 600px; max-width: 600px;">
          <!-- Center circle -->
          <div class="absolute" style="left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 20;">
            <div class="bg-rose-800 rounded-full h-32 w-32 flex items-center justify-center border-2 border-rose-500 shadow-glow-rose">
              <div class="text-center">
                <div class="text-rose-200 font-bold text-lg">Neural</div>
                <div class="text-xs text-rose-300">Network</div>
                <div class="text-xs text-rose-300">Development</div>
                <div class="text-xs text-rose-300">Cycle</div>
              </div>
            </div>
          </div>
          
          <!-- Step nodes -->
          <div v-for="(step, index) in nnSteps" :key="index" class="absolute transition-transform duration-200"
               :style="getNodePosition(index, nnSteps.length)"
               :class="{'z-30': nnActiveStep === index, 'z-20': true, 'scale-105': nnActiveStep === index}">
            <div class="bg-dark-700 rounded-lg p-3 border border-gray-600 cursor-pointer shadow-md w-44 hover:translate-y-[-2px] transition-all"
                 :class="{'border-rose-500 border-2': nnActiveStep === index}"
                 @click="nnActiveStep = index"
                 style="pointer-events: auto;">
              <div class="mb-1 flex items-center">
                <div class="bg-rose-800 text-rose-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">{{ index + 1 }}</div>
                <div class="font-bold text-sm">{{ step.title }}</div>
              </div>
              <p class="text-xs text-gray-400">{{ step.shortDesc }}</p>
            </div>
          </div>
          
          <!-- SVG for connections -->
          <svg class="absolute left-0 top-0 w-full h-full" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" style="z-index: 5; pointer-events: none;">
            <!-- Main circle -->
            <circle :cx="centerX" :cy="centerY" r="200" fill="none" stroke="#2d3748" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- Connection paths -->
            <g v-for="(step, index) in nnSteps" :key="`path-${index}`">
              <path 
                :d="getPathToNextNode(index, nnSteps.length)" 
                fill="none" 
                :stroke="nnActiveStep === index ? '#e11d48' : '#e11d4880'" 
                :stroke-width="nnActiveStep === index ? 3 : 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="nnActiveStep === index ? '0' : '5,5'"
                marker-end="url(#arrow-marker-rose)"
              />
            </g>
            
            <!-- Arrow marker definition -->
            <defs>
              <marker id="arrow-marker-rose" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
                <path d="M0,0 L0,8 L10,4 z" fill="#e11d48" />
              </marker>
            </defs>
          </svg>
        </div>
        
        <!-- Right side detail panel -->
        <div class="w-full md:w-4/12 pl-0 md:pl-4">
          <div class="bg-dark-900 rounded-lg border border-dark-600 p-5 shadow-lg">
            <div class="flex items-start">
              <div class="bg-rose-800 text-rose-200 rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold mr-3 flex-shrink-0">{{ nnActiveStep + 1 }}</div>
              <div>
                <h4 class="font-bold text-rose-300 mb-2 text-lg">{{ nnSteps[nnActiveStep].title }}</h4>
                <p class="text-gray-300 mb-4">{{ nnSteps[nnActiveStep].description }}</p>
                
                <ul class="mb-6 space-y-2">
                  <li v-for="(point, i) in nnSteps[nnActiveStep].details" :key="i" class="flex items-start">
                    <span class="text-rose-400 mr-2 mt-1">•</span>
                    <span class="text-gray-300">{{ point }}</span>
                  </li>
                </ul>
                
                <div class="flex mt-4 text-sm">
                  <div class="bg-rose-900/30 border border-rose-800 rounded px-3 py-1 mr-3">
                    <span class="text-rose-400 font-medium">Time:</span>
                    <span class="text-gray-300 ml-1">{{ nnSteps[nnActiveStep].time }}</span>
                  </div>
                  <div class="bg-rose-900/30 border border-rose-800 rounded px-3 py-1 flex-grow">
                    <span class="text-rose-400 font-medium">Output:</span>
                    <span class="text-gray-300 ml-1">{{ nnSteps[nnActiveStep].output }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- XGBoost Tab Content -->
    <div v-if="activeTab === 'xgboost'">
      <h3 class="text-xl font-bold mb-4">XGBoost Model Development Journey</h3>
      <p class="mb-12">Follow this iterative workflow to develop, tune and deploy gradient boosting models using XGBoost for high-performance predictions.</p>
      
      <div class="flex flex-wrap justify-center">
        <!-- Circular diagram section -->
        <div class="relative w-full md:w-7/12 mx-auto" style="height: 600px; max-width: 600px;">
          <!-- Center circle -->
          <div class="absolute" style="left: 50%; top: 50%; transform: translate(-50%, -50%); z-index: 20;">
            <div class="bg-amber-800 rounded-full h-32 w-32 flex items-center justify-center border-2 border-amber-500 shadow-glow-amber">
              <div class="text-center">
                <div class="text-amber-200 font-bold text-lg">XGBoost</div>
                <div class="text-xs text-amber-300">Gradient</div>
                <div class="text-xs text-amber-300">Boosting</div>
                <div class="text-xs text-amber-300">Cycle</div>
              </div>
            </div>
          </div>
          
          <!-- Step nodes -->
          <div v-for="(step, index) in xgbSteps" :key="index" class="absolute transition-transform duration-200"
               :style="getNodePosition(index, xgbSteps.length)"
               :class="{'z-30': xgbActiveStep === index, 'z-20': true, 'scale-105': xgbActiveStep === index}">
            <div class="bg-dark-700 rounded-lg p-3 border border-gray-600 cursor-pointer shadow-md w-44 hover:translate-y-[-2px] transition-all"
                 :class="{'border-amber-500 border-2': xgbActiveStep === index}"
                 @click="xgbActiveStep = index"
                 style="pointer-events: auto;">
              <div class="mb-1 flex items-center">
                <div class="bg-amber-800 text-amber-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold mr-2">{{ index + 1 }}</div>
                <div class="font-bold text-sm">{{ step.title }}</div>
              </div>
              <p class="text-xs text-gray-400">{{ step.shortDesc }}</p>
            </div>
          </div>
          
          <!-- SVG for connections -->
          <svg class="absolute left-0 top-0 w-full h-full" viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet" style="z-index: 5; pointer-events: none;">
            <!-- Main circle -->
            <circle :cx="centerX" :cy="centerY" r="200" fill="none" stroke="#2d3748" stroke-width="1" stroke-dasharray="5,5" />
            
            <!-- Connection paths -->
            <g v-for="(step, index) in xgbSteps" :key="`path-${index}`">
              <path 
                :d="getPathToNextNode(index, xgbSteps.length)" 
                fill="none" 
                :stroke="xgbActiveStep === index ? '#d97706' : '#d9770680'" 
                :stroke-width="xgbActiveStep === index ? 3 : 2"
                stroke-linecap="round"
                stroke-linejoin="round"
                :stroke-dasharray="xgbActiveStep === index ? '0' : '5,5'"
                marker-end="url(#arrow-marker-amber)"
              />
            </g>
            
            <!-- Arrow marker definition -->
            <defs>
              <marker id="arrow-marker-amber" markerWidth="10" markerHeight="8" refX="8" refY="4" orient="auto">
                <path d="M0,0 L0,8 L10,4 z" fill="#d97706" />
              </marker>
            </defs>
          </svg>
        </div>
        
        <!-- Right side detail panel -->
        <div class="w-full md:w-4/12 pl-0 md:pl-4">
          <div class="bg-dark-900 rounded-lg border border-dark-600 p-5 shadow-lg">
            <div class="flex items-start">
              <div class="bg-amber-800 text-amber-200 rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold mr-3 flex-shrink-0">{{ xgbActiveStep + 1 }}</div>
              <div>
                <h4 class="font-bold text-amber-300 mb-2 text-lg">{{ xgbSteps[xgbActiveStep].title }}</h4>
                <p class="text-gray-300 mb-4">{{ xgbSteps[xgbActiveStep].description }}</p>
                
                <ul class="mb-6 space-y-2">
                  <li v-for="(point, i) in xgbSteps[xgbActiveStep].details" :key="i" class="flex items-start">
                    <span class="text-amber-400 mr-2 mt-1">•</span>
                    <span class="text-gray-300">{{ point }}</span>
                  </li>
                </ul>
                
                <div class="flex mt-4 text-sm">
                  <div class="bg-amber-900/30 border border-amber-800 rounded px-3 py-1 mr-3">
                    <span class="text-amber-400 font-medium">Time:</span>
                    <span class="text-gray-300 ml-1">{{ xgbSteps[xgbActiveStep].time }}</span>
                  </div>
                  <div class="bg-amber-900/30 border border-amber-800 rounded px-3 py-1 flex-grow">
                    <span class="text-amber-400 font-medium">Output:</span>
                    <span class="text-gray-300 ml-1">{{ xgbSteps[xgbActiveStep].output }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KMeansJourney',
  data() {
    return {
      activeTab: 'kmeans',
      activeStep: 0,
      rfActiveStep: 0,
      gdActiveStep: 0,
      nnActiveStep: 0,
      xgbActiveStep: 0,
      centerX: 300,
      centerY: 300,
      kmeansSteps: [
        {
          title: "Data Preparation",
          shortDesc: "Prepare your data for clustering",
          description: "Prepare your data for clustering",
          details: [
            "Load and clean your customer data from Snowflake",
            "Handle missing values and outliers",
            "Perform feature selection for relevant attributes",
            "Scale numerical features (StandardScaler)",
            "Encode categorical features (OneHotEncoder)"
          ],
          time: "Day 1",
          output: "Preprocessed dataset ready for clustering"
        },
        {
          title: "Initial Clustering",
          shortDesc: "Run first experiment with baseline parameters",
          description: "Run first experiment with baseline parameters",
          details: [
            "Configure initial K-means with k=4 clusters",
            "Set random_state=42 for reproducibility",
            "Use k-means++ initialization for better starting centroids",
            "Train model and generate initial cluster assignments",
            "Log experiment details and parameters"
          ],
          time: "Day 2",
          output: "Initial cluster assignments & silhouette score"
        },
        {
          title: "Evaluate Results",
          shortDesc: "Analyze clustering quality and insights",
          description: "Analyze clustering quality and insights",
          details: [
            "Calculate silhouette score (0.61) and inertia metrics",
            "Visualize cluster distributions and separation",
            "Analyze cluster characteristics and business meaning",
            "Identify potential improvements for next experiment",
            "Document insights in the experiment tracking system"
          ],
          time: "Day 3 (AM)",
          output: "Cluster evaluation report & insights"
        },
        {
          title: "Hyperparameter Tuning",
          shortDesc: "Optimize k value and other parameters",
          description: "Optimize k value and other parameters",
          details: [
            "Run grid search over k values (3-8) to find optimal number",
            "Experiment with different initialization methods",
            "Test multiple distance metrics to improve separation",
            "Try different feature combinations",
            "Compare results using silhouette scores and business metrics"
          ],
          time: "Day 3 (PM)",
          output: "Optimized parameters (k=5, silhouette=0.68)"
        },
        {
          title: "Final Model Selection",
          shortDesc: "Compare models and select the best one",
          description: "Compare models and select the best one",
          details: [
            "Compare performance across all experiments",
            "Best model: k=5 with silhouette score of 0.68",
            "Evaluate cluster stability across random initializations",
            "Ensure clusters have meaningful business interpretation",
            "Prepare final model documentation and artifacts"
          ],
          time: "Day 4 (AM)",
          output: "Selected model with 5 meaningful clusters"
        },
        {
          title: "Model Deployment",
          shortDesc: "Deploy selected model to production",
          description: "Deploy selected model to production",
          details: [
            "Package model with preprocessing pipeline",
            "Register model in Snowflake model registry",
            "Create Snowflake UDF for inference",
            "Setup batch scoring procedure",
            "Configure monitoring for model performance"
          ],
          time: "Day 4 (PM)",
          output: "Deployed model as Snowflake UDF"
        },
        {
          title: "Performance Monitoring",
          shortDesc: "Track model performance in production",
          description: "Track model performance in production",
          details: [
            "Monitor silhouette score over time",
            "Track cluster distribution shifts",
            "Set up alerts for significant changes in metrics",
            "Collect feedback on cluster assignments",
            "Generate weekly performance reports"
          ],
          time: "Ongoing",
          output: "Performance dashboards & alerts"
        },
        {
          title: "Continuous Improvement",
          shortDesc: "Retrain model with new data insights",
          description: "Retrain model with new data insights",
          details: [
            "Incorporate new customer data monthly",
            "Apply feature improvements based on monitoring",
            "Adjust parameters based on business feedback",
            "Re-evaluate cluster definitions periodically",
            "Return to Step 1 to begin the next iteration"
          ],
          time: "Monthly",
          output: "Updated model version with improved accuracy"
        }
      ],
      rfSteps: [
        {
          title: "Data Preparation",
          shortDesc: "Prepare your data for the model",
          description: "Prepare your dataset for Random Forest modeling",
          details: [
            "Import data from your data warehouse",
            "Clean data and handle missing values",
            "Perform exploratory data analysis",
            "Engineer relevant features and transformations",
            "Split data into training, validation, and test sets"
          ],
          time: "Day 1",
          output: "Processed datasets ready for modeling"
        },
        {
          title: "Baseline Model",
          shortDesc: "Build initial Random Forest model",
          description: "Create a baseline Random Forest model",
          details: [
            "Configure Random Forest with default parameters",
            "Set n_estimators=100 for initial model",
            "Use random_state=42 for reproducibility",
            "Train model on training dataset",
            "Perform initial predictions and assessment"
          ],
          time: "Day 2 (AM)",
          output: "Baseline model with initial metrics"
        },
        {
          title: "Model Evaluation",
          shortDesc: "Evaluate model performance",
          description: "Assess model performance using appropriate metrics",
          details: [
            "Calculate accuracy, precision, recall for classification",
            "Measure RMSE, MAE, R² for regression tasks",
            "Generate confusion matrix for classification",
            "Plot feature importance to understand key drivers",
            "Identify potential areas for improvement"
          ],
          time: "Day 2 (PM)",
          output: "Performance report with visuals"
        },
        {
          title: "Hyperparameter Tuning",
          shortDesc: "Optimize model parameters",
          description: "Fine-tune Random Forest parameters for better performance",
          details: [
            "Perform grid search for optimal n_estimators (50-500)",
            "Tune max_depth to control tree complexity",
            "Optimize min_samples_split and min_samples_leaf",
            "Test different max_features settings",
            "Use cross-validation to prevent overfitting"
          ],
          time: "Day 3",
          output: "Optimized parameters for final model"
        },
        {
          title: "Feature Engineering",
          shortDesc: "Refine features for better results",
          description: "Enhance model with advanced feature engineering",
          details: [
            "Select optimal features using importance scores",
            "Create interaction features between key variables",
            "Test polynomial features for non-linear relationships",
            "Implement feature selection techniques",
            "Validate improved feature set with cross-validation"
          ],
          time: "Day 4 (AM)",
          output: "Enhanced feature set with improved metrics"
        },
        {
          title: "Model Deployment",
          shortDesc: "Deploy model to production",
          description: "Prepare and deploy the model to production",
          details: [
            "Package model with preprocessing pipeline",
            "Create serialized model artifacts",
            "Set up API endpoints for model serving",
            "Implement batch prediction capabilities",
            "Document deployment architecture"
          ],
          time: "Day 4 (PM)",
          output: "Production-ready model with documentation"
        },
        {
          title: "Performance Monitoring",
          shortDesc: "Monitor model in production",
          description: "Track model performance in production environment",
          details: [
            "Implement data drift detection",
            "Set up monitoring for prediction quality",
            "Create dashboards for key performance metrics",
            "Configure alerts for performance degradation",
            "Schedule regular performance reporting"
          ],
          time: "Weekly",
          output: "Monitoring system and performance reports"
        },
        {
          title: "Model Retraining",
          shortDesc: "Update model with new data",
          description: "Continuously improve model with new data",
          details: [
            "Collect new training data from production",
            "Evaluate model drift using performance metrics",
            "Retrain models with updated feature engineering",
            "Implement A/B testing for model versions",
            "Return to step 1 to refresh the development cycle"
          ],
          time: "Monthly",
          output: "Updated model with improved performance"
        }
      ],
      gdSteps: [
        {
          title: "Problem Definition",
          shortDesc: "Define the optimization problem",
          description: "Define the optimization problem and objective function",
          details: [
            "Identify the function to be minimized or maximized",
            "Define input parameters and expected outputs",
            "Establish the mathematical form of the cost function",
            "Determine constraints and boundary conditions",
            "Analyze the cost function's characteristics"
          ],
          time: "Day 1 (AM)",
          output: "Well-defined optimization problem statement"
        },
        {
          title: "Data Preparation",
          shortDesc: "Prepare data for training",
          description: "Prepare the data needed for optimization",
          details: [
            "Collect and clean training data points",
            "Normalize or standardize input features",
            "Establish baseline performance metrics",
            "Split data into training and validation sets",
            "Create visualization of the cost function landscape"
          ],
          time: "Day 1 (PM)",
          output: "Processed dataset for algorithm training"
        },
        {
          title: "Algorithm Selection",
          shortDesc: "Choose gradient descent variant",
          description: "Select the appropriate gradient descent algorithm variant",
          details: [
            "Compare standard gradient descent vs. stochastic methods",
            "Evaluate batch vs. mini-batch approaches",
            "Consider momentum-based acceleration techniques",
            "Assess adaptive learning rate methods (AdaGrad, RMSProp)",
            "Determine if second-order methods might be beneficial"
          ],
          time: "Day 2 (AM)",
          output: "Selected algorithm variant with justification"
        },
        {
          title: "Initial Implementation",
          shortDesc: "Implement baseline algorithm",
          description: "Create the first implementation of the selected algorithm",
          details: [
            "Code the cost function and gradient calculations",
            "Implement the update rules for parameters",
            "Set initial learning rate and hyperparameters",
            "Add convergence criteria and stopping conditions",
            "Create logging for intermediate optimization steps"
          ],
          time: "Day 2 (PM)",
          output: "Working baseline implementation"
        },
        {
          title: "Convergence Analysis",
          shortDesc: "Analyze algorithm convergence",
          description: "Analyze the algorithm's convergence properties",
          details: [
            "Plot the cost function reduction over iterations",
            "Evaluate the gradient magnitude over time",
            "Check for oscillations or pathological behavior",
            "Verify solution optimality using gradient tests",
            "Document convergence characteristics"
          ],
          time: "Day 3 (AM)",
          output: "Convergence analysis report"
        },
        {
          title: "Hyperparameter Tuning",
          shortDesc: "Optimize algorithm settings",
          description: "Fine-tune the algorithm's hyperparameters",
          details: [
            "Test different learning rate schedules",
            "Experiment with batch sizes (for SGD/mini-batch)",
            "Optimize momentum coefficients if applicable",
            "Tune specific parameters for adaptive methods",
            "Document impact on convergence speed and solution quality"
          ],
          time: "Day 3 (PM)",
          output: "Optimized hyperparameters configuration"
        },
        {
          title: "Performance Testing",
          shortDesc: "Test on varied problem instances",
          description: "Test algorithm performance across different scenarios",
          details: [
            "Evaluate performance on different initial conditions",
            "Test robustness to changes in problem characteristics",
            "Compare against other optimization methods",
            "Measure computational efficiency and scalability",
            "Document performance findings and limitations"
          ],
          time: "Day 4",
          output: "Performance evaluation report"
        },
        {
          title: "Implementation Refinement",
          shortDesc: "Refine and productionize",
          description: "Refine the algorithm implementation for production use",
          details: [
            "Optimize code for better performance",
            "Add robust error handling and edge cases",
            "Incorporate early stopping mechanisms",
            "Package algorithm for reusability",
            "Document API and usage patterns"
          ],
          time: "Day 5",
          output: "Production-ready gradient descent implementation"
        }
      ],
      nnSteps: [
        {
          title: "Problem Definition",
          shortDesc: "Define neural network task",
          description: "Define the problem and neural network objectives",
          details: [
            "Identify task type (classification, regression, etc.)",
            "Define input data structure and dimensions",
            "Establish target outputs and format",
            "Determine evaluation metrics for success",
            "Set performance goals and constraints"
          ],
          time: "Day 1 (AM)",
          output: "Clear problem definition document"
        },
        {
          title: "Data Preparation",
          shortDesc: "Prepare data for network",
          description: "Process data for neural network training",
          details: [
            "Collect and clean relevant training data",
            "Normalize or standardize input features",
            "Encode categorical variables appropriately",
            "Split data into training, validation, and test sets",
            "Implement data augmentation if applicable"
          ],
          time: "Day 1 (PM)",
          output: "Processed datasets ready for training"
        },
        {
          title: "Architecture Design",
          shortDesc: "Design network structure",
          description: "Design the neural network architecture",
          details: [
            "Determine network type (CNN, RNN, Transformer, etc.)",
            "Select activation functions for each layer",
            "Define layer structure and dimensions",
            "Consider skip connections or special blocks",
            "Design input and output processing layers"
          ],
          time: "Day 2 (AM)",
          output: "Detailed network architecture diagram"
        },
        {
          title: "Initial Training",
          shortDesc: "Perform first training run",
          description: "Train initial version of the neural network",
          details: [
            "Initialize weights using appropriate strategy",
            "Set initial learning rate and optimizer",
            "Configure batch size and number of epochs",
            "Implement training loop with validation",
            "Monitor initial metrics and learning curves"
          ],
          time: "Day 2 (PM)",
          output: "Baseline model with initial metrics"
        },
        {
          title: "Error Analysis",
          shortDesc: "Analyze model performance",
          description: "Analyze model errors and performance",
          details: [
            "Evaluate performance on validation dataset",
            "Identify patterns in incorrect predictions",
            "Assess overfitting or underfitting issues",
            "Analyze feature importance or attention patterns",
            "Identify potential architecture improvements"
          ],
          time: "Day 3 (AM)",
          output: "Error analysis report with visuals"
        },
        {
          title: "Hyperparameter Tuning",
          shortDesc: "Optimize model settings",
          description: "Tune hyperparameters for better performance",
          details: [
            "Test different learning rates and schedules",
            "Experiment with various optimizers (Adam, SGD)",
            "Tune regularization parameters (dropout, L2)",
            "Adjust batch size and training epochs",
            "Consider learning rate warmup and decay"
          ],
          time: "Day 3 (PM)",
          output: "Optimized hyperparameter configuration"
        },
        {
          title: "Model Deployment",
          shortDesc: "Deploy model to production",
          description: "Deploy the neural network to production",
          details: [
            "Export model to deployment format (ONNX, TensorRT)",
            "Optimize model for inference (quantization, pruning)",
            "Set up API endpoints for model serving",
            "Implement batch prediction capabilities",
            "Document deployment architecture and limitations"
          ],
          time: "Day 4",
          output: "Deployed model with serving infrastructure"
        },
        {
          title: "Continuous Improvement",
          shortDesc: "Iterate and enhance",
          description: "Continuously improve the neural network",
          details: [
            "Monitor model performance in production",
            "Collect new training data from real usage",
            "Implement A/B testing for model versions",
            "Explore transfer learning from newer architectures",
            "Update model to address shifting data patterns"
          ],
          time: "Ongoing",
          output: "Improved model versions with better metrics"
        }
      ],
      xgbSteps: [
        {
          title: "Problem Framing",
          shortDesc: "Define the prediction task",
          description: "Define the prediction problem for XGBoost",
          details: [
            "Identify prediction task type (classification/regression)",
            "Define business problem and success criteria",
            "Determine appropriate evaluation metrics",
            "Set performance targets and constraints",
            "Analyze data availability and characteristics"
          ],
          time: "Day 1 (AM)",
          output: "Problem specification document"
        },
        {
          title: "Data Preparation",
          shortDesc: "Prepare data for XGBoost",
          description: "Process data for XGBoost modeling",
          details: [
            "Extract features from raw data sources",
            "Handle missing values appropriately",
            "Encode categorical variables (one-hot, target)",
            "Create feature transformations as needed",
            "Split data into training, validation and test sets"
          ],
          time: "Day 1 (PM)",
          output: "Processed datasets with feature matrix"
        },
        {
          title: "Baseline Model",
          shortDesc: "Build initial XGBoost model",
          description: "Create a baseline XGBoost model",
          details: [
            "Configure basic XGBoost parameters",
            "Set default tree structure parameters",
            "Initialize learning rate and regularization",
            "Train first model with early stopping",
            "Evaluate baseline performance metrics"
          ],
          time: "Day 2 (AM)",
          output: "Baseline model with initial performance"
        },
        {
          title: "Feature Importance",
          shortDesc: "Analyze feature importance",
          description: "Analyze feature importance and selection",
          details: [
            "Calculate gain-based feature importance",
            "Generate permutation importance metrics",
            "Visualize importance distributions",
            "Identify and remove irrelevant features",
            "Document key predictive features"
          ],
          time: "Day 2 (PM)",
          output: "Feature importance analysis and visuals"
        },
        {
          title: "Hyperparameter Tuning",
          shortDesc: "Optimize XGBoost parameters",
          description: "Tune XGBoost hyperparameters",
          details: [
            "Optimize tree structure (max_depth, min_child_weight)",
            "Tune regularization parameters (gamma, lambda)",
            "Find optimal learning rate and n_estimators",
            "Adjust subsampling and column sampling rates",
            "Use cross-validation for robust evaluation"
          ],
          time: "Day 3",
          output: "Optimized parameter configuration"
        },
        {
          title: "Model Validation",
          shortDesc: "Validate model performance",
          description: "Thoroughly validate model performance",
          details: [
            "Evaluate on holdout test data",
            "Analyze error distributions and patterns",
            "Check for overfitting or underfitting",
            "Compare against other modeling approaches",
            "Assess performance across data segments"
          ],
          time: "Day 4 (AM)",
          output: "Validation report with performance metrics"
        },
        {
          title: "Model Deployment",
          shortDesc: "Deploy model to production",
          description: "Deploy XGBoost model to production",
          details: [
            "Export model in serialized format",
            "Set up batch prediction pipeline",
            "Implement real-time API if needed",
            "Configure monitoring for model health",
            "Document deployment architecture"
          ],
          time: "Day 4 (PM)",
          output: "Deployed model with serving capabilities"
        },
        {
          title: "Performance Monitoring",
          shortDesc: "Monitor production performance",
          description: "Monitor and maintain model in production",
          details: [
            "Track prediction quality metrics over time",
            "Monitor data drift and concept drift",
            "Set up alerts for performance degradation",
            "Collect feedback for model improvements",
            "Schedule regular model retraining"
          ],
          time: "Ongoing",
          output: "Monitoring dashboards and reports"
        }
      ]
    };
  },
  methods: {
    // Get position for each node
    getNodePosition(index, total) {
      const radius = 230; // Increased radius for better spacing
      // Start at the top position (π * 1.5 or -π/2)
      const angle = (Math.PI * 2 * index) / total - Math.PI / 2;
      
      // Calculate positions
      const x = this.centerX + Math.cos(angle) * radius;
      const y = this.centerY + Math.sin(angle) * radius;
      
      // Adjust for node size (offset from center)
      const nodeWidth = 176; // w-44 = 11rem = 176px
      const nodeHeight = 70; // approximate height
      
      // Special adjustment for the Final Model Selection (#5) node at the bottom
      let adjustedY = y;
      if (index === 4) { // Final Model Selection (index 4 = 5th item)
        adjustedY = y + 15; // Push it down slightly to avoid overlap
      }
      
      return {
        left: `${x - nodeWidth/2}px`,
        top: `${adjustedY - nodeHeight/2}px`
      };
    },
    
    // Create SVG path between nodes
    getPathToNextNode(index, total) {
      // Skip the path that would directly connect to Final Model Selection from node 3/4
      const nextIndex = (index + 1) % total;
      
      const radius = 230;
      const nodeRadius = 260;
      const centerRadius = 65; // Center circle radius + buffer
      
      // Current and next node angles
      const currentAngle = (Math.PI * 2 * index) / total - Math.PI / 2;
      const nextAngle = (Math.PI * 2 * nextIndex) / total - Math.PI / 2;
      
      // Start and end points (slightly away from node centers)
      const startX = this.centerX + Math.cos(currentAngle) * nodeRadius;
      const startY = this.centerY + Math.sin(currentAngle) * nodeRadius;
      
      const endX = this.centerX + Math.cos(nextAngle) * nodeRadius;
      const endY = this.centerY + Math.sin(nextAngle) * nodeRadius;
      
      // Control point (inside the circle)
      const midAngle = (currentAngle + nextAngle) / 2;
      const controlX = this.centerX + Math.cos(midAngle) * centerRadius;
      const controlY = this.centerY + Math.sin(midAngle) * centerRadius;
      
      // Special handling for paths to/from Final Model Selection
      if (index === 3 || nextIndex === 4) { // Path from node 4 to node 5
        const controlY2 = this.centerY + Math.sin(midAngle) * (centerRadius + 40);
        return `M ${startX} ${startY} Q ${controlX} ${controlY2} ${endX} ${endY}`;
      }
      
      // Create a quadratic Bézier curve
      return `M ${startX} ${startY} Q ${controlX} ${controlY} ${endX} ${endY}`;
    }
  }
};
</script>

<style scoped>
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.shadow-glow {
  box-shadow: 0 0 15px rgba(37, 99, 235, 0.4);
  animation: pulse-blue 3s infinite;
}

.shadow-glow-green {
  box-shadow: 0 0 15px rgba(22, 163, 74, 0.4);
  animation: pulse-green 3s infinite;
}

.shadow-glow-purple {
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
  animation: pulse-purple 3s infinite;
}

.shadow-glow-rose {
  box-shadow: 0 0 15px rgba(225, 29, 72, 0.4);
  animation: pulse-rose 3s infinite;
}

.shadow-glow-amber {
  box-shadow: 0 0 15px rgba(217, 119, 6, 0.4);
  animation: pulse-amber 3s infinite;
}

@keyframes pulse-blue {
  0% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.6); }
  50% { box-shadow: 0 0 20px rgba(37, 99, 235, 0.8); }
  100% { box-shadow: 0 0 5px rgba(37, 99, 235, 0.6); }
}

@keyframes pulse-green {
  0% { box-shadow: 0 0 5px rgba(22, 163, 74, 0.6); }
  50% { box-shadow: 0 0 20px rgba(22, 163, 74, 0.8); }
  100% { box-shadow: 0 0 5px rgba(22, 163, 74, 0.6); }
}

@keyframes pulse-purple {
  0% { box-shadow: 0 0 5px rgba(168, 85, 247, 0.6); }
  50% { box-shadow: 0 0 20px rgba(168, 85, 247, 0.8); }
  100% { box-shadow: 0 0 5px rgba(168, 85, 247, 0.6); }
}

@keyframes pulse-rose {
  0% { box-shadow: 0 0 5px rgba(225, 29, 72, 0.6); }
  50% { box-shadow: 0 0 20px rgba(225, 29, 72, 0.8); }
  100% { box-shadow: 0 0 5px rgba(225, 29, 72, 0.6); }
}

@keyframes pulse-amber {
  0% { box-shadow: 0 0 5px rgba(217, 119, 6, 0.6); }
  50% { box-shadow: 0 0 20px rgba(217, 119, 6, 0.8); }
  100% { box-shadow: 0 0 5px rgba(217, 119, 6, 0.6); }
}

/* Dark theme text colors */
.bg-dark-700 {
  background-color: #1e293b;
}

.bg-dark-800 {
  background-color: #0f172a;
}

.bg-dark-900 {
  background-color: #0c1425;
}

.border-dark-600 {
  border-color: #334155;
}
</style> 