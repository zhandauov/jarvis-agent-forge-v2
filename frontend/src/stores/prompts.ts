import { defineStore } from 'pinia'
import { ref } from 'vue'
import { promptsApi, type PromptTemplate } from '@/api/prompts'

export const usePromptsStore = defineStore('prompts', () => {
  const templates = ref<PromptTemplate[]>([])
  const loading = ref(false)
  const saving = ref(false)

  async function fetchAll() {
    loading.value = true
    try {
      templates.value = await promptsApi.list()
    } finally {
      loading.value = false
    }
  }

  async function update(key: string, body: string) {
    saving.value = true
    try {
      const updated = await promptsApi.update(key, body)
      const idx = templates.value.findIndex(t => t.key === key)
      if (idx !== -1) templates.value[idx] = updated
      return updated
    } finally {
      saving.value = false
    }
  }

  async function reset(key: string) {
    saving.value = true
    try {
      const updated = await promptsApi.reset(key)
      const idx = templates.value.findIndex(t => t.key === key)
      if (idx !== -1) templates.value[idx] = updated
      return updated
    } finally {
      saving.value = false
    }
  }

  return { templates, loading, saving, fetchAll, update, reset }
})
