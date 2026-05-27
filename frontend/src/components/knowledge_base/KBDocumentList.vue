<template>
  <div class="kb-list">
    <div v-if="!documents.length" class="empty-state">
      <div class="empty-icon">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
      </div>
      <span>No documents uploaded yet</span>
    </div>
    
    <div v-for="doc in documents" :key="doc.id" class="doc-row">
      <div class="doc-info">
        <div class="doc-icon">
          <svg v-if="doc.file_type === 'pdf'" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
          </svg>
        </div>
        <div class="doc-meta">
          <span class="filename">{{ doc.filename }}</span>
          <span class="chunks" v-if="doc.status === 'ready'">{{ doc.chunk_count }} chunks indexed</span>
        </div>
      </div>
      <div class="doc-right">
        <span :class="['status-badge', doc.status]">
          <span class="status-dot"></span>
          {{ statusLabel(doc.status) }}
        </span>
        <button class="btn-delete" @click="$emit('delete', doc.id)" title="Delete">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { KBDocument } from '@/api/knowledgeBase'

defineProps<{ documents: KBDocument[] }>()
defineEmits<{ delete: [number] }>()

function statusLabel(status: string) {
  switch (status) {
    case 'processing': return 'Processing'
    case 'ready': return 'Ready'
    case 'error': return 'Error'
    default: return status
  }
}
</script>

<style scoped>
.kb-list { 
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.empty-state { 
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-3);
  color: var(--text-4);
  font-size: var(--text-sm);
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
}

.doc-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-md);
  padding: var(--sp-3) var(--sp-4);
  transition: border-color var(--duration-fast) var(--ease-out);
}

.doc-row:hover {
  border-color: var(--border-2);
}

.doc-info { 
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.doc-icon { 
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-md);
  color: var(--text-3);
}

.doc-meta { 
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.filename { 
  color: var(--text-1);
  font-size: var(--text-sm);
  font-weight: 500;
}

.chunks { 
  color: var(--text-4);
  font-size: var(--text-xs);
}

.doc-right { 
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.status-badge { 
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-1) var(--sp-3);
  border-radius: var(--r-full);
  font-size: var(--text-xs);
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-badge.processing { 
  background: var(--warning-soft);
  color: var(--warning);
}

.status-badge.processing .status-dot {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-badge.ready { 
  background: var(--success-soft);
  color: var(--success);
}

.status-badge.error { 
  background: var(--error-soft);
  color: var(--error);
}

.btn-delete { 
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: transparent;
  border: 1px solid var(--border-2);
  border-radius: var(--r-sm);
  color: var(--text-4);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-delete:hover { 
  color: var(--error);
  border-color: var(--error);
  background: var(--error-soft);
}
</style>
