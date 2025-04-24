<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-indigo-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-shield-alt text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Governance & Security</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Ensure compliance, security, and governance of ML models</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Model documentation & cards</li>
        <li>Access control frameworks</li>
        <li>Audit trails & compliance</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> Ongoing
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
        <p>Effective governance ensures that models are transparent, secure, compliant with regulations, and their lifecycle is properly documented and controlled.</p>
        
        <h5 class="text-md font-semibold mt-4">Governance Framework Components:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Model Registry:</strong> Central repository documenting all models</li>
          <li><strong>Model Cards:</strong> Standardized documentation for model details and limitations</li>
          <li><strong>Access Controls:</strong> Role-based access to models and data</li>
          <li><strong>Audit Trails:</strong> Tracking all actions on models for compliance</li>
          <li><strong>Risk Management:</strong> Assess and mitigate model risks</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Leverage Snowflake's security features for ML governance:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowflake's RBAC for granular access control to models</li>
          <li>Create model registry tables with versioning support</li>
          <li>Implement audit logging for all model operations</li>
          <li>Use Row-Level Security for fine-grained data access</li>
          <li>Implement data masking for sensitive features</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Model Card Implementation:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create a model card table
CREATE OR REPLACE TABLE governance.model_cards (
    model_id VARCHAR NOT NULL PRIMARY KEY,
    name VARCHAR NOT NULL,
    version VARCHAR NOT NULL,
    description TEXT,
    model_type VARCHAR NOT NULL,
    intended_use JSON,
    factors JSON,
    metrics JSON,
    evaluation_data JSON,
    training_data JSON,
    quantitative_analyses JSON,
    ethical_considerations JSON,
    caveats_recommendations JSON,
    created_by VARCHAR,
    creation_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    last_updated_date TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    approval_status VARCHAR DEFAULT 'PENDING'
);

-- Insert a sample model card
INSERT INTO governance.model_cards (
    model_id,
    name,
    version,
    description,
    model_type,
    intended_use,
    factors,
    metrics,
    evaluation_data,
    training_data,
    quantitative_analyses,
    ethical_considerations,
    caveats_recommendations,
    created_by
)
VALUES (
    'kmeans-customer-seg-001',
    'Customer Segmentation Model',
    '1.0.0',
    'K-means clustering model for segmenting customers based on purchase behavior and demographics',
    'K-means clustering',
    PARSE_JSON('{
        "primary_uses": ["Customer segmentation for marketing campaigns", "Personalization"],
        "primary_users": ["Marketing Team", "Customer Analytics"],
        "out_of_scope_uses": ["Credit decisions", "Fraud detection"]
    }'),
    PARSE_JSON('{
        "relevant_factors": ["Purchase amount", "Visit frequency", "Customer region", "Customer type"],
        "evaluation_factors": ["Silhouette score", "Inertia", "Business interpretability"]
    }'),
    PARSE_JSON('{
        "performance_metrics": {
            "silhouette_score": 0.68,
            "inertia": 245.7
        },
        "decision_thresholds": {
            "cluster_assignment_confidence": 0.75
        }
    }'),
    PARSE_JSON('{
        "datasets": ["CUSTOMER_DATA_TEST"],
        "preprocessing": "Standard scaling for numerical features, one-hot encoding for categorical",
        "evaluation_timeframe": "Jan 1, 2023 - Feb 1, 2023"
    }'),
    PARSE_JSON('{
        "datasets": ["CUSTOMER_DATA_TRAIN"],
        "preprocessing": "Same as evaluation data",
        "training_timeframe": "Jan 1, 2022 - Dec 31, 2022"
    }'),
    PARSE_JSON('{
        "unitary_results": "Model creates 4 distinct customer segments",
        "intersectional_analysis": "No significant biases observed across demographic groups"
    }'),
    PARSE_JSON('{
        "ethical_risks": "Potential for reinforcing existing marketing biases",
        "mitigations": "Regular review of segment compositions by Ethics Board"
    }'),
    PARSE_JSON('{
        "caveats": ["Model performance degrades for new customer types", "Not suitable for real-time decisions"],
        "recommendations": ["Retrain quarterly", "Monitor segment distribution shifts"]
    }'),
    'data_scientist_123'
);
</pre>
        
        <h5 class="text-md font-semibold mt-4">Access Control Implementation:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
