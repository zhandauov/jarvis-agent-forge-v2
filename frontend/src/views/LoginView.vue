<template>
  <div class="login-wrapper">
    <form class="login-card" @submit.prevent="submit">
      <div class="logo-area">
        <span class="logo-dot"></span>
        <h1>Jarvis</h1>
      </div>
      <p class="subtitle">Consulting Platform</p>

      <div class="field">
        <label>Логин</label>
        <input v-model="username" type="text" autocomplete="username" placeholder="username" required />
      </div>
      <div class="field">
        <label>Пароль</label>
        <input v-model="password" type="password" autocomplete="current-password" placeholder="••••••••" required />
      </div>

      <p v-if="error" class="error">{{ error }}</p>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Вход...' : 'Войти' }}
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
    error.value = 'Неверный логин или пароль'
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
  background-image: radial-gradient(ellipse 80% 50% at 50% -10%, rgba(124, 106, 247, 0.18) 0%, transparent 60%);
}

.login-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-2);
  border-radius: var(--r-xl);
  padding: 48px;
  width: 400px;
  max-width: calc(100vw - 48px);
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  box-shadow: 0 24px 64px rgba(0, 0, 0, 0.5);
}

.logo-area {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  margin-bottom: var(--sp-1);
}

.logo-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--brand);
  box-shadow: 0 0 10px var(--brand);
  flex-shrink: 0;
}

h1 {
  font-size: var(--text-3xl);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.subtitle {
  color: var(--text-3);
  font-size: var(--text-sm);
  margin-top: calc(-1 * var(--sp-3));
  margin-bottom: var(--sp-2);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
}

label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-2);
}

input {
  padding: 10px var(--sp-3);
  background: var(--bg-elevated);
  border: 1px solid var(--border-2);
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-family: var(--font);
  color: var(--text-1);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}

input::placeholder {
  color: var(--text-3);
}

input:focus {
  border-color: var(--brand);
  box-shadow: 0 0 0 3px var(--brand-soft);
}

button[type="submit"] {
  margin-top: var(--sp-2);
  padding: 12px;
  background: var(--brand);
  color: #fff;
  border: none;
  border-radius: var(--r-md);
  font-size: var(--text-base);
  font-weight: 600;
  font-family: var(--font);
  cursor: pointer;
  transition: background 0.15s, box-shadow 0.15s;
}

button[type="submit"]:hover:not(:disabled) {
  background: var(--brand-dim);
  box-shadow: 0 4px 16px rgba(124, 106, 247, 0.35);
}

button[type="submit"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error {
  color: var(--error);
  font-size: var(--text-sm);
  margin: 0;
}
</style>
