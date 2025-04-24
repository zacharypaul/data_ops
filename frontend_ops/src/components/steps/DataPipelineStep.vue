<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-blue-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-exchange-alt text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Data Pipeline</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Build robust data pipelines for data ingestion, preprocessing, and feature engineering</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Data ingestion workflows</li>
        <li>Data cleaning & validation</li>
        <li>Feature engineering processes</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 2-3 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
      
      <div class="prose prose-dark text-gray-300">
        <p>Efficient data pipelines ensure reliable, high-quality data is available for K-means modeling in Snowflake.</p>
        
        <h5 class="text-md font-semibold mt-4">Data Pipeline Components:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Data Ingestion:</strong> Extract data from source systems into Snowflake</li>
          <li><strong>Data Validation:</strong> Apply quality checks and validation rules</li>
          <li><strong>Data Transformation:</strong> Clean, normalize, and prepare data</li>
          <li><strong>Feature Engineering:</strong> Create features for clustering models</li>
          <li><strong>Feature Store:</strong> Manage and version features for consistency</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Leverage Snowflake's data pipeline capabilities:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowpipe for continuous data ingestion</li>
          <li>Implement Streams and Tasks for incremental processing</li>
          <li>Apply data quality validation with constraints and assertions</li>
          <li>Create Stored Procedures for complex transformations</li>
          <li>Set up feature tables with appropriate metadata</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Data Ingestion Example:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Set up external stage for raw data ingestion
CREATE STAGE IF NOT EXISTS ml_ops.raw_data.customer_data_stage
  URL = 's3://customer-data-bucket/daily-feeds/'
  STORAGE_INTEGRATION = s3_data_integration;

-- Create target table for raw data
CREATE TABLE IF NOT EXISTS ml_ops.raw_data.customer_data (
  customer_id VARCHAR,
  region VARCHAR,
  customer_type VARCHAR,
  purchase_amount FLOAT,
  visit_frequency INT,
  last_purchase_date DATE,
  loyalty_score FLOAT,
  source_file VARCHAR,
  ingestion_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Set up Snowpipe for automated ingestion
CREATE OR REPLACE PIPE ml_ops.raw_data.customer_data_pipe 
AUTO_INGEST = TRUE
AS
COPY INTO ml_ops.raw_data.customer_data (
  customer_id, region, customer_type, purchase_amount, 
  visit_frequency, last_purchase_date, loyalty_score, source_file
)
FROM (
  SELECT 
    $1, $2, $3, $4, $5, 
    TO_DATE($6, 'YYYY-MM-DD'), $7, METADATA$FILENAME
  FROM @ml_ops.raw_data.customer_data_stage
)
FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1 FIELD_OPTIONALLY_ENCLOSED_BY = '"');
</pre>
        
        <h5 class="text-md font-semibold mt-4">Data Validation and Cleaning:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create validated data table
CREATE OR REPLACE TABLE ml_ops.processed_data.validated_customer_data AS
SELECT
  customer_id,
  region,
  CASE 
    WHEN customer_type IS NULL THEN 'UNKNOWN'
    WHEN customer_type = '' THEN 'UNKNOWN'
    ELSE UPPER(TRIM(customer_type))
  END AS customer_type,
  -- Handle outliers in purchase amount using capping
  CASE
    WHEN purchase_amount < 0 THEN 0
    WHEN purchase_amount > 10000 THEN 10000
    ELSE purchase_amount
  END AS purchase_amount,
  -- Handle missing values in visit frequency
  COALESCE(visit_frequency, 0) AS visit_frequency,
  last_purchase_date,
  -- Handle invalid loyalty scores
  CASE 
    WHEN loyalty_score < 0 THEN 0
    WHEN loyalty_score > 100 THEN 100
    ELSE loyalty_score
  END AS loyalty_score,
  source_file,
  ingestion_timestamp,
  -- Add data quality flags
  (purchase_amount < 0 OR purchase_amount > 10000) AS purchase_amount_outlier_flag,
  (visit_frequency IS NULL) AS visit_frequency_missing_flag,
  (loyalty_score < 0 OR loyalty_score > 100) AS loyalty_score_invalid_flag,
  -- Add validation timestamp
  CURRENT_TIMESTAMP() AS validation_timestamp
FROM ml_ops.raw_data.customer_data
-- Filter out records with critical missing data
WHERE customer_id IS NOT NULL;

-- Create streams for incremental processing
CREATE OR REPLACE STREAM ml_ops.processed_data.customer_data_stream 
ON TABLE ml_ops.processed_data.validated_customer_data;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Feature Engineering:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create feature engineering task
CREATE OR REPLACE TASK ml_ops.processed_data.feature_engineering_task
  WAREHOUSE = ML_ETL_WH
  SCHEDULE = '5 MINUTE'
