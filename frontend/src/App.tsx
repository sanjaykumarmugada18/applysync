import { Navigate, Route, Routes } from 'react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import { Shell } from './components/Shell'
import { PreviewApplications } from './PreviewApplications'
import { StoredApplications } from './StoredApplications'
import { makeQueryClient } from './query'
import type { PreviewApplication } from './data'

export function App({ initialRecords }: { initialRecords?: PreviewApplication[] }) {
  const [client] = useState(makeQueryClient)
  return <QueryClientProvider client={client}><Shell><Routes>
    <Route path="/applications/:id?" element={<StoredApplications />} />
    <Route path="/preview/applications/:id?" element={<PreviewApplications initialRecords={initialRecords} />} />
    <Route path="*" element={<Navigate to="/applications" replace />} />
  </Routes></Shell></QueryClientProvider>
}
