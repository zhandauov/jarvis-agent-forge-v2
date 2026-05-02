import { defineStore } from 'pinia'
import { ref } from 'vue'
import { knowledgeBaseApi, type KBDocument } from '@/api/knowledgeBase'

export const useKBStore = defineStore('kb', () => {
  const documents = ref<KBDocument[]>([])
  const loading = ref(false)
  const uploading = ref(false)

  async function fetchAll(reportId: number) {
    loading.value = true
    try {
      documents.value = await knowledgeBaseApi.list(reportId)
    } finally {
      loading.value = false
    }
  }

  async function upload(reportId: number, file: File) {
    uploading.value = true
    try {
      const doc = await knowledgeBaseApi.upload(reportId, file)
      documents.value.unshift(doc)
      return doc
    } finally {
      uploading.value = false
    }
  }

  async function remove(reportId: number, docId: number) {
    await knowledgeBaseApi.delete(reportId, docId)
    documents.value = documents.value.filter(d => d.id !== docId)
  }

  async function pollStatus(reportId: number) {
    const docs = await knowledgeBaseApi.list(reportId)
    documents.value = docs
  }

  return { documents, loading, uploading, fetchAll, upload, remove, pollStatus }
})
