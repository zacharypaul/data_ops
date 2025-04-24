<template>
  <div class="bg-dark-700 rounded-lg p-6 shadow-md hover:shadow-glow transition-shadow duration-300">
    <div class="flex items-center mb-4">
      <div class="bg-green-600 rounded-full w-12 h-12 flex items-center justify-center mr-4">
        <i class="fas fa-brain text-white text-xl"></i>
      </div>
      <h3 class="text-xl font-bold">Model Development</h3>
    </div>
    
    <p class="text-gray-300 mb-4">Develop, train, and evaluate K-means clustering models with experiment tracking</p>
    
    <div class="mb-4">
      <h4 class="text-md font-semibold mb-2">Key Components:</h4>
      <ul class="pl-5 list-disc text-gray-300">
        <li>Hyperparameter tuning</li>
        <li>Model training workflows</li>
        <li>Evaluation metrics & procedures</li>
      </ul>
    </div>
    
    <div class="flex justify-between items-center">
      <span class="text-sm text-gray-400">
        <i class="far fa-clock mr-1"></i> 2-3 weeks
      </span>
      <button 
        @click="$emit('view-details')" 
        class="px-4 py-2 bg-green-600 hover:bg-green-700 rounded text-sm font-medium"
      >
        View Details
      </button>
    </div>
    
    <div class="mt-5 border-t border-gray-700 pt-4" v-if="showDetails">
      <h4 class="text-lg font-semibold mb-3">Implementation Guide</h4>
      
      <div class="prose prose-dark text-gray-300">
        <p>Efficiently develop K-means clustering models in Snowflake ML with systematic experimentation and evaluation.</p>
        
        <h5 class="text-md font-semibold mt-4">Model Development Phases:</h5>
        <ul class="pl-5 list-disc">
          <li><strong>Experiment Design:</strong> Define model objectives and evaluation criteria</li>
          <li><strong>Hyperparameter Exploration:</strong> Systematically test different clustering settings</li>
          <li><strong>Model Training:</strong> Train K-means models using optimal parameters</li>
          <li><strong>Evaluation:</strong> Assess cluster quality with appropriate metrics</li>
          <li><strong>Model Selection:</strong> Choose the best performing model</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Snowflake Implementation:</h5>
        <p>Leverage Snowflake's ML capabilities for model development:</p>
        <ul class="pl-5 list-disc">
          <li>Use Snowflake ML's experiment tracking for parameter and metric logging</li>
          <li>Implement hyperparameter tuning with Snowpark for Python</li>
          <li>Evaluate clustering with silhouette score, inertia, and business metrics</li>
          <li>Store and version models in Snowflake</li>
          <li>Document model development decisions</li>
        </ul>
        
        <h5 class="text-md font-semibold mt-4">Hyperparameter Tuning:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# Hyperparameter tuning for K-means clustering
import snowflake.snowpark as snowpark
from snowflake.ml.modeling.preprocessing import OneHotEncoder, StandardScaler
from snowflake.ml.modeling.clustering import KMeans
from snowflake.ml.experiment import Experiment
import pandas as pd
import itertools

