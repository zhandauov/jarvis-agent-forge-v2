import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reportsApi, type Report } from '@/api/reports'

export const useReportsStore = defineStore('reports', () => {
  const reports = ref<Report[]>([])
  const current = ref<Report | null>(null)
  const loading = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      reports.value = await reportsApi.list()
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(id: number) {
    current.value = await reportsApi.get(id)
  }

  async function create(title: string, description?: string) {
    const report = await reportsApi.create({ title, description })
    reports.value.unshift(report)
    return report
  }

  async function update(id: number, data: Partial<Report>) {
    const updated = await reportsApi.update(id, data)
    const idx = reports.value.findIndex(r => r.id === id)
    if (idx !== -1) reports.value[idx] = updated
    if (current.value?.id === id) current.value = updated
    return updated
  }

  async function remove(id: number) {
    await reportsApi.delete(id)
    reports.value = reports.value.filter(r => r.id !== id)
    if (current.value?.id === id) current.value = null
  }

  return { reports, current, loading, fetchAll, fetchOne, create, update, remove }
})
