import { useRef, useState, type FormEvent } from 'react'
import { ApiError, errorMessage } from '../api'
import { Info, Plus } from 'lucide-react'
import { validateCreate, type CreateValues } from '../data'
import { Button } from './ui'

export function ApplicationForm({ onAdd, onClose, mode = 'preview' }: { onAdd: (values: CreateValues) => void | Promise<void>; onClose: () => void; mode?: 'preview' | 'stored' }) {
  const [values, setValues] = useState<CreateValues>({ company: '', role: '', applied_on: '' })
  const [errors, setErrors] = useState<Partial<Record<keyof CreateValues, string>>>({})
  const lock = useRef(false)
  const [pending, setPending] = useState(false)
  const [failure, setFailure] = useState('')
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (lock.current) return
    const form = event.currentTarget
    const result = validateCreate(values)
    setErrors(result.errors)
    if (Object.keys(result.errors).length) {
      const first = Object.keys(result.errors)[0]
      event.currentTarget.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
      return
    }
    lock.current = true
    setPending(true)
    setFailure('')
    try { await onAdd(result.clean) }
    catch (error) {
      if (error instanceof ApiError) {
        setErrors(error.fields)
        const first = Object.keys(error.fields)[0]
        if (first) form.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
      }
      setFailure(errorMessage(error, true))
    } finally { lock.current = false; setPending(false) }
  }
  return <form onSubmit={submit} noValidate className="application-form">
    <div className="info-note"><Info size={18} /><p>{mode === 'preview' ? 'Added to this preview only. Your additions reset when you reload.' : 'Save to the local database. Keep this form open while saving.'}</p></div>
    {failure && <p className="field-error" role="alert">{failure}</p>}
    <div className="form-fields">
      {(['company', 'role', 'applied_on'] as const).map((field, i) => <div className="field" key={field}>
        <label htmlFor={field}>{['Company', 'Role', 'Applied date'][i]} <span aria-hidden="true">*</span></label>
        <input id={field} name={field} data-autofocus={field === 'company' ? '' : undefined} type={field === 'applied_on' ? 'date' : 'text'}
          placeholder={field === 'company' ? 'e.g. Cedar & Finch' : field === 'role' ? 'e.g. Product Designer' : undefined}
          readOnly={pending} required value={values[field]} aria-invalid={!!errors[field]} aria-describedby={errors[field] ? `${field}-error` : `${field}-hint`}
          onChange={event => setValues({ ...values, [field]: event.target.value })} />
        {errors[field] ? <p id={`${field}-error`} className="field-error" role="alert">{errors[field]}</p> :
          <p id={`${field}-hint`} className="field-hint">{field === 'applied_on' ? 'The date you applied. Future dates are also accepted.' : 'Up to 200 characters.'}</p>}
      </div>)}
    </div>
    {mode === 'preview' && <p className="form-stage-note">Starts in <strong>Applied</strong>, a provisional sample stage.</p>}
    <div className="form-actions"><Button disabled={pending} onClick={onClose} type="button">Cancel</Button><Button disabled={pending} variant="primary" type="submit"><Plus size={17} />{pending ? 'Saving…' : mode === 'preview' ? 'Add to preview' : 'Save application'}</Button></div>
  </form>
}
