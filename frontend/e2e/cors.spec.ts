import { expect, test } from "@playwright/test";

test("frontend can reach backend with CORS", async ({ page }) => {
  await page.goto("/");

  const result = await page.evaluate(async () => {
    const response = await fetch("http://127.0.0.1:8000/api/connect", {
      method: "GET",
    });
    const data = await response.json();
    return { ok: response.ok, status: response.status, data };
  });

  expect(result.ok).toBe(true);
  expect(result.status).toBe(200);
  expect(result.data.status).toBe("connected");
});
