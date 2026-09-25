import { useState } from 'react'
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { CalendarDays, Columns3, List, Plus, Search } from 'lucide-react'
import { ApiError, createApplication, errorMessage, getApplication, isUuid, listApplications } from './api'
import { type CreateValues, formatDate } from './data'
import { ApplicationList, CompanyMark, StoredBoard } from './components/ApplicationsView'
import { ApplicationForm } from './components/ApplicationForm'
import { Button, Modal } from './components/ui'

const pageSize = 20
export function StoredApplications() {
  const [params, setParams] = useSearchParams()
  const { id } = useParams()
  const navigate = useNavigate()
  const location = useLocation()
  const client = useQueryClient()
  const [saved, setSaved] = useState(false)
  const rawOffset = params.get('offset') ?? '0'
  const offset = Number(rawOffset)
  const validOffset = /^\d+$/.test(rawOffset) && Number.isSafeInteger(offset) && offset <= 10_000
  const search = params.get('q') ?? ''
  const view = params.get('view') === 'board' ? 'board' : 'list'
  const isNew = id === 'new'
  const validId = !!id && !isNew && isUuid(id)
  const list = useQuery({ queryKey: ['applications', 'list', pageSize, offset],
    queryFn: ({ signal }) => listApplications(pageSize, offset, signal), enabled: validOffset })
  const detail = useQuery({ queryKey: ['applications', 'detail', id],
    queryFn: ({ signal }) => getApplication(id!, signal), enabled: validId })
  const mutation = useMutation({ mutationFn: createApplication, retry: false })
  const close = () => { if (!mutation.isPending) navigate(`/applications${location.search}`, { replace: true }) }
  const rows = list.data?.items ?? []
  const query = search.trim().toLocaleLowerCase()
  const visible = rows.filter(row => `${row.company}\n${row.role}`.toLocaleLowerCase().includes(query))
  function selection(key: string, value: string) {
    setParams(current => { const next = new URLSearchParams(current); next.set(key, value); return next }, { replace: true })
  }
  async function add(values: CreateValues) {
    const record = await mutation.mutateAsync(values)
    client.setQueryData(['applications', 'detail', record.id], record)
    // Creation is already committed. A failed refresh is a read error, not a failed POST.
    await client.invalidateQueries({ queryKey: ['applications', 'list'] })
    setSaved(true)
    navigate(`/applications/${record.id}${location.search}`, { replace: true })
  }
  return <>
    <div className="page-heading"><div><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Applications</h1><p className="page-description">Your stored applications, one opportunity at a time.</p></div>
      <Link id="add-application" className="button button-primary" to={`/applications/new${location.search}`} onClick={() => setSaved(false)}><Plus size={18} />Add application</Link>
    </div>
    <div className="applications-workspace">
      <div className="toolbar"><div className="view-switch" role="group" aria-label="Application view"><button aria-pressed={view === 'board'} onClick={() => selection('view', 'board')}><Columns3 size={17} />Board</button><button aria-pressed={view === 'list'} onClick={() => selection('view', 'list')}><List size={18} />List</button></div><div className="filter-controls"><div className="search-field"><Search size={18} /><label className="sr-only" htmlFor="search">Search this loaded page</label><input id="search" type="search" placeholder="Search this loaded page…" value={search} onChange={event => selection('q', event.target.value)} /></div></div></div>
      <div className="results-meta"><p>{visible.length} shown · {rows.length} loaded on this page</p><span>Oldest first · No total count available</span></div>
      {view === 'board' && <p className="board-explanation">Applications will be grouped by stage when stage tracking is available.</p>}
      {!validOffset ? <div className="empty-state" role="alert"><h2>Invalid page offset</h2><p>Use a whole number from 0 to 10,000.</p><Button onClick={() => selection('offset', '0')}>First page</Button></div>
        : list.isPending ? <p role="status">Loading applications…</p>
        : list.isError ? <div className="empty-state" role="alert"><h2>Applications unavailable</h2><p>{errorMessage(list.error)}</p><Button onClick={() => void list.refetch()}>Retry list</Button></div>
        : visible.length ? view === 'board' ? <StoredBoard applications={visible} search={location.search} /> : <ApplicationList records={visible.map(application => ({ application }))} search={location.search} preview={false} />
        : <div className="empty-state"><h2>{rows.length ? 'No matches on this page' : offset ? 'No applications on this page' : 'No stored applications yet'}</h2><p>{search ? 'Search only covers this loaded page. Clear it or try another page.' : 'Add an application or use the page controls.'}</p>{search && <Button onClick={() => selection('q', '')}>Clear page search</Button>}</div>}
      {validOffset && <nav className="pagination" aria-label="Application pages">
        <Button disabled={offset === 0 || list.isFetching} onClick={() => selection('offset', String(Math.max(0, offset - pageSize)))}>Previous page</Button>
        <span>Offset {offset} · Up to {pageSize} records per page</span>
        <Button disabled={!list.data || list.isError || list.isFetching || rows.length < pageSize || offset + pageSize > 10_000} onClick={() => selection('offset', String(offset + pageSize))}>Next page</Button>
      </nav>}
      {offset + pageSize > 10_000 && <p className="page-description">The API's maximum offset is 10,000. Further pages are unavailable in this version.</p>}
      <footer className="workspace-footer"><span>Search covers this page only. A full page may be followed by an empty page.</span><Link to="/preview/applications">Explore sample Board/List preview</Link></footer>
    </div>
    {id && <Modal key={isNew ? 'new' : id} title={isNew ? 'Add application' : detail.data?.role ?? 'Application details'} subtitle={detail.data?.company} onClose={close} variant={isNew ? 'form' : 'panel'} busy={mutation.isPending} preview={false}>
      {isNew ? <ApplicationForm onAdd={add} onClose={close} mode="stored" /> : <div className="detail-body">
        {saved && <p className="success-note" role="status">Application saved to the database.</p>}
        {!validId ? <p role="alert">Invalid application ID. Use a complete UUID.</p>
          : detail.isPending ? <p role="status">Loading application…</p>
          : detail.isError ? <div role="alert"><p>{errorMessage(detail.error)}</p>{!(detail.error instanceof ApiError && detail.error.kind === 'missing') && <Button onClick={() => void detail.refetch()}>Retry details</Button>}</div>
          : detail.data && <>
            <div className="detail-identity"><CompanyMark company={detail.data.company} /><div><span className="eyebrow">COMPANY</span><strong>{detail.data.company}</strong></div></div>
            <h3>Application overview</h3><dl className="detail-facts"><div><dt><CalendarDays size={16} />Applied date</dt><dd>{formatDate(detail.data.applied_on)}</dd></div><div><dt>Record ID</dt><dd className="record-id">{detail.data.id}</dd></div></dl>
            <p className="detail-preview page-description">Stored in PostgreSQL. This record remains available after reload.</p>
          </>}
        <Button onClick={close}>Back to applications</Button>
      </div>}
    </Modal>}
  </>
}
