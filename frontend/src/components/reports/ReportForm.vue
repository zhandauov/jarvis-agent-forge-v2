<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ report ? 'Edit Report' : 'New Report' }}</h2>
      <div class="field">
        <label>Title</label>
        <input v-model="form.title" placeholder="Report title" />
      </div>
      <div class="field">
        <label>Description</label>
        <textarea v-model="form.description" placeholder="Brief description..." rows="3" />
      </div>
      <div class="actions">
        <button class="btn-secondary" @click="$emit('close')">Cancel</button>
        <button class="btn-primary" :disabled="!form.title.trim()" @click="submit">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { Report } from '@/api/reports'

const props = defineProps<{ report?: Report | null }>()
const emit = defineEmits<{ close: []; submit: [{ title: string; description: string }] }>()

const form = reactive({
  title: props.report?.title ?? '',
  description: props.report?.description ?? '',
})

function submit() {
  if (!form.title.trim()) return
  emit('submit', { title: form.title, description: form.description })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: #1e1e3a; border: 1px solid #3d3d5e; border-radius: 12px;
  padding: 32px; width: 460px; max-width: 90vw;
}
h2 { margin: 0 0 24px; color: #e0e0ff; }
.field { margin-bottom: 16px; }
label { display: block; margin-bottom: 6px; font-size: 13px; color: #888; }
input, textarea {
  width: 100%; box-sizing: border-box;
  background: #14142a; border: 1px solid #3d3d5e;
  color: #e0e0ff; padding: 10px 12px; border-radius: 6px; font-size: 14px;
  outline: none; resize: vertical;
}
input:focus, textarea:focus { border-color: #7c6af7; }
.actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; }
.btn-primary { background: #7c6af7; color: white; border: none; padding: 10px 24px; border-radius: 6px; cursor: pointer; }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn-secondary { background: transparent; border: 1px solid #3d3d5e; color: #aaa; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
</style>
