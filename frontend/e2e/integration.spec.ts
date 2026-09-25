import { expect, test } from '@playwright/test'
import { mkdirSync } from 'node:fs'

const api = process.env.APPLYSYNC_E2E_API_ORIGIN!
const marker = process.env.APPLYSYNC_E2E_RUN_ID!
const screenshots = '../docs/screenshots/Build2_Task2'
mkdirSync(screenshots, { recursive: true })

test('real browser CORS, PostgreSQL creation, query refresh, pagination and reload', async ({ page }) => {
  let listReads = 0
  let posts = 0
  const errors: string[] = []
  page.on('pageerror', error => errors.push(error.message))
  page.on('request', request => {
    if (request.url().startsWith(api + '/applications?')) listReads++
    if (request.url() === api + '/applications' && request.method() === 'POST') posts++
  })
  await page.goto('/applications')
  await expect(page.getByRole('region', { name: 'Application list' }).getByRole('listitem')).toHaveCount(20)
  await expect(page.getByLabel('Sample stage')).toHaveCount(0)
  await expect(page.locator('.stage-label')).toHaveCount(0)
  await expect(page.getByText('Oldest first · No total count available')).toBeVisible()
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(page).toHaveURL(/offset=20/)
  await expect(page.getByRole('region', { name: 'Application list' }).getByRole('listitem').first()).toBeVisible()
  await page.getByRole('button', { name: 'Previous page' }).click()
  await expect(page).toHaveURL(/offset=0/)
  await page.getByRole('searchbox').fill('no-such-synthetic-result')
  await expect(page.getByText('No matches on this page')).toBeVisible()
  await page.getByRole('button', { name: 'Clear page search' }).click()
  await page.screenshot({ path: `${screenshots}/stored-list.png`, fullPage: true })

  const before = listReads
  await page.getByRole('link', { name: 'Add application', exact: true }).click()
  await page.getByRole('dialog').getByLabel('Company', { exact: false }).fill(`  ${marker} created  `)
  await page.getByRole('dialog').getByLabel('Role', { exact: false }).fill('  Browser Engineer  ')
  await page.getByRole('dialog').getByLabel('Applied date', { exact: false }).fill('2100-01-01')
  const confirmed = page.waitForResponse(response => response.url() === api + '/applications' && response.request().method() === 'POST')
  await page.getByRole('button', { name: 'Save application' }).click()
  const response = await confirmed
  expect(response.status()).toBe(201)
  expect(response.headers()['access-control-allow-origin']).toBe('http://127.0.0.1:4173')
  const record = await response.json()
  expect(record.company).toBe(marker + ' created')
  expect(record.role).toBe('Browser Engineer')
  expect(record.created_at).toBeTruthy()
  await expect(page).toHaveURL(new RegExp(`/applications/${record.id}`))
  await expect(page.getByText('Application saved to the database.')).toBeVisible()
  await expect.poll(() => listReads).toBeGreaterThan(before)
  const reread = page.waitForResponse(response => response.url() === `${api}/applications/${record.id}`)
  await page.reload()
  expect((await reread).status()).toBe(200)
  await expect(page.getByRole('dialog')).toContainText(marker + ' created')
  await expect(page.getByRole('dialog')).toContainText('1 Jan 2100')
  await page.screenshot({ path: `${screenshots}/stored-detail.png`, animations: 'disabled' })
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: `${screenshots}/stored-mobile-detail.png`, animations: 'disabled' })
  await page.keyboard.press('Escape')
  await page.screenshot({ path: `${screenshots}/stored-mobile-list.png`, fullPage: true })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)

  await page.goto('/applications/00000000-0000-4000-8000-000000000000')
  await expect(page.getByRole('dialog')).toContainText('Application not found.')
  await page.goto('/applications/not-a-uuid')
  await expect(page.getByRole('dialog')).toContainText('Invalid application ID')
  await page.keyboard.press('Escape')
  await page.getByRole('link', { name: 'Explore sample Board/List preview' }).click()
  const readsBeforePreview = listReads
  await expect(page.getByText('Design preview · Sample data')).toBeVisible()
  await page.getByRole('link', { name: 'Add application', exact: true }).click()
  await page.getByRole('dialog').getByLabel('Company', { exact: false }).fill('Preview-only Company')
  await page.getByRole('dialog').getByLabel('Role', { exact: false }).fill('Preview-only Role')
  await page.getByRole('dialog').getByLabel('Applied date', { exact: false }).fill('2100-01-01')
  await page.getByRole('button', { name: 'Add to preview' }).click()
  await expect(page.getByRole('status')).toContainText('added to the preview')
  expect(posts).toBe(1)
  expect(listReads).toBe(readsBeforePreview)
  await page.reload()
  await expect(page.getByText('Preview-only Company')).toHaveCount(0)
  expect(errors).toEqual([])
})
