import { act, render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { afterEach, expect, it, vi } from 'vitest'
import { App } from './App'

const row = { id: '00000000-0000-4000-8000-000000000099', company: 'Stored Company', role: 'Engineer', applied_on: '2100-01-01', created_at: '2026-01-01T12:00:00Z' }
const json = (body: unknown, status = 200) => new Response(JSON.stringify(body), { status })
function mount(path = '/applications') { render(<MemoryRouter initialEntries={[path]}><App /></MemoryRouter>); return userEvent.setup() }
afterEach(() => vi.unstubAllGlobals())

it('lists real records without stage controls and clearly scopes search/counts', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(json({ items: [row], limit: 20, offset: 0 })))
  const user = mount()
  expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
  expect(screen.queryByLabelText('Sample stage')).not.toBeInTheDocument()
  expect(document.querySelector('.stage-label')).not.toBeInTheDocument()
  expect(screen.getByText('Local development · Stored data')).toBeInTheDocument()
  expect(screen.getByText('BUILD 2 · LOCAL DEVELOPMENT')).toBeInTheDocument()
  await user.type(screen.getByRole('searchbox'), 'no-match')
  expect(screen.getByText('No matches on this page')).toBeInTheDocument()
  expect(screen.getByText('Oldest first · No total count available')).toBeInTheDocument()
})
it.each(['board', 'list'])('has loading, empty, failure and retry states in %s without sample fallback', async view => {
  let resolve!: (response: Response) => void
  const fetchMock = vi.fn().mockImplementationOnce(() => new Promise<Response>(r => { resolve = r }))
    .mockResolvedValueOnce(json({ items: [], limit: 20, offset: 0 }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount(`/applications?view=${view}`)
  expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'List' : 'Board' }))
  expect(screen.getByRole('status')).toHaveTextContent('Loading applications')
  expect(fetchMock).toHaveBeenCalledTimes(1)
  await act(async () => resolve(json({}, 500)))
  expect(await screen.findByRole('alert')).toHaveTextContent('server could not load')
  expect(screen.queryByText('Cedar & Finch')).not.toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'Board' : 'List' }))
  expect(screen.getByRole('alert')).toHaveTextContent('server could not load')
  await user.click(screen.getByRole('button', { name: 'Retry list' }))
  expect(await screen.findByText('No stored applications yet')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: view === 'board' ? 'List' : 'Board' }))
  expect(screen.getByText('No stored applications yet')).toBeInTheDocument()
  expect(screen.queryByText('Cedar & Finch')).not.toBeInTheDocument()
})
it('keeps input on backend validation and blocks duplicate pending submissions', async () => {
  let finish!: (response: Response) => void
  const posts = vi.fn(() => new Promise<Response>(resolve => { finish = resolve }))
  vi.stubGlobal('fetch', vi.fn((_url, options) => options?.method === 'POST' ? posts() : Promise.resolve(json({ items: [], limit: 20, offset: 0 }))))
  const user = mount('/applications/new')
  const form = screen.getByRole('dialog')
  await user.type(within(form).getByLabelText('Company', { exact: false }), 'Retain Me')
  await user.type(within(form).getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(within(form).getByLabelText('Applied date', { exact: false }), '2100-01-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(screen.getByRole('button', { name: 'Saving…' })).toBeDisabled()
  await user.keyboard('{Enter}{Escape}')
  expect(posts).toHaveBeenCalledTimes(1)
  expect(screen.getByRole('dialog')).toBeInTheDocument()
  await act(async () => finish(json({ detail: [{ loc: ['body', 'company'], type: 'string_too_long' }] }, 422)))
  expect(await screen.findByText('Use 200 characters or fewer.')).toBeInTheDocument()
  expect(within(form).getByLabelText('Company', { exact: false })).toHaveValue('Retain Me')
})
it('opens confirmed detail and refreshes the list after creation', async () => {
  let created = false
  let lists = 0
  vi.stubGlobal('fetch', vi.fn((url, options) => {
    if (options?.method === 'POST') { created = true; return Promise.resolve(json(row, 201)) }
    if (String(url).includes('?')) { lists++; return Promise.resolve(json({ items: created ? [row] : [], limit: 20, offset: 0 })) }
    return Promise.resolve(json(row))
  }))
  const user = mount('/applications/new')
  await user.type(screen.getByLabelText('Company', { exact: false }), 'Stored Company')
  await user.type(screen.getByLabelText('Role', { exact: false }), 'Engineer')
  await user.type(screen.getByLabelText('Applied date', { exact: false }), '2100-01-01')
  await user.click(screen.getByRole('button', { name: 'Save application' }))
  expect(await screen.findByText('Application saved to the database.')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  expect(await screen.findByRole('link', { name: 'Engineer at Stored Company' })).toBeInTheDocument()
  expect(lists).toBeGreaterThanOrEqual(2)
})
it('loads direct details, distinguishes missing/malformed IDs, and never fetches preview data', async () => {
  const fetchMock = vi.fn().mockResolvedValue(json({ items: [], limit: 20, offset: 0 }))
  vi.stubGlobal('fetch', fetchMock)
  const user = mount('/applications/bad-id')
  expect(screen.getByRole('alert')).toHaveTextContent('Invalid application ID')
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(1))
  await user.click(screen.getByRole('link', { name: 'Explore sample Board/List preview' }))
  expect(screen.getByText('Cedar & Finch')).toBeInTheDocument()
  expect(screen.getByText('Design preview · Sample data')).toBeInTheDocument()
  expect(fetchMock).toHaveBeenCalledTimes(1)
})
