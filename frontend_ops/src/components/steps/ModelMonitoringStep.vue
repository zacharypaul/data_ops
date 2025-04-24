<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-indigo-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-chart-line text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Model Monitoring</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Implement systems to track model performance and detect data drift</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Automated performance tracking</li>
        <li>Data & concept drift detection</li>
        <li>Alerting & reporting dashboards</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 1-3 weeks
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
        <p>Continuous monitoring ensures your models remain effective and reliable in production environments.</p>
        
        <h5 class="text-md font-semibold mt-4">Key Monitoring Metrics:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Performance Metrics:</strong> Accuracy, precision, recall, silhouette score, etc.</li>
          <li><strong>Operational Metrics:</strong> Latency, throughput, memory usage</li>
          <li><strong>Data Quality Metrics:</strong> Missing values, outliers, cardinality changes</li>
          <li><strong>Drift Metrics:</strong> Feature distribution changes, prediction distribution shifts</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Build a comprehensive monitoring system in Snowflake:</p>
        <ul class="pl-5 list-disc">
          <li>Create automated Snowflake Tasks for regular model evaluation</li>
          <li>Store predictions and actual outcomes for comparison</li>
          <li>Implement data drift detection using statistical tests</li>
          <li>Configure alerts using Snowflake Alerts and Notifications</li>
          <li>Build monitoring dashboards with Snowsight</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Data Drift Detection:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create a stored procedure for detecting data drift
CREATE OR REPLACE PROCEDURE ml_schema.detect_data_drift(
    model_id VARCHAR,
    reference_data_table VARCHAR,
    current_data_table VARCHAR,
    drift_threshold FLOAT
)
RETURNS VARIANT
LANGUAGE SQL
AS
$$
DECLARE
    drift_results VARIANT;
BEGIN
    -- Calculate KL divergence between reference and current distributions
    -- for each feature used in the model
    drift_results = (
        SELECT OBJECT_CONSTRUCT(
            'model_id', model_id,
            'timestamp', CURRENT_TIMESTAMP(),
            'features', OBJECT_AGG(
                feature_name,
                OBJECT_CONSTRUCT(
                    'kl_divergence', kl_div,
                    'drift_detected', IFF(kl_div > drift_threshold, TRUE, FALSE)
                )
            ),
            'overall_drift_detected', 
            (SELECT COUNT(*) > 0 FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())) 
             WHERE kl_div > drift_threshold)
        )
        FROM (
            SELECT 
                f.feature_name,
                -- Calculate KL divergence
                SUM(f.ref_prob * LOG(f.ref_prob / f.curr_prob)) AS kl_div
            FROM (
                SELECT
                    feature_name,
                    feature_value,
                    ref_count / SUM(ref_count) OVER (PARTITION BY feature_name) AS ref_prob,
                    curr_count / SUM(curr_count) OVER (PARTITION BY feature_name) AS curr_prob
                FROM (
                    -- Calculate distributions for categorical features
                    -- This is a simplified example
                    SELECT 
                        column_name AS feature_name,
                        column_value AS feature_value,
                        COUNT(*) AS ref_count,
                        0 AS curr_count
                    FROM LATERAL FLATTEN(
                        SELECT OBJECT_CONSTRUCT(*) FROM identifier(reference_data_table)
                    )
                    GROUP BY 1, 2
                    
                    UNION ALL
                    
                    SELECT 
                        column_name AS feature_name,
                        column_value AS feature_value,
                        0 AS ref_count,
                        COUNT(*) AS curr_count
                    FROM LATERAL FLATTEN(
                        SELECT OBJECT_CONSTRUCT(*) FROM identifier(current_data_table)
                    )
                    GROUP BY 1, 2
                ) 
                WHERE feature_name IN (
                    SELECT feature_name 
                    FROM ml_schema.model_features 
                    WHERE model_id = model_id
                )
            ) f
            -- Only consider features with non-zero probabilities in both datasets
            WHERE f.ref_prob > 0 AND f.curr_prob > 0
            GROUP BY 1
        )
    );
    
    -- Log drift results to audit table
    INSERT INTO ml_schema.model_drift_logs (
        model_id,
        timestamp,
        reference_data,
        current_data,
        drift_results
    )
    VALUES (
        model_id,
        CURRENT_TIMESTAMP(),
        reference_data_table,
        current_data_table,
        drift_results
    );
    
    -- Return the drift detection results
    RETURN drift_results;
END;
$$;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Monitoring Dashboard:</h5>
        <p>Create a comprehensive dashboard to visualize model performance over time:</p>
        <ul class="pl-5 list-disc">
          <li>Model performance metrics by time period</li>
          <li>Feature importance and distribution changes</li>
          <li>Data drift indicators and alerts</li>
          <li>Prediction distribution shifts</li>
          <li>Error analysis by segment</li>
        </ul>
        
        <p class="mt-4">Configure automated alerting when model performance degradation or significant drift is detected.</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelMonitoringStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 