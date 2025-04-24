<template>
  <div class="py-8">
    <h1 class="text-3xl font-display font-bold mb-4 text-center">Data Platform Migration Bracket</h1>
    <p class="text-center text-dark-400 mb-8">Compare migration paths from Snowflake to Microsoft Fabric</p>
    
    <!-- Tab Controls -->
    <div class="flex justify-center mb-8">
      <div class="inline-flex rounded-md shadow-sm" role="group">
        <button 
          @click="activeTab = 'full'"
          type="button" 
          :class="`px-5 py-2.5 text-sm font-medium ${activeTab === 'full' ? 'text-white bg-primary-700' : 'text-dark-300 bg-dark-800'} border border-dark-700 rounded-l-lg hover:bg-primary-900/50 focus:z-10 focus:outline-none`"
        >
          Full Migration
        </button>
        <button 
          @click="activeTab = 'partial'"
          type="button" 
          :class="`px-5 py-2.5 text-sm font-medium ${activeTab === 'partial' ? 'text-white bg-accent-700' : 'text-dark-300 bg-dark-800'} border border-dark-700 rounded-r-lg hover:bg-accent-900/50 focus:z-10 focus:outline-none`"
        >
          Partial Migration
        </button>
      </div>
    </div>
    
    <!-- Full Migration Bracket -->
    <div v-if="activeTab === 'full'" class="bracket-container">
      <!-- Main Bracket Structure -->
      <div class="flex justify-between">
        <!-- Snowflake Side (Left) -->
        <div class="w-[45%]">
          <h2 class="text-2xl font-display font-bold mb-6 text-secondary-500 text-center">Snowflake</h2>
          
          <!-- Round 1 - Snowflake -->
          <div class="mb-12">
            <div class="flex justify-between">
              <div class="w-full">
                <div class="bracket-teams">
                  <div class="bracket-team snowflake-team">
                    <span class="team-name">Data Warehousing</span>
                    <span class="team-score">96</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Traditional Solutions</span>
                    <span class="team-score">74</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team snowflake-team">
                    <span class="team-name">Cloud Scalability</span>
                    <span class="team-score">92</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">On-Prem Systems</span>
                    <span class="team-score">68</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team snowflake-team">
                    <span class="team-name">Data Sharing</span>
                    <span class="team-score">88</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Data Silos</span>
                    <span class="team-score">62</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team snowflake-team">
                    <span class="team-name">Zero-Copy Cloning</span>
                    <span class="team-score">94</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Full Copies</span>
                    <span class="team-score">56</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Round 2 - Snowflake -->
          <div class="mb-12">
            <div class="bracket-teams">
              <div class="bracket-team snowflake-team">
                <span class="team-name">Data Warehousing</span>
                <span class="team-score">89</span>
              </div>
              <div class="bracket-team snowflake-team">
                <span class="team-name">Cloud Scalability</span>
                <span class="team-score">86</span>
              </div>
            </div>
            
            <div class="bracket-teams mt-8">
              <div class="bracket-team snowflake-team">
                <span class="team-name">Data Sharing</span>
                <span class="team-score">84</span>
              </div>
              <div class="bracket-team snowflake-team">
                <span class="team-name">Zero-Copy Cloning</span>
                <span class="team-score">90</span>
              </div>
            </div>
          </div>
          
          <!-- Semifinals - Snowflake -->
          <div class="mb-12">
            <div class="bracket-teams">
              <div class="bracket-team snowflake-team">
                <span class="team-name">Data Warehousing</span>
                <span class="team-score">88</span>
              </div>
              <div class="bracket-team snowflake-team">
                <span class="team-name">Zero-Copy Cloning</span>
                <span class="team-score">92</span>
              </div>
            </div>
          </div>
          
          <!-- Finals - Snowflake Side -->
          <div>
            <div class="bracket-teams">
              <div class="bracket-team snowflake-team snowflake-finalist">
                <span class="team-name">Zero-Copy Cloning</span>
                <span class="team-score">91</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Championship -->
        <div class="flex flex-col items-center justify-center">
          <div class="championship-card glass-effect p-6 rounded-lg border border-gold-500/50 shadow-lg shadow-gold-500/20 text-center">
            <div class="text-2xl font-display font-bold text-white mb-3">Platform Decision</div>
            
            <div class="championship-trophy mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto text-gold-500" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 3.75A2.75 2.75 0 018.75 1h2.5A2.75 2.75 0 0114 3.75v.443c.572.055 1.14.122 1.706.2C17.053 4.582 18 5.75 18 7.07v3.469c0 1.126-.694 2.191-1.83 2.54-1.952.599-4.024.921-6.17.921s-4.219-.322-6.17-.921C2.694 12.73 2 11.665 2 10.539V7.07c0-1.321.947-2.489 2.294-2.676A41.047 41.047 0 016 4.193V3.75zm6.5 0v.325a41.622 41.622 0 00-5 0V3.75c0-.69.56-1.25 1.25-1.25h2.5c.69 0 1.25.56 1.25 1.25zM10 10a1 1 0 00-1 1v.01a1 1 0 001 1h.01a1 1 0 001-1V11a1 1 0 00-1-1H10z" clip-rule="evenodd" />
                <path d="M3 15.055v-.684c.126.053.255.1.39.142 2.092.642 4.313.987 6.61.987 2.297 0 4.518-.345 6.61-.987.135-.041.264-.089.39-.142v.684c0 1.347-.985 2.53-2.363 2.686a41.454 41.454 0 01-9.274 0C3.985 17.585 3 16.402 3 15.055z" />
              </svg>
            </div>
            
            <div class="championship-vs flex items-center justify-center space-x-2 mb-4">
              <div class="w-1/3 h-px bg-gradient-to-r from-transparent to-gold-500/50"></div>
              <span class="text-xl font-display font-bold text-gold-500 px-2">VS</span>
              <div class="w-1/3 h-px bg-gradient-to-l from-transparent to-gold-500/50"></div>
            </div>
            
            <div class="championship-platforms flex items-center justify-center space-x-6 mb-4">
              <div class="flex flex-col items-center">
                <div class="w-10 h-10 rounded-full bg-secondary-900 flex items-center justify-center">
                  <span class="text-secondary-400 font-bold">SF</span>
                </div>
                <span class="text-xs mt-1 text-secondary-400">Snowflake</span>
              </div>
              
              <div class="flex flex-col items-center">
                <div class="w-10 h-10 rounded-full bg-accent-900 flex items-center justify-center">
                  <span class="text-accent-400 font-bold">MS</span>
                </div>
                <span class="text-xs mt-1 text-accent-400">Microsoft</span>
              </div>
            </div>
            
            <div class="championship-result p-3 bg-dark-800/70 rounded-lg border border-dark-700/50">
              <div class="text-sm text-gray-300 mb-2">Winner Depends On</div>
              <div class="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-secondary-400 via-primary-400 to-accent-400 animate-gradient-x">
                Your Specific Use Case
              </div>
              <div class="mt-3 text-xs text-gray-400">
                <p>Consider your existing ecosystem, technical requirements, and organizational goals</p>
              </div>
            </div>
            
            <div class="mt-4 flex items-center justify-center space-x-4">
              <a href="#snowflake-details" class="px-3 py-1 text-xs bg-secondary-900/50 text-secondary-400 rounded-full border border-secondary-800 hover:bg-secondary-800/50 transition-colors">
                Snowflake Details
              </a>
              <a href="#fabric-details" class="px-3 py-1 text-xs bg-accent-900/50 text-accent-400 rounded-full border border-accent-800 hover:bg-accent-800/50 transition-colors">
                Fabric Details
              </a>
            </div>
          </div>
        </div>
        
        <!-- Microsoft Fabric Side (Right) -->
        <div class="w-[45%]">
          <h2 class="text-2xl font-display font-bold mb-6 text-accent-500 text-center">Microsoft Fabric</h2>
          
          <!-- Round 1 - Fabric -->
          <div class="mb-12">
            <div class="flex justify-between">
              <div class="w-full">
                <div class="bracket-teams">
                  <div class="bracket-team fabric-team">
                    <span class="team-name">OneLake</span>
                    <span class="team-score">92</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Multiple Data Sources</span>
                    <span class="team-score">71</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team fabric-team">
                    <span class="team-name">Power BI Integration</span>
                    <span class="team-score">98</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">3rd Party BI</span>
                    <span class="team-score">76</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team fabric-team">
                    <span class="team-name">Synapse Integration</span>
                    <span class="team-score">90</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Standalone Analytics</span>
                    <span class="team-score">64</span>
                  </div>
                </div>
                
                <div class="bracket-teams mt-8">
                  <div class="bracket-team fabric-team">
                    <span class="team-name">Microsoft Ecosystem</span>
                    <span class="team-score">95</span>
                  </div>
                  <div class="bracket-team">
                    <span class="team-name">Multiple Vendors</span>
                    <span class="team-score">68</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Round 2 - Fabric -->
          <div class="mb-12">
            <div class="bracket-teams">
              <div class="bracket-team fabric-team">
                <span class="team-name">OneLake</span>
                <span class="team-score">86</span>
              </div>
              <div class="bracket-team fabric-team">
                <span class="team-name">Power BI Integration</span>
                <span class="team-score">96</span>
              </div>
            </div>
            
            <div class="bracket-teams mt-8">
              <div class="bracket-team fabric-team">
                <span class="team-name">Synapse Integration</span>
                <span class="team-score">88</span>
              </div>
              <div class="bracket-team fabric-team">
                <span class="team-name">Microsoft Ecosystem</span>
                <span class="team-score">92</span>
              </div>
            </div>
          </div>
          
          <!-- Semifinals - Fabric -->
          <div class="mb-12">
            <div class="bracket-teams">
              <div class="bracket-team fabric-team">
                <span class="team-name">Power BI Integration</span>
                <span class="team-score">94</span>
              </div>
              <div class="bracket-team fabric-team">
                <span class="team-name">Microsoft Ecosystem</span>
                <span class="team-score">91</span>
              </div>
            </div>
          </div>
          
          <!-- Finals - Fabric Side -->
          <div>
            <div class="bracket-teams">
              <div class="bracket-team fabric-team fabric-finalist">
                <span class="team-name">Power BI Integration</span>
                <span class="team-score">93</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Partial Migration Bracket -->
    <div v-if="activeTab === 'partial'" class="bracket-container">
      <div class="flex justify-between">
        <!-- Snowflake Side (Left) -->
        <div class="w-[45%]">
          <h2 class="text-2xl font-display font-bold mb-6 text-secondary-500 text-center">Retained in Snowflake</h2>
          
          <!-- Components to Retain in Snowflake -->
          <div class="mb-8">
            <div class="bg-dark-800/70 p-6 rounded-lg border border-secondary-700">
              <h3 class="text-xl font-display font-bold mb-4 text-secondary-400">Core Data Warehouse</h3>
              
              <div class="space-y-4">
                <div class="partial-component snowflake-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M3 12v3c0 1.657 3.134 3 7 3s7-1.343 7-3v-3c0 1.657-3.134 3-7 3s-7-1.343-7-3z" />
                        <path d="M3 7v3c0 1.657 3.134 3 7 3s7-1.343 7-3V7c0 1.657-3.134 3-7 3S3 8.657 3 7z" />
                        <path d="M17 5c0 1.657-3.134 3-7 3S3 6.657 3 5s3.134-3 7-3 7 1.343 7 3z" />
                      </svg>
                    </span>
                    <span class="component-name">Historical Data</span>
                  </div>
                  <div class="component-benefit">90% Cost Savings vs Migration</div>
                </div>
                
                <div class="partial-component snowflake-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 0l-2 2a1 1 0 101.414 1.414L8 10.414l1.293 1.293a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                      </svg>
                    </span>
                    <span class="component-name">Complex Transformations</span>
                  </div>
                  <div class="component-benefit">Leverages Existing SQL</div>
                </div>
                
                <div class="partial-component snowflake-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM11 12a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd" />
                      </svg>
                    </span>
                    <span class="component-name">Data Science Workloads</span>
                  </div>
                  <div class="component-benefit">Specialized Compute Options</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Data Bridge -->
          <div class="data-bridge-section flex justify-end">
            <div class="w-3/4 bg-dark-800/70 p-4 rounded-lg border border-gold-700">
              <h3 class="text-lg font-display font-bold mb-2 text-gold-400">Data Bridge</h3>
              
              <div class="space-y-3">
                <div class="data-bridge-component">
                  <div class="flex items-center justify-between">
                    <span class="bridge-name">Snowflake External Tables</span>
                    <span class="bridge-direction">→</span>
                  </div>
                </div>
                
                <div class="data-bridge-component">
                  <div class="flex items-center justify-between">
                    <span class="bridge-name">Automated Data Pipeline</span>
                    <span class="bridge-direction">→</span>
                  </div>
                </div>
                
                <div class="data-bridge-component">
                  <div class="flex items-center justify-between">
                    <span class="bridge-name">Metadata Synchronization</span>
                    <span class="bridge-direction">↔</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Center Column -->
        <div class="flex flex-col items-center justify-center">
          <div class="championship-trophy">
            <div class="migration-arrow text-center mb-4">
              <span class="block text-dark-400 text-sm">Hybrid Approach</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gold-500 rotate-45" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-20 w-20 text-gold-500" viewBox="0 0 20 20" fill="currentColor">
              <path d="M11 17a1 1 0 001.447.894l4-2A1 1 0 0017 15V9.236a1 1 0 00-1.447-.894l-4 2a1 1 0 00-.553.894V17zM15.211 6.276a1 1 0 000-1.788l-4.764-2.382a1 1 0 00-.894 0L4.789 4.488a1 1 0 000 1.788l4.764 2.382a1 1 0 00.894 0l4.764-2.382zM4.447 8.342A1 1 0 003 9.236V15a1 1 0 00.553.894l4 2A1 1 0 009 17v-5.764a1 1 0 00-.553-.894l-4-2z" />
            </svg>
          </div>
          <div class="championship-vs mt-4 text-center">
            <span class="text-3xl font-display font-bold text-gold-500">+</span>
            <div class="text-xs text-dark-400 mt-2">Hybrid Platform Strategy</div>
          </div>
          <div class="championship-result mt-4 px-6 py-3 bg-dark-800 rounded-lg">
            <div class="text-sm text-dark-300 text-center mb-1">Best For</div>
            <div class="text-lg font-bold text-center bg-clip-text text-transparent bg-gradient-to-r from-secondary-400 via-gold-400 to-accent-400 animate-gradient-x">
              Phased Migration Strategy
            </div>
          </div>
        </div>
        
        <!-- Microsoft Fabric Side (Right) -->
        <div class="w-[45%]">
          <h2 class="text-2xl font-display font-bold mb-6 text-accent-500 text-center">Migrated to Fabric</h2>
          
          <!-- Components to Migrate to Fabric -->
          <div class="mb-8">
            <div class="bg-dark-800/70 p-6 rounded-lg border border-accent-700">
              <h3 class="text-xl font-display font-bold mb-4 text-accent-400">Analytics & Reporting</h3>
              
              <div class="space-y-4">
                <div class="partial-component fabric-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11 4a1 1 0 10-2 0v4a1 1 0 102 0V7zm-3 1a1 1 0 10-2 0v3a1 1 0 102 0V8zM8 9a1 1 0 00-2 0v2a1 1 0 102 0V9z" clip-rule="evenodd" />
                      </svg>
                    </span>
                    <span class="component-name">Power BI Reporting</span>
                  </div>
                  <div class="component-benefit">Native Integration</div>
                </div>
                
                <div class="partial-component fabric-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                        <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
                      </svg>
                    </span>
                    <span class="component-name">Semantic Layer</span>
                  </div>
                  <div class="component-benefit">Business User Access</div>
                </div>
                
                <div class="partial-component fabric-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
                      </svg>
                    </span>
                    <span class="component-name">Data Lakehouse</span>
                  </div>
                  <div class="component-benefit">New Analytics Capabilities</div>
                </div>
                
                <div class="partial-component fabric-component">
                  <div class="flex items-center">
                    <span class="component-icon">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                      </svg>
                    </span>
                    <span class="component-name">ML Notebooks</span>
                  </div>
                  <div class="component-benefit">Integrated AI/ML</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- New Fabric Capabilities -->
          <div class="new-capabilities-section">
            <div class="bg-dark-800/70 p-4 rounded-lg border border-accent-700">
              <h3 class="text-lg font-display font-bold mb-2 text-accent-400">New Capabilities</h3>
              
              <div class="space-y-3">
                <div class="capability-component">
                  <div class="flex items-center">
                    <span class="capability-dot bg-accent-500"></span>
                    <span class="capability-name">Real-time Analytics</span>
                  </div>
                </div>
                
                <div class="capability-component">
                  <div class="flex items-center">
                    <span class="capability-dot bg-accent-500"></span>
                    <span class="capability-name">Copilot Integration</span>
                  </div>
                </div>
                
                <div class="capability-component">
                  <div class="flex items-center">
                    <span class="capability-dot bg-accent-500"></span>
                    <span class="capability-name">Low-Code Data Prep</span>
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

