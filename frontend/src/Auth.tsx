import { createContext, useContext, useEffect, useRef, useState, type FormEvent, type ReactNode } from 'react'
import { Link, Navigate, useLocation, useNavigate, useSearchParams } from 'react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { ApiError, errorMessage, request } from './api'
import { makeQueryClient } from './query'
import { Button } from './components/ui'

type Identity = { id: string; email: string }
type AuthState = { user: Identity | null; checking: boolean; failure: string }
type AuthContextValue = AuthState & { signIn: (email: string, password: string, register: boolean) => Promise<void>; logout: () => Promise<void>; restore: () => void }
const AuthContext = createContext<AuthContextValue | null>(null)
export const useAuth = () => useContext(AuthContext)

function identity(value: unknown): Identity {
  const user = value as Identity
  if (!user || typeof user.id !== 'string' || typeof user.email !== 'string') throw new ApiError('response')
  return { id: user.id, email: user.email }
}

// A newly mounted cache for each identity. Old requests can only reference their
// old cache, which is cancelled/cleared on unmount, never another account's cache.
export function PrivateCache({ children }: { children: ReactNode }) {
  const [client] = useState(makeQueryClient)
  useEffect(() => () => { void client.cancelQueries(); client.clear() }, [client])
  return <QueryClientProvider client={client}>{children}</QueryClientProvider>
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({ user: null, checking: true, failure: '' })
  const active = useRef<AbortController | null>(null)
  const changingSession = useRef(false)
  function begin() { active.current?.abort(); const controller = new AbortController(); active.current = controller; return controller }
  async function restore(background = false) {
    if (background && changingSession.current) return
    const controller = begin()
    if (!background) setState(previous => ({ ...previous, checking: true, failure: '' }))
    try {
      const user = identity(await request('/auth/me', undefined, controller.signal))
      if (!controller.signal.aborted) setState({ user, checking: false, failure: '' })
    } catch (error) {
      if (!controller.signal.aborted) setState(previous => ({ user: error instanceof ApiError && error.kind === 'unauthorized' ? null : previous.user,
        checking: false, failure: error instanceof ApiError && error.kind === 'unauthorized' ? '' : errorMessage(error) }))
    }
  }
  useEffect(() => {
    void restore()
    const expired = () => { active.current?.abort(); setState({ user: null, checking: false, failure: '' }) }
    const focus = () => { void restore(true) }
    const timer = window.setInterval(() => { void restore(true) }, 60_000)
    window.addEventListener('applysync:expired', expired)
    window.addEventListener('focus', focus)
    return () => { window.clearInterval(timer); active.current?.abort(); window.removeEventListener('applysync:expired', expired); window.removeEventListener('focus', focus) }
  }, [])
  async function signIn(email: string, password: string, register: boolean) {
    const controller = begin()
    changingSession.current = true
    try {
      const user = identity(await request(register ? '/auth/register' : '/auth/login', { email, password }, controller.signal))
      if (!controller.signal.aborted) setState({ user, checking: false, failure: '' })
    } finally { changingSession.current = false }
  }
  async function logout() {
    const controller = begin()
    changingSession.current = true
    // Hide/unmount all private content immediately, including pending mutations.
    setState(previous => ({ ...previous, checking: true, failure: '' }))
    try {
      await request('/auth/logout', {}, controller.signal)
      if (!controller.signal.aborted) setState({ user: null, checking: false, failure: '' })
    } catch (error) {
      if (!controller.signal.aborted) setState(previous => ({ ...previous, checking: false,
        user: error instanceof ApiError && error.kind === 'unauthorized' ? null : previous.user,
        failure: error instanceof ApiError && error.kind === 'unauthorized' ? '' : 'Logout could not be confirmed. Retry the session check, then log out again.' }))
    } finally { changingSession.current = false }
  }
  return <AuthContext.Provider value={{ ...state, signIn, logout, restore: () => void restore() }}>{children}</AuthContext.Provider>
}

export function SessionGate({ children }: { children: ReactNode }) {
  const auth = useAuth()!
  if (auth.checking) return <p role="status">Checking your session…</p>
  if (auth.failure) return <div className="empty-state" role="alert"><h2>Session unavailable</h2><p>{auth.failure}</p><Button onClick={auth.restore}>Retry session</Button></div>
  return children
}

export function ProtectedApplications({ children }: { children: ReactNode }) {
  const auth = useAuth()!
  const location = useLocation()
  return <SessionGate>{auth.user ? <PrivateCache key={auth.user.id}>{children}</PrivateCache>
    : <Navigate to={`/login?returnTo=${encodeURIComponent(location.pathname + location.search)}`} replace />}</SessionGate>
}

export function internalDestination(value: string | null) {
  if (value === '/settings/gmail') return value
  if (!value || !/^\/applications(?:\/(?:new|[0-9a-fA-F-]{36}))?(?:\?[^#]*)?$/.test(value) || value.includes('\\')) return '/applications'
  return value
}

export function AuthForm({ register = false }: { register?: boolean }) {
  const auth = useAuth()!
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [pending, setPending] = useState(false)
  const lock = useRef(false)
  const [failure, setFailure] = useState('')
  const destination = internalDestination(params.get('returnTo'))
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (lock.current) return
    lock.current = true; setPending(true); setFailure('')
    try { await auth.signIn(email, password, register); setPassword(''); navigate(destination, { replace: true }) }
    catch (error) { setFailure(error instanceof ApiError && error.kind === 'unauthorized' ? 'Invalid email or password.'
      : error instanceof ApiError && error.kind === 'validation' ? 'Use a valid email and a password of 12–128 characters.' : errorMessage(error)) }
    finally { lock.current = false; setPending(false) }
  }
  return <SessionGate>{auth.user ? <Navigate to={destination} replace /> : <div className="auth-card applications-workspace">
    <p className="eyebrow">YOUR PRIVATE WORKSPACE</p><h1>{register ? 'Create your account' : 'Welcome back'}</h1>
    <p className="page-description">{register ? 'Keep your applications together, and private to you.' : 'Sign in to your stored applications. If your session ended, submit any unfinished creation again after signing in.'}</p>
    <form onSubmit={submit} className="application-form">
      {failure && <p role="alert" className="field-error">{failure}</p>}
      <div className="field"><label htmlFor="email">Email</label><input id="email" type="email" autoComplete="username" required maxLength={254} value={email} readOnly={pending} onChange={e => setEmail(e.target.value)} /></div>
      <div className="field"><label htmlFor="password">Password</label><input id="password" type="password" autoComplete={register ? 'new-password' : 'current-password'} required minLength={12} maxLength={128} aria-describedby="password-hint" value={password} readOnly={pending} onChange={e => setPassword(e.target.value)} /><p id="password-hint" className="field-hint">12–128 characters. Spaces are preserved.</p></div>
      <Button type="submit" variant="primary" disabled={pending}>{pending ? 'Please wait…' : register ? 'Create account' : 'Sign in'}</Button>
    </form>
    <p><Link to={`${register ? '/login' : '/register'}?returnTo=${encodeURIComponent(destination)}`}>{register ? 'Already registered? Sign in' : 'New here? Create an account'}</Link></p>
    <Link to="/preview/applications">Explore the labelled sample preview</Link>
  </div>}</SessionGate>
}
