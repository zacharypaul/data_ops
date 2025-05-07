<template>
  <div class="relative mb-8">
    <div class="text-center mb-8 relative">
      <div class="flex items-center justify-center">
        <h3 class="text-xl font-semibold mb-2">AI Memory Architecture</h3>
        <button @click="showInfoModal = true" class="ml-2 text-gray-400 hover:text-primary-400 transition-colors focus:outline-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <p class="text-gray-400">Configure how your AI agent stores and retrieves information</p>
    </div>
    
    <!-- Brain diagram with memory regions -->
    <div class="relative w-full mx-auto h-[600px]">
      <!-- Container for brain image -->
      <div class="absolute inset-0 flex items-center justify-center">
        <!-- Original Brain SVG -->
        <div class="brain-container w-full h-full relative">
          <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 1280 1090" class="brain-svg"
            preserveAspectRatio="xMidYMid meet">
            <defs>
              <!-- Purple glow filter -->
              <filter id="brain-glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="15" result="blur" />
                <feFlood flood-color="#a855f7" flood-opacity="0.8" result="color"/>
                <feComposite in="color" in2="blur" operator="in" result="coloredBlur"/>
                <feComposite in="SourceGraphic" in2="coloredBlur" operator="over" />
              </filter>
              
              <!-- Neural network nodes gradient -->
              <radialGradient id="node-gradient" cx="50%" cy="50%" r="50%" fx="50%" fy="50%">
                <stop offset="0%" stop-color="#ffffff" />
                <stop offset="30%" stop-color="#e9d5ff" />
                <stop offset="100%" stop-color="#a855f7" />
              </radialGradient>
              
              <!-- Neural lighting effect -->
              <filter id="neural-lighting" x="-10%" y="-10%" width="120%" height="120%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feFlood flood-color="#e9d5ff" flood-opacity="0.9" result="color"/>
                <feComposite in="color" in2="blur" operator="in" result="glow"/>
                <feComposite in="SourceGraphic" in2="glow" operator="over" />
              </filter>
              
              <!-- Focal point glow -->
              <filter id="focal-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="10" result="blur" />
                <feFlood flood-color="#a855f7" flood-opacity="1" result="color"/>
                <feComposite in="color" in2="blur" operator="in" result="glow"/>
                <feComposite in="SourceGraphic" in2="glow" operator="over" />
              </filter>
            </defs>
            
            <!-- Brain path from original SVG -->
            <g transform="translate(0.000000,1090.000000) scale(0.100000,-0.100000)"
              fill="#1e1b4b" stroke="#e9d5ff" stroke-width="20" filter="url(#brain-glow)">
              <path d="M6277 10879 c-76 -10 -184 -30 -240 -42 -98 -23 -104 -23 -187 -8
                -63 11 -157 15 -360 15 -244 0 -290 -2 -405 -23 -148 -26 -268 -56 -423 -105
                -99 -31 -113 -33 -177 -25 -117 14 -440 10 -575 -6 -462 -57 -912 -251 -1255
                -540 -33 -28 -68 -57 -79 -65 -14 -11 -44 -14 -120 -12 -126 4 -218 -18 -348
                -83 -204 -101 -394 -250 -633 -496 -273 -281 -509 -510 -582 -568 -40 -31
                -102 -78 -139 -106 -174 -131 -349 -397 -464 -705 -24 -63 -74 -172 -112 -241
                -38 -69 -85 -170 -105 -225 -32 -88 -36 -112 -41 -220 -5 -137 6 -185 59 -270
                l31 -48 -36 -72 c-40 -79 -86 -242 -86 -303 0 -54 43 -243 75 -326 57 -153
                174 -342 303 -494 80 -92 80 -94 105 -196 57 -232 157 -411 323 -580 284 -290
                713 -491 1289 -605 61 -12 115 -26 120 -30 6 -5 17 -26 24 -47 20 -56 70 -129
                138 -203 58 -62 61 -69 72 -137 6 -39 15 -83 21 -98 5 -14 10 -69 10 -120 0
                -110 13 -151 75 -240 75 -106 149 -169 350 -295 71 -45 166 -110 210 -144 357
                -279 724 -443 1149 -516 153 -26 763 -39 931 -20 130 14 419 61 559 90 148 30
                134 37 200 -96 109 -219 287 -449 442 -574 136 -110 148 -124 271 -332 252
                -424 540 -958 627 -1163 120 -283 223 -422 381 -517 82 -49 205 -92 247 -85
                89 13 195 39 215 52 59 39 72 147 34 292 -11 45 -64 204 -116 354 -101 287
                -118 355 -93 364 8 3 61 -5 119 -19 234 -55 313 -66 482 -66 89 0 200 -4 247
                -10 320 -35 422 -32 689 21 374 75 609 146 803 243 338 170 590 435 644 676
                13 56 26 81 67 132 65 82 83 125 104 244 16 96 16 102 -4 193 -12 52 -19 99
                -17 106 4 8 57 14 173 19 267 10 445 49 637 140 383 181 652 556 789 1096 61
                242 109 654 102 883 -17 556 -63 1001 -133 1282 -58 233 -152 451 -244 563
                -43 53 -58 82 -92 185 -107 324 -290 605 -472 725 -39 26 -76 58 -83 72 -7 14
                -13 52 -13 86 0 159 -76 399 -180 570 -135 221 -376 455 -621 601 -77 47 -79
                49 -99 108 -30 91 -82 171 -182 281 -50 54 -129 151 -176 214 -100 135 -303
                340 -420 425 -342 248 -749 429 -1227 545 -99 24 -227 64 -305 95 -336 133
                -595 186 -941 190 l-205 3 -70 35 c-308 154 -721 223 -1057 176z" />
            </g>
            
            <!-- Neural network nodes -->
            <g class="neural-nodes" filter="url(#neural-lighting)"></g>
            
            <!-- Neural connections -->
            <g class="neural-connections" stroke="#a78bfa" stroke-opacity="0.3" stroke-width="1"></g>
            
            <!-- Focal points for memory regions -->
            <g class="focal-points">
              <!-- Short-Term Memory node -->
              <circle cx="420" cy="400" r="24" fill="url(#node-gradient)" filter="url(#focal-glow)" class="pulse-slow" />
              
              <!-- Long-Term Memory node -->
              <circle cx="820" cy="380" r="24" fill="url(#node-gradient)" filter="url(#focal-glow)" class="pulse-slow" />
              
              <!-- Analytical Intelligence node -->
              <circle cx="360" cy="250" r="24" fill="url(#node-gradient)" filter="url(#focal-glow)" class="pulse-slow" />
              
              <!-- Speech Generation node -->
              <circle cx="700" cy="600" r="24" fill="url(#node-gradient)" filter="url(#focal-glow)" class="pulse-slow" />
              
              <!-- Cross-Memory Integration node -->
              <circle cx="610" cy="440" r="24" fill="url(#node-gradient)" filter="url(#focal-glow)" class="pulse-slow" />
            </g>
          </svg>
        </div>
      </div>
      
      <!-- Labels positioned absolutely -->
      <div class="absolute inset-0">
        <!-- Analytical Thinking - Upper left -->
        <div class="absolute top-[-8%] left-[5%]">
          <div class="p-3 rounded-lg brain-label bg-dark-800/90 border border-cyan-500/50 shadow-glow-cyan">
            <div class="font-bold text-sm text-cyan-400 mb-1">Analytical Intelligence</div>
            <table class="w-full text-xs">
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Human IQ:</td>
                <td class="py-1">Problem solving & logical reasoning</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">AI Tools:</td>
                <td class="py-1">Function calling & API integrations</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Evolution:</td>
                <td class="py-1">Tool use correlates with higher intelligence</td>
              </tr>
              <tr>
                <td class="py-1 pr-2 font-medium">Pitfalls:</td>
                <td class="py-1">Reasoning errors<br>Hallucinations</td>
              </tr>
            </table>
          </div>
        </div>
        
        <!-- Short-Term Memory - Left side -->
        <div class="absolute top-[38%] left-[5%]">
          <div class="p-3 rounded-lg brain-label bg-dark-800/90 border border-purple-500/50 shadow-glow-purple">
            <div class="font-bold text-sm text-purple-400 mb-1">Short-Term Memory</div>
            <table class="w-full text-xs">
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Storage:</td>
                <td class="py-1">Context window</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Input:</td>
                <td class="py-1">Recent interactions</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Access:</td>
                <td class="py-1">Live API connections</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Process:</td>
                <td class="py-1">Working memory</td>
              </tr>
              <tr>
                <td class="py-1 pr-2 font-medium">Pitfalls:</td>
                <td class="py-1">Limited capacity<br>Context loss</td>
              </tr>
            </table>
          </div>
        </div>
        
        <!-- Long-Term Memory - Right side -->
        <div class="absolute top-[5%] right-[5%]">
          <div class="p-3 rounded-lg brain-label bg-dark-800/90 border border-blue-500/50 shadow-glow-blue">
            <div class="font-bold text-sm text-blue-400 mb-1">Long-Term Memory</div>
            <table class="w-full text-xs">
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Storage:</td>
                <td class="py-1">Vector databases</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Source:</td>
                <td class="py-1">Knowledge bases</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Index:</td>
                <td class="py-1">Document indexes</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Process:</td>
                <td class="py-1">Embedding models</td>
              </tr>
              <tr>
                <td class="py-1 pr-2 font-medium">Pitfalls:</td>
                <td class="py-1">Retrieval inaccuracy<br>Outdated info</td>
              </tr>
            </table>
          </div>
        </div>
        
        <!-- Speech Generation - Bottom right -->
        <div class="absolute top-[60%] right-[5%]">
          <div class="p-3 rounded-lg brain-label bg-dark-800/90 border border-amber-500/50 shadow-glow-amber">
            <div class="font-bold text-sm text-amber-400 mb-1">Speech Generation</div>
            <table class="w-full text-xs">
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Human:</td>
                <td class="py-1">Formulates fluent, contextual speech</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">AI:</td>
                <td class="py-1">Natural language generation models</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Uncanny:</td>
                <td class="py-1">Too perfect or stilted responses</td>
              </tr>
              <tr>
                <td class="py-1 pr-2 font-medium">Pitfalls:</td>
                <td class="py-1">Voice inconsistency<br>Unnatural phrasing</td>
              </tr>
            </table>
          </div>
        </div>
        
        <!-- Cross-Memory Integration - Bottom left -->
        <div class="absolute top-[75%] left-[5%]">
          <div class="p-3 rounded-lg brain-label bg-dark-800/90 border border-green-500/50 shadow-glow-green" style="max-width: 240px;">
            <div class="font-bold text-sm text-green-400 mb-2">Cross-Memory Integration</div>
            <table class="w-full text-xs">
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Function:</td>
                <td class="py-1">Connect LTM & STM systems</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Components:</td>
                <td class="py-1">Live API connections, similarity search</td>
              </tr>
              <tr class="border-b border-dark-600">
                <td class="py-1 pr-2 font-medium">Output:</td>
                <td class="py-1">Relevance-ranked results</td>
              </tr>
              <tr>
                <td class="py-1 pr-2 font-medium">Pitfalls:</td>
                <td class="py-1">Query misalignment<br>Retrieval latency</td>
              </tr>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Info Modal -->
    <div v-if="showInfoModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <!-- Background overlay -->
        <div class="fixed inset-0 bg-dark-900 bg-opacity-75 transition-opacity" aria-hidden="true" @click="showInfoModal = false"></div>

        <!-- Modal panel -->
        <div class="inline-block align-bottom bg-dark-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
          <div class="bg-dark-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-200" id="modal-title">
                  AI Memory Architecture Details
                </h3>
                <div class="mt-4 max-h-[70vh] overflow-y-auto">
                  <div class="mb-6">
                    <h4 class="text-md font-semibold text-primary-400 mb-2">Pictured Regions</h4>
                    <div class="overflow-x-auto">
                      <table class="min-w-full divide-y divide-dark-600">
                        <thead>
                          <tr>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Label</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Color</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Brain region (approx.)</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Why here?</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-dark-700">
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Analytical Intelligence</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-cyan-400">Cyan</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Upper-left (frontal / parietal area)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Mirrors the human pre-frontal & parietal cortices that drive reasoning and problem-solving.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Short-Term Memory</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-purple-400">Violet</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Mid-left (dorsolateral pre-frontal)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Working-memory "scratch-pad" that juggles the current context window and live API calls.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Cross-Memory Integration</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-green-400">Green</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Lower-left (temporal / hippocampal bridge)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Hub that hands off facts between LTM & STM, performs similarity search, and ranks relevance.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Long-Term Memory</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-blue-400">Blue</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Mid-right (temporal lobe / hippocampus)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Where durable embeddings, knowledge-bases, and document indexes are stored and recalled.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Speech Generation</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-amber-400">Amber</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Lower-right (Broca-Wernicke axis)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Produces natural language output—fluent, contextual speech or text responses.</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                  
                  <div>
                    <h4 class="text-md font-semibold text-primary-400 mb-2">Not Pictured (Additional Capabilities)</h4>
                    <div class="overflow-x-auto">
                      <table class="min-w-full divide-y divide-dark-600">
                        <thead>
                          <tr>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">#</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Capability (Box Title)</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Where to place on diagram</th>
                            <th scope="col" class="px-3 py-2 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">What it does & why you might add it</th>
                          </tr>
                        </thead>
                        <tbody class="divide-y divide-dark-700">
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">1</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Perception / Multimodal Input</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Far-left "occipital" edge</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Ingests and embeds images, audio, video or sensor data. Lets the agent ground its reasoning in real-world signals (e.g., vision models, ASR, Whisper).</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">2</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Planning / Executive Control</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Very top-front ridge</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Breaks high-level goals into ordered tool calls, schedules, or chain-of-thought steps (a task-planner or ReAct-style reasoning loop).</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">3</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Reward & Feedback Loop</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Central "basal ganglia" area</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Stores RL feedback, user ratings, and offline evaluation signals—important for continuous improvement and A/B testing.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">4</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Memory Consolidation</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Deep mid-brain / hippocampal core</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Periodically distills short-term events into long-term embeddings, prunes noise, and re-indexes so LTM stays fresh and compact.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">5</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Alignment & Safety Guardrails</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Lower-front (orbitofrontal)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Filters or rewrites prompts/responses, enforces policy, detects jailbreak attempts—critical in customer-facing agents.</td>
                          </tr>
                          <tr>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">6</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Self-Monitoring / Observability</td>
                            <td class="px-3 py-2 whitespace-nowrap text-sm text-gray-300">Mid-front (anterior cingulate)</td>
                            <td class="px-3 py-2 text-sm text-gray-300">Logs internal traces, latency, token counts; flags hallucinations; emits metrics for dashboards and alerts ops teams.</td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="bg-dark-900 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm" @click="showInfoModal = false">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';

