<template>
  <div class="workspace">
    <div class="workspace-header">
      <router-link :to="`/reports/${reportId}`" class="back-link">← Report</router-link>
      <h2>{{ chapter?.title ?? 'Loading...' }}</h2>
      <GenerationStatus :status="genStore.runStatus" />
    </div>

    <div v-if="chapter" class="workspace-body">
      <!-- Chapters nav -->
      <div class="panel panel-chapters">
        <div class="panel-title">Chapters</div>
        <nav class="chapters-nav">
          <router-link
            v-for="ch in chaptersStore.chapters"
            :key="ch.id"
            :to="`/reports/${reportId}/chapters/${ch.id}`"
            :class="['chapter-link', { active: ch.id === chapterId }]"
          >
            <span class="ch-status" :class="ch.status" />
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
        <div class="panel-title">Agent Conversation</div>
        <AgentConversation
          :messages="genStore.messages"
          :streaming-chunk="genStore.streamingChunk"
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
      Error: {{ genStore.errorMessage }}
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
.workspace { display: flex; flex-direction: column; height: calc(100vh - 56px); }
.workspace-header {
  display: flex; align-items: center; gap: 16px;
  padding: 12px 24px; border-bottom: 1px solid #2d2d4e;
  background: #14142a; flex-shrink: 0;
}
.back-link { color: #888; text-decoration: none; font-size: 14px; white-space: nowrap; }
.back-link:hover { color: #9d8fff; }
h2 { margin: 0; font-size: 18px; color: #e0e0ff; flex: 1; }
.workspace-body {
  display: grid; grid-template-columns: 180px 280px 1fr 1fr;
  flex: 1; overflow: hidden;
}
.panel {
  border-right: 1px solid #2d2d4e; overflow: hidden;
  display: flex; flex-direction: column;
}
.panel:last-child { border-right: none; }
.panel-title {
  padding: 12px 16px; border-bottom: 1px solid #2d2d4e;
  font-size: 13px; color: #888; text-transform: uppercase; letter-spacing: 0.5px;
  flex-shrink: 0;
}
.panel-chapters { background: #12122a; }
.chapters-nav { display: flex; flex-direction: column; gap: 2px; padding: 8px; overflow-y: auto; flex: 1; }
.chapter-link {
  display: flex; align-items: flex-start; gap: 8px;
  padding: 8px 10px; border-radius: 6px; text-decoration: none;
  color: #aaa; font-size: 13px; transition: background 0.15s;
}
.chapter-link:hover { background: #1e1e3a; color: #e0e0ff; }
.chapter-link.active { background: #2d2d5e; color: #9d8fff; }
.ch-status {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; margin-top: 4px;
}
.ch-status.pending { background: #555; }
.ch-status.running { background: #5ba3f5; }
.ch-status.complete { background: #4caf7d; }
.ch-status.error { background: #e74c3c; }
.ch-title { line-height: 1.3; }
.error-bar {
  background: #3a1a1a; border-top: 1px solid #e74c3c;
  color: #e74c3c; padding: 10px 24px; font-size: 14px; flex-shrink: 0;
}
</style>
