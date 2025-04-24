<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-indigo-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-database text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Data Management</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Establish data pipelines and version control for your ML datasets</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Data versioning strategies</li>
        <li>Feature stores implementation</li>
        <li>Data quality validation frameworks</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 1-2 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
      
      <div class="prose prose-dark text-gray-300">
        <p>Data management for ML involves creating reliable, reproducible data sources for model training and inference.</p>
        
        <h5 class="text-md font-semibold mt-4">Best Practices:</h5>
        <ul class="pl-5 list-disc">
          <li>Implement data versioning with tools like DVC or LakeFS</li>
          <li>Create data validation pipelines to ensure quality</li>
          <li>Maintain metadata about datasets (sources, schemas, lineage)</li>
          <li>Use a feature store for consistent feature engineering</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Leverage Snowflake's capabilities to build robust data management:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowflake Time Travel for data versioning</li>
          <li>Implement stream processing for real-time feature updates</li>
          <li>Utilize Snowflake's data sharing for cross-team collaboration</li>
          <li>Set up automated testing with Snowflake Tasks and Streams</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Sample Configuration:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# Snowflake Time Travel configuration
ALTER DATABASE ml_datasets SET DATA_RETENTION_TIME_IN_DAYS = 90;

# Create a versioned feature table
CREATE OR REPLACE TABLE feature_store.customer_features (
  customer_id VARCHAR,
  feature_timestamp TIMESTAMP_NTZ,
  feature1 FLOAT,
  feature2 FLOAT,
  feature_vector ARRAY,
  version_id VARCHAR,
  valid_from TIMESTAMP_NTZ,
  valid_to TIMESTAMP_NTZ
);
</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataManagementStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 