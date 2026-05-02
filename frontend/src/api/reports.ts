import client from './client'

export interface Report {
  id: number
  title: string
  description: string | null
  status: string
  created_at: string
  updated_at: string
}

export const reportsApi = {
  list: () => client.get<Report[]>('/reports').then(r => r.data),
  get: (id: number) => client.get<Report>(`/reports/${id}`).then(r => r.data),
  create: (data: { title: string; description?: string }) => client.post<Report>('/reports', data).then(r => r.data),
  update: (id: number, data: Partial<Report>) => client.put<Report>(`/reports/${id}`, data).then(r => r.data),
  delete: (id: number) => client.delete(`/reports/${id}`),
}
