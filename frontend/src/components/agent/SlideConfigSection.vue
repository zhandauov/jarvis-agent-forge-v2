<template>
  <div class="slide-section">
    <button class="section-toggle" @click="open = !open">
      <svg
        width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
        stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
        :style="{ transform: open ? 'rotate(90deg)' : 'rotate(0deg)', transition: 'transform 0.15s' }"
      >
        <polyline points="9 18 15 12 9 6"/>
      </svg>
      <span>Slide Settings</span>
      <span v-if="draft.output_mode === 'pptx'" class="mode-badge pptx">PPTX</span>
      <span v-else class="mode-badge md">MD</span>
    </button>

    <div v-if="open" class="section-body">
      <!-- Output mode -->
      <div class="field">
        <label class="field-label">Output Mode</label>
        <div class="mode-toggle">
          <button
            :class="['mode-btn', { active: draft.output_mode === 'markdown' }]"
            @click="draft.output_mode = 'markdown'"
          >Markdown</button>
          <button
            :class="['mode-btn', { active: draft.output_mode === 'pptx' }]"
            @click="draft.output_mode = 'pptx'"
          >Slide (PPTX)</button>
        </div>
      </div>

      <template v-if="draft.output_mode === 'pptx'">
        <!-- Slide ratio -->
        <div class="field">
          <label class="field-label">Slide Ratio</label>
          <select class="input-select" v-model="draft.slide_ratio">
            <option value="16:9">16:9 (Widescreen)</option>
            <option value="4:3">4:3 (Standard)</option>
          </select>
        </div>

        <!-- Background -->
        <div class="field">
          <label class="field-label">Background Color</label>
          <div class="color-row">
            <input type="color" class="color-swatch" :value="'#' + draft.bg_color" @input="draft.bg_color = ($event.target as HTMLInputElement).value.replace('#', '')"/>
            <span class="color-code">#{{ draft.bg_color }}</span>
          </div>
        </div>

        <!-- Title styling -->
        <div class="subsection-label">Title</div>
        <div class="field-row">
          <div class="field">
            <label class="field-label">Font</label>
            <input class="input-text" v-model="draft.title_font" placeholder="Calibri" />
          </div>
          <div class="field field-narrow">
            <label class="field-label">Size (pt)</label>
            <input class="input-text" type="number" v-model.number="draft.title_font_size" min="8" max="72" />
          </div>
        </div>
        <div class="field-row">
          <div class="field">
            <label class="field-label">Color</label>
            <div class="color-row">
              <input type="color" class="color-swatch" :value="'#' + draft.title_color" @input="draft.title_color = ($event.target as HTMLInputElement).value.replace('#', '')"/>
              <span class="color-code">#{{ draft.title_color }}</span>
            </div>
          </div>
          <div class="field field-narrow field-checkbox">
            <label class="field-label">Bold</label>
            <input type="checkbox" class="checkbox" v-model="draft.title_bold" />
          </div>
        </div>

        <!-- Body styling -->
        <div class="subsection-label">Body Text</div>
        <div class="field-row">
          <div class="field">
            <label class="field-label">Font</label>
            <input class="input-text" v-model="draft.body_font" placeholder="Calibri" />
          </div>
          <div class="field field-narrow">
            <label class="field-label">Size (pt)</label>
            <input class="input-text" type="number" v-model.number="draft.body_font_size" min="8" max="60" />
          </div>
        </div>
        <div class="field-row">
          <div class="field">
            <label class="field-label">Color</label>
            <div class="color-row">
              <input type="color" class="color-swatch" :value="'#' + draft.body_color" @input="draft.body_color = ($event.target as HTMLInputElement).value.replace('#', '')"/>
              <span class="color-code">#{{ draft.body_color }}</span>
            </div>
          </div>
          <div class="field field-narrow field-checkbox">
            <label class="field-label">Bold</label>
            <input type="checkbox" class="checkbox" v-model="draft.body_bold" />
          </div>
        </div>

        <!-- Margins -->
        <div class="subsection-label">Margins (inches)</div>
        <div class="field-row four-col">
          <div class="field field-narrow">
            <label class="field-label">Top</label>
            <input class="input-text" type="number" step="0.1" min="0" max="3" v-model.number="draft.margin_top" />
          </div>
          <div class="field field-narrow">
            <label class="field-label">Right</label>
            <input class="input-text" type="number" step="0.1" min="0" max="3" v-model.number="draft.margin_right" />
          </div>
          <div class="field field-narrow">
            <label class="field-label">Bottom</label>
            <input class="input-text" type="number" step="0.1" min="0" max="3" v-model.number="draft.margin_bottom" />
          </div>
          <div class="field field-narrow">
            <label class="field-label">Left</label>
            <input class="input-text" type="number" step="0.1" min="0" max="3" v-model.number="draft.margin_left" />
          </div>
        </div>
      </template>

      <button class="save-btn" :disabled="saving" @click="save">
        <span v-if="saving">Saving…</span>
        <span v-else>Save Slide Settings</span>
      </button>
      <div v-if="savedMsg" class="saved-msg">{{ savedMsg }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { slideConfigsApi, DEFAULT_SLIDE_CONFIG } from '@/api/slideConfigs'
import type { SlideConfig, SlideConfigUpsert } from '@/api/slideConfigs'

const props = defineProps<{
  chapterId: number
  initialConfig: SlideConfig | null
}>()

const emit = defineEmits<{ (e: 'saved', config: SlideConfig): void }>()

const open = ref(false)
const saving = ref(false)
const savedMsg = ref('')

const draft = reactive<SlideConfigUpsert>({ ...DEFAULT_SLIDE_CONFIG })

watch(
  () => props.initialConfig,
  (cfg) => {
    if (cfg) {
      Object.assign(draft, {
        output_mode: cfg.output_mode,
        slide_ratio: cfg.slide_ratio,
        title_font: cfg.title_font,
        title_font_size: cfg.title_font_size,
        title_bold: cfg.title_bold,
        title_color: cfg.title_color,
        body_font: cfg.body_font,
        body_font_size: cfg.body_font_size,
        body_bold: cfg.body_bold,
        body_color: cfg.body_color,
        bg_color: cfg.bg_color,
        margin_top: cfg.margin_top,
        margin_left: cfg.margin_left,
        margin_right: cfg.margin_right,
        margin_bottom: cfg.margin_bottom,
      })
    }
  },
  { immediate: true }
)

async function save() {
  saving.value = true
  savedMsg.value = ''
  try {
    const saved = await slideConfigsApi.save(props.chapterId, { ...draft })
    emit('saved', saved)
    savedMsg.value = 'Saved!'
    setTimeout(() => (savedMsg.value = ''), 2000)
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.slide-section {
  border-top: 1px solid var(--border-1);
}

.section-toggle {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  width: 100%;
  padding: var(--sp-3) var(--sp-4);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-2);
  font-size: var(--text-xs);
  font-weight: 600;
  font-family: var(--font);
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  transition: color var(--duration-fast);
}

.section-toggle:hover { color: var(--text-1); }

.mode-badge {
  margin-left: auto;
  font-size: 10px;
  padding: 1px 6px;
  border-radius: var(--r-sm);
  font-weight: 700;
  letter-spacing: 0.03em;
}

.mode-badge.pptx { background: var(--brand-soft); color: var(--brand-text); }
.mode-badge.md { background: var(--bg-overlay); color: var(--text-3); }

.section-body {
  padding: 0 var(--sp-4) var(--sp-4);
  display: flex;
  flex-direction: column;
  gap: var(--sp-3);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--sp-1);
  flex: 1;
}

.field-narrow { max-width: 90px; }

.field-checkbox {
  align-items: center;
  flex-direction: column;
}

.field-row {
  display: flex;
  gap: var(--sp-3);
  align-items: flex-end;
}

.four-col {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--sp-2);
}

