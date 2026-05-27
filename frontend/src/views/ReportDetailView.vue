<template>
  <div class="report-detail">
    <div v-if="loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>Loading report...</span>
    </div>
    
    <template v-else-if="report">
      <div class="page-header">
        <div class="title-area">
          <router-link to="/" class="back-link">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="19" y1="12" x2="5" y2="12"/>
              <polyline points="12 19 5 12 12 5"/>
            </svg>
            <span>Back to Reports</span>
          </router-link>
          <h1>{{ report.title }}</h1>
          <p v-if="report.description" class="desc">{{ report.description }}</p>
        </div>
        <div class="header-actions">
          <router-link :to="`/reports/${report.id}/kb`" class="btn-secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            </svg>
            <span>Knowledge Base</span>
          </router-link>
          <button class="btn-primary" @click="showChapterForm = true">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="5" x2="12" y2="19"/>
              <line x1="5" y1="12" x2="19" y2="12"/>
            </svg>
            <span>Add Chapter</span>
          </button>
        </div>
      </div>

      <div v-if="!chaptersStore.chapters.length" class="empty-state">
        <div class="empty-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
            <line x1="12" y1="6" x2="12" y2="14"/>
            <line x1="8" y1="10" x2="16" y2="10"/>
          </svg>
        </div>
        <h2 class="empty-title">No chapters yet</h2>
        <p class="empty-hint">Add chapters to structure your report. Each chapter can be generated with AI assistance.</p>
        <button class="btn-create-empty" @click="showChapterForm = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>Add First Chapter</span>
        </button>
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
.report-detail {
  padding: var(--sp-8);
  max-width: 960px;
  margin: 0 auto;
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--sp-8);
  gap: var(--sp-6);
  flex-wrap: wrap;
}

.title-area { 
  flex: 1;
  min-width: 200px;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--text-3);
  font-size: var(--text-sm);
  margin-bottom: var(--sp-3);
  transition: color var(--duration-fast) var(--ease-out);
}

.back-link:hover { 
  color: var(--brand-text); 
}

h1 {
  margin: 0 0 var(--sp-2);
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.desc {
  margin: 0;
  color: var(--text-3);
  font-size: var(--text-base);
  line-height: var(--leading-relaxed);
}

.header-actions {
  display: flex;
  gap: var(--sp-3);
  flex-shrink: 0;
  align-items: center;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: var(--brand);
  color: #fff;
  border: none;
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-primary:hover {
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-2);
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-secondary:hover {
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}

.chapters-list {
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-16);
  color: var(--text-3);
  font-size: var(--text-sm);
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-2);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-16);
  text-align: center;
}

.empty-icon {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-xl);
  color: var(--text-4);
  margin-bottom: var(--sp-2);
}

.empty-title {
  color: var(--text-2);
  font-size: var(--text-xl);
  font-weight: 600;
  margin: 0;
}

.empty-hint {
  color: var(--text-3);
  font-size: var(--text-base);
  max-width: 360px;
  margin: 0;
  line-height: var(--leading-relaxed);
}

.btn-create-empty {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: var(--brand);
  color: #fff;
  border: none;
  padding: var(--sp-3) var(--sp-5);
  border-radius: var(--r-lg);
  cursor: pointer;
  font-size: var(--text-base);
  font-weight: 500;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
  margin-top: var(--sp-2);
}

.btn-create-empty:hover {
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}
</style>
