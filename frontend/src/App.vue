<template>
  <div class="app">
    <AppHeader />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
</script>

<style>
*, *::before, *::after { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg-root);
  color: var(--text-1);
  font-family: var(--font);
  -webkit-font-smoothing: antialiased;
}

a { color: var(--brand-text); text-decoration: none; }
a:hover { color: var(--brand); }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-surface); }
::-webkit-scrollbar-thumb { background: var(--border-3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--brand-dim); }
</style>

<style scoped>
.app { display: flex; flex-direction: column; min-height: 100vh; }
.main-content { flex: 1; }
</style>
