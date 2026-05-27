<template>
  <div
    class="uploader"
    :class="{ dragover }"
    @dragover.prevent="dragover = true"
    @dragleave="dragover = false"
    @drop.prevent="onDrop"
  >
    <input ref="inputRef" type="file" accept=".pdf,.docx,.doc" multiple @change="onFileInput" hidden />
    <div class="inner" @click="inputRef?.click()">
      <div class="upload-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </div>
      <p class="upload-text">Drop PDF or DOCX files here, or <strong>click to browse</strong></p>
      <span class="upload-hint">Max {{ maxMB }} MB per file</span>
    </div>
    <div v-if="uploading" class="uploading-state">
      <div class="upload-spinner"></div>
      <span>Uploading...</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ uploading: boolean; maxMB?: number }>()
const emit = defineEmits<{ files: [File[]] }>()

const dragover = ref(false)
const inputRef = ref<HTMLInputElement | null>(null)

function onDrop(e: DragEvent) {
  dragover.value = false
  const files = Array.from(e.dataTransfer?.files ?? [])
  if (files.length) emit('files', files)
}

function onFileInput(e: Event) {
  const files = Array.from((e.target as HTMLInputElement).files ?? [])
  if (files.length) emit('files', files)
  if (inputRef.value) inputRef.value.value = ''
}
</script>

<style scoped>
.uploader {
  border: 2px dashed var(--border-2);
  border-radius: var(--r-lg);
  background: var(--bg-surface);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  position: relative;
  overflow: hidden;
}

.uploader:hover {
  border-color: var(--border-3);
  background: var(--bg-elevated);
}

.uploader.dragover { 
  border-color: var(--brand);
  background: var(--brand-soft);
}

.inner { 
  padding: var(--sp-8);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-3);
}

.upload-icon { 
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-lg);
  color: var(--text-3);
  margin-bottom: var(--sp-2);
}

.dragover .upload-icon {
  background: var(--brand-soft);
  color: var(--brand-text);
}

.upload-text { 
  margin: 0;
  font-size: var(--text-base);
  color: var(--text-2);
}

.upload-text strong { 
  color: var(--brand-text);
}

.upload-hint { 
  font-size: var(--text-xs);
  color: var(--text-4);
}

.uploading-state { 
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  background: var(--bg-surface);
  color: var(--brand-text);
  font-size: var(--text-sm);
}

.upload-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--brand-soft);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
