<template>
  <div class="kb-view">
    <div class="page-header">
      <div class="title-area">
        <router-link :to="`/reports/${reportId}`" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          <span>Back to Report</span>
        </router-link>
        <h1>Knowledge Base</h1>
        <p class="hint">Upload PDF and DOCX files with market data, research, and figures. Agents will use this data when writing report sections.</p>
      </div>
    </div>

    <KBUploader :uploading="kbStore.uploading" :max-m-b="50" @files="onFiles" />

    <div class="section-header">
      <div class="section-title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        <span>Documents ({{ kbStore.documents.length }})</span>
      </div>
      <button class="btn-refresh" @click="refresh">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"/>
          <polyline points="1 20 1 14 7 14"/>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
        </svg>
        <span>Refresh</span>
      </button>
    </div>
    
    <KBDocumentList :documents="kbStore.documents" @delete="onDelete" />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useKBStore } from '@/stores/kb'
import KBUploader from '@/components/knowledge_base/KBUploader.vue'
import KBDocumentList from '@/components/knowledge_base/KBDocumentList.vue'

const route = useRoute()
const reportId = Number(route.params.id)
const kbStore = useKBStore()

onMounted(() => kbStore.fetchAll(reportId))

async function onFiles(files: File[]) {
  for (const file of files) {
    await kbStore.upload(reportId, file)
  }
}

async function onDelete(docId: number) {
  if (confirm('Remove this document from the knowledge base?')) {
    await kbStore.remove(reportId, docId)
  }
}

function refresh() {
  kbStore.pollStatus(reportId)
}
</script>

<style scoped>
.kb-view { 
  padding: var(--sp-8);
  max-width: 800px;
  margin: 0 auto;
  width: 100%;
}

.page-header { 
  margin-bottom: var(--sp-6);
}

.title-area {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.back-link { 
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--text-3);
  text-decoration: none;
  font-size: var(--text-sm);
  margin-bottom: var(--sp-2);
  transition: color var(--duration-fast) var(--ease-out);
}

.back-link:hover { 
  color: var(--brand-text);
}

h1 { 
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.hint { 
  color: var(--text-3);
  font-size: var(--text-sm);
  margin: var(--sp-1) 0 0;
  line-height: var(--leading-relaxed);
}

.section-header { 
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: var(--sp-6) 0 var(--sp-4);
}

.section-title { 
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--text-2);
  font-size: var(--text-sm);
  font-weight: 500;
}

.btn-refresh { 
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-refresh:hover {
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}
</style>