-- Create roles for ML model access
CREATE ROLE IF NOT EXISTS ML_ADMIN;
CREATE ROLE IF NOT EXISTS ML_DEVELOPER;
CREATE ROLE IF NOT EXISTS ML_VIEWER;

-- Grant privileges
GRANT USAGE ON DATABASE ML_MODELS TO ROLE ML_ADMIN;
GRANT USAGE ON DATABASE ML_MODELS TO ROLE ML_DEVELOPER;
GRANT USAGE ON DATABASE ML_MODELS TO ROLE ML_VIEWER;

GRANT USAGE ON SCHEMA ML_MODELS.ML_SCHEMA TO ROLE ML_ADMIN;
GRANT USAGE ON SCHEMA ML_MODELS.ML_SCHEMA TO ROLE ML_DEVELOPER;
GRANT USAGE ON SCHEMA ML_MODELS.ML_SCHEMA TO ROLE ML_VIEWER;

-- Admin privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ML_MODELS.ML_SCHEMA TO ROLE ML_ADMIN;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN SCHEMA ML_MODELS.ML_SCHEMA TO ROLE ML_ADMIN;

-- Developer privileges
GRANT SELECT, INSERT, UPDATE ON TABLE ML_MODELS.ML_SCHEMA.MODEL_REGISTRY TO ROLE ML_DEVELOPER;
GRANT SELECT, INSERT ON TABLE ML_MODELS.ML_SCHEMA.MODEL_VERSIONS TO ROLE ML_DEVELOPER;
GRANT USAGE ON FUNCTION ML_MODELS.ML_SCHEMA.PREDICT_CUSTOMER_SEGMENT TO ROLE ML_DEVELOPER;

-- Viewer privileges
GRANT SELECT ON TABLE ML_MODELS.ML_SCHEMA.MODEL_REGISTRY TO ROLE ML_VIEWER;
GRANT SELECT ON TABLE ML_MODELS.ML_SCHEMA.MODEL_CARDS TO ROLE ML_VIEWER;
GRANT USAGE ON FUNCTION ML_MODELS.ML_SCHEMA.PREDICT_CUSTOMER_SEGMENT TO ROLE ML_VIEWER;

-- Create audit logging table
CREATE OR REPLACE TABLE governance.audit_logs (
    log_id VARCHAR DEFAULT UUID_STRING() PRIMARY KEY,
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    user_name VARCHAR,
    session_id VARCHAR,
    client_ip VARCHAR,
    operation VARCHAR,
    object_name VARCHAR,
    query_text TEXT,
    status VARCHAR,
    error_code VARCHAR,
    error_message TEXT
);

-- Create a stream for auditing
CREATE OR REPLACE STREAM governance.model_registry_audit_stream 
ON TABLE ML_MODELS.ML_SCHEMA.MODEL_REGISTRY;

-- Create task to process audit events
CREATE OR REPLACE TASK governance.process_audit_events
    WAREHOUSE = GOVERNANCE_WH
    SCHEDULE = '1 MINUTE'
WHEN
    SYSTEM$STREAM_HAS_DATA('governance.model_registry_audit_stream')
AS
INSERT INTO governance.audit_logs (
    user_name, 
    session_id,
    operation,
    object_name,
    query_text
)
SELECT 
    CURRENT_USER(),
    CURRENT_SESSION(),
    CASE 
        WHEN METADATA$ACTION = 'INSERT' THEN 'CREATE'
        WHEN METADATA$ACTION = 'DELETE' THEN 'DELETE'
        ELSE 'UPDATE'
    END,
    'MODEL_REGISTRY',
    'Model ID: ' || MODEL_ID
FROM governance.model_registry_audit_stream;
</pre>
        
        <h5 class="text-md font-semibold mt-4">Governance Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Create standardized model cards for all production models</li>
          <li>Implement approval workflows for model deployment</li>
          <li>Maintain comprehensive audit logs for all model activities</li>
          <li>Conduct regular model risk assessments</li>
          <li>Establish model review committee with cross-functional stakeholders</li>
          <li>Document data lineage for all model inputs</li>
          <li>Implement version control and immutable model artifacts</li>
          <li>Create regular compliance reports for regulatory requirements</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GovernanceSecurityStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 