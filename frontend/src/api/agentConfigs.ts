import client from './client'

export type AgentMode = 'team' | 'single'

export interface AgentConfig {
  id: number
  chapter_id: number
  supervisor_prompt: string
  worker_prompt: string
  worker_roles: string[]
  worker_count: number
  max_rounds: number
  model: string
  internet_access: boolean
  aggregate_prompt: string | null
  pptx_aggregate_prompt: string | null
  mode: AgentMode
  single_agent_instructions: string | null
  created_at: string
  updated_at: string
}

export interface AgentConfigUpsert {
  supervisor_prompt: string
  worker_prompt: string
  worker_roles: string[]
  worker_count: number
  max_rounds: number
  model: string
  internet_access: boolean
  aggregate_prompt: string | null
  pptx_aggregate_prompt: string | null
  mode: AgentMode
  single_agent_instructions: string | null
}

export const agentConfigsApi = {
  get: (chapterId: number) => client.get<AgentConfig>(`/chapters/${chapterId}/agent-config`).then(r => r.data),
  upsert: (chapterId: number, data: AgentConfigUpsert) =>
    client.put<AgentConfig>(`/chapters/${chapterId}/agent-config`, data).then(r => r.data),
}
