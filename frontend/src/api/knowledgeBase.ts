import client from './client'

export interface KBDocument {
  id: number
  report_id: number
  filename: string
  file_type: string
  status: string
  chunk_count: number
  error_msg: string | null
  created_at: string
}

export const knowledgeBaseApi = {
  list: (reportId: number) => client.get<KBDocument[]>(`/reports/${reportId}/kb`).then(r => r.data),
  upload: (reportId: number, file: File) => {
    const form = new FormData()
    form.append('file', file)
    return client.post<KBDocument>(`/reports/${reportId}/kb/upload`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }).then(r => r.data)
  },
  delete: (reportId: number, docId: number) => client.delete(`/reports/${reportId}/kb/${docId}`),
}
