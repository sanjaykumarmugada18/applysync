import { useState, type FormEvent } from 'react'
import { Info, Plus } from 'lucide-react'
import { validateCreate, type CreateValues } from '../data'
import { Button } from './ui'

export function ApplicationForm({ onAdd, onClose }: { onAdd: (values: CreateValues) => void; onClose: () => void }) {
  const [values, setValues] = useState<CreateValues>({ company: '', role: '', applied_on: '' })
  const [errors, setErrors] = useState<Partial<Record<keyof CreateValues, string>>>({})
  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const result = validateCreate(values)
    setErrors(result.errors)
    if (Object.keys(result.errors).length) {
      const first = Object.keys(result.errors)[0]
      event.currentTarget.querySelector<HTMLInputElement>(`[name="${first}"]`)?.focus()
      return
    }
    onAdd(result.clean)
  }
  return <form onSubmit={submit} noValidate className="application-form">
    <div className="info-note"><Info size={18} /><p>Added to this preview only. Your additions reset when you reload.</p></div>
    <div className="form-fields">
      {(['company', 'role', 'applied_on'] as const).map((field, i) => <div className="field" key={field}>
        <label htmlFor={field}>{['Company', 'Role', 'Applied date'][i]} <span aria-hidden="true">*</span></label>
        <input id={field} name={field} data-autofocus={field === 'company' ? '' : undefined} type={field === 'applied_on' ? 'date' : 'text'}
          placeholder={field === 'company' ? 'e.g. Cedar & Finch' : field === 'role' ? 'e.g. Product Designer' : undefined}
          required value={values[field]} aria-invalid={!!errors[field]} aria-describedby={errors[field] ? `${field}-error` : `${field}-hint`}
          onChange={event => setValues({ ...values, [field]: event.target.value })} />
        {errors[field] ? <p id={`${field}-error`} className="field-error" role="alert">{errors[field]}</p> :
          <p id={`${field}-hint`} className="field-hint">{field === 'applied_on' ? 'The date you applied. Future dates are also accepted.' : 'Up to 200 characters.'}</p>}
      </div>)}
    </div>
    <p className="form-stage-note">Starts in <strong>Applied</strong>, a provisional sample stage.</p>
    <div className="form-actions"><Button onClick={onClose} type="button">Cancel</Button><Button variant="primary" type="submit"><Plus size={17} />Add to preview</Button></div>
  </form>
}
