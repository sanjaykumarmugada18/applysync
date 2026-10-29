import { useEffect, useRef, useState } from 'react'
import { useSearchParams } from 'react-router'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { request } from './api'
import { Button } from './components/ui'

type Connection = { available: boolean; status: 'not_connected' | 'connected' | 'disconnected' | 'reauthorization_needed'; email: string | null; revocation_warning: boolean }
const labels = { not_connected: 'Not connected', connected: 'Connected', disconnected: 'Disconnected', reauthorization_needed: 'Reauthorization needed' }
const outcomes: Record<string, string> = {
  connected: 'Google authorization completed.',
  failed: 'Connection could not be completed. Try connecting again.',
  different_account: 'Your existing connection was preserved. Disconnect it before connecting a different Google account.',
  reauthorization_needed: 'Offline authorization is missing or expired. Connect again to grant consent.',
}
export function googleDestination(value: unknown) {
  if (typeof value !== 'string') throw new Error('Invalid destination')
  const url = new URL(value)
  if (url.origin !== 'https://accounts.google.com' || url.pathname !== '/o/oauth2/v2/auth' || url.username || url.password || url.hash) throw new Error('Invalid destination')
  return url.href
}
export function GmailSettings() {
  const [params, setParams] = useSearchParams()
  const client = useQueryClient()
  const active = useRef<AbortController | null>(null)
  const [pending, setPending] = useState('')
  const [failure, setFailure] = useState('')
  useEffect(() => () => { active.current?.abort() }, [])
  const query = useQuery({ queryKey: ['gmail'], queryFn: async ({ signal }) => {
    const value = await request('/gmail', undefined, signal) as Connection
    if (!value || !Object.hasOwn(labels, value.status) || typeof value.available !== 'boolean' || typeof value.revocation_warning !== 'boolean' || (value.email !== null && typeof value.email !== 'string')) throw new Error('Invalid status')
    return value
  } })
  async function act(action: 'start' | 'disconnect') {
    if (active.current) return
    const controller = new AbortController(); active.current = controller
    setParams({}, { replace: true })
    setPending(action); setFailure('')
    try {
      const value = await request(`/gmail/${action}`, {}, controller.signal)
      if (controller.signal.aborted) return
      if (action === 'start') window.location.assign(googleDestination((value as { authorization_url?: unknown })?.authorization_url))
      else await client.invalidateQueries({ queryKey: ['gmail'] })
    } catch {
      if (!controller.signal.aborted) setFailure('The connection change could not be confirmed. Refresh status before retrying.')
    } finally {
      if (!controller.signal.aborted) { active.current = null; setPending('') }
    }
  }
  const data = query.data
  return <section className="applications-workspace">
    <div className="page-heading"><div><p className="eyebrow">YOUR PRIVATE WORKSPACE</p><h1>Gmail connection</h1>
    <p className="page-description">Connect your Google account separately from your ApplySync sign-in.</p></div></div>
    <div className="auth-card gmail-card">
      <h2>Read-only access, deliberate setup</h2>
      <p>Google grants read-only access across your mailbox. ApplySync will limit future reading through its approved Gmail connector and verified label setup. Label and filter verification comes next; this task reads no messages.</p>
      <p>Only your Google account identity and encrypted offline authorization are stored. You can disconnect at any time.</p>
      {outcomes[params.get('result') ?? ''] && <p role="status">{outcomes[params.get('result') ?? '']}</p>}
      {query.isPending && <p role="status">Loading connection…</p>}
      {query.isError && <p role="alert">Connection status is unavailable. Retry status.</p>}
      {data && <>
        <h3>{labels[data.status]}</h3>
        {data.email && <p>{data.email}</p>}
        {!data.available && <p role="status">Gmail is unavailable until local Google Cloud configuration is complete. Application tracking still works.</p>}
        {data.revocation_warning && <p role="alert">Disconnected locally, but Google revocation could not be confirmed. Remove ApplySync access in <a href="https://myaccount.google.com/connections" target="_blank" rel="noreferrer">Google account connections</a>.</p>}
        <div className="gmail-actions">
          <Button variant="primary" disabled={!!pending || !data.available || query.isError} onClick={() => void act('start')}>{pending === 'start' ? 'Starting connection…' : data.status === 'connected' ? 'Reconnect Google account' : 'Connect Google account'}</Button>
          {['connected', 'reauthorization_needed'].includes(data.status) && <Button disabled={!!pending} onClick={() => void act('disconnect')}>{pending === 'disconnect' ? 'Disconnecting…' : 'Disconnect'}</Button>}
        </div>
      </>}
      {failure && <p role="alert">{failure}</p>}
      <Button disabled={!!pending || query.isFetching} onClick={() => void query.refetch()}>Refresh status</Button>
    </div>
  </section>
}