<script setup>
import { ref } from 'vue';

const activeTab = ref('full');
</script>

<style scoped>
.bracket-container {
  @apply flex justify-between;
}

.bracket-teams {
  @apply flex flex-col;
}

.bracket-team {
  @apply flex justify-between items-center p-3 rounded-md border border-dark-700;
  background-color: #232B4F; /* dark-800 */
}

.snowflake-team {
  @apply border-secondary-700;
  background-color: rgba(35, 43, 79, 0.8); /* dark-800 with 80% opacity */
}

.snowflake-finalist {
  @apply border-secondary-600;
  background-color: rgba(18, 34, 47, 0.3); /* secondary-900 with 30% opacity */
}

.fabric-team {
  @apply border-accent-700;
  background-color: rgba(35, 43, 79, 0.8); /* dark-800 with 80% opacity */
}

.fabric-finalist {
  @apply border-accent-600;
  background-color: rgba(16, 45, 39, 0.3); /* accent-900 with 30% opacity */
}

.team-name {
  @apply font-medium;
}

.team-score {
  @apply text-sm bg-dark-900 rounded px-2 py-0.5;
}

.glass-effect {
  background: rgba(15, 23, 42, 0.6);
  border-radius: 0.5rem;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .bracket-container {
    @apply flex-col items-center;
  }
  
  .bracket-container > div {
    @apply w-full max-w-lg mb-8;
  }
}

