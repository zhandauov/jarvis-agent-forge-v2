<template>
  <div class="report-detail">
    <div v-if="loading" class="loading">Loading...</div>
    <template v-else-if="report">
      <div class="page-header">
        <div class="title-area">
          <router-link to="/" class="back-link">← Back</router-link>
          <h1>{{ report.title }}</h1>
          <p v-if="report.description" class="desc">{{ report.description }}</p>
        </div>
        <div class="header-actions">
          <router-link :to="`/reports/${report.id}/kb`" class="btn-secondary">Knowledge Base</router-link>
          <button class="btn-primary" @click="showChapterForm = true">+ Add Chapter</button>
        </div>
      </div>

      <div v-if="!chaptersStore.chapters.length" class="empty">
        <p>No chapters yet. Add a chapter to start building your report.</p>
      </div>
      <div v-else class="chapters-list">
        <ChapterCard
          v-for="(chapter, i) in chaptersStore.chapters"
          :key="chapter.id"
          :chapter="chapter"
          :index="i"
          @open="goToChapter(chapter.id)"
          @edit="startEditChapter(chapter)"
          @delete="deleteChapter(chapter.id)"
        />
      </div>
    </template>

    <ChapterForm
      v-if="showChapterForm"
      :chapter="editingChapter"
      @close="closeChapterForm"
      @submit="submitChapter"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useReportsStore } from '@/stores/reports'
import { useChaptersStore } from '@/stores/chapters'
import ChapterCard from '@/components/chapters/ChapterCard.vue'
import ChapterForm from '@/components/chapters/ChapterForm.vue'
import type { Chapter } from '@/api/chapters'
import type { Report } from '@/api/reports'

const route = useRoute()
const router = useRouter()
const reportsStore = useReportsStore()
const chaptersStore = useChaptersStore()

const reportId = Number(route.params.id)
const report = ref<Report | null>(null)
const loading = ref(true)
const showChapterForm = ref(false)
const editingChapter = ref<Chapter | null>(null)

onMounted(async () => {
  await Promise.all([
    reportsStore.fetchOne(reportId).then(() => { report.value = reportsStore.current }),
    chaptersStore.fetchAll(reportId),
  ])
  loading.value = false
})

function goToChapter(chapterId: number) {
  router.push(`/reports/${reportId}/chapters/${chapterId}`)
}

function startEditChapter(chapter: Chapter) {
  editingChapter.value = chapter
  showChapterForm.value = true
}

function closeChapterForm() {
  showChapterForm.value = false
  editingChapter.value = null
}

async function submitChapter(data: { title: string; description: string }) {
  if (editingChapter.value) {
    await chaptersStore.update(reportId, editingChapter.value.id, data)
  } else {
    await chaptersStore.create(reportId, data)
  }
  closeChapterForm()
}

async function deleteChapter(chapterId: number) {
  if (confirm('Delete this chapter?')) {
    await chaptersStore.remove(reportId, chapterId)
  }
}
</script>

<style scoped>
.report-detail { padding: 32px; max-width: 900px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 32px; gap: 16px; }
.title-area { flex: 1; }
.back-link { display: inline-block; color: #888; text-decoration: none; font-size: 13px; margin-bottom: 8px; }
.back-link:hover { color: #9d8fff; }
h1 { margin: 0 0 6px; font-size: 24px; color: #e0e0ff; }
.desc { margin: 0; color: #888; font-size: 14px; }
.header-actions { display: flex; gap: 12px; flex-shrink: 0; }
.btn-primary { background: #7c6af7; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-flex; align-items: center; }
.btn-secondary { background: transparent; border: 1px solid #3d3d5e; color: #aaa; padding: 10px 16px; border-radius: 8px; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-flex; align-items: center; }
.btn-secondary:hover { border-color: #7c6af7; color: #9d8fff; }
.chapters-list { display: flex; flex-direction: column; gap: 8px; }
.loading, .empty { color: #666; text-align: center; padding: 60px; }
</style>
