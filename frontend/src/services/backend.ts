/**
 * Frontend Integration Guide - SemiML Backend Connection
 * 
 * Add this service to your frontend project:
 * Location: frontend/src/services/backend.ts
 */

const BACKEND_URL = "http://localhost:8000";

export const backendService = {
  /**
   * Test connection to backend
   * Call this on app startup or from a connection test page
   */
  async testConnection() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/connect`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Backend Connected:", data);
      return data;
    } catch (error) {
      console.error("Backend connection failed:", error);
      throw error;
    }
  },

  /**
   * Get system information from backend
   * Displays available modules and endpoints
   */
  async getSystemInfo() {
    try {
      const response = await fetch(`${BACKEND_URL}/api/system-info`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("System Info:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch system info:", error);
      throw error;
    }
  },

  /**
   * Check health of backend
   */
  async checkHealth() {
    try {
      const response = await fetch(`${BACKEND_URL}/health`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("Health check failed:", error);
      throw error;
    }
  },

  /**
   * Upload a dataset
   */
  async uploadDataset(
    file: File,
    description: string = ""
  ): Promise<any> {
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("description", description);

      const response = await fetch(`${BACKEND_URL}/api/upload-dataset`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Dataset uploaded:", data);
      return data;
    } catch (error) {
      console.error("Failed to upload dataset:", error);
      throw error;
    }
  },

  /**
   * Get dataset information
   */
  async getDatasetInfo(datasetId: string): Promise<any> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/dataset/${datasetId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Dataset info:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch dataset info:", error);
      throw error;
    }
  },

  /**
   * List all uploaded datasets
   */
  async listDatasets(): Promise<any> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/datasets`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Datasets:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch datasets:", error);
      throw error;
    }
  },

  /**
   * Delete a dataset
   */
  async deleteDataset(datasetId: string): Promise<any> {
    try {
      const response = await fetch(`${BACKEND_URL}/api/dataset/${datasetId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Dataset deleted:", data);
      return data;
    } catch (error) {
      console.error("Failed to delete dataset:", error);
      throw error;
    }
  },

  /**
   * Extract meta-features from a dataset
   * Module 3
   */
  async extractMetaFeatures(datasetId: string): Promise<any> {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/extract-meta-features/${datasetId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Meta-features extracted:", data);
      return data;
    } catch (error) {
      console.error("Failed to extract meta-features:", error);
      throw error;
    }
  },

  /**
   * Get meta-features for a dataset
   * Module 3
   */
  async getMetaFeatures(datasetId: string): Promise<any> {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/meta-features/${datasetId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Meta-features:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch meta-features:", error);
      throw error;
    }
  },

  /**
   * Get data preview for a dataset
   * Module 3
   */
  async getDataPreview(datasetId: string, rows: number = 10): Promise<any> {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/data-preview/${datasetId}?rows=${rows}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Data preview:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch data preview:", error);
      throw error;
    }
  },

  /**
   * Get comprehensive dataset summary
   * Module 3
   */
  async getDatasetSummary(datasetId: string): Promise<any> {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/dataset-summary/${datasetId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Dataset summary:", data);
      return data;
    } catch (error) {
      console.error("Failed to fetch dataset summary:", error);
      throw error;
    }
  },

  /**
   * Compare two datasets
   * Module 3
   */
  async compareDatasets(
    datasetId1: string,
    datasetId2: string
  ): Promise<any> {
    try {
      const response = await fetch(
        `${BACKEND_URL}/api/compare-datasets?dataset_1_id=${datasetId1}&dataset_2_id=${datasetId2}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Datasets compared:", data);
      return data;
    } catch (error) {
      console.error("Failed to compare datasets:", error);
      throw error;
    }
  },
};

export default backendService;
