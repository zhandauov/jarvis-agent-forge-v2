<template>
  <div class="slide-panel">
    <div class="slide-header">
      <span class="panel-title">Output — Slide Preview</span>
      <div class="header-actions" v-if="parsedContent">
        <a
          class="action-btn"
          :href="downloadUrl"
          download
          title="Download PPTX"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>Download PPTX</span>
        </a>
      </div>
    </div>

    <div class="slide-viewport" v-if="parsedContent">
      <div class="slide-scale-wrapper" ref="scaleWrapper">
        <div
          class="slide"
          :style="slideStyle"
          ref="slideEl"
        >
          <div class="slide-title" :style="titleStyle">{{ parsedContent.title }}</div>
          <ul class="slide-bullets" :style="bodyContainerStyle">
            <li
              v-for="(bullet, i) in parsedContent.bullets"
              :key="i"
              class="slide-bullet"
              :style="bodyStyle"
            >{{ bullet }}</li>
          </ul>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <rect x="2" y="3" width="20" height="14" rx="2"/>
          <path d="M8 21h8M12 17v4"/>
        </svg>
      </div>
      <p class="empty-text">No slide yet</p>
      <span class="empty-hint">Generate in PPTX mode to see the slide preview here.</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import type { SlideConfig } from '@/api/slideConfigs'
import { slideConfigsApi } from '@/api/slideConfigs'

const props = defineProps<{
  content: string | null
  config: SlideConfig
  chapterId: number
  chapterTitle: string
}>()

const scaleWrapper = ref<HTMLElement | null>(null)
const slideEl = ref<HTMLElement | null>(null)
const scale = ref(1)

// Slide natural dimensions (px, at 96dpi equivalent)
const SLIDE_W = computed(() => props.config.slide_ratio === '4:3' ? 960 : 1280)
const SLIDE_H = computed(() => props.config.slide_ratio === '4:3' ? 720 : 720)

function updateScale() {
  if (!scaleWrapper.value) return
  const availW = scaleWrapper.value.clientWidth - 32
  const availH = scaleWrapper.value.clientHeight - 32
  const scaleW = availW / SLIDE_W.value
  const scaleH = availH / SLIDE_H.value
  scale.value = Math.min(scaleW, scaleH, 1)
}

const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(updateScale) : null

onMounted(() => {
  updateScale()
  if (ro && scaleWrapper.value) ro.observe(scaleWrapper.value)
})

onUnmounted(() => ro?.disconnect())

// Parse JSON content from agent
interface SlideContent { title: string; bullets: string[] }

const parsedContent = computed<SlideContent | null>(() => {
  if (!props.content) return null
  let raw = props.content.trim()
  // Strip markdown code fences
  raw = raw.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim()
  try {
    const data = JSON.parse(raw)
    if (data.title && Array.isArray(data.bullets)) {
      return { title: data.title, bullets: data.bullets }
    }
  } catch {}
  // Fallback: first line = title, rest = bullets
  const lines = raw.split('\n').map(l => l.trim()).filter(Boolean)
  const firstLine = lines[0]
  if (!firstLine) return null
  return {
    title: firstLine.replace(/^#+\s*/, ''),
    bullets: lines.slice(1).filter(Boolean).map(l => l.replace(/^[-•*]\s*/, '')),
  }
})

const downloadUrl = computed(() => slideConfigsApi.exportPptxUrl(props.chapterId))

function hex(c: string) { return `#${c.replace('#', '')}` }

const slideStyle = computed(() => ({
  width: `${SLIDE_W.value}px`,
  height: `${SLIDE_H.value}px`,
  transform: `scale(${scale.value})`,
  transformOrigin: 'top left',
  backgroundColor: hex(props.config.bg_color),
  padding: `${props.config.margin_top * 96}px ${props.config.margin_right * 96}px ${props.config.margin_bottom * 96}px ${props.config.margin_left * 96}px`,
  boxSizing: 'border-box' as const,
  display: 'flex',
  flexDirection: 'column' as const,
  gap: '16px',
}))

const titleStyle = computed(() => ({
  fontFamily: `"${props.config.title_font}", sans-serif`,
  fontSize: `${props.config.title_font_size}px`,
  fontWeight: props.config.title_bold ? '700' : '400',
  color: hex(props.config.title_color),
  lineHeight: '1.2',
  flexShrink: '0',
}))

const bodyContainerStyle = computed(() => ({
  flex: '1',
  overflow: 'hidden',
  margin: '0',
  padding: '0',
  listStyle: 'none',
  display: 'flex',
  flexDirection: 'column' as const,
  gap: '10px',
  justifyContent: 'center',
}))

const bodyStyle = computed(() => ({
  fontFamily: `"${props.config.body_font}", sans-serif`,
  fontSize: `${props.config.body_font_size}px`,
  fontWeight: props.config.body_bold ? '700' : '400',
  color: hex(props.config.body_color),
  lineHeight: '1.4',
  display: 'flex',
  alignItems: 'flex-start',
  gap: '10px',
}))
</script>

<style scoped>
.slide-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: var(--bg-surface);
}

.slide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--sp-3) var(--sp-4);
  border-bottom: 1px solid var(--border-1);
  flex-shrink: 0;
}

.panel-title {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header-actions {
  display: flex;
  gap: var(--sp-2);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  background: transparent;
  border: 1px solid var(--border-2);
  color: var(--text-3);
  padding: var(--sp-1) var(--sp-3);
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-xs);
  font-family: var(--font);
  text-decoration: none;
  transition: all var(--duration-fast) var(--ease-out);
}

.action-btn:hover {
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}

.slide-viewport {
  flex: 1;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--sp-4);
  background: var(--bg-overlay);
}

.slide-scale-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.slide {
  border-radius: 4px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.18);
  flex-shrink: 0;
}

.slide-title {
  word-break: break-word;
}

.slide-bullets {
  word-break: break-word;
}

.slide-bullet::before {
  content: '•';
  flex-shrink: 0;
  margin-top: 2px;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--sp-3);
  text-align: center;
  padding: var(--sp-8);
}

.empty-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-overlay);
  border-radius: var(--r-lg);
  color: var(--text-4);
}

.empty-text {
  color: var(--text-2);
  font-size: var(--text-base);
  font-weight: 500;
  margin: 0;
}

.empty-hint {
  color: var(--text-4);
  font-size: var(--text-sm);
  max-width: 240px;
}
</style>
