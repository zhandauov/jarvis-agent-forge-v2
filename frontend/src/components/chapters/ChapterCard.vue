<template>
  <div class="chapter-card" @click="$emit('open')">
    <div class="left">
      <span class="index">{{ index + 1 }}</span>
      <div class="info">
        <span class="title">{{ chapter.title }}</span>
        <span class="desc">{{ chapter.description || '' }}</span>
      </div>
    </div>
    <div class="right" @click.stop>
      <span :class="['status', chapter.status]">{{ chapter.status }}</span>
      <button class="btn-ghost" @click="$emit('edit')">Edit</button>
      <button class="btn-ghost danger" @click="$emit('delete')">✕</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Chapter } from '@/api/chapters'
defineProps<{ chapter: Chapter; index: number }>()
defineEmits<{ open: []; edit: []; delete: [] }>()
</script>

<style scoped>
.chapter-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-md);
  padding: 14px var(--sp-4);
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  transition: border-color 0.15s, box-shadow 0.15s;
}

.chapter-card:hover {
  border-color: var(--brand);
  box-shadow: 0 0 0 1px var(--brand-soft), 0 4px 12px rgba(0, 0, 0, 0.3);
}

.left {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  flex: 1;
  min-width: 0;
}

.index {
  width: 28px;
  height: 28px;
  border-radius: 50%;
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

.info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.title {
  color: var(--text-1);
  font-size: var(--text-base);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.desc {
  color: var(--text-3);
  font-size: var(--text-sm);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.right {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  flex-shrink: 0;
}

.status {
  padding: 2px 8px;
  border-radius: var(--r-sm);
  font-size: var(--text-xs);
  font-weight: 500;
}

.status.pending {
  background: var(--bg-overlay);
  color: var(--text-3);
}

.status.running {
  background: var(--info-bg);
  color: var(--info);
}

.status.complete {
  background: var(--success-bg);
  color: var(--success);
}

.status.error {
  background: var(--error-bg);
  color: var(--error);
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
</style>