WHEN
  SYSTEM$STREAM_HAS_DATA('ml_ops.processed_data.customer_data_stream')
AS
BEGIN
  -- Insert into feature store
  INSERT INTO ml_ops.processed_data.customer_features (
    customer_id,
    feature_timestamp,
    region,
    customer_type,
    purchase_amount,
    visit_frequency,
    -- Derived features
    recency_days,
    purchase_frequency,
    monetary_value,
    loyalty_level,
    feature_version
  )
  SELECT
    customer_id,
    CURRENT_TIMESTAMP() AS feature_timestamp,
    region,
    customer_type,
    purchase_amount,
    visit_frequency,
    -- Calculate recency feature (days since last purchase)
    DATEDIFF('day', last_purchase_date, CURRENT_DATE()) AS recency_days,
    -- Calculate frequency feature (normalized)
    visit_frequency / 10.0 AS purchase_frequency,
    -- Calculate monetary value feature (normalized)
    purchase_amount / 1000.0 AS monetary_value,
    -- Calculate loyalty level
    CASE
      WHEN loyalty_score >= 80 THEN 'HIGH'
      WHEN loyalty_score >= 40 THEN 'MEDIUM'
      ELSE 'LOW'
    END AS loyalty_level,
    '1.0' AS feature_version
  FROM ml_ops.processed_data.customer_data_stream;
  
  -- Generate aggregated features
  MERGE INTO ml_ops.processed_data.customer_aggregate_features t
  USING (
    SELECT
      customer_id,
      AVG(purchase_amount) AS avg_purchase_amount,
      MAX(purchase_amount) AS max_purchase_amount,
      COUNT(*) AS transaction_count,
      SUM(purchase_amount) AS total_spend,
      AVG(visit_frequency) AS avg_visit_frequency
    FROM ml_ops.processed_data.validated_customer_data
    GROUP BY customer_id
  ) s
  ON t.customer_id = s.customer_id
  WHEN MATCHED THEN
    UPDATE SET
      avg_purchase_amount = s.avg_purchase_amount,
      max_purchase_amount = s.max_purchase_amount,
      transaction_count = s.transaction_count,
      total_spend = s.total_spend,
      avg_visit_frequency = s.avg_visit_frequency,
      last_updated = CURRENT_TIMESTAMP()
  WHEN NOT MATCHED THEN
    INSERT (
      customer_id, avg_purchase_amount, max_purchase_amount,
      transaction_count, total_spend, avg_visit_frequency,
      created_at, last_updated
    )
    VALUES (
      s.customer_id, s.avg_purchase_amount, s.max_purchase_amount,
      s.transaction_count, s.total_spend, s.avg_visit_frequency,
      CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP()
    );
END;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Pipeline Monitoring and Alerting:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create data quality monitoring task
CREATE OR REPLACE TASK ml_ops.monitoring.data_quality_check_task
  WAREHOUSE = ML_ETL_WH
  SCHEDULE = 'USING CRON 0 */4 * * * America/Los_Angeles'
AS
BEGIN
  -- Check for data freshness
  INSERT INTO ml_ops.monitoring.data_pipeline_alerts (
    alert_type, alert_level, alert_message, affected_entity
  )
  SELECT
    'DATA_FRESHNESS',
    'HIGH',
    'No new data ingested in the last 24 hours',
    'customer_data'
  WHERE (
    SELECT MAX(ingestion_timestamp)
    FROM ml_ops.raw_data.customer_data
  ) < DATEADD('hour', -24, CURRENT_TIMESTAMP());
  
  -- Check for data quality issues
  INSERT INTO ml_ops.monitoring.data_pipeline_alerts (
    alert_type, alert_level, alert_message, affected_entity
  )
  SELECT
    'DATA_QUALITY',
    'MEDIUM',
    'High percentage of outliers detected: ' || 
    ROUND(outlier_pct, 2) || '% of records',
    'purchase_amount'
  FROM (
    SELECT
      100.0 * COUNT(CASE WHEN purchase_amount_outlier_flag THEN 1 END) / COUNT(*) AS outlier_pct
    FROM ml_ops.processed_data.validated_customer_data
    WHERE validation_timestamp > DATEADD('hour', -24, CURRENT_TIMESTAMP())
  )
  WHERE outlier_pct > 5.0;
END;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Data Pipeline Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Design for idempotency (pipelines can be safely rerun)</li>
          <li>Implement comprehensive data validation and quality checks</li>
          <li>Create incremental processing flows for efficiency</li>
          <li>Maintain detailed metadata for all transformations</li>
          <li>Set up monitoring and alerting for pipeline health</li>
          <li>Use separate workflows for real-time vs. batch processing</li>
          <li>Create proper error handling and dead-letter queues</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DataPipelineStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 