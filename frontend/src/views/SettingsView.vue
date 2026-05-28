<template>
  <div class="settings-view">
    <div class="page-header">
      <h1>Settings</h1>
      <p class="hint">Edit the prompt templates used by AI agents during report generation. Changes take effect immediately on the next run.</p>
    </div>

    <div class="settings-body">
      <aside class="sidebar">
        <div class="sidebar-label">Prompt Templates</div>
        <nav class="prompt-nav">
          <button
            v-for="t in store.templates"
            :key="t.key"
            class="nav-item"
            :class="{ active: selected?.key === t.key, dirty: isDirty(t.key) }"
            @click="selectTemplate(t)"
          >
            <span class="nav-item-name">{{ t.name }}</span>
            <span v-if="isDirty(t.key)" class="dirty-dot" title="Unsaved changes"></span>
          </button>
        </nav>
      </aside>

      <main class="editor-panel">
        <div v-if="store.loading" class="loading-state">
          <span class="spinner"></span>
          <span>Loading prompts…</span>
        </div>

        <template v-else-if="selected">
          <div class="editor-header">
            <div class="editor-title">
              <h2>{{ selected.name }}</h2>
              <p class="description">{{ selected.description }}</p>
            </div>
            <div class="editor-actions">
              <button class="btn-secondary" :disabled="store.saving" @click="onReset">
                Reset to Default
              </button>
              <button
                class="btn-primary"
                :disabled="store.saving || !isDirty(selected.key)"
                @click="onSave"
              >
                <span v-if="store.saving" class="spinner-sm"></span>
                {{ store.saving ? 'Saving…' : 'Save' }}
              </button>
            </div>
          </div>

          <div v-if="toast" class="toast" :class="toast.type">{{ toast.message }}</div>

          <textarea
            class="prompt-textarea"
            v-model="draftBodies[selected.key]"
            spellcheck="false"
            autocomplete="off"
          ></textarea>
        </template>

        <div v-else class="empty-state">
          Select a prompt template from the list.
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { usePromptsStore } from '@/stores/prompts'
import type { PromptTemplate } from '@/api/prompts'

const store = usePromptsStore()
const selected = ref<PromptTemplate | null>(null)
const draftBodies = reactive<Record<string, string>>({})
const toast = ref<{ type: 'success' | 'error'; message: string } | null>(null)

let toastTimer: ReturnType<typeof setTimeout> | null = null

onMounted(async () => {
  await store.fetchAll()
  const first = store.templates[0]
  if (first) selectTemplate(first)
})

watch(
  () => store.templates,
  (templates) => {
    for (const t of templates) {
      if (!(t.key in draftBodies)) {
        draftBodies[t.key] = t.body
      }
    }
  },
  { immediate: true },
)

function selectTemplate(t: PromptTemplate) {
  selected.value = t
  if (!(t.key in draftBodies)) {
    draftBodies[t.key] = t.body
  }
}

function isDirty(key: string): boolean {
  const original = store.templates.find(t => t.key === key)
  return !!original && draftBodies[key] !== original.body
}

function showToast(type: 'success' | 'error', message: string) {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { type, message }
  toastTimer = setTimeout(() => (toast.value = null), 3000)
}

async function onSave() {
  if (!selected.value) return
  try {
    const updated = await store.update(selected.value.key, draftBodies[selected.value.key] ?? '')
    if (updated) draftBodies[selected.value.key] = updated.body
    showToast('success', 'Prompt saved.')
  } catch {
    showToast('error', 'Failed to save. Please try again.')
  }
}

async function onReset() {
  if (!selected.value) return
  if (!confirm('Reset this prompt to its original default? This cannot be undone.')) return
  try {
    const updated = await store.reset(selected.value.key)
    if (updated) draftBodies[selected.value.key] = updated.body
    showToast('success', 'Prompt reset to default.')
  } catch {
    showToast('error', 'Failed to reset. Please try again.')
  }
}
</script>

<style scoped>
.settings-view {
  padding: var(--sp-8);
  max-width: 1100px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
}

.page-header {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

h1 {
  margin: 0;
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.hint {
  color: var(--text-3);
  font-size: var(--text-sm);
  margin: 0;
  line-height: var(--leading-relaxed);
}

.settings-body {
  display: flex;
  gap: var(--sp-6);
  min-height: 520px;
}

/* Sidebar */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.sidebar-label {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--text-4);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0 var(--sp-2);
}

.prompt-nav {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
}

.nav-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-2);
  width: 100%;
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--r-md);
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-3);
  font-size: var(--text-sm);
  font-family: var(--font);
  cursor: pointer;
  text-align: left;
  transition: all var(--duration-fast) var(--ease-out);
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-1);
}

.nav-item.active {
  background: var(--bg-overlay);
  border-color: var(--border-2);
  color: var(--text-1);
  font-weight: 500;
}

.nav-item-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dirty-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--brand);
  flex-shrink: 0;
}

/* Editor panel */
.editor-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  min-width: 0;
}

.editor-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
}

.editor-title {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
}

h2 {
  margin: 0;
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-1);
}

.description {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--text-3);
  line-height: var(--leading-relaxed);
}

.editor-actions {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  flex-shrink: 0;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-2) var(--sp-4);
  background: var(--brand);
  color: #fff;
  border: none;
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-family: var(--font);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-primary:hover:not(:disabled) {
  background: var(--brand-hover);
}

.btn-primary:disabled {
  opacity: 0.45;
  cursor: default;
}

.btn-secondary {
  padding: var(--sp-2) var(--sp-4);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-secondary:hover:not(:disabled) {
  border-color: var(--border-3);
  color: var(--text-1);
  background: var(--bg-hover);
}

.btn-secondary:disabled {
  opacity: 0.45;
  cursor: default;
}

.prompt-textarea {
  flex: 1;
  width: 100%;
  min-height: 400px;
  padding: var(--sp-4);
  background: var(--bg-overlay);
  border: 1px solid var(--border-2);
  border-radius: var(--r-lg);
  color: var(--text-1);
  font-size: var(--text-sm);
  font-family: 'SF Mono', 'Fira Code', 'Menlo', monospace;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: border-color var(--duration-fast) var(--ease-out);
  box-sizing: border-box;
}

.prompt-textarea:focus {
  border-color: var(--brand);
}

.toast {
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-weight: 500;
}

.toast.success {
  background: color-mix(in srgb, #22c55e 12%, transparent);
  border: 1px solid color-mix(in srgb, #22c55e 30%, transparent);
  color: #4ade80;
}

.toast.error {
  background: color-mix(in srgb, #ef4444 12%, transparent);
  border: 1px solid color-mix(in srgb, #ef4444 30%, transparent);
  color: #f87171;
}

.loading-state {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  color: var(--text-3);
  font-size: var(--text-sm);
  padding: var(--sp-8) 0;
}

.empty-state {
  color: var(--text-4);
  font-size: var(--text-sm);
  padding: var(--sp-8) 0;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-2);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

.spinner-sm {
  display: inline-block;
  width: 12px;
  height: 12px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
