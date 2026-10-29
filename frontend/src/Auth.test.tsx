import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'
import { internalDestination } from './Auth'

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
const a = { id: 'user-a', email: 'synthetic-a@example.com' }
const b = { id: 'user-b', email: 'synthetic-b@example.com' }
const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Private A', role: 'Engineer', applied_on: '2026-09-01', created_at: '2026-09-01T00:00:00Z' }
const mount = (path = '/applications') => { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('waits for session restoration and separates network failure from signed out', async () => {
  let resolve!: (response: Response) => void
  const fetchMock = vi.fn().mockImplementationOnce(() => new Promise<Response>(r => { resolve = r }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount()
  expect(screen.getByRole('status')).toHaveTextContent('Checking your session')
  expect(screen.queryByRole('searchbox')).not.toBeInTheDocument()
  expect(screen.queryByLabelText('Password')).not.toBeInTheDocument()
  await act(async () => resolve(json({}, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('Session unavailable')
  expect(screen.queryByLabelText('Password')).not.toBeInTheDocument()
  fetchMock.mockResolvedValue(json({}, 401))
  await user.click(screen.getByRole('button', { name: 'Retry session' }))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
})

it('uses credentialed writes with CSRF protection and prevents duplicate auth submission', async () => {
  let complete!: (response: Response) => void
  const posts = vi.fn(() => new Promise<Response>(resolve => { complete = resolve }))
  const fetchMock = vi.fn((url, options) => String(url).endsWith('/auth/me') ? Promise.resolve(json({}, 401))
    : options?.method === 'POST' ? posts() : Promise.resolve(json({ items: [], limit: 20, offset: 0 })))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount('/register')
  await user.type(await screen.findByLabelText('Email'), 'synthetic@example.com')
  await user.type(screen.getByLabelText('Password'), 'synthetic-password-only')
  await user.click(screen.getByRole('button', { name: 'Create account' }))
  expect(screen.getByRole('button', { name: 'Please wait…' })).toBeDisabled()
  await user.keyboard('{Enter}')
  expect(posts).toHaveBeenCalledTimes(1)
  const options = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/auth/register'))![1]
  expect(options.credentials).toBe('include')
  expect(options.headers['X-ApplySync-CSRF']).toBe('1')
  await act(async () => complete(json(a, 201)))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
})

it('discards private cache and cancels an old in-flight list before switching accounts', async () => {
  let finishOld!: (response: Response) => void
  let oldSignal!: AbortSignal
  let active = a
  let lists = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(active))
    if (String(url).endsWith('/auth/logout')) return Promise.resolve(new Response(null, { status: 204 }))
    if (String(url).endsWith('/auth/login')) { active = b; return Promise.resolve(json(b)) }
    lists++
    if (lists === 1) { oldSignal = options.signal; return new Promise<Response>(resolve => { finishOld = resolve }) }
    return Promise.resolve(json({ items: [], limit: 20, offset: 0 }))
  }))
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Log out' }))
  await user.type(await screen.findByLabelText('Email'), b.email)
  await user.type(screen.getByLabelText('Password'), 'synthetic-password-only')
  await user.click(screen.getByRole('button', { name: 'Sign in' }))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
  expect(oldSignal.aborted).toBe(true)
  await act(async () => finishOld(json({ items: [row], limit: 20, offset: 0 })))
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
  expect(screen.getByText(b.email)).toBeInTheDocument()
})

it('a 401 creation ends the session and never automatically replays the write', async () => {
  let writes = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(a))
    if (options?.method === 'POST') { writes++; return Promise.resolve(json({}, 401)) }
    return Promise.resolve(json({ items: [], limit: 20, offset: 0 }))
  }))
  const user = mount('/applications/new')
  await user.type(await screen.findByLabelText('Company', { exact: false }), 'Unsaved')
  await user.type(screen.getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(screen.getByLabelText('Applied date', { exact: false }), '2026-09-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  await waitFor(() => expect(writes).toBe(1))
})

it('rejects external and ambiguous return destinations', () => {
  for (const value of ['https://evil.example', '//evil.example', '/\\evil.example', '/login', '/applications/../login']) {
    expect(internalDestination(value)).toBe('/applications')
  }
  expect(internalDestination('/applications?offset=20&view=board')).toBe('/applications?offset=20&view=board')
})

it('does not claim logout succeeded when the network fails, and hides private data', async () => {
  vi.stubGlobal('fetch', vi.fn((url) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(a))
    if (String(url).endsWith('/auth/logout')) return Promise.reject(new Error('network unavailable'))
    return Promise.resolve(json({ items: [row], limit: 20, offset: 0 }))
  }))
  const user = mount()
  await screen.findByText('Private A')
  await user.click(screen.getByRole('button', { name: 'Log out' }))
  expect(await screen.findByRole('alert')).toHaveTextContent('Logout could not be confirmed')
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'Welcome back' })).not.toBeInTheDocument()
})

it('refreshing session on focus catches expiry and removes already loaded private records', async () => {
  let expired = false
  vi.stubGlobal('fetch', vi.fn((url) => String(url).endsWith('/auth/me')
    ? Promise.resolve(json(expired ? {} : a, expired ? 401 : 200))
    : Promise.resolve(json({ items: [row], limit: 20, offset: 0 }))))
  mount()
  await screen.findByText('Private A')
  expired = true
  await act(async () => { window.dispatchEvent(new Event('focus')) })
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByText('Private A')).not.toBeInTheDocument()
})
