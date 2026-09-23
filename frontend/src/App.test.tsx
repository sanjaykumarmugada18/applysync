import { fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router'
import { expect, it } from 'vitest'
import { App } from './App'

function setup(path = '/applications', empty = false) {
  const user = userEvent.setup()
  render(<MemoryRouter initialEntries={[path]}><App initialRecords={empty ? [] : undefined} /></MemoryRouter>)
  return user
}
it('shows stage counts and an empty Offer column', () => {
  setup()
  expect(screen.getByRole('region', { name: 'Applied, 4 applications' })).toBeInTheDocument()
  expect(screen.getByRole('region', { name: 'Offer, 0 applications' })).toHaveTextContent('No applications here')
})
it('retains combined filters across views and clears no-results', async () => {
  const user = setup()
  await user.type(screen.getByRole('searchbox'), 'cedar')
  await user.selectOptions(screen.getByLabelText('Sample stage'), 'Interview')
  expect(screen.getByText('No matching applications')).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'List' }))
  expect(screen.getByRole('searchbox')).toHaveValue('cedar')
  expect(screen.getByLabelText('Sample stage')).toHaveValue('Interview')
  await user.click(screen.getByRole('button', { name: 'Clear search & filter' }))
  expect(screen.getByRole('region', { name: 'Application list' })).toBeInTheDocument()
  expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true')
})
it('preserves input on validation errors and adds a trimmed preview record to both views', async () => {
  const user = setup()
  await user.click(screen.getByRole('link', { name: 'Add application' }))
  const dialog = screen.getByRole('dialog')
  await user.type(within(dialog).getByLabelText('Company', { exact: false }), '   ')
  await user.type(within(dialog).getByLabelText('Role', { exact: false }), ' Engineer ')
  fireEvent.change(within(dialog).getByLabelText('Applied date', { exact: false }), { target: { value: '2100-01-01' } })
  await user.click(screen.getByRole('button', { name: 'Add to preview' }))
  expect(screen.getByRole('alert')).toHaveTextContent('Enter a company.')
  expect(within(dialog).getByLabelText('Role', { exact: false })).toHaveValue(' Engineer ')
  await user.clear(within(dialog).getByLabelText('Company', { exact: false }))
  await user.type(within(dialog).getByLabelText('Company', { exact: false }), ' Preview Company ')
  await user.click(screen.getByRole('button', { name: 'Add to preview' }))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('status')).toHaveTextContent('Preview Company added to the preview')
  expect(screen.getByRole('link', { name: 'Engineer at Preview Company' })).toBeInTheDocument()
  await user.click(screen.getByRole('button', { name: 'List' }))
  expect(screen.getByRole('link', { name: 'Engineer at Preview Company' })).toBeInTheDocument()
})
it('opens route-backed detail and returns without losing search', async () => {
  const user = setup('/applications?q=cedar&view=list')
  await user.click(screen.getByRole('link', { name: 'Product Designer at Cedar & Finch' }))
  expect(screen.getByRole('dialog')).toHaveTextContent('Application overview')
  expect(screen.getByRole('dialog')).toHaveTextContent('21 Sept 2026')
  await user.click(screen.getByRole('button', { name: 'Back to applications' }))
  expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  expect(screen.getByRole('searchbox')).toHaveValue('cedar')
})
it('supports an empty dataset and direct missing-record routes', () => {
  setup('/applications/missing', true)
  expect(screen.getByText('Your next chapter starts here')).toBeInTheDocument()
  expect(screen.getByRole('dialog')).toHaveTextContent('Application not found')
})
