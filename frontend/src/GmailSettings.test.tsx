import { act, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'
import { googleDestination } from './GmailSettings'

const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
const identity = { id: 'synthetic-user', email: 'synthetic@example.com' }
const disconnected = { available: true, status: 'not_connected', email: null, revocation_warning: false }
const mount = (path = '/settings/gmail') => { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('shows unavailable configuration without offering a broken connection', async () => {
  vi.stubGlobal('fetch', vi.fn(url => Promise.resolve(json(String(url).endsWith('/auth/me') ? identity : { ...disconnected, available: false }))))
  mount()
  expect(await screen.findByText('Not connected')).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'Connect Google account' })).toBeDisabled()
  expect(screen.getByText(/this task reads no messages/)).toBeInTheDocument()
})

it('disables duplicate starts, uses CSRF and displays safe failure', async () => {
  let finish!: (value: Response) => void
  const fetchMock = vi.fn((url, options) => String(url).endsWith('/auth/me') ? Promise.resolve(json(identity))
    : options.method === 'POST' ? new Promise<Response>(r => { finish = r }) : Promise.resolve(json(disconnected)))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Connect Google account' }))
  expect(screen.getByRole('button', { name: 'Starting connection…' })).toBeDisabled()
  const options = fetchMock.mock.calls.find(([url]) => String(url).endsWith('/gmail/start'))![1]
  expect(options.credentials).toBe('include'); expect(options.headers['X-ApplySync-CSRF']).toBe('1')
  await act(async () => finish(json({ detail: 'do not display raw provider error' }, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('could not be confirmed')
  expect(screen.queryByText('do not display raw provider error')).not.toBeInTheDocument()
})

it('disconnects and refreshes safe status including revocation warning', async () => {
  let connection = { ...disconnected, status: 'connected', email: 'synthetic-google@example.com' as string | null }
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(identity))
    if (options.method === 'POST') connection = { ...disconnected, status: 'disconnected', revocation_warning: true }
    return Promise.resolve(json(connection))
  }))
  const user = mount('/settings/gmail?result=connected')
  await user.click(await screen.findByRole('button', { name: 'Disconnect' }))
  expect(await screen.findByText('Disconnected')).toBeInTheDocument()
  expect(screen.queryByText('synthetic-google@example.com')).not.toBeInTheDocument()
  expect(screen.getByRole('alert')).toHaveTextContent('revocation could not be confirmed')
})

it('allows only the fixed Google authorization destination', () => {
  expect(googleDestination('https://accounts.google.com/o/oauth2/v2/auth?state=synthetic')).toContain('accounts.google.com')
  for (const value of ['https://evil.example/', 'javascript:alert(1)', 'https://accounts.google.com/other', 'https://user@accounts.google.com/o/oauth2/v2/auth']) expect(() => googleDestination(value)).toThrow()
})

it('aborts a delayed start on logout so it cannot navigate a new account', async () => {
  let finish!: (value: Response) => void
  let signal!: AbortSignal
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (String(url).endsWith('/auth/me')) return Promise.resolve(json(identity))
    if (String(url).endsWith('/auth/logout')) return Promise.resolve(new Response(null, { status: 204 }))
    if (String(url).endsWith('/gmail/start')) { signal = options.signal; return new Promise<Response>(r => { finish = r }) }
    return Promise.resolve(json(disconnected))
  }))
  const user = mount()
  await user.click(await screen.findByRole('button', { name: 'Connect Google account' }))
  await user.click(screen.getByRole('button', { name: 'Log out' }))
  expect(signal.aborted).toBe(true)
  await act(async () => finish(json({ authorization_url: 'https://accounts.google.com/o/oauth2/v2/auth?state=synthetic' })))
  expect(await screen.findByRole('heading', { name: 'Welcome back' })).toBeInTheDocument()
  expect(screen.queryByRole('heading', { name: 'Gmail connection' })).not.toBeInTheDocument()
})
