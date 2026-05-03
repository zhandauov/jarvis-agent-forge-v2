<template>
  <header class="app-header">
    <div class="left">
      <div class="brand" @click="$router.push('/')">
        <span class="brand-dot"></span>
        <span class="brand-name">Jarvis</span>
      </div>
      <nav class="breadcrumb" v-if="crumbs.length">
        <span v-for="(crumb, i) in crumbs" :key="i">
          <router-link v-if="crumb.to" :to="crumb.to">{{ crumb.label }}</router-link>
          <span v-else class="crumb-current">{{ crumb.label }}</span>
          <span v-if="i < crumbs.length - 1" class="sep">/</span>
        </span>
      </nav>
    </div>
    <button v-if="auth.isAuthenticated" class="logout-btn" @click="auth.logout()">
      Sign out
    </button>
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
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border-1);
  position: sticky;
  top: 0;
  z-index: 50;
}

.left {
  display: flex;
  align-items: center;
  gap: var(--sp-6);
}

.brand {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  cursor: pointer;
  user-select: none;
}

.brand-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand);
  box-shadow: 0 0 8px var(--brand);
  flex-shrink: 0;
}

.brand-name {
  font-size: var(--text-base);
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.01em;
}

.breadcrumb {
  font-size: var(--text-sm);
  color: var(--text-3);
}

.breadcrumb a {
  color: var(--text-2);
}

.breadcrumb a:hover {
  color: var(--brand-text);
}

.crumb-current {
  color: var(--text-1);
}

.sep {
  margin: 0 var(--sp-2);
  color: var(--border-3);
}

.logout-btn {
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: 6px 14px;
  border-radius: var(--r-md);
  font-size: var(--text-sm);
  font-family: var(--font);
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}

.logout-btn:hover {
  border-color: var(--border-3);
  color: var(--text-2);
}
</style>
