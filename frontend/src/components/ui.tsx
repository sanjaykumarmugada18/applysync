import { useEffect, useId, useRef, type ButtonHTMLAttributes, type ReactNode } from 'react'
import { X } from 'lucide-react'
import type { Stage } from '../data'

export function Button({ variant = 'secondary', className = '', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'quiet' }) {
  return <button {...props} className={`button button-${variant} ${className}`} />
}
export function StageLabel({ stage }: { stage: Stage }) {
  return <span className={`stage-label stage-${stage.toLowerCase()}`}><span className="stage-dot" />{stage}</span>
}
export function PreviewNotice({ children = 'Design preview · Sample data' }: { children?: ReactNode }) {
  return <span className="preview-notice"><span className="preview-dot" />{children}</span>
}

export function Modal({ title, subtitle, children, onClose, variant = 'panel' }: {
  title: string; subtitle?: string; children: ReactNode; onClose: () => void; variant?: 'panel' | 'form' | 'navigation'
}) {
  const dialog = useRef<HTMLDialogElement>(null)
  const titleId = useId()
  useEffect(() => {
    const previous = document.activeElement as HTMLElement | null
    const element = dialog.current!
    element.showModal()
    element.querySelector<HTMLElement>('[data-autofocus]')?.focus()
    const overflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      element.close()
      document.body.style.overflow = overflow
      const target = previous?.isConnected && previous !== document.body ? previous : document.getElementById('add-application')
      target?.focus({ preventScroll: true })
    }
  }, [])
  return <dialog ref={dialog} className={`modal modal-${variant}`} aria-labelledby={titleId}
    onKeyDown={event => {
      if (event.key !== 'Tab') return
      const targets = Array.from(event.currentTarget.querySelectorAll<HTMLElement>('button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), [tabindex="0"]'))
        .filter(element => element.getClientRects().length > 0)
      const first = targets[0]
      const last = targets.at(-1)
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus() }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus() }
    }}
    onCancel={event => { event.preventDefault(); onClose() }}>
    <div className="modal-heading">
      <div><p className="eyebrow">APPLYSYNC PREVIEW</p><h2 id={titleId}>{title}</h2>{subtitle && <p className="text-muted mt-2">{subtitle}</p>}</div>
      <button className="icon-button shrink-0" aria-label="Close panel" onClick={onClose}><X size={20} /></button>
    </div>
    {children}
  </dialog>
}
