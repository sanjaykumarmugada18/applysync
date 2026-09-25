import { expect, test } from '@playwright/test'
import { mkdirSync } from 'node:fs'

const base = 'http://127.0.0.1:8000'
const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Synthetic Company', role: 'Engineer', applied_on: '2026-09-01', created_at: '2026-09-01T12:00:00Z' }
const headers = { 'access-control-allow-origin': 'http://127.0.0.1:4173' }

test('real Board/List share IDs, query state and paging with neutral stage fallback', async ({ page }) => {
  const records = Array.from({ length: 22 }, (_, i) => ({ ...row,
    id: `00000000-0000-4000-8000-${String(i + 100).padStart(12, '0')}`,
    company: `Synthetic Company ${i + 1}`,
  }))
  let reads = 0
  let writes = 0
  await page.route(`${base}/**`, async route => {
    const request = route.request()
    if (request.method() !== 'GET') { writes++; return route.abort() }
    const url = new URL(request.url())
    if (url.pathname === '/applications') {
      reads++
      const offset = Number(url.searchParams.get('offset'))
      return route.fulfill({ headers, json: { items: records.slice(offset, offset + 20), offset, limit: 20 } })
    }
    await route.fulfill({ headers, json: records.find(record => url.pathname.endsWith(record.id)) })
  })
  await page.goto('/applications?q=Synthetic&offset=0')
  const list = page.getByRole('region', { name: 'Application list' })
  await expect(list.getByRole('link')).toHaveCount(20)
  const ids = async (selector: string) => page.locator(selector).evaluateAll(links => links.map(link => new URL((link as HTMLAnchorElement).href).pathname))
  const listIds = await ids('.list-row')
  const before = reads
  await page.getByRole('button', { name: 'Board', exact: true }).click()
  const board = page.getByRole('region', { name: 'Stored application board' })
  await expect(board.getByRole('link')).toHaveCount(20)
  expect(await ids('.application-card')).toEqual(listIds)
  expect(reads).toBe(before)
  await expect(board.getByRole('heading', { name: 'Stage not recorded' })).toBeVisible()
  await expect(page.getByText('Applications will be grouped by stage when stage tracking is available.')).toBeVisible()
  await expect(page.getByText('Cedar & Finch')).toHaveCount(0)
  await expect(page.locator('.stage-label')).toHaveCount(0)
  await expect(page.getByLabel('Sample stage')).toHaveCount(0)
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(board.getByRole('link')).toHaveCount(2)
  await expect(page.getByText('2 shown · 2 loaded on this page')).toBeVisible()
  await expect(page.getByRole('searchbox')).toHaveValue('Synthetic')
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  const secondPageIds = await ids('.application-card')
  const shots = '../docs/screenshots/Build2_Task2/correction'
  mkdirSync(shots, { recursive: true })
  await page.screenshot({ path: `${shots}/stored-board.png`, fullPage: true })
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await expect(list.getByRole('link')).toHaveCount(2)
  expect(await ids('.list-row')).toEqual(secondPageIds)
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  await expect(page.getByRole('searchbox')).toHaveValue('Synthetic')
  await page.screenshot({ path: `${shots}/stored-list.png`, fullPage: true })
  await page.getByRole('button', { name: 'Board', exact: true }).click()
  await board.getByRole('link').first().click()
  expect(new URL(page.url()).pathname).toBe(secondPageIds[0])
  await expect(page.getByRole('dialog')).toContainText('Synthetic Company 21')
  await page.keyboard.press('Escape')
  await expect(page.getByRole('button', { name: 'Board', exact: true })).toHaveAttribute('aria-pressed', 'true')
  expect(new URL(page.url()).searchParams.get('offset')).toBe('20')
  await page.setViewportSize({ width: 390, height: 844 })
  await page.screenshot({ path: `${shots}/stored-mobile-board.png`, fullPage: true })
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true)
  await page.getByRole('button', { name: 'List', exact: true }).click()
  await page.screenshot({ path: `${shots}/stored-mobile-list.png`, fullPage: true })
  expect(await ids('.list-row')).toEqual(secondPageIds)
  expect(writes).toBe(0)
})

