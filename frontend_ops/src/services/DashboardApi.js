/**
 * Dashboard API Service
 * Handles all API calls for the dashboard data
 */

// Mock data for development - would be replaced with actual API calls
const mockData = {
  metrics: {
    activeConnectors: { current: 28, total: 32, percentage: 87 },
    freshnessScore: { value: 94, percentage: 94 },
    qualityChecks: { passed: 582, total: 612, percentage: 95 },
    pipelineRuntime: { value: 42, unit: 'min', percentage: 68 }
  },
  
  alerts: [
    {
      id: 1,
      title: 'Stale Customer Data',
      description: 'Customer data hasn\'t been updated in the last 48 hours (Fivetran)',
      severity: 'WARNING',
      type: 'primary',
      timestamp: new Date().toISOString()
    },
    {
      id: 2,
      title: 'Anomaly Detected',
      description: 'Orders table row count decreased by 15% (dbt test failure)',
      severity: 'CRITICAL',
      type: 'accent',
      timestamp: new Date().toISOString()
    },
    {
      id: 3,
      title: 'Schema Change Detected',
      description: 'New column added to product_catalog table (Snowflake check)',
      severity: 'INFO',
      type: 'gold',
      timestamp: new Date().toISOString()
    }
  ],
  
  connectors: [
    {
      id: 1,
      name: 'Customer Data',
      type: { name: 'Fivetran', class: 'primary' },
      lastRefresh: '3 hours ago',
      lastRefreshTimestamp: '2023-07-01T12:00:00Z',
      freshness: { value: 98, status: 'green' },
      quality: { value: 100, status: 'green' },
      details: {
        source: 'MySQL Database',
        destination: 'Snowflake',
        schedule: 'Every 6 hours',
        owner: 'Data Engineering Team'
      }
    },
    {
      id: 2,
      name: 'Sales Transactions',
      type: { name: 'Airflow', class: 'accent' },
      lastRefresh: '30 minutes ago',
      lastRefreshTimestamp: '2023-07-01T14:30:00Z',
      freshness: { value: 96, status: 'green' },
      quality: { value: 98, status: 'green' },
      details: {
        source: 'API',
        destination: 'Snowflake',
        schedule: 'Every hour',
        owner: 'Data Engineering Team'
      }
    },
    {
      id: 3,
      name: 'Product Catalog',
      type: { name: 'ADF', class: 'secondary' },
      lastRefresh: '2 days ago',
      lastRefreshTimestamp: '2023-06-29T09:15:00Z',
      freshness: { value: 72, status: 'yellow' },
      quality: { value: 85, status: 'yellow' },
      details: {
        source: 'REST API',
        destination: 'Azure Synapse',
        schedule: 'Daily',
        owner: 'Product Team'
      }
    },
    {
      id: 4,
      name: 'Marketing Campaigns',
      type: { name: 'Lambda', class: 'gold' },
      lastRefresh: '12 hours ago',
      lastRefreshTimestamp: '2023-07-01T02:45:00Z',
      freshness: { value: 92, status: 'green' },
      quality: { value: 97, status: 'green' },
      details: {
        source: 'Marketing Platform API',
        destination: 'Snowflake',
        schedule: 'Every 12 hours',
        owner: 'Marketing Analytics'
      }
    }
  ],

  // Mock trend data
  trends: {
    '24h': {
      timestamps: generateTimestamps(24, 'hours'),
      series: [
        {
          id: 'freshness',
          name: 'Freshness Score',
          data: generateRandomData(24, 80, 100)
        },
        {
          id: 'quality',
          name: 'Quality Score',
          data: generateRandomData(24, 85, 100)
        },
        {
          id: 'runtime',
          name: 'Pipeline Runtime (min)',
          data: generateRandomData(24, 30, 60)
        },
        {
          id: 'volume',
          name: 'Data Volume (GB)',
          data: generateRandomData(24, 5, 20)
        }
      ],
      insights: [
        { 
          message: 'Freshness score improved by 5% in the last 6 hours', 
          trend: 'up',
          type: 'green'
        },
        { 
          message: 'Pipeline runtime briefly spiked at 06:00 UTC', 
          trend: 'up',
          type: 'yellow'
        }
      ]
    },
    '7d': {
      timestamps: generateTimestamps(7, 'days'),
      series: [
        {
          id: 'freshness',
          name: 'Freshness Score',
          data: generateRandomData(7, 75, 98)
        },
        {
          id: 'quality',
          name: 'Quality Score',
          data: generateRandomData(7, 80, 100)
        },
        {
          id: 'runtime',
          name: 'Pipeline Runtime (min)',
          data: generateRandomData(7, 35, 55)
        },
        {
          id: 'volume',
          name: 'Data Volume (GB)',
          data: generateRandomData(7, 5, 25)
        }
      ],
      insights: [
        { 
          message: 'Freshness score improved by 3% over the last 7 days', 
          trend: 'up',
          type: 'green'
        },
        { 
          message: 'Quality checks decreased by 2% in the last 3 days', 
          trend: 'down',
          type: 'yellow'
        },
        { 
          message: 'Pipeline runtime has remained stable over the last week', 
          trend: 'stable',
          type: 'primary'
        }
      ]
    },
    '30d': {
      timestamps: generateTimestamps(30, 'days'),
      series: [
        {
          id: 'freshness',
          name: 'Freshness Score',
          data: generateRandomData(30, 70, 98)
        },
        {
          id: 'quality',
          name: 'Quality Score',
          data: generateRandomData(30, 75, 100)
        },
        {
          id: 'runtime',
          name: 'Pipeline Runtime (min)',
          data: generateRandomData(30, 30, 60)
        },
        {
          id: 'volume',
          name: 'Data Volume (GB)',
          data: generateRandomData(30, 5, 30)
        }
      ],
      insights: [
        { 
          message: 'Freshness trending upward overall in the last month', 
          trend: 'up',
          type: 'green'
        },
        { 
          message: 'Data volume increased by 25% month-over-month', 
          trend: 'up',
          type: 'primary'
        },
        { 
          message: 'Quality dipped during system update mid-month', 
          trend: 'down',
          type: 'yellow'
        }
      ]
    },
    '90d': {
      timestamps: generateTimestamps(90, 'days'),
      series: [
        {
          id: 'freshness',
          name: 'Freshness Score',
          data: generateRandomData(90, 65, 98)
        },
        {
          id: 'quality',
          name: 'Quality Score',
          data: generateRandomData(90, 70, 100)
        },
        {
          id: 'runtime',
          name: 'Pipeline Runtime (min)',
          data: generateRandomData(90, 25, 65)
        },
        {
          id: 'volume',
          name: 'Data Volume (GB)',
          data: generateRandomData(90, 5, 35)
        }
      ],
      insights: [
        { 
          message: 'Overall quality has improved by 12% over the quarter', 
          trend: 'up',
          type: 'green'
        },
        { 
          message: 'Runtime performance decreased as data volume grew', 
          trend: 'down',
          type: 'yellow'
        },
        { 
          message: 'Pipeline optimizations in week 8 reduced average runtime by 15%', 
          trend: 'up',
          type: 'green'
        }
      ]
    }
  },

  // Data lineage for the connectors
  lineage: [
    {
      id: 1,
      name: 'Customer Data',
      type: 'Fivetran',
      lastRefresh: '3 hours ago',
      upstream: [],
      downstream: [
        { id: 2, name: 'Sales Transactions', type: 'Airflow' },
        { id: 4, name: 'Marketing Campaigns', type: 'Lambda' }
      ],
      quality: { value: 98, status: 'green' }
    },
    {
      id: 2,
      name: 'Sales Transactions',
      type: 'Airflow',
      lastRefresh: '30 minutes ago',
      upstream: [
        { id: 1, name: 'Customer Data', type: 'Fivetran' }
      ],
      downstream: [
        { id: 5, name: 'Sales Analytics', type: 'Airflow' },
        { id: 6, name: 'Revenue Dashboard', type: 'Lambda' }
      ],
      quality: { value: 96, status: 'green' }
    },
    {
      id: 3,
      name: 'Product Catalog',
      type: 'ADF',
      lastRefresh: '2 days ago',
      upstream: [],
      downstream: [
        { id: 5, name: 'Sales Analytics', type: 'Airflow' }
      ],
      quality: { value: 85, status: 'yellow' }
    },
    {
      id: 4,
      name: 'Marketing Campaigns',
      type: 'Lambda',
      lastRefresh: '12 hours ago',
      upstream: [
        { id: 1, name: 'Customer Data', type: 'Fivetran' }
      ],
      downstream: [
        { id: 7, name: 'Marketing Analytics', type: 'Lambda' }
      ],
      quality: { value: 92, status: 'green' }
    },
    {
      id: 5,
      name: 'Sales Analytics',
      type: 'Airflow',
      lastRefresh: '1 hour ago',
      upstream: [
        { id: 2, name: 'Sales Transactions', type: 'Airflow' },
        { id: 3, name: 'Product Catalog', type: 'ADF' }
      ],
      downstream: [
        { id: 8, name: 'Executive Dashboard', type: 'Fivetran' }
      ],
      quality: { value: 94, status: 'green' }
    },
    {
      id: 6,
      name: 'Revenue Dashboard',
      type: 'Lambda',
      lastRefresh: '45 minutes ago',
      upstream: [
        { id: 2, name: 'Sales Transactions', type: 'Airflow' }
      ],
      downstream: [],
      quality: { value: 96, status: 'green' }
    },
    {
      id: 7,
      name: 'Marketing Analytics',
      type: 'Lambda',
      lastRefresh: '5 hours ago',
      upstream: [
        { id: 4, name: 'Marketing Campaigns', type: 'Lambda' }
      ],
      downstream: [
        { id: 8, name: 'Executive Dashboard', type: 'Fivetran' }
      ],
      quality: { value: 90, status: 'green' }
    },
    {
      id: 8,
      name: 'Executive Dashboard',
      type: 'Fivetran',
      lastRefresh: '2 hours ago',
      upstream: [
        { id: 5, name: 'Sales Analytics', type: 'Airflow' },
        { id: 7, name: 'Marketing Analytics', type: 'Lambda' }
      ],
      downstream: [],
      quality: { value: 95, status: 'green' }
    }
  ]
};

