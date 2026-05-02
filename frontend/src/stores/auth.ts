import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('auth_token'))

  const isAuthenticated = computed(() => !!token.value)

  async function login(username: string, password: string): Promise<void> {
    const res = await axios.post('/api/auth/login', { username, password })
    token.value = res.data.access_token
    localStorage.setItem('auth_token', token.value!)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('auth_token')
    window.location.href = '/login'
  }

  return { token, isAuthenticated, login, logout }
})
