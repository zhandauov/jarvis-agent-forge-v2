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
      <span class="icon">📂</span>
      <p>Drop PDF or DOCX files here, or <strong>click to browse</strong></p>
      <span class="hint">Max {{ maxMB }} MB per file</span>
    </div>
    <div v-if="uploading" class="uploading">Uploading...</div>
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
  border: 2px dashed #3d3d5e; border-radius: 10px;
  background: #14142a; cursor: pointer; transition: border-color 0.2s;
}
.uploader.dragover { border-color: #7c6af7; background: #1a1a3e; }
.inner { padding: 32px; text-align: center; color: #888; }
.icon { font-size: 32px; display: block; margin-bottom: 8px; }
p { margin: 0 0 4px; font-size: 14px; }
strong { color: #9d8fff; }
.hint { font-size: 12px; color: #555; }
.uploading { text-align: center; padding: 12px; color: #7c6af7; font-size: 14px; }
</style>
