<template>
  <div class="conversation">
    <div v-if="!messages.length && !streamingChunk" class="empty">
      <p>No messages yet. Configure the agent team and click Generate.</p>
    </div>
    <AgentMessageBubble v-for="msg in messages" :key="msg.id" :message="msg" />
    <div v-if="streamingChunk" class="streaming-bubble">
      <div class="bubble-header">
        <span class="role-badge">Supervisor</span>
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

const props = defineProps<{ messages: AgentMessage[]; streamingChunk: string }>()
const bottomRef = ref<HTMLElement | null>(null)

const renderedChunk = computed(() => marked.parse(props.streamingChunk) as string)

watch([() => props.messages.length, () => props.streamingChunk], async () => {
  await nextTick()
  bottomRef.value?.scrollIntoView({ behavior: 'smooth' })
})
</script>

<style scoped>
.conversation { display: flex; flex-direction: column; height: 100%; overflow-y: auto; padding: 16px; gap: 4px; }
.empty { flex: 1; display: flex; align-items: center; justify-content: center; color: #555; text-align: center; }
.streaming-bubble {
  background: #1a2a3a; border-left: 3px solid #5ba3f5;
  border-radius: 8px; padding: 14px 16px; margin-bottom: 8px;
  animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.8; } }
.bubble-header { display: flex; gap: 8px; margin-bottom: 8px; }
.role-badge { font-size: 11px; font-weight: 700; text-transform: uppercase; color: #5ba3f5; }
.type-badge { font-size: 11px; background: #2d2d4e; color: #888; padding: 1px 6px; border-radius: 10px; }
.streaming-content { color: #d0d0e8; font-size: 14px; line-height: 1.6; }
.streaming-content :deep(p) { margin: 6px 0; }
</style>
