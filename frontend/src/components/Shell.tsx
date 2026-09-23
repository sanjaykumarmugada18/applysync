import { useState, type ReactNode } from 'react'
import { Link } from 'react-router'
import { ArrowUpRight, Layers3, Menu, ShieldCheck } from 'lucide-react'
import { Modal, PreviewNotice } from './ui'

function Sidebar({ onNavigate }: { onNavigate?: () => void }) {
  return <div className="sidebar-inner">
    <Link className="brand" to="/applications" onClick={onNavigate}><img src="/mark.svg" alt="" width="32" height="32" /><span>ApplySync<span className="brand-dot">.</span></span></Link>
    <div className="sidebar-body">
      <p className="eyebrow">YOUR WORKSPACE</p>
      <nav aria-label="Main navigation"><Link className="nav-link" aria-current="page" to="/applications" onClick={onNavigate}><Layers3 size={19} /> Applications <ArrowUpRight size={16} className="ml-auto" /></Link></nav>
      <div className="sidebar-note"><span className="tiny-tag">BUILD 2 · PREVIEW</span><h2>A little more clarity.</h2><p>One place to see your next opportunity taking shape.</p></div>
    </div>
    <div className="sidebar-footer"><ShieldCheck size={20} /><div><strong>Private by design</strong><p>Fictional data. All local.</p></div></div>
  </div>
}
export function Shell({ children }: { children: ReactNode }) {
  const [navigationOpen, setNavigationOpen] = useState(false)
  return <div className="app-shell">
    <a className="skip-link" href="#main-content">Skip to applications</a>
    <aside className="desktop-sidebar"><Sidebar /></aside>
    <div className="workspace">
      <header className="topbar">
        <button className="icon-button mobile-menu" aria-label="Open navigation" onClick={() => setNavigationOpen(true)}><Menu size={21} /></button>
        <div className="breadcrumb"><span>Workspace</span><span aria-hidden="true">/</span><strong>Applications</strong></div>
        <PreviewNotice />
      </header>
      <main id="main-content" tabIndex={-1}>{children}</main>
    </div>
    {navigationOpen && <Modal title="Your workspace" variant="navigation" onClose={() => setNavigationOpen(false)}><Sidebar onNavigate={() => setNavigationOpen(false)} /></Modal>}
  </div>
}
