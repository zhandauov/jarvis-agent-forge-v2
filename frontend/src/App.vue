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
  background: #0f0f1e;
  color: #e0e0ff;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}

a { color: #9d8fff; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #14142a; }
::-webkit-scrollbar-thumb { background: #3d3d5e; border-radius: 3px; }
</style>

<style scoped>
.app { display: flex; flex-direction: column; min-height: 100vh; }
.main-content { flex: 1; }
</style>