.field-label {
  font-size: var(--text-xs);
  color: var(--text-3);
  font-weight: 500;
}

.subsection-label {
  font-size: var(--text-xs);
  font-weight: 700;
  color: var(--text-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: var(--sp-1);
}

.mode-toggle {
  display: flex;
  border: 1px solid var(--border-2);
  border-radius: var(--r-md);
  overflow: hidden;
}

.mode-btn {
  flex: 1;
  padding: var(--sp-1) var(--sp-2);
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: var(--text-xs);
  font-family: var(--font);
  color: var(--text-3);
  transition: all var(--duration-fast);
}

.mode-btn.active {
  background: var(--brand);
  color: #fff;
}

.input-text {
  background: var(--bg-overlay);
  border: 1px solid var(--border-2);
  border-radius: var(--r-sm);
  padding: var(--sp-1) var(--sp-2);
  font-size: var(--text-xs);
  font-family: var(--font);
  color: var(--text-1);
  width: 100%;
  box-sizing: border-box;
}

.input-text:focus {
  outline: none;
  border-color: var(--brand);
}

.input-select {
  background: var(--bg-overlay);
  border: 1px solid var(--border-2);
  border-radius: var(--r-sm);
  padding: var(--sp-1) var(--sp-2);
  font-size: var(--text-xs);
  font-family: var(--font);
  color: var(--text-1);
  width: 100%;
}

.color-row {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}

.color-swatch {
  width: 28px;
  height: 28px;
  border: 1px solid var(--border-2);
  border-radius: var(--r-sm);
  padding: 2px;
  cursor: pointer;
  background: none;
}

.color-code {
  font-size: var(--text-xs);
  color: var(--text-3);
  font-family: var(--font-mono);
}

.checkbox {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: var(--brand);
}

.save-btn {
  margin-top: var(--sp-1);
  padding: var(--sp-2) var(--sp-3);
  background: var(--brand);
  color: #fff;
  border: none;
  border-radius: var(--r-md);
  cursor: pointer;
  font-size: var(--text-xs);
  font-family: var(--font);
  font-weight: 600;
  transition: opacity var(--duration-fast);
}

.save-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.save-btn:not(:disabled):hover { opacity: 0.88; }

.saved-msg {
  font-size: var(--text-xs);
  color: var(--success);
  text-align: center;
}
</style>
