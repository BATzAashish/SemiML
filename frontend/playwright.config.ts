import { defineConfig } from "@playwright/test";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default defineConfig({
  testDir: "./e2e",
  timeout: 60000,
  expect: {
    timeout: 10000,
  },
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "on-first-retry",
  },
  webServer: [
    {
      command: "npm run dev -- --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: true,
      cwd: __dirname,
    },
    {
      command: "python -m uvicorn app.main:app --reload --port 8000",
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: true,
      cwd: path.join(__dirname, "..", "backend"),
    },
  ],
});
