<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-indigo-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-sync text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Feedback Loops</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Create systems for model retraining based on new data and performance feedback</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Continuous learning pipelines</li>
        <li>Human-in-the-loop validation</li>
        <li>Model iteration strategies</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 2-3 weeks
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
        <p>Effective feedback loops ensure models adapt, improve, and remain relevant over time as data patterns and business needs evolve.</p>
        
        <h5 class="text-md font-semibold mt-4">Types of Feedback Loops:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Performance-Based:</strong> Automatically retrain when model performance drops below thresholds</li>
          <li><strong>Time-Based:</strong> Schedule regular retraining on predetermined intervals</li>
          <li><strong>Data-Based:</strong> Retrain when significant data drift is detected</li>
          <li><strong>Human-in-the-Loop:</strong> Incorporate expert feedback and validation</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Implement automated feedback loops in Snowflake:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowflake Tasks to schedule and trigger model retraining</li>
          <li>Create data pipelines that collect and prepare new training data</li>
          <li>Implement a model champion/challenger framework</li>
          <li>Store human feedback and corrections in dedicated tables</li>
          <li>Develop a model iteration workflow with version control</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Automated Retraining Task:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create a stored procedure for model retraining
CREATE OR REPLACE PROCEDURE ml_schema.retrain_kmeans_model(
    model_id VARCHAR,
    training_data_table VARCHAR,
    n_clusters INTEGER,
    random_state INTEGER
)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ('snowflake-snowpark-python', 'scikit-learn', 'joblib')
HANDLER = 'retrain_model'
AS
$$
import snowflake.snowpark as snowpark
from snowflake.snowpark.session import Session
from snowflake.ml.modeling.preprocessing import StandardScaler, OneHotEncoder
from snowflake.ml.modeling.clustering import KMeans
from snowflake.ml.experiment import Experiment
import joblib
import uuid
import datetime

def retrain_model(session, model_id, training_data_table, n_clusters, random_state):
    # Create experiment for tracking
    experiment = Experiment(session, f"Retraining_{model_id}")
    run_id = experiment.start_run()
    
    try:
        # Log parameters
        experiment.log_param("model_id", model_id)
        experiment.log_param("training_data", training_data_table)
        experiment.log_param("n_clusters", n_clusters)
        experiment.log_param("random_state", random_state)
        experiment.log_param("retrain_timestamp", datetime.datetime.now().isoformat())
        
        # Load training data
        df = session.table(training_data_table)
        
        # Preprocess data - this would typically be loaded from the original model config
        encoder = OneHotEncoder(
            input_cols=["REGION", "CUSTOMER_TYPE"],
            output_cols=["REGION_ENCODED", "TYPE_ENCODED"]
        )
        df_encoded = encoder.fit_transform(df)
        
        scaler = StandardScaler(
            input_cols=["PURCHASE_AMOUNT", "VISIT_FREQUENCY"],
            output_cols=["AMOUNT_SCALED", "FREQUENCY_SCALED"]
        )
        df_scaled = scaler.fit_transform(df_encoded)
        
        # Train model
        features = ["AMOUNT_SCALED", "FREQUENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]
        kmeans = KMeans(n_clusters=n_clusters, random_state=random_state)
        kmeans.fit(df_scaled[features])
        
        # Evaluate model
        silhouette = kmeans.score(df_scaled[features])
        inertia = kmeans.inertia_
        
        # Log metrics
        experiment.log_metric("silhouette_score", silhouette)
        experiment.log_metric("inertia", inertia)
        
        # Generate new model version
        new_model_version = str(uuid.uuid4())
        
        # Save model artifacts
        model_path = f"/tmp/{new_model_version}.joblib"
        joblib.dump(kmeans, model_path)
        
        # Upload model to Snowflake stage
        session.file.put(
            model_path,
            f"@ML_MODELS/{model_id}/versions/{new_model_version}.joblib", 
            auto_compress=False, overwrite=True
        )
        
        # Update model registry with new version
        session.sql(f"""
        INSERT INTO ml_schema.model_versions (
            model_id,
            version_id,
            training_data,
            parameters,
            metrics,
            artifact_path,
            created_at,
            experiment_run_id
        )
        VALUES (
            '{model_id}',
            '{new_model_version}',
            '{training_data_table}',
            PARSE_JSON('{"n_clusters": ' || n_clusters || ', "random_state": ' || random_state || '}'),
            PARSE_JSON('{"silhouette_score": ' || {silhouette} || ', "inertia": ' || {inertia} || '}'),
            '@ML_MODELS/{model_id}/versions/{new_model_version}.joblib',
            CURRENT_TIMESTAMP(),
            '{run_id}'
        )
        """).collect()
        
        # Log success
        experiment.log_param("status", "success")
        experiment.end_run()
        
        return new_model_version
        
    except Exception as e:
        # Log failure
        experiment.log_param("status", "failed")
        experiment.log_param("error", str(e))
        experiment.end_run()
        raise e
$$;

-- Create a scheduled task to check model performance and trigger retraining
CREATE OR REPLACE TASK ml_schema.monitor_and_retrain_task
    WAREHOUSE = ML_WAREHOUSE
    SCHEDULE = 'USING CRON 0 0 * * * America/Los_Angeles'
AS
BEGIN
    -- For each model that needs retraining based on performance
    -- Simplified example that would be expanded based on your metrics and thresholds
    FOR model_record IN (
        SELECT 
            m.model_id,
            m.parameters:n_clusters::INTEGER AS n_clusters,
            m.parameters:random_state::INTEGER AS random_state
        FROM ml_schema.model_registry m
        JOIN ml_schema.model_performance_logs p
            ON m.model_id = p.model_id
        WHERE 
            m.model_type = 'KMEANS'
            AND p.metrics:silhouette_score::FLOAT < 0.6
            AND p.timestamp > DATEADD('day', -7, CURRENT_TIMESTAMP())
    )
    DO
        -- Trigger retraining
        CALL ml_schema.retrain_kmeans_model(
            model_record.model_id,
            'ML_DATA.TRAINING.CUSTOMER_DATA_CURRENT',
            model_record.n_clusters,
            model_record.random_state
        );
    END FOR;
END;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Human Feedback Collection:</h5>
        <p>Implement a system to collect human feedback on model predictions:</p>
        <ul class="pl-5 list-disc">
          <li>Create interfaces for subject matter experts to review model outputs</li>
          <li>Store corrections and feedback in structured format</li>
          <li>Use feedback to identify patterns in model errors</li>
          <li>Incorporate corrections into retraining datasets</li>
          <li>Track feedback metrics to measure model improvement over time</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Champion/Challenger Framework:</h5>
        <p>Implement a champion/challenger framework to systematically test model improvements:</p>
        <ol class="pl-5 list-decimal">
          <li>Current production model serves as the "champion"</li>
          <li>New model versions are deployed as "challengers"</li>
          <li>Distribute small portion of traffic to challenger models</li>
          <li>Compare performance metrics between champion and challengers</li>
          <li>Promote challenger to champion when significantly better</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeedbackLoopsStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 