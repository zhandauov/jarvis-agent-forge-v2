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
  display: flex; justify-content: space-between; align-items: center;
  background: #1e1e3a; border: 1px solid #2d2d4e; border-radius: 8px;
  padding: 14px 16px; transition: border-color 0.2s; cursor: pointer;
}
.chapter-card:hover { border-color: #7c6af7; }
.left { display: flex; align-items: center; gap: 12px; flex: 1; }
.index { width: 28px; height: 28px; border-radius: 50%; background: #2d2d4e; color: #9d8fff; display: flex; align-items: center; justify-content: center; font-size: 13px; flex-shrink: 0; }
.info { display: flex; flex-direction: column; }
.title { color: #e0e0ff; font-size: 15px; }
.desc { color: #666; font-size: 13px; }
.right { display: flex; align-items: center; gap: 8px; }
.status { padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.status.pending { background: #2d2d4e; color: #888; }
.status.running { background: #1a3a5e; color: #5ba3f5; }
.status.complete { background: #1a3a2e; color: #4caf7d; }
.status.error { background: #3a1a1a; color: #e74c3c; }
.btn-ghost { background: transparent; border: 1px solid #3d3d5e; color: #aaa; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 13px; }
.btn-ghost:hover { border-color: #7c6af7; color: #e0e0ff; }
.btn-ghost.danger:hover { border-color: #e74c3c; color: #e74c3c; }
</style>
