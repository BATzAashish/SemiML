import { defineConfig } from "@playwright/test";
import path from "path";

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
      command: "d:/Projects/SemiML/.venv/Scripts/python.exe -m uvicorn app.main:app --reload",
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: true,
      cwd: path.join(__dirname, "..", "backend"),
    },
  ],
});