test('read network/server failures, retry, empty page and malformed pagination', async ({ page }) => {
  let state = 'network'
  await page.route(`${base}/**`, async route => {
    if (state === 'network') return route.abort('connectionrefused')
    await route.fulfill({ status: state === 'server' ? 500 : 200, headers, json: state === 'server' ? { detail: 'synthetic-private' } : { items: [], limit: 20, offset: 0 } })
  })
  await page.goto('/applications')
  await expect(page.getByRole('alert')).toContainText('Cannot reach the backend')
  state = 'server'
  await page.getByRole('button', { name: 'Retry list' }).click()
  await expect(page.getByRole('alert')).toContainText('server could not load')
  await expect(page.getByText('synthetic-private')).toHaveCount(0)
  state = 'empty'
  await page.getByRole('button', { name: 'Retry list' }).click()
  await expect(page.getByText('No stored applications yet')).toBeVisible()
  await page.goto('/applications?offset=-1')
  await expect(page.getByRole('alert')).toContainText('Invalid page offset')
})

test('pending POST, backend validation, server/network uncertainty and success', async ({ page }) => {
  let mode = 'validation'
  let finish!: () => void
  let postCount = 0
  await page.route(`${base}/**`, async route => {
    if (route.request().method() === 'POST') {
      postCount++
      await new Promise<void>(resolve => { finish = resolve })
      if (mode === 'network') return route.abort('connectionreset')
      return route.fulfill({ headers, status: mode === 'validation' ? 422 : mode === 'server' ? 500 : 201,
        json: mode === 'validation' ? { detail: [{ loc: ['body', 'company'], type: 'string_too_long', msg: 'synthetic-private' }] } : mode === 'server' ? { detail: 'synthetic-private' } : row })
    }
    await route.fulfill({ headers, json: route.request().url().includes('?') ? { items: [], limit: 20, offset: 0 } : row })
  })
  await page.goto('/applications/new')
  const dialog = page.getByRole('dialog')
  await dialog.getByLabel('Company', { exact: false }).fill('Synthetic Company')
  await dialog.getByLabel('Role', { exact: false }).fill('Engineer')
  await dialog.getByLabel('Applied date', { exact: false }).fill('2026-09-01')
  await dialog.getByRole('button', { name: 'Save application' }).click()
  await expect(dialog.getByRole('button', { name: 'Saving…' })).toBeDisabled()
  await page.keyboard.press('Enter')
  await page.keyboard.press('Escape')
  await expect(dialog).toBeVisible()
  await expect.poll(() => postCount).toBe(1)
  finish()
  await expect(dialog.getByText('Use 200 characters or fewer.')).toBeVisible()
  await expect(dialog.getByLabel('Company', { exact: false })).toHaveValue('Synthetic Company')
  for (const next of ['server', 'network']) {
    mode = next
    const before = postCount
    await dialog.getByRole('button', { name: 'Save application' }).click()
    await expect.poll(() => postCount).toBe(before + 1)
    finish()
    await expect(dialog.getByRole('alert')).toContainText('may have been saved')
    await expect(dialog.getByLabel('Role', { exact: false })).toHaveValue('Engineer')
  }
  expect(postCount).toBe(3)
  mode = 'success'
  await dialog.getByRole('button', { name: 'Save application' }).click()
  await expect.poll(() => postCount).toBe(4)
  finish()
  await expect(page.getByText('Application saved to the database.')).toBeVisible()
  await expect(page).toHaveURL(new RegExp(row.id))
})

test('direct detail read failure retries and full last page leads to honest empty next page', async ({ page }) => {
  let detailFails = true
  await page.route(`${base}/**`, async route => {
    const url = new URL(route.request().url())
    if (url.search) {
      const offset = Number(url.searchParams.get('offset'))
      return route.fulfill({ headers, json: { items: offset ? [] : Array.from({ length: 20 }, (_, i) => ({ ...row, id: `00000000-0000-4000-8000-${String(i).padStart(12, '0')}` })), limit: 20, offset } })
    }
    await route.fulfill({ headers, status: detailFails ? 500 : 200, json: detailFails ? {} : row })
  })
  await page.goto(`/applications/${row.id}`)
  await expect(page.getByRole('dialog').getByRole('alert')).toContainText('server could not load')
  detailFails = false
  await page.getByRole('button', { name: 'Retry details' }).click()
  await expect(page.getByRole('dialog')).toContainText('Synthetic Company')
  await page.keyboard.press('Escape')
  await page.getByRole('button', { name: 'Next page' }).click()
  await expect(page.getByText('No applications on this page')).toBeVisible()
  await expect(page.getByRole('button', { name: 'Next page' })).toBeDisabled()
  await expect(page.getByRole('button', { name: 'Previous page' })).toBeEnabled()
})