/* Partial Migration Styles */
.partial-component {
  @apply p-3 rounded border flex justify-between items-center;
}

.snowflake-component {
  @apply border-secondary-700;
  background-color: rgba(18, 34, 47, 0.2); /* secondary-900 with 20% opacity */
}

.fabric-component {
  @apply border-accent-700;
  background-color: rgba(16, 45, 39, 0.2); /* accent-900 with 20% opacity */
}

.component-icon {
  @apply mr-2 text-dark-300;
}

.snowflake-component .component-icon {
  @apply text-secondary-400;
}

.fabric-component .component-icon {
  @apply text-accent-400;
}

.component-name {
  @apply text-sm font-medium;
}

.component-benefit {
  @apply text-xs px-2 py-1 rounded;
}

.snowflake-component .component-benefit {
  @apply text-secondary-300;
  background-color: rgba(35, 68, 93, 0.3); /* secondary-800 with 30% opacity */
}

.fabric-component .component-benefit {
  @apply text-accent-300;
  background-color: rgba(32, 91, 77, 0.3); /* accent-800 with 30% opacity */
}

.data-bridge-component, .capability-component {
  @apply p-2 rounded border border-dark-600;
  background-color: rgba(55, 65, 81, 0.5); /* dark-700 with 50% opacity */
}

.bridge-name, .capability-name {
  @apply text-xs font-medium text-dark-300;
}

.bridge-direction {
  @apply text-xs font-bold text-gold-400;
}

.capability-dot {
  @apply h-2 w-2 rounded-full mr-2;
}
</style> 