def tune_kmeans_hyperparameters(session, data_table):
    """
    Perform hyperparameter tuning for K-means clustering.
    """
    # Load preprocessed data
    df = session.table(data_table)
    
    # Initialize experiment
    experiment = Experiment(session, "KMeans_HyperparameterTuning")
    experiment.start_run()
    
    try:
        # One-hot encode categorical features
        encoder = OneHotEncoder(
            input_cols=["REGION", "CUSTOMER_TYPE"],
            output_cols=["REGION_ENCODED", "TYPE_ENCODED"]
        )
        df_encoded = encoder.fit_transform(df)
        
        # Scale numerical features
        scaler = StandardScaler(
            input_cols=["PURCHASE_AMOUNT", "VISIT_FREQUENCY"],
            output_cols=["AMOUNT_SCALED", "FREQUENCY_SCALED"]
        )
        df_scaled = scaler.fit_transform(df_encoded)
        
        # Features for clustering
        features = ["AMOUNT_SCALED", "FREQUENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]
        
        # Hyperparameter grid
        param_grid = {
            'n_clusters': [3, 4, 5, 6, 8],
            'init': ['k-means++', 'random'],
            'max_iter': [100, 300],
            'random_state': [42]
        }
        
        # Generate all parameter combinations
        param_combinations = list(itertools.product(
            param_grid['n_clusters'],
            param_grid['init'],
            param_grid['max_iter'],
            param_grid['random_state']
        ))
        
        results = []
        best_score = -1
        best_params = None
        
        # Perform grid search
        for n_clusters, init, max_iter, random_state in param_combinations:
            # Log parameters
            experiment.log_param("n_clusters", n_clusters)
            experiment.log_param("init", init)
            experiment.log_param("max_iter", max_iter)
            experiment.log_param("random_state", random_state)
            
            # Create and train model
            kmeans = KMeans(
                n_clusters=n_clusters,
                init=init,
                max_iter=max_iter,
                random_state=random_state
            )
            kmeans.fit(df_scaled[features])
            
            # Calculate metrics
            silhouette = kmeans.score(df_scaled[features])
            inertia = kmeans.inertia_
            
            # Log metrics
            experiment.log_metric("silhouette_score", silhouette)
            experiment.log_metric("inertia", inertia)
            
            # Store results
            results.append({
                'n_clusters': n_clusters,
                'init': init,
                'max_iter': max_iter,
                'random_state': random_state,
                'silhouette_score': silhouette,
                'inertia': inertia
            })
            
            # Track best model
            if silhouette > best_score:
                best_score = silhouette
                best_params = {
                    'n_clusters': n_clusters,
                    'init': init,
                    'max_iter': max_iter,
                    'random_state': random_state
                }
        
        # Log best parameters
        experiment.log_param("best_n_clusters", best_params['n_clusters'])
        experiment.log_param("best_init", best_params['init'])
        experiment.log_param("best_max_iter", best_params['max_iter'])
        experiment.log_param("best_silhouette", best_score)
        
        # Create results dataframe
        results_df = pd.DataFrame(results)
        
        # End experiment
        experiment.end_run()
        
        return results_df, best_params
        
    except Exception as e:
        experiment.log_param("error", str(e))
        experiment.end_run()
        raise e
</pre>
        
        <h5 class="text-md font-semibold mt-4">Model Training and Evaluation:</h5>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
# Train final K-means model with optimal parameters
def train_final_kmeans_model(session, data_table, model_params):
    """
    Train final K-means model with optimal parameters.
    """
    # Load preprocessed data
    df = session.table(data_table)
    
    # Initialize experiment for final model
    experiment = Experiment(session, "KMeans_FinalModel")
    run_id = experiment.start_run()
    
    try:
        # Preprocess data
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
        
        # Features for clustering
        features = ["AMOUNT_SCALED", "FREQUENCY_SCALED", "REGION_ENCODED", "TYPE_ENCODED"]
        
        # Log parameters
        for key, value in model_params.items():
            experiment.log_param(key, value)
        
        # Create and train model
        kmeans = KMeans(
            n_clusters=model_params['n_clusters'],
            init=model_params['init'],
            max_iter=model_params['max_iter'],
            random_state=model_params['random_state']
        )
        kmeans.fit(df_scaled[features])
        
        # Calculate metrics
        silhouette = kmeans.score(df_scaled[features])
        inertia = kmeans.inertia_
        
        # Log metrics
        experiment.log_metric("silhouette_score", silhouette)
        experiment.log_metric("inertia", inertia)
        
        # Add cluster assignments to data
        cluster_labels = kmeans.predict(df_scaled[features])
        df_with_clusters = df_scaled.with_column("CLUSTER_ID", cluster_labels)
        
        # Analyze clusters
        cluster_stats = df_with_clusters.group_by("CLUSTER_ID").agg({
            "PURCHASE_AMOUNT": ["avg", "min", "max", "count"],
            "VISIT_FREQUENCY": ["avg", "min", "max"]
        }).to_pandas()
        
        # Log cluster statistics as metrics
        for idx, row in cluster_stats.iterrows():
            cluster_id = row["CLUSTER_ID"]
            experiment.log_metric(f"cluster_{cluster_id}_size", row["PURCHASE_AMOUNT_count"])
            experiment.log_metric(f"cluster_{cluster_id}_avg_purchase", row["PURCHASE_AMOUNT_avg"])
            experiment.log_metric(f"cluster_{cluster_id}_avg_frequency", row["VISIT_FREQUENCY_avg"])
        
        # Generate business interpretations of clusters
        interpretations = interpret_clusters(df_with_clusters)
        
        # Log model and artifacts
        model_id = experiment.log_model(kmeans, "kmeans_model")
        experiment.log_artifact(encoder, "encoder")
        experiment.log_artifact(scaler, "scaler")
        
        # Save model metadata to Snowflake table
        session.sql(f"""
        INSERT INTO ml_ops.models.model_registry (
            model_id,
            model_type,
            description,
            parameters,
            metrics,
            experiment_run_id,
            created_at
        )
        VALUES (
            '{model_id}',
            'KMEANS',
            'Customer segmentation model',
            PARSE_JSON('{"n_clusters": ' || model_params["n_clusters"] || ', "init": "' || model_params["init"] || '", "max_iter": ' || model_params["max_iter"] || ', "random_state": ' || model_params["random_state"] || '}'),
            PARSE_JSON('{"silhouette_score": ' || silhouette || ', "inertia": ' || inertia || '}'),
            '{run_id}',
            CURRENT_TIMESTAMP()
        )
        """).collect()
        
        # End experiment
        experiment.end_run()
        
        return {
            "model_id": model_id,
            "model": kmeans,
            "encoder": encoder,
            "scaler": scaler,
            "silhouette_score": silhouette,
            "inertia": inertia,
            "cluster_stats": cluster_stats,
            "interpretations": interpretations
        }
        
    except Exception as e:
        experiment.log_param("error", str(e))
        experiment.end_run()
        raise e
</pre>
        
        <h5 class="text-md font-semibold mt-4">Cluster Interpretation:</h5>
        <p>Interpret clusters based on feature distributions to provide business value:</p>
        <pre class="bg-dark-800 p-3 rounded text-sm overflow-x-auto">
def interpret_clusters(df_with_clusters):
    """
    Generate business interpretations of clusters.
    """
    # Convert to Pandas for analysis
    pdf = df_with_clusters.to_pandas()
    
    # Initialize interpretations dictionary
    interpretations = {}
    
    # For each cluster
    for cluster_id in pdf["CLUSTER_ID"].unique():
        # Filter data for this cluster
        cluster_data = pdf[pdf["CLUSTER_ID"] == cluster_id]
        
        # Calculate key statistics
        avg_purchase = cluster_data["PURCHASE_AMOUNT"].mean()
        avg_frequency = cluster_data["VISIT_FREQUENCY"].mean()
        size = len(cluster_data)
        size_pct = (size / len(pdf)) * 100
        
        # Determine dominant region and customer type
        region_counts = cluster_data["REGION"].value_counts()
        dominant_region = region_counts.index[0] if not region_counts.empty else "Unknown"
        region_pct = (region_counts.iloc[0] / size) * 100 if not region_counts.empty else 0
        
        customer_type_counts = cluster_data["CUSTOMER_TYPE"].value_counts()
        dominant_type = customer_type_counts.index[0] if not customer_type_counts.empty else "Unknown"
        type_pct = (customer_type_counts.iloc[0] / size) * 100 if not customer_type_counts.empty else 0
        
        # Generate interpretation based on statistics
        if avg_purchase > 5000 and avg_frequency > 15:
            segment = "High Value"
            description = "Premium customers with high spending and frequent visits"
        elif avg_purchase > 3000 or avg_frequency > 10:
            segment = "Medium-High Value"
            description = "Valuable customers with above average spending or visit frequency"
        elif avg_purchase > 1000 or avg_frequency > 5:
            segment = "Medium Value"
            description = "Regular customers with moderate spending and visits"
        else:
            segment = "Low Value"
            description = "Occasional customers with lower spending and infrequent visits"
        
        # Store interpretation
        interpretations[cluster_id] = {
            "segment_name": segment,
            "description": description,
            "size": size,
            "size_percentage": size_pct,
            "avg_purchase_amount": avg_purchase,
            "avg_visit_frequency": avg_frequency,
            "dominant_region": dominant_region,
            "region_percentage": region_pct,
            "dominant_customer_type": dominant_type,
            "customer_type_percentage": type_pct,
            "recommended_actions": generate_recommendations(segment, avg_purchase, avg_frequency)
        }
    
    return interpretations

def generate_recommendations(segment, avg_purchase, avg_frequency):
    """
    Generate business recommendations based on segment.
    """
    if segment == "High Value":
        return [
            "Implement premium loyalty program",
            "Provide personalized concierge service",
            "Offer exclusive early access to new products"
        ]
    elif segment == "Medium-High Value":
        return [
            "Create targeted upgrade offers",
            "Develop retention campaigns",
            "Implement cross-selling strategies"
        ]
    elif segment == "Medium Value":
        return [
            "Focus on increasing purchase frequency",
            "Develop targeted upsell campaigns",
            "Implement engagement programs"
        ]
    else:  # Low Value
        return [
            "Create re-engagement campaigns",
            "Offer special promotions to increase frequency",
            "Analyze churn risk and implement preventive measures"
        ]
</pre>
        
        <h5 class="text-md font-semibold mt-4">Model Development Best Practices:</h5>
        <ol class="pl-5 list-decimal">
          <li>Start with exploratory analysis to understand the data</li>
          <li>Use systematic hyperparameter tuning to optimize models</li>
          <li>Evaluate models with multiple metrics (technical and business)</li>
          <li>Document all experiments, parameters, and decisions</li>
          <li>Interpret clusters to provide clear business value</li>
          <li>Create reproducible training workflows</li>
          <li>Store all artifacts, metadata, and code with proper versioning</li>
        </ol>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModelDevelopmentStep',
  emits: ['view-details'],
  props: {
    showDetails: {
      type: Boolean,
      default: false
    }
  }
}
</script> 