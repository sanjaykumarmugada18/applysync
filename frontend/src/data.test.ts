import { describe, expect, it } from 'vitest'
import { filterApplications, formatDate, sampleApplications, validateCreate } from './data'

describe('preview data boundaries', () => {
  it('combines company/role search and stage filtering', () => {
    expect(filterApplications(sampleApplications, '  PRODUCT ', 'Interview')).toHaveLength(1)
    expect(filterApplications(sampleApplications, 'cedar', 'Interview')).toHaveLength(0)
    expect(filterApplications(sampleApplications, 'cedar', 'All stages')).toHaveLength(1)
  })
  it('formats calendar dates without timezone shifts', () => {
    expect(formatDate('2026-09-01')).toBe('1 Sept 2026')
  })
  it('trims and allows future dates and duplicate values', () => {
    const values = { company: ' Cedar & Finch ', role: ' Engineer ', applied_on: '2100-01-01' }
    const result = validateCreate(values)
    expect(result.errors).toEqual({})
    expect(result.clean.company).toBe('Cedar & Finch')
    expect(result.clean.role).toBe('Engineer')
    expect(validateCreate(values)).toEqual(result)
  })
  it('rejects blank, oversized and impossible date values', () => {
    expect(validateCreate({ company: '   ', role: 'r'.repeat(201), applied_on: '2026-02-30' }).errors)
      .toEqual({ company: 'Enter a company.', role: 'Use 200 characters or fewer.', applied_on: 'Enter a valid date.' })
    for (const applied_on of ['', '2026-2-1', '0000-01-01', '2025-02-29']) {
      expect(validateCreate({ company: 'A', role: 'B', applied_on }).errors.applied_on).toBeTruthy()
    }
    expect(validateCreate({ company: 'x'.repeat(200), role: 'r'.repeat(200), applied_on: '2024-02-29' }).errors).toEqual({})
  })
})
