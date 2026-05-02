<template>
  <div class="report-card" @click="$emit('select')">
    <div class="card-header">
      <h3>{{ report.title }}</h3>
      <span :class="['status-badge', report.status]">{{ report.status }}</span>
    </div>
    <p class="desc">{{ report.description || 'No description' }}</p>
    <div class="card-footer">
      <span class="date">{{ formatDate(report.created_at) }}</span>
      <div class="actions" @click.stop>
        <button class="btn-ghost" @click="$emit('edit')">Edit</button>
        <button class="btn-ghost danger" @click="$emit('delete')">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Report } from '@/api/reports'

defineProps<{ report: Report }>()
defineEmits<{ select: []; edit: []; delete: [] }>()

function formatDate(d: string) {
  return new Date(d).toLocaleDateString()
}
</script>

<style scoped>
.report-card {
  background: #1e1e3a;
  border: 1px solid #2d2d4e;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: border-color 0.2s, transform 0.1s;
}
.report-card:hover { border-color: #7c6af7; transform: translateY(-1px); }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
h3 { margin: 0; font-size: 16px; color: #e0e0ff; }
.desc { color: #888; font-size: 14px; margin: 0 0 16px; }
.card-footer { display: flex; justify-content: space-between; align-items: center; }
.date { font-size: 12px; color: #666; }
.actions { display: flex; gap: 8px; }
.btn-ghost { background: transparent; border: 1px solid #3d3d5e; color: #aaa; padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.btn-ghost:hover { border-color: #7c6af7; color: #e0e0ff; }
.btn-ghost.danger:hover { border-color: #e74c3c; color: #e74c3c; }
.status-badge { padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.status-badge.draft { background: #2d2d4e; color: #888; }
.status-badge.in_progress { background: #1a3a5e; color: #5ba3f5; }
.status-badge.complete { background: #1a3a2e; color: #4caf7d; }
</style>
