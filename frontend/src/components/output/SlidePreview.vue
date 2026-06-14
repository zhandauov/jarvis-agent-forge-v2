<template>
  <div class="slide-panel">
    <div class="slide-header">
      <span class="panel-title">Output — Slide Preview</span>
      <div class="header-actions" v-if="parsedContent">
        <button class="action-btn" :disabled="downloading" @click="downloadPptx" title="Download PPTX">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="7 10 12 15 17 10"/>
            <line x1="12" y1="15" x2="12" y2="3"/>
          </svg>
          <span>{{ downloading ? 'Downloading…' : 'Download PPTX' }}</span>
        </button>
      </div>
    </div>

    <div class="slide-viewport" ref="viewport" v-if="parsedContent">
      <!--
        slide-positioner has the *visual* (scaled) dimensions so flex centering works.
        .slide inside is full size but shrunk via CSS transform from top-left.
      -->
      <div
        class="slide-positioner"
        :style="{ width: scaledW + 'px', height: scaledH + 'px' }"
      >
        <div class="slide" :style="slideStyle">
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

// Natural slide dimensions in px (96 dpi)
const SLIDE_W = computed(() => props.config.slide_ratio === '4:3' ? 960 : 1280)
const SLIDE_H = 720

const viewport = ref<HTMLElement | null>(null)
const scale = ref(1)

function updateScale() {
  if (!viewport.value) return
  const availW = viewport.value.clientWidth - 32   // 16px padding each side
  const availH = viewport.value.clientHeight - 32
  const sw = availW / SLIDE_W.value
  const sh = availH / SLIDE_H
  scale.value = Math.min(sw, sh)
}

const ro = typeof ResizeObserver !== 'undefined' ? new ResizeObserver(updateScale) : null

onMounted(() => {
  updateScale()
  if (ro && viewport.value) ro.observe(viewport.value)
})
onUnmounted(() => ro?.disconnect())

// Visual dimensions after scaling — used to size the positioner div
const scaledW = computed(() => SLIDE_W.value * scale.value)
const scaledH = computed(() => SLIDE_H * scale.value)

// Parsed content
interface SlideContent { title: string; bullets: string[] }

const parsedContent = computed<SlideContent | null>(() => {
  if (!props.content) return null
  let raw = props.content.trim()
  raw = raw.replace(/^```json\s*/i, '').replace(/```\s*$/, '').trim()
  try {
    const data = JSON.parse(raw)
    if (data.title && Array.isArray(data.bullets)) {
      return { title: data.title, bullets: data.bullets }
    }
  } catch {}
  const lines = raw.split('\n').map(l => l.trim()).filter(Boolean)
  const firstLine = lines[0]
  if (!firstLine) return null
  return {
    title: firstLine.replace(/^#+\s*/, ''),
    bullets: lines.slice(1).filter(Boolean).map(l => l.replace(/^[-•*]\s*/, '')),
  }
})

// Download
const downloading = ref(false)

async function downloadPptx() {
  downloading.value = true
  try {
    const token = localStorage.getItem('auth_token')
    const res = await fetch(slideConfigsApi.exportPptxUrl(props.chapterId), {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    })
    if (!res.ok) throw new Error('Export failed')
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.chapterTitle.replace(/\s+/g, '_')}.pptx`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    downloading.value = false
  }
}

function hex(c: string) { return `#${c.replace('#', '')}` }

const slideStyle = computed(() => ({
  width: `${SLIDE_W.value}px`,
  height: `${SLIDE_H}px`,
  transform: `scale(${scale.value})`,
  transformOrigin: 'top left',
  backgroundColor: hex(props.config.bg_color),
  padding: `${props.config.margin_top * 96}px ${props.config.margin_right * 96}px ${props.config.margin_bottom * 96}px ${props.config.margin_left * 96}px`,
  boxSizing: 'border-box' as const,
  display: 'flex',
  flexDirection: 'column' as const,
  gap: '16px',
  borderRadius: '4px',
  boxShadow: '0 4px 32px rgba(0,0,0,0.22)',
  flexShrink: '0',
}))

const titleStyle = computed(() => ({
  fontFamily: `"${props.config.title_font}", sans-serif`,
  fontSize: `${props.config.title_font_size}px`,
  fontWeight: props.config.title_bold ? '700' : '400',
  color: hex(props.config.title_color),
  lineHeight: '1.2',
  flexShrink: '0',
  wordBreak: 'break-word' as const,
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
  wordBreak: 'break-word' as const,
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
  transition: all var(--duration-fast) var(--ease-out);
}

.action-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.action-btn:not(:disabled):hover {
  border-color: var(--brand);
  color: var(--brand-text);
  background: var(--brand-soft);
}

/* ─── Viewport: full available space, centres the positioner ─── */
.slide-viewport {
  flex: 1;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background: var(--bg-overlay);
}

/*
  Positioner is sized to the *visual* (scaled) slide dimensions.
  This is what gets centred inside the viewport.
  The actual .slide div inside is full-size but shrunk via transform.
*/
.slide-positioner {
  position: relative;
  flex-shrink: 0;
}

/* .slide styles are fully inline (slideStyle computed) */
.slide {
  position: absolute;
  top: 0;
  left: 0;
}

/* ─── Empty state ─── */
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
