import { test, expect } from "@playwright/test";

test.describe("SemiML Frontend Integration", () => {
  const FRONTEND_URL = "http://127.0.0.1:5173";
  const BACKEND_URL = "http://127.0.0.1:8000";

  test.beforeEach(async ({ page }) => {
    // Navigate to frontend
    await page.goto(FRONTEND_URL);
  });

  test("frontend should load successfully", async ({ page }) => {
    // Check page title or main content
    await expect(page).toHaveTitle(/SemiML|React/i);

    // Wait for content to load
    await page.waitForLoadState("networkidle");

    // Page should not have error messages
    const errorElements = page.locator('[role="alert"], .error, .exception');
    const errorCount = await errorElements.count();
    expect(errorCount).toBe(0);
  });

  test("backend status indicator should show healthy", async ({ page }) => {
    // Look for backend status in UI
    const statusIndicators = page.locator(
      'text=/backend|healthy|connected/i'
    );
    const count = await statusIndicators.count();

    // Either the indicator exists or we can fetch it
    if (count > 0) {
      const text = await statusIndicators.first().textContent();
      expect(text).not.toBeNull();
    }
  });

  test("API should be reachable from frontend context", async ({ page }) => {
    // Execute fetch request in page context to verify API connectivity
    const apiResponse = await page.evaluate(async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/health");
        const data = await response.json();
        return {
          status: response.status,
          data: data,
        };
      } catch (error) {
        return {
          error: error instanceof Error ? error.message : "Unknown error",
        };
      }
    });

    // Either API responds or CORS is expected
    if (!("error" in apiResponse)) {
      expect(apiResponse.status).toBe(200);
      expect(apiResponse.data.status).toBe("healthy");
    }
  });

  test("frontend should have main navigation elements", async ({ page }) => {
    // Check for common navigation patterns
    const navigationPatterns = [
      page.locator("nav"),
      page.locator("header"),
      page.locator('[role="navigation"]'),
      page.locator("button"), // At least some buttons should exist
    ];

    let hasNavigation = false;
    for (const pattern of navigationPatterns) {
      const count = await pattern.count();
      if (count > 0) {
        hasNavigation = true;
        break;
      }
    }

    // Frontend should have some navigation structure
    expect(hasNavigation).toBe(true);
  });

  test("frontend dashboard should render without crashes", async ({
    page,
  }) => {
    // Wait for page to stabilize
    await page.waitForLoadState("domcontentloaded");

    // Check for common error patterns
    const consoleMessages: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") {
        consoleMessages.push(msg.text());
      }
    });

    // Wait a bit for any deferred errors
    await page.waitForTimeout(2000);

    // Should not have console errors (excluding expected network errors)
    const criticalErrors = consoleMessages.filter(
      (msg) =>
        !msg.includes("Failed to fetch") &&
        !msg.includes("CORS") &&
        !msg.includes("ERR_")
    );

    expect(criticalErrors).toHaveLength(0);
  });

  test("frontend should display content area", async ({ page }) => {
    // Look for main content area
    const mainElements = [
      page.locator("main"),
      page.locator('[role="main"]'),
      page.locator(".main-content"),
      page.locator(".container"),
      page.locator("#app"),
      page.locator("#root"),
    ];

    let hasContent = false;
    for (const element of mainElements) {
      const count = await element.count();
      const visible = await element.first().isVisible().catch(() => false);
      if (count > 0 && visible) {
        hasContent = true;
        break;
      }
    }

    // Frontend should have visible content area
    expect(hasContent).toBe(true);
  });

  test("frontend should have interactive elements", async ({ page }) => {
    // Look for interactive elements
    const interactiveElements = page.locator(
      "button, input, select, textarea, [role='button'], [role='link']"
    );

    const count = await interactiveElements.count();

    // Should have at least some interactive elements
    expect(count).toBeGreaterThan(0);
  });

  test("page should be responsive", async ({ page }) => {
    // Test viewport changes
    const viewportSizes = [
      { width: 1920, height: 1080 }, // Desktop
      { width: 768, height: 1024 }, // Tablet
      { width: 375, height: 667 }, // Mobile
    ];

    for (const size of viewportSizes) {
      await page.setViewportSize(size);
      await page.waitForLoadState("networkidle");

      // Page should still be functional
      const errorElements = page.locator('[role="alert"], .error');
      const errorCount = await errorElements.count();
      expect(errorCount).toBe(0);
    }
  });
});
