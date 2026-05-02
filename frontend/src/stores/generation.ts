import { defineStore } from 'pinia'
import { ref } from 'vue'
import { generationApi, type AgentMessage, type GenerationRun } from '@/api/generation'

export const useGenerationStore = defineStore('generation', () => {
  const activeRunId = ref<number | null>(null)
  const runStatus = ref<'idle' | 'pending' | 'running' | 'complete' | 'error'>('idle')
  const messages = ref<AgentMessage[]>([])
  const finalMarkdown = ref<string | null>(null)
  const streamingChunk = ref('')
  const errorMessage = ref<string | null>(null)

  function handleWsEvent(event: { type: string; data: Record<string, unknown> }) {
    switch (event.type) {
      case 'status_update':
        runStatus.value = event.data.status as typeof runStatus.value
        break
      case 'agent_message':
        messages.value.push({
          id: Date.now(),
          run_id: activeRunId.value!,
          sequence: event.data.sequence as number,
          role: event.data.role as string,
          content: event.data.content as string,
          message_type: event.data.message_type as string,
          created_at: new Date().toISOString(),
        })
        streamingChunk.value = ''
        break
      case 'streaming_chunk':
        streamingChunk.value += event.data.delta as string
        break
      case 'final_output':
        finalMarkdown.value = event.data.markdown as string
        runStatus.value = 'complete'
        streamingChunk.value = ''
        break
      case 'error':
        errorMessage.value = event.data.message as string
        runStatus.value = 'error'
        break
    }
  }

  async function stopGeneration() {
    if (!activeRunId.value) return
    await generationApi.stop(activeRunId.value)
    runStatus.value = 'idle'
  }

  async function startGeneration(chapterId: number) {
    reset()
    runStatus.value = 'pending'
    const { run_id } = await generationApi.trigger(chapterId)
    activeRunId.value = run_id
    runStatus.value = 'running'
    return run_id
  }

  async function loadRun(runId: number) {
    activeRunId.value = runId
    const run = await generationApi.getRun(runId)
    runStatus.value = run.status as typeof runStatus.value
    if (run.final_output) finalMarkdown.value = run.final_output
    const msgs = await generationApi.getMessages(runId)
    messages.value = msgs
  }

  function reset() {
    activeRunId.value = null
    runStatus.value = 'idle'
    messages.value = []
    finalMarkdown.value = null
    streamingChunk.value = ''
    errorMessage.value = null
  }

  return {
    activeRunId, runStatus, messages, finalMarkdown, streamingChunk, errorMessage,
    handleWsEvent, startGeneration, stopGeneration, loadRun, reset,
  }
})
