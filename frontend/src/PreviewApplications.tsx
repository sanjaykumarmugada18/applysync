import { useState } from 'react'
import { Link, useLocation, useNavigate, useParams, useSearchParams } from 'react-router'
import { ArrowLeft, CalendarDays, Columns3, List, Plus, Search, SearchX, SlidersHorizontal } from 'lucide-react'
import { Board, ApplicationList, CompanyMark } from './components/ApplicationsView'
import { Button, Modal, PreviewNotice, StageLabel } from './components/ui'
import { ApplicationForm } from './components/ApplicationForm'
import { filterApplications, formatDate, sampleApplications, stages, type CreateValues, type PreviewApplication } from './data'

export function PreviewApplications({ initialRecords = sampleApplications }: { initialRecords?: PreviewApplication[] }) {
  const [records, setRecords] = useState(initialRecords)
  const [feedback, setFeedback] = useState('')
  const [params, setParams] = useSearchParams()
  const location = useLocation()
  const navigate = useNavigate()
  const { id } = useParams()
  const search = params.get('q') ?? ''
  const selectedStage = stages.find(stage => stage === params.get('stage')) ?? 'All stages'
  const view = params.get('view') === 'list' ? 'list' : 'board'
  const filtered = filterApplications(records, search, selectedStage)
  const selected = records.find(record => record.application.id === id)
  const isNew = id === 'new'
  const close = () => navigate(`/preview/applications${location.search}`, { replace: true })
  function setSelection(key: string, value: string) {
    setParams(current => {
      const next = new URLSearchParams(current)
      value ? next.set(key, value) : next.delete(key)
      return next
    }, { replace: true })
  }
  function add(values: CreateValues) {
    setRecords(current => [{ application: { ...values, id: crypto.randomUUID(), created_at: new Date().toISOString() }, sampleStage: 'Applied' }, ...current])
    setFeedback(`${values.company} added to the preview. Reloading removes this addition.`)
    close()
  }
  return <>
    <div className="page-heading"><div><p className="eyebrow">YOUR NEXT CHAPTER</p><h1>Applications</h1><p className="page-description">A clear view of every opportunity, from first step to next move.</p></div>
      <Link id="add-application" className="button button-primary" to={`/preview/applications/new${location.search}`}><Plus size={18} />Add application</Link>
    </div>
    <div className="applications-workspace">
      <div className="toolbar">
        <div className="view-switch" role="group" aria-label="Application view"><button aria-pressed={view === 'board'} onClick={() => setSelection('view', '')}><Columns3 size={17} />Board</button><button aria-pressed={view === 'list'} onClick={() => setSelection('view', 'list')}><List size={18} />List</button></div>
        <div className="filter-controls"><div className="search-field"><Search size={18} /><label className="sr-only" htmlFor="search">Search company or role</label><input id="search" type="search" placeholder="Search company or role…" value={search} onChange={event => setSelection('q', event.target.value)} /></div>
          <div className="stage-filter"><SlidersHorizontal size={16} /><label className="sr-only" htmlFor="stage-filter">Sample stage</label><select id="stage-filter" value={selectedStage} onChange={event => setSelection('stage', event.target.value === 'All stages' ? '' : event.target.value)}><option>All stages</option>{stages.map(stage => <option key={stage}>{stage}</option>)}</select></div>
        </div>
      </div>
      <div className="results-meta"><p aria-live="polite"><strong>{filtered.length}</strong> of {records.length} applications</p><span>Stages are for this preview only</span></div>
      {feedback && <div className="success-note" role="status"><span>{feedback}{(search || selectedStage !== 'All stages') && ' Your current filters may hide it.'}</span><Button variant="quiet" onClick={() => setFeedback('')}>Dismiss</Button></div>}
      {!filtered.length ? <div className="empty-state"><SearchX size={28} /><h2>{records.length ? 'No matching applications' : 'Your next chapter starts here'}</h2><p>{records.length ? 'Try a different company, role, or sample stage.' : 'Add an application to explore your preview.'}</p>
        {records.length ? <Button onClick={() => setParams(view === 'list' ? { view: 'list' } : {}, { replace: true })}>Clear search & filter</Button> : <Link className="button button-primary" to={`/preview/applications/new${location.search}`}>Add application</Link>}
      </div> : view === 'board' ? <Board records={filtered} search={location.search} /> : <ApplicationList records={filtered} search={location.search} />}
      <footer className="workspace-footer"><Link to="/applications">Return to stored applications</Link><span>Preview additions reset on reload.</span></footer>
    </div>
    {id && <Modal title={isNew ? 'Add application' : selected?.application.role ?? 'Application not found'} subtitle={isNew ? 'Make room for your next opportunity.' : selected?.application.company} variant={isNew ? 'form' : 'panel'} onClose={close}>
      {isNew ? <ApplicationForm onAdd={add} onClose={close} /> : selected ? <div className="detail-body">
        <div className="detail-identity"><CompanyMark company={selected.application.company} /><div><span className="eyebrow">COMPANY</span><strong>{selected.application.company}</strong></div></div>
        <h3>Application overview</h3><dl className="detail-facts"><div><dt><CalendarDays size={16} />Applied date</dt><dd>{formatDate(selected.application.applied_on)}</dd></div><div><dt>Sample stage</dt><dd><StageLabel stage={selected.sampleStage} /></dd></div></dl>
        <div className="detail-preview"><PreviewNotice /><p>This is a fictional application. Stages help you explore the layout; they are not saved application history.</p></div>
        <Button onClick={close}><ArrowLeft size={17} />Back to applications</Button>
      </div> : <div className="detail-body"><p>This preview record is unavailable. Preview additions disappear on reload.</p><Button onClick={close}>Back to applications</Button></div>}
    </Modal>}
  </>
}
