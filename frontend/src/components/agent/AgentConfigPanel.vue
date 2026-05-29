<template>
  <div class="config-panel">
    <div class="panel-header">
      <span class="panel-title">Agent Team</span>
    </div>
    
    <div class="config-form">
      <div class="field">
        <label>Model</label>
        <select v-model="form.model" class="select">
          <option value="claude-sonnet-4-6">Claude Sonnet 4.6 (balanced)</option>
          <option value="claude-opus-4-6">Claude Opus 4.6 (most capable)</option>
          <option value="claude-haiku-4-5-20251001">Claude Haiku 4.5 (fastest)</option>
        </select>
      </div>

      <div class="field">
        <label>Supervisor Prompt</label>
        <textarea v-model="form.supervisor_prompt" rows="4" placeholder="System prompt for the supervisor agent..." class="textarea" />
      </div>

      <div class="field">
        <label>Worker Prompt</label>
        <textarea v-model="form.worker_prompt" rows="3" placeholder="Base system prompt for worker agents..." class="textarea" />
      </div>

      <div class="field">
        <label>Worker Roles</label>
        <div class="roles-list">
          <div v-for="(role, i) in form.worker_roles" :key="i" class="role-row">
            <input v-model="form.worker_roles[i]" placeholder="Role name" class="input" />
            <button class="btn-remove" @click="removeRole(i)" title="Remove">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>
        <button class="btn-add-role" @click="addRole">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          <span>Add Role</span>
        </button>
      </div>

      <div class="row-fields">
        <div class="field field-small">
          <label>Max Rounds</label>
          <input type="number" v-model.number="form.max_rounds" min="1" max="10" class="input" />
        </div>
      </div>

      <div class="field">
        <label class="toggle-label">
          <span class="toggle-track" :class="{ active: form.internet_access }">
            <span class="toggle-thumb"></span>
          </span>
          <input type="checkbox" v-model="form.internet_access" class="toggle-input" />
          <div class="toggle-text">
            <span class="toggle-name">Internet Access</span>
            <span class="toggle-hint">Workers can search the web and follow links</span>
          </div>
        </label>
      </div>

      <div class="field">
        <label>Aggregate Prompt <span class="label-hint">(override)</span></label>
        <textarea
          v-model="form.aggregate_prompt"
          rows="3"
          placeholder="Leave empty to use the global default from Settings → Aggregation Prompt"
          class="textarea"
        />
      </div>

      <div class="field">
        <label>PPTX Slide Prompt <span class="label-hint">(override)</span></label>
        <textarea
          v-model="form.pptx_aggregate_prompt"
          rows="3"
          placeholder="Leave empty to use the global default from Settings → Slide Aggregation Prompt"
          class="textarea"
        />
      </div>
    </div>

    <SlideConfigSection
      :chapter-id="chapterId"
      :initial-config="slideConfig"
      @saved="onSlideConfigSaved"
    />

    <div class="panel-footer">
      <button class="btn-save" :disabled="saving" @click="save">
        <span v-if="saving" class="spinner"></span>
        <span>{{ saving ? 'Saving...' : 'Save Config' }}</span>
      </button>
      
      <button
        v-if="!generating"
        class="btn-generate"
        :disabled="!configSaved"
        @click="$emit('generate')"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polygon points="5 3 19 12 5 21 5 3"/>
        </svg>
        <span>Generate</span>
      </button>
      
      <button
        v-else
        class="btn-stop"
        @click="$emit('stop')"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="6" y="6" width="12" height="12"/>
        </svg>
        <span>Stop</span>
      </button>

      <p v-if="!configSaved" class="hint">Save config before generating.</p>
      <p v-if="saveError" class="error">{{ saveError }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { agentConfigsApi, type AgentConfigUpsert } from '@/api/agentConfigs'
import { SUPERVISOR_DEFAULT, WORKER_DEFAULT } from '@/constants/prompts'
import type { SlideConfig } from '@/api/slideConfigs'
import SlideConfigSection from './SlideConfigSection.vue'

const props = defineProps<{
  chapterId: number
  initialConfig?: { supervisor_prompt: string; worker_prompt: string; worker_roles: string[]; max_rounds: number; model?: string; internet_access?: boolean; aggregate_prompt?: string | null; pptx_aggregate_prompt?: string | null } | null
  slideConfig: SlideConfig | null
  generating: boolean
}>()

const emit = defineEmits<{ generate: []; saved: []; stop: []; 'slide-config-saved': [config: SlideConfig] }>()

const form = reactive<AgentConfigUpsert>({
  supervisor_prompt: props.initialConfig?.supervisor_prompt ?? SUPERVISOR_DEFAULT,
  worker_prompt: props.initialConfig?.worker_prompt ?? WORKER_DEFAULT,
  worker_roles: props.initialConfig?.worker_roles ?? ['Data Analyst', 'Market Researcher', 'Report Writer'],
  worker_count: props.initialConfig?.worker_roles?.length ?? 3,
  max_rounds: props.initialConfig?.max_rounds ?? 4,
  model: props.initialConfig?.model ?? 'claude-sonnet-4-6',
  internet_access: props.initialConfig?.internet_access ?? false,
  aggregate_prompt: props.initialConfig?.aggregate_prompt ?? null,
  pptx_aggregate_prompt: props.initialConfig?.pptx_aggregate_prompt ?? null,
})

function onSlideConfigSaved(config: SlideConfig) {
  emit('slide-config-saved', config)
}

const saving = ref(false)
const configSaved = ref(!!props.initialConfig)
const saveError = ref('')

function addRole() {
  form.worker_roles.push('')
}

function removeRole(i: number) {
  form.worker_roles.splice(i, 1)
  form.worker_count = form.worker_roles.length
}

async function save() {
  saving.value = true
  saveError.value = ''
  try {
    form.worker_count = form.worker_roles.filter(r => r.trim()).length
    await agentConfigsApi.upsert(props.chapterId, { ...form, worker_roles: form.worker_roles.filter(r => r.trim()) })
    configSaved.value = true
    emit('saved')
  } catch (e: any) {
    saveError.value = e?.response?.data?.detail ?? 'Save failed'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.config-panel { 
  display: flex; 
  flex-direction: column;
  height: 100%;
  background: var(--bg-surface);
}

.panel-header {
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

.config-form {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  padding: var(--sp-4);
  overflow-y: auto;
  flex: 1;
}

.field { 
  display: flex; 
  flex-direction: column; 
  gap: var(--sp-2);
}

label { 
  font-size: var(--text-xs);
  font-weight: 500;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.textarea, .input, .select {
  background: var(--bg-elevated);
  border: 1px solid var(--border-2);
  color: var(--text-1);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-family: var(--font);
  outline: none;
  resize: vertical;
  transition: border-color var(--duration-fast) var(--ease-out);
}

.select { 
  resize: none; 
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' viewBox='0 0 16 16'%3E%3Cpath fill='%236b6b80' d='M4 6l4 4 4-4'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--sp-2) center;
  padding-right: var(--sp-6);
}

.textarea:hover:not(:focus), 
.input:hover:not(:focus), 
.select:hover:not(:focus) {
  border-color: var(--border-3);
}

.textarea:focus, .input:focus, .select:focus { 
  border-color: var(--brand);
  box-shadow: 0 0 0 2px var(--brand-soft);
}

.roles-list { 
  display: flex; 
  flex-direction: column; 
  gap: var(--sp-2);
}

.role-row { 
  display: flex; 
  gap: var(--sp-2);
}

.role-row .input { 
  flex: 1;
}

.btn-remove { 
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: 1px solid var(--border-2);
  border-radius: var(--r-md);
  color: var(--text-4);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
  flex-shrink: 0;
}

.btn-remove:hover { 
  color: var(--error);
  border-color: var(--error);
  background: var(--error-soft);
}

.btn-add-role { 
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px dashed var(--border-2);
  color: var(--text-3);
  padding: var(--sp-2);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-add-role:hover { 
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}

.row-fields { 
  display: flex; 
  gap: var(--sp-3);
}

.field-small .input { 
  width: 80px;
}

.panel-footer { 
  display: flex; 
  flex-direction: column; 
  gap: var(--sp-2);
  padding: var(--sp-4);
  border-top: 1px solid var(--border-1);
  background: var(--bg-surface);
}

.btn-save { 
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--brand);
  color: var(--brand-text);
  padding: var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-save:hover:not(:disabled) { 
  background: var(--brand-soft);
}

.btn-save:disabled { 
  opacity: 0.5; 
  cursor: not-allowed;
}

.btn-generate { 
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  background: var(--brand);
  color: white;
  border: none;
  padding: var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 600;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-generate:hover:not(:disabled) { 
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}

.btn-generate:disabled { 
  opacity: 0.5; 
  cursor: not-allowed;
}

.btn-stop { 
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  background: var(--error);
  color: white;
  border: none;
  padding: var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-sm);
  font-weight: 600;
  font-family: var(--font);
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-stop:hover { 
  background: #ef4444;
}

.hint { 
  color: var(--text-4);
  font-size: var(--text-xs);
  margin: 0;
  text-align: center;
}

.error { 
  color: var(--error);
  font-size: var(--text-xs);
  margin: 0;
  text-align: center;
}

.toggle-label { 
  display: flex;
  align-items: flex-start;
  gap: var(--sp-3);
  cursor: pointer;
  user-select: none;
}

.toggle-input { 
  display: none;
}

.toggle-track { 
  position: relative;
  width: 36px;
  height: 20px;
  background: var(--border-3);
  border-radius: var(--r-full);
  flex-shrink: 0;
  transition: background var(--duration-fast) var(--ease-out);
}

.toggle-track.active { 
  background: var(--brand);
}

.toggle-thumb { 
  position: absolute;
  top: 2px;
  left: 2px;
  width: 16px;
  height: 16px;
  background: #fff;
  border-radius: 50%;
  transition: left var(--duration-fast) var(--ease-out);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.toggle-track.active .toggle-thumb { 
  left: 18px;
}

.toggle-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.toggle-name {
  font-size: var(--text-sm);
  color: var(--text-1);
  font-weight: 500;
}

.toggle-hint {
  color: var(--text-4);
  font-size: var(--text-xs);
  text-transform: none;
  letter-spacing: 0;
}

.label-hint {
  font-weight: 400;
  color: var(--text-4);
  text-transform: none;
  letter-spacing: 0;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(139, 124, 246, 0.3);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
