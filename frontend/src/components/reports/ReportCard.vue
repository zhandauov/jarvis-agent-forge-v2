<template>
  <div class="report-card" @click="$emit('select')">
    <div class="card-content">
      <div class="card-header">
        <h3 class="card-title">{{ report.title }}</h3>
        <span :class="['status-badge', statusClass]">{{ statusLabel }}</span>
      </div>
      <p class="card-desc">{{ report.description || 'No description provided' }}</p>
    </div>
    <div class="card-footer">
      <span class="card-date">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
          <line x1="16" y1="2" x2="16" y2="6"/>
          <line x1="8" y1="2" x2="8" y2="6"/>
          <line x1="3" y1="10" x2="21" y2="10"/>
        </svg>
        {{ formatDate(report.created_at) }}
      </span>
      <div class="card-actions" @click.stop>
        <button class="action-btn" @click="$emit('edit')" title="Edit">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </button>
        <button class="action-btn action-btn-danger" @click="$emit('delete')" title="Delete">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Report } from '@/api/reports'

const props = defineProps<{ report: Report }>()
defineEmits<{ select: []; edit: []; delete: [] }>()

const statusClass = computed(() => {
  switch (props.report.status) {
    case 'complete': return 'status-success'
    case 'in_progress': return 'status-info'
    default: return 'status-default'
  }
})

const statusLabel = computed(() => {
  switch (props.report.status) {
    case 'complete': return 'Complete'
    case 'in_progress': return 'In Progress'
    default: return 'Draft'
  }
})

function formatDate(d: string) {
  return new Date(d).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}
</script>

<style scoped>
.report-card {
  display: flex;
  flex-direction: column;
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-lg);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  overflow: hidden;
}

.report-card:hover {
  border-color: var(--brand);
  box-shadow: 0 0 0 1px var(--brand-soft), var(--shadow-lg);
  transform: translateY(-2px);
}

.card-content {
  padding: var(--sp-5);
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--sp-3);
}

.card-title {
  margin: 0;
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-1);
  line-height: var(--leading-snug);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.status-badge {
  padding: 3px var(--sp-2);
  border-radius: var(--r-sm);
  font-size: var(--text-xs);
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-default {
  background: var(--bg-overlay);
  color: var(--text-3);
}

.status-info {
  background: var(--info-soft);
  color: var(--info);
}

.status-success {
  background: var(--success-soft);
  color: var(--success);
}

.card-desc {
  color: var(--text-3);
  font-size: var(--text-sm);
  margin: 0;
  line-height: var(--leading-relaxed);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-3) var(--sp-5);
  border-top: 1px solid var(--border-1);
  background: var(--bg-elevated);
}

.card-date {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-size: var(--text-xs);
  color: var(--text-4);
}

.card-date svg {
  opacity: 0.6;
}

.card-actions {
  display: flex;
  gap: var(--sp-1);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: transparent;
  border: 1px solid var(--border-2);
  border-radius: var(--r-sm);
  color: var(--text-3);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.action-btn:hover {
  border-color: var(--border-3);
  color: var(--text-1);
  background: var(--bg-hover);
}

.action-btn-danger:hover {
  border-color: var(--error);
  color: var(--error);
  background: var(--error-soft);
}
</style>
