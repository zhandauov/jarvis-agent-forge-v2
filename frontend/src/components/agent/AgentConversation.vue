<template>
  <div class="conversation">
    <div v-if="!messages.length && !streamingChunk && !hasAgentStreaming" class="empty-state">
      <div class="empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </div>
      <p class="empty-text">No messages yet</p>
      <span class="empty-hint">Configure the agent team and click Generate to start.</span>
    </div>
    
    <AgentMessageBubble v-for="msg in messages" :key="msg.id" :message="msg" />
    
    <div v-for="(text, role) in agentStreaming" :key="role" class="streaming-bubble worker-streaming">
      <div class="bubble-header">
        <span class="role-badge badge-worker">{{ formatRole(role) }}</span>
        <span class="type-badge">thinking...</span>
      </div>
      <div class="streaming-content" v-html="renderMarkdown(text)" />
    </div>
    
    <div v-if="streamingChunk" class="streaming-bubble supervisor-streaming">
      <div class="bubble-header">
        <span class="role-badge badge-supervisor">Supervisor</span>
        <span class="type-badge">writing...</span>
      </div>
      <div class="streaming-content" v-html="renderedChunk" />
    </div>
    
    <div ref="bottomRef" />
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { marked } from 'marked'
import type { AgentMessage } from '@/api/generation'
import AgentMessageBubble from './AgentMessageBubble.vue'

const props = defineProps<{
  messages: AgentMessage[]
  streamingChunk: string
  agentStreaming: Record<string, string>
}>()

const bottomRef = ref<HTMLElement | null>(null)

const hasAgentStreaming = computed(() => Object.keys(props.agentStreaming).length > 0)
const renderedChunk = computed(() => marked.parse(props.streamingChunk) as string)

function formatRole(role: string) {
  return role.charAt(0).toUpperCase() + role.slice(1).replace(/_/g, ' ')
}

function renderMarkdown(text: string) {
  return marked.parse(text) as string
}

watch([() => props.messages.length, () => props.streamingChunk, () => props.agentStreaming], async () => {
  await nextTick()
  bottomRef.value?.scrollIntoView({ behavior: 'smooth' })
}, { deep: true })
</script>

<style scoped>
.conversation { 
  display: flex; 
  flex-direction: column; 
  height: 100%; 
  overflow-y: auto; 
  padding: var(--sp-4);
  gap: var(--sp-3);
}

.empty-state { 
  flex: 1; 
  display: flex;
  flex-direction: column;
  align-items: center; 
  justify-content: center;
  gap: var(--sp-3);
  text-align: center;
  padding: var(--sp-8);
}

.empty-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-lg);
  color: var(--text-4);
}

.empty-text {
  color: var(--text-2);
  font-size: var(--text-base);
  font-weight: 500;
  margin: 0;
}

.empty-hint {
  color: var(--text-4);
  font-size: var(--text-sm);
  max-width: 220px;
}

.streaming-bubble {
  background: var(--bg-elevated);
  border-radius: var(--r-lg);
  padding: var(--sp-4);
  border-left: 3px solid var(--brand);
  animation: pulse 2s ease-in-out infinite;
}

.streaming-bubble.worker-streaming { 
  border-left-color: var(--success);
}

.streaming-bubble.supervisor-streaming {
  border-left-color: var(--brand);
}

@keyframes pulse { 
  0%, 100% { opacity: 1; } 
  50% { opacity: 0.85; } 
}

.bubble-header { 
  display: flex; 
  align-items: center;
  gap: var(--sp-2);
  margin-bottom: var(--sp-3);
}

.role-badge { 
  font-size: var(--text-xs);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.badge-supervisor { 
  color: var(--brand-text);
}

.badge-worker { 
  color: var(--success);
}

.type-badge { 
  font-size: var(--text-xs);
  background: var(--bg-overlay);
  color: var(--text-3);
  padding: 2px var(--sp-2);
  border-radius: var(--r-full);
}

.streaming-content { 
  color: var(--text-2);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

.streaming-content :deep(p) { 
  margin: var(--sp-2) 0;
}

.streaming-content :deep(p:first-child) {
  margin-top: 0;
}

.streaming-content :deep(p:last-child) {
  margin-bottom: 0;
}
</style>