// Helper function to generate timestamps
function generateTimestamps(count, unit) {
  const timestamps = [];
  const now = new Date();
  
  if (unit === 'hours') {
    for (let i = count - 1; i >= 0; i--) {
      const date = new Date(now);
      date.setHours(date.getHours() - i);
      timestamps.push(date.toISOString());
    }
  } else if (unit === 'days') {
    for (let i = count - 1; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      timestamps.push(date.toISOString());
    }
  }
  
  return timestamps;
}

// Helper function to generate random data
function generateRandomData(count, min, max) {
  return Array.from({ length: count }, () => Math.floor(Math.random() * (max - min + 1)) + min);
}

// Simulated API delay
const apiDelay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

export default {
  /**
   * Get dashboard metrics
   * @returns {Promise} Promise with metrics data
   */
  async getDashboardMetrics() {
    await apiDelay(500);
    return mockData.metrics;
  },

  /**
   * Get quality alerts
   * @returns {Promise} Promise with alerts data
   */
  async getQualityAlerts() {
    await apiDelay(700);
    return mockData.alerts;
  },

  /**
   * Get connector list
   * @param {Object} params - Filter parameters
   * @returns {Promise} Promise with connectors data
   */
  async getConnectors(params = {}) {
    await apiDelay(800);
    
    // In a real implementation, we would use params to filter the data
    // For now, just return all mock connectors
    return mockData.connectors;
  },

  /**
   * Get connector details by ID
   * @param {Number} id - Connector ID
   * @returns {Promise} Promise with connector details
   */
  async getConnectorDetails(id) {
    await apiDelay(600);
    
    const connector = mockData.connectors.find(c => c.id === id);
    if (!connector) {
      throw new Error(`Connector with ID ${id} not found`);
    }
    
    return connector;
  },

  /**
   * Refresh a connector
   * @param {Number} id - Connector ID to refresh
   * @returns {Promise} Promise with refresh status
   */
  async refreshConnector(id) {
    await apiDelay(1500);
    
    return {
      success: true,
      message: `Connector ${id} refresh triggered successfully`,
      jobId: `job-${Date.now()}`
    };
  },

  /**
   * Get trend data for connectors
   * @param {String} timeRange - Time range (24h, 7d, 30d, 90d)
   * @param {Number} connectorId - Optional connector ID to filter by
   * @returns {Promise} Promise with trend data
   */
  async getTrendData(timeRange = '7d', connectorId = null) {
    await apiDelay(1000);
    
    // Get trend data for the specified time range
    const trendData = mockData.trends[timeRange];
    
    if (!trendData) {
      throw new Error(`Invalid time range: ${timeRange}`);
    }
    
    // In a real implementation, we would filter by connector ID
    // For now, just return the mocked data
    return trendData;
  },

  /**
   * Get data lineage for connectors
   * @returns {Promise} Promise with lineage data
   */
  async getConnectorLineage() {
    await apiDelay(1200);
    
    return mockData.lineage;
  }
}; 