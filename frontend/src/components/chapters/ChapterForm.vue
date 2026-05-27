<template>
  <Teleport to="body">
    <div class="modal-overlay" @click.self="$emit('close')">
      <div class="modal">
        <div class="modal-header">
          <h2>{{ chapter ? 'Edit Chapter' : 'Create New Chapter' }}</h2>
          <button class="close-btn" @click="$emit('close')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submit" class="modal-form">
          <div class="field">
            <label for="title">Title</label>
            <input 
              id="title"
              v-model="form.title" 
              placeholder="Enter chapter title" 
              autocomplete="off"
            />
          </div>
          
          <div class="field">
            <label for="description">Description</label>
            <textarea 
              id="description"
              v-model="form.description" 
              placeholder="What should this chapter cover?" 
              rows="3" 
            />
          </div>
          
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="$emit('close')">Cancel</button>
            <button type="submit" class="btn-submit" :disabled="!form.title.trim()">
              {{ chapter ? 'Save Changes' : 'Create Chapter' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
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
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: var(--sp-6);
  animation: fade-in 0.15s var(--ease-out);
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal {
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-xl);
  width: 100%;
  max-width: 480px;
  box-shadow: var(--shadow-xl);
  animation: slide-up 0.2s var(--ease-out);
}

@keyframes slide-up {
  from { 
    opacity: 0;
    transform: translateY(8px) scale(0.98);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-5) var(--sp-6);
  border-bottom: 1px solid var(--border-1);
}

h2 {
  margin: 0;
  color: var(--text-1);
  font-size: var(--text-lg);
  font-weight: 600;
  letter-spacing: -0.01em;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background: transparent;
  border: none;
  border-radius: var(--r-md);
  color: var(--text-3);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.close-btn:hover {
  background: var(--bg-hover);
  color: var(--text-1);
}

.modal-form {
  padding: var(--sp-6);
  display: flex;
  flex-direction: column;
  gap: var(--sp-5);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--sp-2);
}

label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-2);
}

input,
textarea {
  width: 100%;
  background: var(--bg-elevated);
  border: 1px solid var(--border-2);
  color: var(--text-1);
  padding: var(--sp-3) var(--sp-4);
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-family: var(--font);
  outline: none;
  resize: vertical;
  transition: border-color var(--duration-fast) var(--ease-out), 
              box-shadow var(--duration-fast) var(--ease-out);
}

input::placeholder,
textarea::placeholder {
  color: var(--text-4);
}

input:hover:not(:focus),
textarea:hover:not(:focus) {
  border-color: var(--border-3);
}

input:focus,
textarea:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
  padding-top: var(--sp-2);
}

.btn-cancel {
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-2);
  padding: var(--sp-3) var(--sp-5);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-cancel:hover {
  border-color: var(--border-3);
  color: var(--text-1);
  background: var(--bg-hover);
}

.btn-submit {
  background: var(--brand);
  color: #fff;
  border: none;
  padding: var(--sp-3) var(--sp-5);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.btn-submit:hover:not(:disabled) {
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
