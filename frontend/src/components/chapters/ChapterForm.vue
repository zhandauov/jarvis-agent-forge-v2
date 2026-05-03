<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <h2>{{ chapter ? 'Edit Chapter' : 'New Chapter' }}</h2>
      <div class="field">
        <label>Title</label>
        <input v-model="form.title" placeholder="Chapter title" />
      </div>
      <div class="field">
        <label>Description</label>
        <textarea v-model="form.description" placeholder="What should this chapter cover?" rows="3" />
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
import type { Chapter } from '@/api/chapters'

const props = defineProps<{ chapter?: Chapter | null }>()
const emit = defineEmits<{ close: []; submit: [{ title: string; description: string }] }>()

const form = reactive({
  title: props.chapter?.title ?? '',
  description: props.chapter?.description ?? '',
})

function submit() {
  if (!form.title.trim()) return
  emit('submit', { title: form.title, description: form.description })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: var(--bg-elevated);
  border: 1px solid var(--border-2);
  border-radius: var(--r-lg);
  padding: 32px;
  width: 460px;
  max-width: 90vw;
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
}

h2 {
  margin: 0 0 var(--sp-6);
  color: var(--text-1);
  font-size: var(--text-xl);
  font-weight: 700;
  letter-spacing: -0.01em;
}

.field {
  margin-bottom: var(--sp-4);
}

label {
  display: block;
  margin-bottom: var(--sp-1);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-2);
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  background: var(--bg-surface);
  border: 1px solid var(--border-2);
  color: var(--text-1);
  padding: 10px var(--sp-3);
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-family: var(--font);
  outline: none;
  resize: vertical;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input::placeholder,
textarea::placeholder {
  color: var(--text-3);
}

input:focus,
textarea:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
  margin-top: var(--sp-6);
}

.btn-primary {
  background: var(--brand);
  color: #fff;
  border: none;
  padding: 10px var(--sp-6);
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  transition: background 0.15s;
}

.btn-primary:hover:not(:disabled) {
  background: var(--brand-dim);
}

.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-secondary {
  background: transparent;
  border: 1px solid var(--border-3);
  color: var(--text-2);
  padding: 10px var(--sp-4);
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-family: var(--font);
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}

.btn-secondary:hover {
  border-color: var(--border-3);
  color: var(--text-1);
}
</style>
