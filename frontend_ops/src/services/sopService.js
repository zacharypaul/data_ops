import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Service for generating Standard Operating Procedures (SOPs)
 */
export default {
  /**
   * Generate a new SOP based on the provided data points and configuration
   * 
   * @param {Object} sopConfig - The SOP configuration
   * @param {Array} sopConfig.dataPoints - Selected data points to include in the SOP
   * @param {string} sopConfig.template - Template type (default, detailed, quickstart)
   * @param {string} sopConfig.audience - Target audience (technical, business, executive, mixed)
   * @param {string} sopConfig.goals - Key process goals for the SOP
   * @returns {Promise} - Promise resolving to the generated SOP document
   */
  async generateSOP(sopConfig) {
    try {
      const response = await axios.post(`${API_URL}/api/generate-sop`, sopConfig);
      
      if (response.data.success) {
        return response.data.sopDocument;
      } else {
        throw new Error(response.data.error || 'Failed to generate SOP');
      }
    } catch (error) {
      console.error('Error generating SOP:', error);
      throw error;
    }
  },
  
  /**
   * Exports the SOP document to a specified format (PDF, Markdown, etc.)
   * This is a placeholder for future implementation
   * 
   * @param {Object} sopDocument - The SOP document to export
   * @param {string} format - Export format (pdf, md, html)
   * @returns {Promise} - Promise resolving to the exported file data
   */
  async exportSOP(sopDocument, format = 'pdf') {
    // Placeholder for future implementation
    // Would send document to backend for conversion to specified format
    console.log(`Exporting SOP to ${format} format`, sopDocument);
    
    // For now, return a mock response
    return {
      success: true,
      message: `SOP exported to ${format} format (mock implementation)`
    };
  }
}; 