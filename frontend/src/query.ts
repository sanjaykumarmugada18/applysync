import { QueryClient } from '@tanstack/react-query'

export function makeQueryClient() {
  return new QueryClient({ defaultOptions: {
    queries: { retry: false, staleTime: 0, refetchOnWindowFocus: false, networkMode: 'always' },
    mutations: { retry: false, networkMode: 'always' },
  } })
}
