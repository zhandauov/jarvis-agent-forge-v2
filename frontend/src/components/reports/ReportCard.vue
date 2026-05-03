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
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-md);
  padding: 20px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

.report-card:hover {
  border-color: var(--brand);
  box-shadow: 0 0 0 1px var(--brand-soft), 0 8px 24px rgba(0, 0, 0, 0.4);
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--sp-2);
}

h3 {
  margin: 0;
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-1);
  line-height: 1.4;
}

.desc {
  color: var(--text-2);
  font-size: var(--text-sm);
  margin: 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--sp-2);
}

.date {
  font-size: var(--text-xs);
  color: var(--text-3);
}

.actions {
  display: flex;
  gap: var(--sp-2);
}

.btn-ghost {
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: 4px 10px;
  border-radius: var(--r-sm);
  cursor: pointer;
  font-size: var(--text-xs);
  font-family: var(--font);
  transition: border-color 0.15s, color 0.15s;
}

.btn-ghost:hover {
  border-color: var(--border-3);
  color: var(--text-1);
}

.btn-ghost.danger:hover {
  border-color: var(--error);
  color: var(--error);
}

.status-badge {
  padding: 2px 8px;
  border-radius: var(--r-sm);
  font-size: var(--text-xs);
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.draft {
  background: var(--bg-overlay);
  color: var(--text-3);
}

.status-badge.in_progress {
  background: var(--info-bg);
  color: var(--info);
}

.status-badge.complete {
  background: var(--success-bg);
  color: var(--success);
}
</style>
