<template>
  <div class="preview-panel">
    <div class="preview-header">
      <span class="panel-title">Output</span>
      <div class="header-actions" v-if="markdown">
        <button class="action-btn" @click="copyMarkdown" :title="copied ? 'Copied!' : 'Copy Markdown'">
          <svg v-if="!copied" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
          </svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          <span>{{ copied ? 'Copied' : 'Copy' }}</span>
        </button>
        <button class="action-btn" @click="downloadMarkdown" title="Download Markdown">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>Download</span>
        </button>
      </div>
    </div>
    
    <div v-if="markdown" class="rendered" v-html="rendered" />
    
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
      </div>
      <p class="empty-text">No output yet</p>
      <span class="empty-hint">The generated report section will appear here after generation.</span>
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
.preview-panel { 
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-surface);
}

.preview-header { 
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-3) var(--sp-4);
  border-bottom: 1px solid var(--border-1);
  flex-shrink: 0;
}

.panel-title {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header-actions { 
  display: flex;
  gap: var(--sp-2);
}

.action-btn { 
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: var(--sp-1) var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-xs);
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.action-btn:hover { 
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}

.rendered {
  flex: 1;
  overflow-y: auto;
  padding: var(--sp-5);
  color: var(--text-2);
  font-size: var(--text-sm);
  line-height: var(--leading-relaxed);
}

.rendered :deep(h1) { 
  font-size: var(--text-xl);
  color: var(--text-1);
  border-bottom: 1px solid var(--border-1);
  padding-bottom: var(--sp-3);
  margin: 0 0 var(--sp-4);
  font-weight: 700;
}

.rendered :deep(h2) { 
  font-size: var(--text-lg);
  color: var(--text-1);
  margin: var(--sp-6) 0 var(--sp-3);
  font-weight: 600;
}

.rendered :deep(h3) { 
  font-size: var(--text-base);
  color: var(--text-1);
  margin: var(--sp-4) 0 var(--sp-2);
  font-weight: 600;
}

.rendered :deep(p) {
  margin: var(--sp-3) 0;
}

.rendered :deep(strong) { 
  color: var(--text-1);
  font-weight: 600;
}

.rendered :deep(table) { 
  border-collapse: collapse;
  width: 100%;
  margin: var(--sp-4) 0;
}

.rendered :deep(td), 
.rendered :deep(th) { 
  border: 1px solid var(--border-2);
  padding: var(--sp-2) var(--sp-3);
}

.rendered :deep(th) { 
  background: var(--bg-overlay);
  color: var(--text-1);
  font-weight: 600;
  text-align: left;
}

.rendered :deep(blockquote) { 
  border-left: 3px solid var(--brand);
  margin: var(--sp-4) 0;
  padding: var(--sp-3) var(--sp-4);
  color: var(--text-3);
  background: var(--bg-elevated);
  border-radius: 0 var(--r-md) var(--r-md) 0;
}

.rendered :deep(code) { 
  background: var(--bg-overlay);
  padding: 2px var(--sp-2);
  border-radius: var(--r-xs);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
}

.rendered :deep(pre) {
  background: var(--bg-overlay);
  padding: var(--sp-4);
  border-radius: var(--r-md);
  overflow-x: auto;
  margin: var(--sp-4) 0;
}

.rendered :deep(pre code) {
  background: none;
  padding: 0;
}

.rendered :deep(ul),
.rendered :deep(ol) {
  margin: var(--sp-3) 0;
  padding-left: var(--sp-5);
}

.rendered :deep(li) {
  margin: var(--sp-1) 0;
}

.empty-state { 
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  text-align: center;
  padding: var(--sp-8);
}

.empty-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-lg);
  color: var(--text-4);
}

.empty-text {
  color: var(--text-2);
  font-size: var(--text-base);
  font-weight: 500;
  margin: 0;
}

.empty-hint {
  color: var(--text-4);
  font-size: var(--text-sm);
  max-width: 220px;
}
</style>
