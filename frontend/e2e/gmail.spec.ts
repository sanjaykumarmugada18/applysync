import { expect, test } from '@playwright/test'

test('Gmail status, protected start, callback result, disconnect and mobile settings (mocked Google/API)', async ({ page }) => {
  const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173', 'access-control-allow-credentials': 'true' }
  let connection = { available: true, status: 'not_connected', email: null as string | null, revocation_warning: false }
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  await page.route('http://127.0.0.1:8000/**', async route => {
    const path = new URL(route.request().url()).pathname
    if (path === '/auth/me') return route.fulfill({ headers, json: { id: 'synthetic-user', email: 'synthetic@example.com' } })
    if (path === '/gmail/start') {
      expect(route.request().headers()['x-applysync-csrf']).toBe('1')
      return route.fulfill({ headers, json: { authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?state=synthetic' } })
    }
    if (path === '/gmail/disconnect') {
      expect(route.request().headers()['x-applysync-csrf']).toBe('1')
      connection = { ...connection, status: 'disconnected', email: null, revocation_warning: true }
    }
    return route.fulfill({ headers, json: connection })
  })
  await page.route('https://accounts.google.com/**', route => route.fulfill({ contentType: 'text/html', body: '<p>Mock Google authorization; no provider access.</p>' }))
  await page.goto('/settings/gmail')
  await expect(page.getByText('Not connected', { exact: true })).toBeVisible()
  await page.getByRole('button', { name: 'Connect Google account', exact: true }).click()
  await expect(page).toHaveURL(/https:\/\/accounts.google.com\/o\/oauth2\/v2\/auth/)
  connection = { ...connection, status: 'connected', email: 'synthetic-google@example.com' }
  await page.goto('/settings/gmail?result=connected')
  await expect(page.getByText('synthetic-google@example.com', { exact: true })).toBeVisible()
  await page.screenshot({ path: '../docs/screenshots/Build4_Task1/gmail-connected.png', fullPage: true })
  await page.getByRole('button', { name: 'Disconnect', exact: true }).click()
  await expect(page.getByText('Disconnected', { exact: true })).toBeVisible()
  await expect(page.getByRole('alert')).toContainText('revocation could not be confirmed')
  await page.setViewportSize({ width: 390, height: 844 })
  await page.emulateMedia({ reducedMotion: 'reduce' })
  await page.getByRole('button', { name: 'Open navigation' }).click()
  await page.keyboard.press('Escape')
  await expect(page.getByRole('dialog')).toHaveCount(0)
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true)
  await page.screenshot({ path: '../docs/screenshots/Build4_Task1/gmail-mobile.png', fullPage: true })
  await page.goto('/settings/gmail?result=different_account')
  await expect(page.getByText(/existing connection was preserved/)).toBeVisible()
  await page.goto('/settings/gmail?result=reauthorization_needed')
  await expect(page.getByText(/Offline authorization is missing/)).toBeVisible()
  await page.goto('/settings/gmail?result=failed')
  await expect(page.getByText(/Connection could not be completed/)).toBeVisible()
  expect(errors).toEqual([])
})
