<template>
  <header class="app-header">
    <div class="brand" @click="$router.push('/')">
      <span class="brand-icon">📊</span>
      <span class="brand-name">ConsultAI</span>
    </div>
    <nav class="breadcrumb" v-if="crumbs.length">
      <span v-for="(crumb, i) in crumbs" :key="i">
        <router-link v-if="crumb.to" :to="crumb.to">{{ crumb.label }}</router-link>
        <span v-else class="crumb-current">{{ crumb.label }}</span>
        <span v-if="i < crumbs.length - 1" class="sep">/</span>
      </span>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const crumbs = computed(() => (route.meta.crumbs as any[] | undefined) ?? [])
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 0 24px;
  height: 56px;
  background: #1a1a2e;
  border-bottom: 1px solid #2d2d4e;
  color: #e0e0ff;
}
.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: 700;
  color: #7c6af7;
}
.breadcrumb {
  font-size: 14px;
  color: #888;
}
.breadcrumb a {
  color: #9d8fff;
  text-decoration: none;
}
.breadcrumb a:hover { text-decoration: underline; }
.crumb-current { color: #e0e0ff; }
.sep { margin: 0 6px; color: #555; }
</style>
