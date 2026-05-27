<template>
  <div :class="['gen-status', status]">
    <span class="status-dot"></span>
    <span class="status-label">{{ label }}</span>
    <span v-if="status === 'running'" class="status-spinner"></span>
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
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--r-full);
  font-size: var(--text-xs);
  font-weight: 500;
}

.idle { 
  background: var(--bg-overlay);
  color: var(--text-3);
}

.pending { 
  background: var(--warning-soft);
  color: var(--warning);
}

.running { 
  background: var(--info-soft);
  color: var(--info);
}

.complete { 
  background: var(--success-soft);
  color: var(--success);
}

.error { 
  background: var(--error-soft);
  color: var(--error);
}

.status-dot { 
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.running .status-dot {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.status-spinner {
  width: 12px;
  height: 12px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { 
  to { transform: rotate(360deg); } 
}
</style>
