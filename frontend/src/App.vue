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

a { 
  color: var(--brand-text); 
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);
}

a:hover { 
  color: var(--brand-hover); 
}

::-webkit-scrollbar { 
  width: 8px; 
  height: 8px; 
}

::-webkit-scrollbar-track { 
  background: transparent; 
}

::-webkit-scrollbar-thumb { 
  background: var(--border-3); 
  border-radius: var(--r-full);
  border: 2px solid transparent;
  background-clip: padding-box;
}

::-webkit-scrollbar-thumb:hover { 
  background: var(--text-4);
  border: 2px solid transparent;
  background-clip: padding-box;
}
</style>

<style scoped>
.app { 
  display: flex; 
  flex-direction: column; 
  min-height: 100vh;
  background: var(--bg-root);
}

.main-content { 
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
