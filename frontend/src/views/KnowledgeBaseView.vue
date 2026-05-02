<template>
  <div class="kb-view">
    <div class="page-header">
      <div>
        <router-link :to="`/reports/${reportId}`" class="back-link">← Report</router-link>
        <h1>Knowledge Base</h1>
      </div>
    </div>

    <p class="hint">Upload PDF and DOCX files with market data, research, and figures. Agents will use this data when writing report sections.</p>

    <KBUploader :uploading="kbStore.uploading" :max-m-b="50" @files="onFiles" />

    <div class="section-title">
      <span>Documents ({{ kbStore.documents.length }})</span>
      <button class="btn-refresh" @click="refresh">↻ Refresh</button>
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
.kb-view { padding: 32px; max-width: 800px; margin: 0 auto; }
.page-header { margin-bottom: 8px; }
.back-link { color: #888; text-decoration: none; font-size: 14px; }
.back-link:hover { color: #9d8fff; }
h1 { margin: 4px 0 0; font-size: 24px; color: #e0e0ff; }
.hint { color: #888; font-size: 14px; margin: 0 0 24px; }
.section-title { display: flex; justify-content: space-between; align-items: center; margin: 24px 0 12px; color: #aaa; font-size: 14px; }
.btn-refresh { background: transparent; border: none; color: #7c6af7; cursor: pointer; font-size: 14px; }
</style>
