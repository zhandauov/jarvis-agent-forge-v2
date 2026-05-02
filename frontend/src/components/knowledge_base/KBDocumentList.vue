<template>
  <div class="kb-list">
    <div v-if="!documents.length" class="empty">No documents uploaded yet.</div>
    <div v-for="doc in documents" :key="doc.id" class="doc-row">
      <div class="doc-info">
        <span class="doc-icon">{{ doc.file_type === 'pdf' ? '📄' : '📝' }}</span>
        <div class="doc-meta">
          <span class="filename">{{ doc.filename }}</span>
          <span class="chunks">{{ doc.status === 'ready' ? `${doc.chunk_count} chunks` : '' }}</span>
        </div>
      </div>
      <div class="doc-right">
        <span :class="['status', doc.status]">{{ doc.status }}</span>
        <button class="btn-delete" @click="$emit('delete', doc.id)" title="Delete">✕</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { KBDocument } from '@/api/knowledgeBase'
defineProps<{ documents: KBDocument[] }>()
defineEmits<{ delete: [number] }>()
</script>

<style scoped>
.kb-list { display: flex; flex-direction: column; gap: 8px; }
.empty { color: #555; font-size: 14px; text-align: center; padding: 20px; }
.doc-row {
  display: flex; justify-content: space-between; align-items: center;
  background: #1e1e3a; border: 1px solid #2d2d4e; border-radius: 6px; padding: 10px 14px;
}
.doc-info { display: flex; align-items: center; gap: 10px; }
.doc-icon { font-size: 20px; }
.doc-meta { display: flex; flex-direction: column; }
.filename { color: #e0e0ff; font-size: 14px; }
.chunks { color: #666; font-size: 12px; }
.doc-right { display: flex; align-items: center; gap: 10px; }
.status { padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.status.processing { background: #2d2d1a; color: #f5c842; }
.status.ready { background: #1a3a2e; color: #4caf7d; }
.status.error { background: #3a1a1a; color: #e74c3c; }
.btn-delete { background: transparent; border: none; color: #666; cursor: pointer; font-size: 16px; padding: 2px 6px; border-radius: 4px; }
.btn-delete:hover { color: #e74c3c; }
</style>