// Modal state
const showInfoModal = ref(false);

// Brain visualization enhancement after component mount
onMounted(() => {
  // Generate neural nodes
  const nodesGroup = document.querySelector('.neural-nodes');
  const connectionsGroup = document.querySelector('.neural-connections');
  
  if (!nodesGroup || !connectionsGroup) return;
  
  // Create neural nodes
  const nodeCount = 120;
  const nodePositions = [];
  
  for (let i = 0; i < nodeCount; i++) {
    // Create node at random position
    const cx = 200 + Math.random() * 880; // Keep within brain
    const cy = 200 + Math.random() * 690;
    
    const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    circle.setAttribute("cx", cx);
    circle.setAttribute("cy", cy);
    circle.setAttribute("r", Math.random() > 0.9 ? 3 + Math.random() * 3 : 1 + Math.random() * 2);
    circle.setAttribute("fill", "url(#node-gradient)");
    circle.classList.add("pulse");
    circle.style.animationDelay = (Math.random() * 3) + "s";
    
    nodesGroup.appendChild(circle);
    nodePositions.push({ x: cx, y: cy });
  }
  
  // Create neural connections
  const connectionCount = 180;
  
  for (let i = 0; i < connectionCount; i++) {
    const startNode = nodePositions[Math.floor(Math.random() * nodePositions.length)];
    const endNode = nodePositions[Math.floor(Math.random() * nodePositions.length)];
    
    if (startNode && endNode) {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("x1", startNode.x);
      line.setAttribute("y1", startNode.y);
      line.setAttribute("x2", endNode.x);
      line.setAttribute("y2", endNode.y);
      
      connectionsGroup.appendChild(line);
    }
  }
  
  // Add connections to focal points
  const focalPoints = document.querySelectorAll('.focal-points circle');
  
  focalPoints.forEach(point => {
    // Add animation delay
    point.style.animationDelay = (Math.random() * 2) + "s";
    
    // Create 3 connections from this focal point to neural nodes
    for (let i = 0; i < 3; i++) {
      const targetNode = nodePositions[Math.floor(Math.random() * nodePositions.length)];
      
      if (targetNode) {
        const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
        line.setAttribute("x1", point.getAttribute("cx"));
        line.setAttribute("y1", point.getAttribute("cy"));
        line.setAttribute("x2", targetNode.x);
        line.setAttribute("y2", targetNode.y);
        line.setAttribute("stroke-width", "1.5");
        line.setAttribute("stroke-opacity", "0.5");
        
        connectionsGroup.appendChild(line);
      }
    }
  });
});
</script>

<style scoped>
.brain-svg {
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 600px;
  display: block;
  margin: 0 auto;
}

.brain-label {
  max-width: 200px;
  z-index: 30;
}

.shadow-glow-blue {
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
}

.shadow-glow-purple {
  box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
}

.shadow-glow-green {
  box-shadow: 0 0 15px rgba(34, 197, 94, 0.4);
}

.shadow-glow-amber {
  box-shadow: 0 0 15px rgba(245, 158, 11, 0.4);
}

.shadow-glow-cyan {
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
}

.pulse {
  animation: blink 3s infinite ease-in-out;
}

.pulse-slow {
  animation: blink 4s infinite ease-in-out;
}

@keyframes blink {
  0%, 100% { opacity: 0.25; }
  50%      { opacity: 1;    }
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .brain-label {
    max-width: 180px;
    font-size: 0.9em;
  }
}

@media (max-width: 768px) {
  .brain-label {
    max-width: 150px;
    font-size: 0.8em;
  }
}
</style> 