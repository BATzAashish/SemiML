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
};

export default backendService;
