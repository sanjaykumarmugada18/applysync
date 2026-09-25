import { CalendarDays, ChevronRight, Inbox } from 'lucide-react'
import { Link } from 'react-router'
import { formatDate, initials, stages, type Application, type Stage, type PreviewApplication } from '../data'
import { StageLabel } from './ui'

export function CompanyMark({ company }: { company: string }) {
  const color = company.charCodeAt(0) % 5
  return <span aria-hidden="true" className={`company-mark company-color-${color}`}>{initials(company)}</span>
}
function ApplicationCard({ application, search, preview = true }: { application: Application; search: string; preview?: boolean }) {
  return <Link to={`${preview ? '/preview' : ''}/applications/${application.id}${search}`} className="application-card" aria-label={`${application.role} at ${application.company}`}>
    <div className="card-top"><CompanyMark company={application.company} /><ChevronRight size={17} className="card-arrow" /></div>
    <h3>{application.role}</h3><p className="card-company">{application.company}</p>
    <div className="card-footer"><CalendarDays size={15} /><span>Applied {formatDate(application.applied_on)}</span></div>
  </Link>
}
export function Board({ records, search }: { records: PreviewApplication[]; search: string }) {
  return <div className="board-scroll" role="region" aria-label="Application board, scroll horizontally for more stages" tabIndex={0}>
    <div className="board">
      {stages.map(stage => {
        const cards = records.filter(record => record.sampleStage === stage)
        return <section key={stage} className="board-column" aria-label={`${stage}, ${cards.length} applications`}>
          <div className={`column-heading stage-${stage.toLowerCase()}`}><h2>{stage}</h2><span className="column-count">{cards.length}</span></div>
          <div className="column-cards">{cards.map(record => <ApplicationCard key={record.application.id} application={record.application} search={search} />)}
            {!cards.length && <div className="column-empty"><Inbox size={22} /><p>No applications here</p><span>Room for what’s next.</span></div>}
          </div>
        </section>
      })}
    </div>
  </div>
}
export function StoredBoard({ applications, search }: { applications: Application[]; search: string }) {
  // A display fallback only: never assign a stage to an API record.
  return <section className="stored-board board-column" aria-label="Stored application board">
    <div className="column-heading neutral-heading"><h2>Stage not recorded</h2><span className="column-count" aria-label={`${applications.length} shown on this page`}>{applications.length}</span></div>
    <div className="column-cards">{applications.map(application => <ApplicationCard key={application.id} application={application} search={search} preview={false} />)}</div>
  </section>
}
export function ApplicationList({ records, search, preview = true }: { records: { application: Application; sampleStage?: Stage }[]; search: string; preview?: boolean }) {
  return <div className={`application-list ${preview ? "" : "stored-list"}`} role="region" aria-label="Application list">
    <div className="list-heading" aria-hidden="true"><span>Company</span><span>Role</span><span>Applied date</span>{preview && <span>Sample stage</span>}<span /></div>
    <ul>{records.map(({ application, sampleStage }) => <li key={application.id}>
      <Link className="list-row" to={`${preview ? "/preview" : ""}/applications/${application.id}${search}`} aria-label={`${application.role} at ${application.company}`}>
        <span className="list-company"><CompanyMark company={application.company} /><span>{application.company}</span></span>
        <span className="list-role">{application.role}</span>
        <span className="list-date"><span className="mobile-only">Applied </span>{formatDate(application.applied_on)}</span>
        {preview && sampleStage && <span className="list-stage"><StageLabel stage={sampleStage} /></span>}
        <ChevronRight size={17} className="list-arrow" />
      </Link>
    </li>)}</ul>
  </div>
}
