import client from './client'

export interface GenerationRun {
  id: number
  chapter_id: number
  status: string
  final_output: string | null
  error_msg: string | null
  started_at: string | null
  completed_at: string | null
  created_at: string
}

export interface AgentMessage {
  id: number
  run_id: number
  sequence: number
  role: string
  content: string
  message_type: string
  created_at: string
}

export const generationApi = {
  trigger: (chapterId: number) =>
    client.post<{ run_id: number }>(`/chapters/${chapterId}/generate`).then(r => r.data),
  stop: (runId: number) => client.post(`/runs/${runId}/stop`).then(r => r.data),
  listRuns: (chapterId: number) =>
    client.get<GenerationRun[]>(`/chapters/${chapterId}/runs`).then(r => r.data),
  getRun: (runId: number) => client.get<GenerationRun>(`/runs/${runId}`).then(r => r.data),
  getMessages: (runId: number) => client.get<AgentMessage[]>(`/runs/${runId}/messages`).then(r => r.data),
}
