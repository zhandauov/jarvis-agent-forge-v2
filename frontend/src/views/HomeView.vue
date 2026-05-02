<template>
  <div class="home">
    <div class="page-header">
      <h1>Reports</h1>
      <button class="btn-primary" @click="showForm = true">+ New Report</button>
    </div>

    <div v-if="store.loading" class="loading">Loading...</div>
    <div v-else-if="!store.reports.length" class="empty">
      <p>No reports yet. Create your first report to get started.</p>
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
.home { padding: 32px; max-width: 1200px; margin: 0 auto; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
h1 { margin: 0; font-size: 24px; color: #e0e0ff; }
.btn-primary { background: #7c6af7; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-size: 14px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.loading, .empty { color: #666; text-align: center; padding: 60px; }
</style>
