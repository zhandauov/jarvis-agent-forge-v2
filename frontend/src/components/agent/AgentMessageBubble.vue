<template>
  <div :class="['bubble', roleClass]">
    <div class="bubble-header">
      <span :class="['role-badge', `badge-${roleClass}`]">{{ displayRole }}</span>
      <span class="type-badge">{{ messageTypeLabel }}</span>
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

const messageTypeLabel = computed(() => {
  const type = props.message.message_type
  switch (type) {
    case 'final': return 'Final Output'
    case 'tool_call': return 'Tool Call'
    case 'tool_result': return 'Tool Result'
    default: return type.charAt(0).toUpperCase() + type.slice(1).replace(/_/g, ' ')
  }
})

const renderedContent = computed(() => marked.parse(props.message.content) as string)
</script>

<style scoped>
.bubble {
  border-radius: var(--r-lg);
  padding: var(--sp-4);
  border-left: 3px solid transparent;
  background: var(--bg-elevated);
}

.supervisor { 
  border-left-color: var(--brand);
}

.worker { 
  border-left-color: var(--success);
}

.final { 
  border-left-color: var(--info);
  background: var(--info-soft);
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

.badge-final { 
  color: var(--info);
}

.type-badge { 
  font-size: var(--text-xs);
  background: var(--bg-overlay);
  color: var(--text-3);
  padding: 2px var(--sp-2);
  border-radius: var(--r-full);
}

.content { 
  color: var(--text-2);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

.content :deep(h1), 
.content :deep(h2), 
.content :deep(h3) { 
  color: var(--text-1);
  margin: var(--sp-4) 0 var(--sp-2);
  font-weight: 600;
}

.content :deep(h1) { font-size: var(--text-lg); }
.content :deep(h2) { font-size: var(--text-base); }
.content :deep(h3) { font-size: var(--text-sm); }

.content :deep(strong) { 
  color: var(--text-1);
  font-weight: 600;
}

.content :deep(p) { 
  margin: var(--sp-2) 0;
}

.content :deep(p:first-child) {
  margin-top: 0;
}

.content :deep(p:last-child) {
  margin-bottom: 0;
}

.content :deep(ul), 
.content :deep(ol) { 
  margin: var(--sp-2) 0;
  padding-left: var(--sp-5);
}

.content :deep(li) {
  margin: var(--sp-1) 0;
}

.content :deep(table) { 
  border-collapse: collapse;
  width: 100%;
  margin: var(--sp-3) 0;
  font-size: var(--text-xs);
}

.content :deep(td), 
.content :deep(th) { 
  border: 1px solid var(--border-2);
  padding: var(--sp-2) var(--sp-3);
}

.content :deep(th) { 
  background: var(--bg-overlay);
  color: var(--text-1);
  font-weight: 600;
  text-align: left;
}

.content :deep(code) {
  background: var(--bg-overlay);
  padding: 2px var(--sp-1);
  border-radius: var(--r-xs);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
}

.content :deep(pre) {
  background: var(--bg-overlay);
  padding: var(--sp-3);
  border-radius: var(--r-md);
  overflow-x: auto;
  margin: var(--sp-3) 0;
}

.content :deep(pre code) {
  background: none;
  padding: 0;
}

.content :deep(blockquote) {
  border-left: 3px solid var(--border-3);
  margin: var(--sp-3) 0;
  padding: var(--sp-2) var(--sp-4);
  color: var(--text-3);
}
</style>
