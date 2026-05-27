<template>
  <div class="login-wrapper">
    <div class="login-bg-gradient"></div>
    <form class="login-card" @submit.prevent="submit">
      <div class="logo-area">
        <div class="logo-container">
          <span class="logo-dot"></span>
        </div>
        <div class="logo-text">
          <h1>Jarvis</h1>
          <p class="subtitle">Consulting Platform</p>
        </div>
      </div>

      <div class="form-fields">
        <div class="field">
          <label for="username">Login</label>
          <input 
            id="username"
            v-model="username" 
            type="text" 
            autocomplete="username" 
            placeholder="Enter your username" 
            required 
          />
        </div>
        <div class="field">
          <label for="password">Password</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            autocomplete="current-password" 
            placeholder="Enter your password" 
            required 
          />
        </div>
      </div>

      <div v-if="error" class="error-message">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
        <span>{{ error }}</span>
      </div>

      <button type="submit" class="submit-btn" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        <span>{{ loading ? 'Signing in...' : 'Sign in' }}</span>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch {
    error.value = 'Invalid login or password'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-root);
  padding: var(--sp-6);
  position: relative;
  overflow: hidden;
}

.login-bg-gradient {
  position: absolute;
  inset: 0;
  background: 
    radial-gradient(ellipse 60% 40% at 50% 0%, var(--brand-glow) 0%, transparent 50%),
    radial-gradient(ellipse 40% 30% at 80% 80%, rgba(96, 165, 250, 0.08) 0%, transparent 50%);
  pointer-events: none;
}

.login-card {
  position: relative;
  background: var(--bg-surface);
  border: 1px solid var(--border-1);
  border-radius: var(--r-2xl);
  padding: var(--sp-10);
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: var(--sp-6);
  box-shadow: var(--shadow-xl), 0 0 80px -20px var(--brand-glow);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  margin-bottom: var(--sp-2);
}

.logo-container {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-lg);
  border: 1px solid var(--border-2);
}

.logo-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-hover) 100%);
  box-shadow: 0 0 20px var(--brand-glow);
}

.logo-text {
  display: flex;
  flex-direction: column;
}

h1 {
  font-size: var(--text-2xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
  margin: 0;
  line-height: 1.2;
}

.subtitle {
  color: var(--text-3);
  font-size: var(--text-sm);
  margin: 0;
}

.form-fields {
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
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

input {
  padding: var(--sp-3) var(--sp-4);
  background: var(--bg-elevated);
  border: 1px solid var(--border-2);
  border-radius: var(--r-lg);
  font-size: var(--text-base);
  font-family: var(--font);
  color: var(--text-1);
  outline: none;
  transition: border-color var(--duration-fast) var(--ease-out), 
              box-shadow var(--duration-fast) var(--ease-out);
}

input::placeholder {
  color: var(--text-4);
}

input:hover:not(:focus) {
  border-color: var(--border-3);
}

input:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

.error-message {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  padding: var(--sp-3) var(--sp-4);
  background: var(--error-soft);
  border: 1px solid rgba(248, 113, 113, 0.2);
  border-radius: var(--r-md);
  color: var(--error);
  font-size: var(--text-sm);
}

.error-message svg {
  flex-shrink: 0;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  margin-top: var(--sp-2);
  padding: var(--sp-3) var(--sp-4);
  background: var(--brand);
  color: #fff;
  border: none;
  border-radius: var(--r-lg);
  font-size: var(--text-base);
  font-weight: 600;
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.submit-btn:hover:not(:disabled) {
  background: var(--brand-hover);
  box-shadow: var(--shadow-glow);
}

.submit-btn:active:not(:disabled) {
  background: var(--brand-dim);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
