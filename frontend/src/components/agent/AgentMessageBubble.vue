<template>
  <div :class="['bubble', roleClass]">
    <div class="bubble-header">
      <span class="role-badge">{{ displayRole }}</span>
      <span class="type-badge">{{ message.message_type }}</span>
    </div>
    <div class="content" v-html="renderedContent" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'
import type { AgentMessage } from '@/api/generation'

const props = defineProps<{ message: AgentMessage }>()

const roleClass = computed(() => {
  if (props.message.role === 'supervisor') return 'supervisor'
  if (props.message.message_type === 'final') return 'final'
  return 'worker'
})

const displayRole = computed(() => {
  const r = props.message.role
  return r.charAt(0).toUpperCase() + r.slice(1).replace(/_/g, ' ')
})

const renderedContent = computed(() => marked.parse(props.message.content) as string)
</script>

<style scoped>
.bubble {
  border-radius: 8px; padding: 14px 16px; margin-bottom: 8px;
  border-left: 3px solid transparent;
}
.supervisor { background: #1a1a3a; border-left-color: #7c6af7; }
.worker { background: #1a2a1a; border-left-color: #4caf7d; }
.final { background: #1a2a3a; border-left-color: #5ba3f5; }
.bubble-header { display: flex; gap: 8px; margin-bottom: 8px; }
.role-badge { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #9d8fff; }
.supervisor .role-badge { color: #9d8fff; }
.worker .role-badge { color: #4caf7d; }
.final .role-badge { color: #5ba3f5; }
.type-badge { font-size: 11px; background: #2d2d4e; color: #888; padding: 1px 6px; border-radius: 10px; }
.content { color: #d0d0e8; font-size: 14px; line-height: 1.6; }
.content :deep(h1), .content :deep(h2), .content :deep(h3) { color: #e0e0ff; margin: 12px 0 6px; }
.content :deep(strong) { color: #e0e0ff; }
.content :deep(p) { margin: 6px 0; }
.content :deep(ul), .content :deep(ol) { margin: 6px 0; padding-left: 20px; }
.content :deep(table) { border-collapse: collapse; width: 100%; }
.content :deep(td), .content :deep(th) { border: 1px solid #3d3d5e; padding: 6px 10px; }
.content :deep(th) { background: #2d2d4e; color: #e0e0ff; }
</style>
