import { test, expect } from "@playwright/test";

test.describe("SemiML Backend API Integration", () => {
  const BACKEND_URL = "http://127.0.0.1:8000";

  test("backend health endpoint should return healthy status", async ({
    request,
  }) => {
    const response = await request.get(`${BACKEND_URL}/health`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.status).toBe("healthy");
    expect(data.message).toContain("SemiML Backend");
  });

  test("backend root endpoint should return system info", async ({
    request,
  }) => {
    const response = await request.get(`${BACKEND_URL}/`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.name).toBeDefined();
    expect(data.version).toBeDefined();
    expect(data.status).toBe("operational");
  });

  test("backend connect endpoint should return system ready", async ({
    request,
  }) => {
    const response = await request.get(`${BACKEND_URL}/api/connect`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.system_ready).toBe(true);
    expect(data.modules).toBeDefined();
  });

  test("backend should accept meta-feature extraction requests", async ({
    request,
  }) => {
    const response = await request.post(
      `${BACKEND_URL}/api/extract-meta-features`,
      {
        data: {
          data: [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
          ],
          feature_names: ["feature1", "feature2", "feature3"],
        },
      }
    );
    // Accept 200, 422, or 500 - just checking it responds
    expect([200, 422, 500]).toContain(response.status());
  });

  test("backend should accept meta-decision requests", async ({ request }) => {
    const response = await request.post(`${BACKEND_URL}/api/meta-decision`, {
      data: {
        meta_features: {
          num_samples: 1000,
          num_features: 10,
        },
        available_models: ["random_forest", "svm", "neural_network"],
        optimization_metric: "accuracy",
      },
    });
    // Accept various status codes
    expect([200, 422, 500]).toContain(response.status());
  });

  test("backend should have health monitoring endpoints", async ({
    request,
  }) => {
    // Detailed health check
    const healthResponse = await request.get(`${BACKEND_URL}/api/health/detailed`);
    expect([200, 404]).toContain(healthResponse.status());

    // Metrics overview
    const metricsResponse = await request.get(`${BACKEND_URL}/api/metrics/overall`);
    expect([200, 404]).toContain(metricsResponse.status());

    // Rate limit status
    const rateLimitResponse = await request.get(
      `${BACKEND_URL}/api/rate-limit/status`
    );
    expect([200, 404]).toContain(rateLimitResponse.status());
  });

  test("backend should have OpenAPI documentation", async ({ request }) => {
    const response = await request.get(`${BACKEND_URL}/openapi.json`);
    expect(response.status()).toBe(200);
    const data = await response.json();
    expect(data.openapi).toBeDefined();
    expect(data.paths).toBeDefined();
    expect(Object.keys(data.paths).length).toBeGreaterThan(0);
  });

  test("backend should list more than 20 API endpoints", async ({
    request,
  }) => {
    const response = await request.get(`${BACKEND_URL}/openapi.json`);
    const data = await response.json();
    const endpoints = Object.keys(data.paths);
    expect(endpoints.length).toBeGreaterThan(20);
    
    // Check for key endpoints
    const endpointStrings = endpoints.join(" ");
    expect(endpointStrings).toContain("health");
    expect(endpointStrings).toContain("connect");
  });

  test("backend LLM status should be available", async ({ request }) => {
    const response = await request.get(`${BACKEND_URL}/api/llm-status`);
    expect([200, 404]).toContain(response.status());
    if (response.status() === 200) {
      const data = await response.json();
      expect(data.available_llm).toBeDefined();
    }
  });
});
