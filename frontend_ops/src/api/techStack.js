// API for tech stack data

export const getTechStackData = () => {
  return new Promise((resolve) => {
    // Mock response delay
    setTimeout(() => {
      resolve({
        nodes: [
          {
            id: 'snowflake',
            name: 'Snowflake',
            type: 'source',
            description: 'Cloud data warehouse platform',
            technologies: ['SQL', 'Snowpipe', 'Streams'],
            icon: '/images/snowflake-icon.png',
            x: 200,
            y: 150,
            z: 10
          },
          {
            id: 'fabric',
            name: 'Microsoft Fabric',
            type: 'processor',
            description: 'Analytics platform for data professionals',
            technologies: ['Data Factory', 'Synapse Analytics', 'Power BI'],
            icon: '/images/fabric-icon.png',
            x: 500,
            y: 150,
            z: 10
          },
          {
            id: 'powerbi',
            name: 'Power BI',
            type: 'destination',
            description: 'Business analytics service',
            technologies: ['DAX', 'Power Query', 'Data Modeling'],
            icon: '/images/powerbi-icon.png',
            x: 350,
            y: 400,
            z: 0
          }
        ],
        links: [
          {
            source: 'snowflake',
            target: 'fabric',
            value: 10,
            type: 'data',
            active: true,
            refreshFrequency: 'hourly',
            description: 'Data flows from Snowflake to Fabric'
          },
          {
            source: 'snowflake',
            target: 'powerbi',
            value: 5,
            type: 'reporting',
            active: true,
            refreshFrequency: 'daily',
            description: 'Direct connection from Snowflake to Power BI'
          },
          {
            source: 'fabric',
            target: 'powerbi',
            value: 8,
            type: 'visualization',
            active: true,
            refreshFrequency: 'real-time',
            description: 'Visualizations in Power BI fed by Fabric'
          }
        ]
      });
    }, 500);
  });
};

export const getNodeMetrics = (nodeId) => {
  return new Promise((resolve) => {
    // Mock response delay
    setTimeout(() => {
      const metrics = {
        snowflake: {
          dataVolume: '2.3 TB',
          queryPerformance: '0.8s avg',
          costEstimate: '$1,200/month',
          activeUsers: 34,
          dataTables: 156
        },
        fabric: {
          dataVolume: '1.8 TB',
          processingJobs: 42,
          pipelineSuccess: '98.5%',
          costEstimate: '$950/month',
          dataflows: 23
        },
        powerbi: {
          reports: 28,
          dashboards: 12,
          dailyUsers: 156,
          refreshSuccess: '99.2%',
          viewTime: '45 min avg'
        }
      };
      
      resolve(metrics[nodeId] || {});
    }, 300);
  });
}; 