// The eventual API shape has no stage. Preview-only values stay in a separate wrapper.
export interface Application {
  id: string
  company: string
  role: string
  applied_on: string
  created_at: string
}
export const stages = ['Applied', 'Assessment', 'Interview', 'Offer', 'Rejected'] as const
export type Stage = typeof stages[number]
export interface PreviewApplication { application: Application; sampleStage: Stage }
export type CreateValues = Pick<Application, 'company' | 'role' | 'applied_on'>

const samples: [string, string, string, Stage][] = [
  ['Cedar & Finch', 'Product Designer', '2026-09-21', 'Applied'],
  ['Orbitwell', 'Frontend Engineer', '2026-09-20', 'Applied'],
  ['Northstar Sustainable Infrastructure Collective', 'Senior User Experience Researcher, Digital Products', '2026-09-18', 'Applied'],
  ['Morrow Studio', 'Design Systems Designer', '2026-09-17', 'Applied'],
  ['Fernpath', 'UX Researcher', '2026-09-16', 'Assessment'],
  ['Lumenfield', 'Software Engineer', '2026-09-14', 'Assessment'],
  ['Kindred Works', 'Product Designer', '2026-09-12', 'Interview'],
  ['Aster & Co.', 'Interaction Designer', '2026-09-10', 'Interview'],
  ['Pebblewave', 'Frontend Developer', '2026-09-04', 'Rejected'],
]
export const sampleApplications: PreviewApplication[] = samples.map(([company, role, applied_on, sampleStage], i) => ({
  application: { id: `00000000-0000-4000-8000-${String(i + 1).padStart(12, '0')}`, company, role, applied_on, created_at: `${applied_on}T12:00:00Z` },
  sampleStage,
}))

export function filterApplications(records: PreviewApplication[], search: string, stage: string) {
  const query = search.trim().toLocaleLowerCase()
  return records.filter(({ application, sampleStage }) =>
    (stage === 'All stages' || sampleStage === stage) &&
    `${application.company}\n${application.role}`.toLocaleLowerCase().includes(query))
}

export function formatDate(value: string) {
  // Date-only values must retain the calendar day in every timezone.
  return new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' })
    .format(new Date(`${value}T12:00:00Z`))
}
export function initials(company: string) {
  return company.split(/\s+/).filter(word => /^[a-z]/i.test(word)).slice(0, 2).map(word => word[0]).join('').toUpperCase()
}
export function validateCreate(values: CreateValues) {
  const clean = { ...values, company: values.company.trim(), role: values.role.trim() }
  const errors: Partial<Record<keyof CreateValues, string>> = {}
  for (const key of ['company', 'role'] as const) {
    if (!clean[key]) errors[key] = `Enter a ${key}.`
    else if ([...clean[key]].length > 200) errors[key] = 'Use 200 characters or fewer.'
  }
  const date = new Date(`${values.applied_on}T12:00:00Z`)
  if (!/^\d{4}-\d{2}-\d{2}$/.test(values.applied_on) || values.applied_on.startsWith('0000') ||
      Number.isNaN(date.getTime()) || date.toISOString().slice(0, 10) !== values.applied_on) {
    errors.applied_on = 'Enter a valid date.'
  }
  return { clean, errors }
}
