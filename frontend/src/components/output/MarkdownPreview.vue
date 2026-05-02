<template>
  <div class="preview-panel">
    <div class="preview-header">
      <h3>Output</h3>
      <div class="actions" v-if="markdown">
        <button class="btn-action" @click="copyMarkdown">{{ copied ? '✓ Copied' : 'Copy MD' }}</button>
        <button class="btn-action" @click="downloadMarkdown">Download</button>
      </div>
    </div>
    <div v-if="markdown" class="rendered" v-html="rendered" />
    <div v-else class="empty">
      <p>The final report section will appear here after generation.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { marked } from 'marked'

const props = defineProps<{ markdown: string | null; chapterTitle?: string }>()
const copied = ref(false)

const rendered = computed(() => props.markdown ? marked.parse(props.markdown) as string : '')

async function copyMarkdown() {
  if (!props.markdown) return
  await navigator.clipboard.writeText(props.markdown)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}

function downloadMarkdown() {
  if (!props.markdown) return
  const blob = new Blob([props.markdown], { type: 'text/markdown' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `${props.chapterTitle ?? 'chapter'}.md`
  a.click()
}
</script>

<style scoped>
.preview-panel { display: flex; flex-direction: column; height: 100%; }
.preview-header { display: flex; justify-content: space-between; align-items: center; padding: 16px; border-bottom: 1px solid #2d2d4e; }
h3 { margin: 0; color: #e0e0ff; font-size: 16px; }
.actions { display: flex; gap: 8px; }
.btn-action { background: transparent; border: 1px solid #3d3d5e; color: #aaa; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; }
.btn-action:hover { border-color: #7c6af7; color: #9d8fff; }
.rendered {
  flex: 1; overflow-y: auto; padding: 20px;
  color: #d0d0e8; font-size: 15px; line-height: 1.7;
}
.rendered :deep(h1) { font-size: 22px; color: #e0e0ff; border-bottom: 1px solid #2d2d4e; padding-bottom: 8px; }
.rendered :deep(h2) { font-size: 18px; color: #e0e0ff; }
.rendered :deep(h3) { font-size: 15px; color: #c0c0e8; }
.rendered :deep(strong) { color: #e0e0ff; }
.rendered :deep(table) { border-collapse: collapse; width: 100%; margin: 12px 0; }
.rendered :deep(td), .rendered :deep(th) { border: 1px solid #3d3d5e; padding: 8px 12px; }
.rendered :deep(th) { background: #2d2d4e; color: #e0e0ff; }
.rendered :deep(blockquote) { border-left: 3px solid #7c6af7; margin: 0; padding: 8px 16px; color: #888; }
.rendered :deep(code) { background: #2d2d4e; padding: 2px 6px; border-radius: 4px; font-size: 13px; }
.empty { flex: 1; display: flex; align-items: center; justify-content: center; color: #555; text-align: center; padding: 40px; }
</style>
