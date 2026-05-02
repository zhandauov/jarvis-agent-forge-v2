<template>
  <div class="config-panel">
    <h3>Agent Team</h3>

    <div class="field">
      <label>Model</label>
      <select v-model="form.model">
        <option value="claude-opus-4-7">Claude Opus 4.7 (most capable)</option>
        <option value="claude-sonnet-4-6">Claude Sonnet 4.6 (balanced)</option>
        <option value="claude-haiku-4-5-20251001">Claude Haiku 4.5 (fastest)</option>
      </select>
    </div>

    <div class="field">
      <label>Supervisor Prompt</label>
      <textarea v-model="form.supervisor_prompt" rows="5" placeholder="System prompt for the supervisor agent..." />
    </div>

    <div class="field">
      <label>Worker Prompt</label>
      <textarea v-model="form.worker_prompt" rows="3" placeholder="Base system prompt for worker agents..." />
    </div>

    <div class="field">
      <label>Worker Roles</label>
      <div class="roles-list">
        <div v-for="(role, i) in form.worker_roles" :key="i" class="role-row">
          <input v-model="form.worker_roles[i]" placeholder="Role name" />
          <button class="btn-remove" @click="removeRole(i)">✕</button>
        </div>
      </div>
      <button class="btn-add-role" @click="addRole">+ Add Role</button>
    </div>

    <div class="row-fields">
      <div class="field small">
        <label>Max Rounds</label>
        <input type="number" v-model.number="form.max_rounds" min="1" max="10" />
      </div>
    </div>

    <div class="field">
      <label class="toggle-label">
        <span class="toggle-track" :class="{ active: form.internet_access }">
          <span class="toggle-thumb" />
        </span>
        <input type="checkbox" v-model="form.internet_access" class="toggle-input" />
        Internet Access
        <span class="toggle-hint">Workers can search the web and follow links</span>
      </label>
    </div>

    <div class="panel-actions">
      <button class="btn-save" :disabled="saving" @click="save">
        {{ saving ? 'Saving...' : 'Save Config' }}
      </button>
      <button
        v-if="!generating"
        class="btn-generate"
        :disabled="!configSaved"
        @click="$emit('generate')"
      >
        ▶ Generate
      </button>
      <button
        v-else
        class="btn-stop"
        @click="$emit('stop')"
      >
        ■ Stop
      </button>
    </div>

    <p v-if="!configSaved" class="hint">Save config before generating.</p>
    <p v-if="saveError" class="error">{{ saveError }}</p>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { agentConfigsApi, type AgentConfigUpsert } from '@/api/agentConfigs'
import { SUPERVISOR_DEFAULT, WORKER_DEFAULT } from '@/constants/prompts'

const props = defineProps<{
  chapterId: number
  initialConfig?: { supervisor_prompt: string; worker_prompt: string; worker_roles: string[]; max_rounds: number; model?: string; internet_access?: boolean } | null
  generating: boolean
}>()

const emit = defineEmits<{ generate: []; saved: []; stop: [] }>()

const form = reactive<AgentConfigUpsert>({
  supervisor_prompt: props.initialConfig?.supervisor_prompt ?? SUPERVISOR_DEFAULT,
  worker_prompt: props.initialConfig?.worker_prompt ?? WORKER_DEFAULT,
  worker_roles: props.initialConfig?.worker_roles ?? ['Data Analyst', 'Market Researcher', 'Report Writer'],
  worker_count: props.initialConfig?.worker_roles?.length ?? 3,
  max_rounds: props.initialConfig?.max_rounds ?? 4,
  model: props.initialConfig?.model ?? 'claude-opus-4-7',
  internet_access: props.initialConfig?.internet_access ?? false,
})

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
.config-panel { display: flex; flex-direction: column; gap: 16px; padding: 16px; overflow-y: auto; height: 100%; box-sizing: border-box; }
h3 { margin: 0; color: #e0e0ff; font-size: 16px; }
.field { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; }
textarea, input[type="text"], input[type="number"], select {
  background: #14142a; border: 1px solid #3d3d5e; color: #e0e0ff;
  padding: 8px 10px; border-radius: 6px; font-size: 13px; outline: none; resize: vertical;
}
select { resize: none; cursor: pointer; }
textarea:focus, input:focus, select:focus { border-color: #7c6af7; }
.roles-list { display: flex; flex-direction: column; gap: 6px; }
.role-row { display: flex; gap: 6px; }
.role-row input { flex: 1; }
.btn-remove { background: transparent; border: none; color: #666; cursor: pointer; font-size: 16px; }
.btn-remove:hover { color: #e74c3c; }
.btn-add-role { background: transparent; border: 1px dashed #3d3d5e; color: #888; padding: 6px; border-radius: 6px; cursor: pointer; font-size: 13px; }
.btn-add-role:hover { border-color: #7c6af7; color: #9d8fff; }
.row-fields { display: flex; gap: 12px; }
.small input { width: 80px; }
.panel-actions { display: flex; flex-direction: column; gap: 8px; margin-top: auto; }
.btn-save { background: transparent; border: 1px solid #7c6af7; color: #9d8fff; padding: 10px; border-radius: 6px; cursor: pointer; }
.btn-save:hover { background: #2d2d5e; }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-generate { background: #7c6af7; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600; }
.btn-generate:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-stop { background: #c0392b; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 600; }
.btn-stop:hover { background: #e74c3c; }
.hint { color: #666; font-size: 12px; margin: 0; }
.error { color: #e74c3c; font-size: 13px; margin: 0; }
.toggle-label { display: flex; align-items: center; gap: 10px; cursor: pointer; font-size: 13px; color: #e0e0ff; user-select: none; }
.toggle-input { display: none; }
.toggle-track { position: relative; width: 36px; height: 20px; background: #3d3d5e; border-radius: 10px; flex-shrink: 0; transition: background 0.2s; }
.toggle-track.active { background: #7c6af7; }
.toggle-thumb { position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; background: #fff; border-radius: 50%; transition: left 0.2s; }
.toggle-track.active .toggle-thumb { left: 18px; }
.toggle-hint { color: #666; font-size: 11px; margin-left: 2px; }
</style>
