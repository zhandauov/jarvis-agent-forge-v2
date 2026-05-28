import client from './client'

export interface PromptTemplate {
  id: number
  key: string
  name: string
  description: string
  body: string
  updated_at: string
}

export const promptsApi = {
  list: () => client.get<PromptTemplate[]>('/prompts').then(r => r.data),
  get: (key: string) => client.get<PromptTemplate>(`/prompts/${key}`).then(r => r.data),
  update: (key: string, body: string) =>
    client.put<PromptTemplate>(`/prompts/${key}`, { body }).then(r => r.data),
  reset: (key: string) =>
    client.post<PromptTemplate>(`/prompts/${key}/reset`).then(r => r.data),
}
