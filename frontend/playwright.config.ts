import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e', testIgnore: '**/integration.spec.ts', fullyParallel: false, workers: 1, reporter: 'list',
  use: { baseURL: 'http://127.0.0.1:4173', browserName: 'chromium', viewport: { width: 1600, height: 1000 }, trace: 'retain-on-failure' },
  webServer: { command: 'npm run preview -- --port 4173 --strictPort', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
})
