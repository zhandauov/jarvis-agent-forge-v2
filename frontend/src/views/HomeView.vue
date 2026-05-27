<template>
  <div class="home">
    <div class="page-header">
      <div class="header-text">
        <h1>Reports</h1>
        <p class="header-subtitle">Manage your consulting reports and chapters</p>
      </div>
      <button class="btn-create" @click="showForm = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>New Report</span>
      </button>
    </div>

    <div v-if="store.loading" class="loading-state">
      <div class="loading-spinner"></div>
      <span>Loading reports...</span>
    </div>
    
    <div v-else-if="!store.reports.length" class="empty-state">
      <div class="empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="12" y1="18" x2="12" y2="12"/>
          <line x1="9" y1="15" x2="15" y2="15"/>
        </svg>
      </div>
      <h2 class="empty-title">No reports yet</h2>
      <p class="empty-hint">Create your first report to get started with AI-powered consulting.</p>
      <button class="btn-create-empty" @click="showForm = true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"/>
          <line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        <span>Create Report</span>
      </button>
    </div>
    
    <div v-else class="reports-grid">
      <ReportCard
        v-for="report in store.reports"
        :key="report.id"
        :report="report"
        @select="goToReport(report.id)"
        @edit="startEdit(report)"
        @delete="deleteReport(report.id)"
      />
    </div>

    <ReportForm
      v-if="showForm"
      :report="editingReport"
      @close="closeForm"
      @submit="submitForm"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useReportsStore } from '@/stores/reports'
import ReportCard from '@/components/reports/ReportCard.vue'
import ReportForm from '@/components/reports/ReportForm.vue'
import type { Report } from '@/api/reports'

const store = useReportsStore()
const router = useRouter()

const showForm = ref(false)
const editingReport = ref<Report | null>(null)

onMounted(() => store.fetchAll())

function goToReport(id: number) {
  router.push(`/reports/${id}`)
}

function startEdit(report: Report) {
  editingReport.value = report
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editingReport.value = null
}

async function submitForm(data: { title: string; description: string }) {
  if (editingReport.value) {
    await store.update(editingReport.value.id, data)
  } else {
    await store.create(data.title, data.description)
  }
  closeForm()
}

async function deleteReport(id: number) {
  if (confirm('Delete this report and all its chapters?')) {
    await store.remove(id)
  }
}
</script>

<style scoped>
.home {
  padding: var(--sp-8);
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--sp-8);
  gap: var(--sp-4);
}

.header-text {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
}

h1 {
  margin: 0;
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.header-subtitle {
  margin: 0;
  color: var(--text-3);
  font-size: var(--text-base);
}

.btn-create {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: var(--brand);
  color: #fff;
  border: none;
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--r-lg);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
  flex-shrink: 0;
}

.btn-create:hover {
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}

.reports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--sp-4);
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
  max-width: 320px;
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
