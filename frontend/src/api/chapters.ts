import client from './client'

export interface Chapter {
  id: number
  report_id: number
  title: string
  description: string | null
  order_index: number
  status: string
  final_output: string | null
  created_at: string
  updated_at: string
}

export const chaptersApi = {
  list: (reportId: number) => client.get<Chapter[]>(`/reports/${reportId}/chapters`).then(r => r.data),
  get: (reportId: number, chapterId: number) => client.get<Chapter>(`/reports/${reportId}/chapters/${chapterId}`).then(r => r.data),
  create: (reportId: number, data: { title: string; description?: string; order_index?: number }) =>
    client.post<Chapter>(`/reports/${reportId}/chapters`, data).then(r => r.data),
  update: (reportId: number, chapterId: number, data: Partial<Chapter>) =>
    client.put<Chapter>(`/reports/${reportId}/chapters/${chapterId}`, data).then(r => r.data),
  delete: (reportId: number, chapterId: number) => client.delete(`/reports/${reportId}/chapters/${chapterId}`),
  reorder: (reportId: number, orderedIds: number[]) =>
    client.patch<Chapter[]>(`/reports/${reportId}/chapters/reorder`, { ordered_ids: orderedIds }).then(r => r.data),
}
