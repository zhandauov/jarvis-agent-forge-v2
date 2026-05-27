<template>
  <header class="app-header">
    <div class="header-left">
      <div class="brand" @click="$router.push('/')">
        <div class="brand-logo">
          <span class="brand-dot"></span>
        </div>
        <span class="brand-name">Jarvis</span>
      </div>
      <nav class="breadcrumb" v-if="crumbs.length">
        <span class="breadcrumb-sep">/</span>
        <span v-for="(crumb, i) in crumbs" :key="i" class="breadcrumb-item">
          <router-link v-if="crumb.to" :to="crumb.to" class="breadcrumb-link">{{ crumb.label }}</router-link>
          <span v-else class="breadcrumb-current">{{ crumb.label }}</span>
          <span v-if="i < crumbs.length - 1" class="breadcrumb-sep">/</span>
        </span>
      </nav>
    </div>
    <div class="header-right">
      <button v-if="auth.isAuthenticated" class="logout-btn" @click="auth.logout()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
          <polyline points="16 17 21 12 16 7"/>
          <line x1="21" y1="12" x2="9" y2="12"/>
        </svg>
        <span>Sign out</span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()
const crumbs = computed(() => (route.meta.crumbs as any[] | undefined) ?? [])
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--sp-6);
  height: 56px;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-1);
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(8px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  cursor: pointer;
  user-select: none;
  padding: var(--sp-2) var(--sp-2);
  margin: calc(-1 * var(--sp-2));
  border-radius: var(--r-md);
  transition: background var(--duration-fast) var(--ease-out);
}

.brand:hover {
  background: var(--bg-hover);
}

.brand-logo {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-md);
  border: 1px solid var(--border-2);
}

.brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--brand) 0%, var(--brand-hover) 100%);
  box-shadow: 0 0 12px var(--brand-glow);
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 8px var(--brand-glow); }
  50% { box-shadow: 0 0 16px var(--brand-glow); }
}

.brand-name {
  font-size: var(--text-base);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.breadcrumb {
  display: flex;
  align-items: center;
  font-size: var(--text-sm);
}

.breadcrumb-sep {
  color: var(--text-4);
  margin: 0 var(--sp-2);
}

.breadcrumb-item {
  display: flex;
  align-items: center;
}

.breadcrumb-link {
  color: var(--text-3);
  transition: color var(--duration-fast) var(--ease-out);
}

.breadcrumb-link:hover {
  color: var(--brand-text);
}

.breadcrumb-current {
  color: var(--text-1);
  font-weight: 500;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: var(--sp-2) var(--sp-3);
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-family: var(--font);
  cursor: pointer;
  transition: all var(--duration-fast) var(--ease-out);
}

.logout-btn:hover {
  border-color: var(--border-3);
  color: var(--text-1);
  background: var(--bg-hover);
}

.logout-btn svg {
  opacity: 0.7;
}

.logout-btn:hover svg {
  opacity: 1;
}
</style>
