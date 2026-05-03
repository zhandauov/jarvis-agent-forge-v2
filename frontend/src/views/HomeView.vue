<template>
  <div class="home">
    <div class="page-header">
      <h1>Reports</h1>
      <button class="btn-primary" @click="showForm = true">+ New Report</button>
    </div>

    <div v-if="store.loading" class="loading">Loading...</div>
    <div v-else-if="!store.reports.length" class="empty">
      <span class="empty-icon">✦</span>
      <p>No reports yet.</p>
      <span class="empty-hint">Create your first report to get started.</span>
    </div>
    <div v-else class="grid">
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
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--sp-8);
}

h1 {
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.btn-primary {
  background: var(--brand);
  color: #fff;
  border: none;
  padding: 9px var(--sp-4);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  transition: background 0.15s, box-shadow 0.15s;
}

.btn-primary:hover {
  background: var(--brand-dim);
  box-shadow: 0 4px 12px rgba(124, 106, 247, 0.3);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--sp-4);
}

.loading {
  color: var(--text-3);
  text-align: center;
  padding: 80px;
  font-size: var(--text-sm);
}

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-2);
  padding: 80px;
  text-align: center;
}

.empty-icon {
  font-size: 36px;
  color: var(--border-3);
  line-height: 1;
  margin-bottom: var(--sp-2);
}

.empty p {
  color: var(--text-2);
  font-size: var(--text-lg);
  font-weight: 500;
}

.empty-hint {
  color: var(--text-3);
  font-size: var(--text-sm);
}
</style>
