<template>
  <div class="chapter-card" @click="$emit('open')">
    <div class="card-left">
      <div class="chapter-index">{{ index + 1 }}</div>
      <div class="chapter-info">
        <span class="chapter-title">{{ chapter.title }}</span>
        <span class="chapter-desc" v-if="chapter.description">{{ chapter.description }}</span>
      </div>
    </div>
    <div class="card-right" @click.stop>
      <span :class="['status-badge', statusClass]">
        <span class="status-dot"></span>
        {{ statusLabel }}
      </span>
      <button class="action-btn" @click="$emit('edit')" title="Edit">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
        </svg>
      </button>
      <button class="action-btn action-btn-danger" @click="$emit('delete')" title="Delete">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="6" x2="6" y2="18"/>
          <line x1="6" y1="6" x2="18" y2="18"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Chapter } from '@/api/chapters'

const props = defineProps<{ chapter: Chapter; index: number }>()
defineEmits<{ open: []; edit: []; delete: [] }>()

const statusClass = computed(() => {
  switch (props.chapter.status) {
    case 'complete': return 'status-success'
    case 'running': return 'status-info'
    case 'error': return 'status-error'
    default: return 'status-default'
  }
})

const statusLabel = computed(() => {
  switch (props.chapter.status) {
    case 'complete': return 'Complete'
    case 'running': return 'Running'
    case 'error': return 'Error'
    default: return 'Pending'
  }
})
</script>

<style scoped>
.chapter-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-lg);
  padding: var(--sp-4) var(--sp-5);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.chapter-card:hover {
  border-color: var(--brand);
  box-shadow: 0 0 0 1px var(--brand-soft), var(--shadow-md);
  transform: translateX(4px);
}

.card-left {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  flex: 1;
  min-width: 0;
}

.chapter-index {
  width: 32px;
  height: 32px;
  border-radius: var(--r-md);
  background: var(--bg-overlay);
  border: 1px solid var(--border-2);
  color: var(--brand-text);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--text-sm);
  font-weight: 600;
  flex-shrink: 0;
}

.chapter-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.chapter-title {
  color: var(--text-1);
  font-size: var(--text-base);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chapter-desc {
  color: var(--text-3);
  font-size: var(--text-sm);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-right {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  flex-shrink: 0;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-1) var(--sp-3);
  border-radius: var(--r-full);
  font-size: var(--text-xs);
  font-weight: 500;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.status-default {
  background: var(--bg-overlay);
  color: var(--text-3);
}

.status-info {
  background: var(--info-soft);
  color: var(--info);
}

.status-info .status-dot {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-success {
  background: var(--success-soft);
  color: var(--success);
}

.status-error {
  background: var(--error-soft);
  color: var(--error);
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
