import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'login', component: () => import('@/views/LoginView.vue') },
    { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
    { path: '/reports/:id', name: 'report', component: () => import('@/views/ReportDetailView.vue') },
    {
      path: '/reports/:reportId/chapters/:chapterId',
      name: 'chapter',
      component: () => import('@/views/ChapterWorkspaceView.vue'),
    },
    { path: '/reports/:id/kb', name: 'kb', component: () => import('@/views/KnowledgeBaseView.vue') },
  ],
})

router.beforeEach((to) => {
  if (to.name === 'login') return

  const token = localStorage.getItem('auth_token')
  if (!token) return { name: 'login' }

  try {
    const payload = JSON.parse(atob(token.split('.')[1] ?? ''))
    if (payload.exp && payload.exp * 1000 < Date.now()) {
      localStorage.removeItem('auth_token')
      return { name: 'login' }
    }
  } catch {
    localStorage.removeItem('auth_token')
    return { name: 'login' }
  }
})

export default router
