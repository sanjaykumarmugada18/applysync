import { afterEach, expect, it, vi } from 'vitest'
import { ApiError, apiBase, createApplication, errorMessage, listApplications } from './api'

afterEach(() => vi.unstubAllGlobals())
it('validates public configuration without echoing it', () => {
  expect(apiBase('http://127.0.0.1:8000')).toBe('http://127.0.0.1:8000')
  for (const value of ['', 'replace-with-local-api-origin', 'https://remote.example', 'http://user:synthetic@localhost:8000', 'http://localhost:8000/?token=synthetic']) {
    expect(() => apiBase(value)).toThrow('configuration')
  }
})
it('maps validation using safe field names without exposing raw input or messages', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response(JSON.stringify({ detail: [
    { loc: ['body', 'company'], type: 'string_too_long', msg: 'synthetic-private', input: 'synthetic-private' },
  ] }), { status: 422 })))
  await expect(createApplication({ company: 'A', role: 'B', applied_on: '2026-01-01' })).rejects.toMatchObject({
    kind: 'validation', fields: { company: 'Use 200 characters or fewer.' },
  })
})
it('does not retry a failed POST and describes its uncertain outcome', async () => {
  const fetchMock = vi.fn().mockRejectedValue(new Error('synthetic-private'))
  vi.stubGlobal('fetch', fetchMock)
  await expect(createApplication({ company: 'A', role: 'B', applied_on: '2026-01-01' })).rejects.toMatchObject({ kind: 'network' })
  expect(fetchMock).toHaveBeenCalledTimes(1)
  expect(errorMessage(new ApiError('network'), true)).toContain('may have been saved')
  expect(errorMessage(new Error('synthetic-private'))).not.toContain('synthetic-private')
})
it('rejects malformed successful responses rather than falling back to fixtures', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(new Response('{}')))
  await expect(listApplications(20, 0)).rejects.toMatchObject({ kind: 'response' })
})
