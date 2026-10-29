import { Navigate, Route, Routes } from 'react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'
import { GmailSettings } from './GmailSettings'
import { Shell } from './components/Shell'
import { PreviewApplications } from './PreviewApplications'
import { StoredApplications } from './StoredApplications'
import { makeQueryClient } from './query'
import type { PreviewApplication } from './data'
import { AuthForm, AuthProvider, ProtectedApplications } from './Auth'

export function App({ initialRecords }: { initialRecords?: PreviewApplication[] }) {
  const [client] = useState(makeQueryClient)
  return <Routes>
    <Route path="/preview/applications/:id?" element={<QueryClientProvider client={client}><Shell><PreviewApplications initialRecords={initialRecords} /></Shell></QueryClientProvider>} />
    <Route path="*" element={<AuthProvider><Shell><Routes>
      <Route path="/login" element={<AuthForm />} />
      <Route path="/register" element={<AuthForm register />} />
      <Route path="/settings/gmail" element={<ProtectedApplications><GmailSettings /></ProtectedApplications>} />
      <Route path="/applications/:id?" element={<ProtectedApplications><StoredApplications /></ProtectedApplications>} />
      <Route path="*" element={<Navigate to="/applications" replace />} />
    </Routes></Shell></AuthProvider>} />
  </Routes>
}
