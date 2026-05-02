<template>
  <div :class="['gen-status', status]">
    <span class="indicator" />
    <span class="label">{{ label }}</span>
    <span v-if="status === 'running'" class="spinner" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ status: string }>()

const label = computed(() => ({
  idle: 'Not started',
  pending: 'Initializing...',
  running: 'Agents working...',
  complete: 'Complete',
  error: 'Error',
}[props.status] ?? props.status))
</script>

<style scoped>
.gen-status {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 6px 14px; border-radius: 20px; font-size: 13px;
}
.idle { background: #2d2d4e; color: #888; }
.pending { background: #2d2d1a; color: #f5c842; }
.running { background: #1a3a5e; color: #5ba3f5; }
.complete { background: #1a3a2e; color: #4caf7d; }
.error { background: #3a1a1a; color: #e74c3c; }
.indicator { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.spinner {
  width: 12px; height: 12px; border: 2px solid currentColor;
  border-top-color: transparent; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
