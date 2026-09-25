import type { Application, CreateValues } from './data'

export interface ApplicationPage { items: Application[]; limit: number; offset: number }
export type FieldErrors = Partial<Record<keyof CreateValues, string>>
export class ApiError extends Error {
  constructor(public kind: 'configuration' | 'network' | 'server' | 'validation' | 'missing' | 'response', public fields: FieldErrors = {}) {
    super(kind)
  }
}

export function apiBase(value = import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000') {
  try {
    const url = new URL(value)
    if (url.protocol !== 'http:' || !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) ||
        url.username || url.password || url.search || url.hash || url.pathname !== '/') throw new Error()
    return url.origin
  } catch { throw new ApiError('configuration') }
}

export function errorMessage(error: unknown, writing = false) {
  const kind = error instanceof ApiError ? error.kind : 'network'
  if (kind === 'configuration') return 'Set VITE_API_BASE_URL to the local backend origin, then restart Vite.'
  if (kind === 'validation') return 'Check the highlighted fields and try again.'
  if (kind === 'missing') return 'Application not found.'
  if (writing) return 'Creation could not be confirmed. It may have been saved. Check the application list before submitting again.'
  if (kind === 'server') return 'The server could not load applications. Try again.'
  if (kind === 'response') return 'The server returned an unexpected response. Try again.'
  return 'Cannot reach the backend. Check that it is running, then retry.'
}

function validationFields(body: unknown): FieldErrors {
  const fields: FieldErrors = {}
  const details = (body as { detail?: unknown })?.detail
  if (Array.isArray(details)) for (const item of details) {
    const field: unknown = item?.loc?.at(-1)
    // Never surface raw server messages or echoed input values.
    if (field === 'company' || field === 'role') fields[field] = item.type === 'string_too_long'
      ? 'Use 200 characters or fewer.' : `Enter a valid ${field}.`
    if (field === 'applied_on') fields.applied_on = 'Enter a valid date.'
  }
  return fields
}

async function request(path: string, body?: CreateValues, signal?: AbortSignal): Promise<unknown> {
  const base = apiBase()
  const timeout = AbortSignal.timeout(15_000)
  let response: Response
  try {
    response = await fetch(`${base}${path}`, {
      method: body ? 'POST' : 'GET', credentials: 'omit',
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body: body ? JSON.stringify(body) : undefined,
      signal: signal ? AbortSignal.any([signal, timeout]) : timeout,
    })
  } catch { throw new ApiError('network') }
  if (response.status === 404) throw new ApiError('missing')
  if (response.status === 422) {
    let details: unknown
    try { details = await response.json() } catch { details = undefined }
    throw new ApiError('validation', validationFields(details))
  }
  if (!response.ok) throw new ApiError('server')
  try { return await response.json() } catch { throw new ApiError('response') }
}

function application(value: unknown): Application {
  const row = value as Application
  if (!row || !['id', 'company', 'role', 'applied_on', 'created_at'].every(key => typeof row[key as keyof Application] === 'string')) throw new ApiError('response')
  if (!isUuid(row.id) || !/^\d{4}-\d{2}-\d{2}$/.test(row.applied_on) || Number.isNaN(Date.parse(row.applied_on))) throw new ApiError('response')
  return { id: row.id, company: row.company, role: row.role, applied_on: row.applied_on, created_at: row.created_at }
}
export function isUuid(value: string) { return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value) }
export async function listApplications(limit: number, offset: number, signal?: AbortSignal): Promise<ApplicationPage> {
  const page = await request(`/applications?limit=${limit}&offset=${offset}`, undefined, signal) as ApplicationPage
  if (!page || !Array.isArray(page.items) || page.limit !== limit || page.offset !== offset) throw new ApiError('response')
  return { items: page.items.map(application), limit, offset }
}
export async function getApplication(id: string, signal?: AbortSignal) { return application(await request(`/applications/${encodeURIComponent(id)}`, undefined, signal)) }
export async function createApplication(values: CreateValues) { return application(await request('/applications', values)) }
