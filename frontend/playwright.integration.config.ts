import { defineConfig } from '@playwright/test'

if (!process.env.APPLYSYNC_E2E_RUN_ID || !process.env.APPLYSYNC_E2E_API_ORIGIN) {
  throw new Error('Run the guarded Python integration runner from the repository root.')
}
export default defineConfig({
  testDir: './e2e', testMatch: '**/integration.spec.ts', workers: 1, reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1440, height: 1000 }, trace: 'retain-on-failure' },
  webServer: { command: 'npm run dev -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false,
    env: { VITE_API_BASE_URL: process.env.APPLYSYNC_E2E_API_ORIGIN } },
})
