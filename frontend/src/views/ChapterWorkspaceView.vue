<template>
  <div class="workspace">
    <div class="workspace-header">
      <div class="header-left">
        <router-link :to="`/reports/${reportId}`" class="back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"/>
            <polyline points="12 19 5 12 12 5"/>
          </svg>
          <span>Report</span>
        </router-link>
        <span class="header-divider"></span>
        <h2>{{ chapter?.title ?? 'Loading...' }}</h2>
      </div>
      <GenerationStatus :status="genStore.runStatus" />
    </div>

    <div v-if="chapter" class="workspace-body">
      <!-- Chapters nav -->
      <div class="panel panel-chapters">
        <div class="panel-header">
          <span class="panel-title">Chapters</span>
        </div>
        <nav class="chapters-nav">
          <router-link
            v-for="ch in chaptersStore.chapters"
            :key="ch.id"
            :to="`/reports/${reportId}/chapters/${ch.id}`"
            :class="['chapter-link', { active: ch.id === chapterId }]"
          >
            <span :class="['ch-status', ch.status]"></span>
            <span class="ch-title">{{ ch.title }}</span>
          </router-link>
        </nav>
      </div>

      <!-- Left: Agent Config -->
      <div class="panel panel-config">
        <AgentConfigPanel
          :chapter-id="chapterId"
          :initial-config="agentConfig"
          :generating="genStore.runStatus === 'running' || genStore.runStatus === 'pending'"
          @generate="onGenerate"
          @stop="onStop"
          @saved="onConfigSaved"
        />
      </div>

      <!-- Middle: Conversation -->
      <div class="panel panel-conversation">
        <div class="panel-header">
          <span class="panel-title">Agent Conversation</span>
        </div>
        <AgentConversation
          :messages="genStore.messages"
          :streaming-chunk="genStore.streamingChunk"
          :agent-streaming="genStore.agentStreaming"
        />
      </div>

      <!-- Right: Output -->
      <div class="panel panel-output">
        <MarkdownPreview
          :markdown="genStore.finalMarkdown"
          :chapter-title="chapter.title"
        />
      </div>
    </div>

    <div v-if="genStore.errorMessage" class="error-bar">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <span>{{ genStore.errorMessage }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useChaptersStore } from '@/stores/chapters'
import { useGenerationStore } from '@/stores/generation'
import { agentConfigsApi, type AgentConfig } from '@/api/agentConfigs'
import { useWebSocket } from '@/composables/useWebSocket'
import AgentConfigPanel from '@/components/agent/AgentConfigPanel.vue'
import AgentConversation from '@/components/agent/AgentConversation.vue'
import GenerationStatus from '@/components/agent/GenerationStatus.vue'
import MarkdownPreview from '@/components/output/MarkdownPreview.vue'

const route = useRoute()
const reportId = Number(route.params.reportId)
const chapterId = Number(route.params.chapterId)

const chaptersStore = useChaptersStore()
const genStore = useGenerationStore()

const chapter = computed(() => chaptersStore.current)
const agentConfig = ref<AgentConfig | null>(null)

const wsRunId = computed(() => genStore.activeRunId)
useWebSocket(wsRunId)

onMounted(async () => {
  genStore.reset()
  await Promise.all([
    chaptersStore.fetchOne(reportId, chapterId),
    chaptersStore.fetchAll(reportId),
  ])
  try {
    agentConfig.value = await agentConfigsApi.get(chapterId)
  } catch {}

  if (chapter.value?.final_output) {
    genStore.finalMarkdown = chapter.value.final_output
    genStore.runStatus = 'complete'
  }
})

async function onGenerate() {
  genStore.reset()
  await genStore.startGeneration(chapterId)
}

async function onStop() {
  await genStore.stopGeneration()
}

function onConfigSaved() {
  agentConfigsApi.get(chapterId).then(c => { agentConfig.value = c }).catch(() => {})
}
</script>

<style scoped>
.workspace { 
  display: flex; 
  flex-direction: column; 
  height: calc(100vh - 56px);
  background: var(--bg-root);
}

.workspace-header {
  display: flex; 
  align-items: center; 
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-3) var(--sp-5);
  border-bottom: 1px solid var(--border-1);
  background: var(--bg-surface);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  min-width: 0;
}

.back-link { 
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--text-3); 
  text-decoration: none; 
  font-size: var(--text-sm);
  white-space: nowrap;
  transition: color var(--duration-fast) var(--ease-out);
}

.back-link:hover { 
  color: var(--brand-text); 
}

.header-divider {
  width: 1px;
  height: 20px;
  background: var(--border-2);
}

h2 { 
  margin: 0; 
  font-size: var(--text-base);
  font-weight: 600;
  color: var(--text-1);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.workspace-body {
  display: grid; 
  grid-template-columns: 180px 300px 1fr 1fr;
  flex: 1; 
  overflow: hidden;
}

.panel {
  border-right: 1px solid var(--border-1);
  overflow: hidden;
  display: flex; 
  flex-direction: column;
  background: var(--bg-base);
}

.panel:last-child { 
  border-right: none; 
}

.panel-header {
  padding: var(--sp-3) var(--sp-4);
  border-bottom: 1px solid var(--border-1);
  flex-shrink: 0;
  background: var(--bg-surface);
}

.panel-title {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.panel-chapters { 
  background: var(--bg-surface);
}

.chapters-nav { 
  display: flex; 
  flex-direction: column; 
  gap: var(--sp-1);
  padding: var(--sp-2);
  overflow-y: auto; 
  flex: 1;
}

.chapter-link {
  display: flex; 
  align-items: flex-start; 
  gap: var(--sp-3);
  padding: var(--sp-3);
  border-radius: var(--r-md);
  text-decoration: none;
  color: var(--text-2);
  font-size: var(--text-sm);
  transition: all var(--duration-fast) var(--ease-out);
}

.chapter-link:hover { 
  background: var(--bg-hover);
  color: var(--text-1);
}

.chapter-link.active { 
  background: var(--brand-soft);
  color: var(--brand-text);
}

.ch-status {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 5px;
  background: var(--text-4);
}

.ch-status.pending { 
  background: var(--text-4);
}

.ch-status.running { 
  background: var(--info);
  animation: pulse 1.5s ease-in-out infinite;
}

.ch-status.complete { 
  background: var(--success);
}

.ch-status.error { 
  background: var(--error);
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.ch-title { 
  line-height: var(--leading-snug);
}

.error-bar {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  background: var(--error-soft);
  border-top: 1px solid var(--error);
  color: var(--error);
  padding: var(--sp-3) var(--sp-5);
  font-size: var(--text-sm);
  flex-shrink: 0;
}
</style>
