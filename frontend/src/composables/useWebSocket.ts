import { onUnmounted, watch, type Ref } from 'vue'
import { useGenerationStore } from '@/stores/generation'

export function useWebSocket(runId: Ref<number | null>) {
  const generationStore = useGenerationStore()
  let ws: WebSocket | null = null
  let retries = 0
  const MAX_RETRIES = 3

  function connect() {
    if (!runId.value) return
    const proto = location.protocol === 'https:' ? 'wss' : 'ws'
    const token = localStorage.getItem('auth_token') ?? ''
    ws = new WebSocket(`${proto}://${location.host}/ws/runs/${runId.value}?token=${token}`)

    ws.onmessage = (e) => {
      try {
        const event = JSON.parse(e.data)
        generationStore.handleWsEvent(event)
      } catch {}
    }

    ws.onclose = () => {
      if (retries < MAX_RETRIES && generationStore.runStatus === 'running') {
        setTimeout(connect, 1000 * Math.pow(2, retries++))
      }
    }

    ws.onerror = () => ws?.close()
  }

  function disconnect() {
    ws?.close()
    ws = null
  }

  watch(runId, (id) => {
    disconnect()
    if (id) {
      retries = 0
      connect()
    }
  }, { immediate: true })

  onUnmounted(disconnect)

  return { connect, disconnect }
}
