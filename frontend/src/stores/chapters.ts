import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chaptersApi, type Chapter } from '@/api/chapters'

export const useChaptersStore = defineStore('chapters', () => {
  const chapters = ref<Chapter[]>([])
  const current = ref<Chapter | null>(null)
  const loading = ref(false)

  async function fetchAll(reportId: number) {
    loading.value = true
    try {
      chapters.value = await chaptersApi.list(reportId)
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(reportId: number, chapterId: number) {
    current.value = await chaptersApi.get(reportId, chapterId)
  }

  async function create(reportId: number, data: { title: string; description?: string }) {
    const chapter = await chaptersApi.create(reportId, { ...data, order_index: chapters.value.length })
    chapters.value.push(chapter)
    return chapter
  }

  async function update(reportId: number, chapterId: number, data: Partial<Chapter>) {
    const updated = await chaptersApi.update(reportId, chapterId, data)
    const idx = chapters.value.findIndex(c => c.id === chapterId)
    if (idx !== -1) chapters.value[idx] = updated
    if (current.value?.id === chapterId) current.value = updated
    return updated
  }

  async function remove(reportId: number, chapterId: number) {
    await chaptersApi.delete(reportId, chapterId)
    chapters.value = chapters.value.filter(c => c.id !== chapterId)
    if (current.value?.id === chapterId) current.value = null
  }

  function updateLocal(chapter: Chapter) {
    const idx = chapters.value.findIndex(c => c.id === chapter.id)
    if (idx !== -1) chapters.value[idx] = chapter
    if (current.value?.id === chapter.id) current.value = chapter
  }

  return { chapters, current, loading, fetchAll, fetchOne, create, update, remove, updateLocal }
})
