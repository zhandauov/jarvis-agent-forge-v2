import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ReportDetailView from '@/views/ReportDetailView.vue'
import ChapterWorkspaceView from '@/views/ChapterWorkspaceView.vue'
import KnowledgeBaseView from '@/views/KnowledgeBaseView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/reports/:id', name: 'report', component: ReportDetailView },
    {
      path: '/reports/:reportId/chapters/:chapterId',
      name: 'chapter',
      component: ChapterWorkspaceView,
    },
    { path: '/reports/:id/kb', name: 'kb', component: KnowledgeBaseView },
  ],
})

export default router
