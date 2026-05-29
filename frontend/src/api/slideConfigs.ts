import client from './client'

export interface SlideConfig {
  id: number
  chapter_id: number
  output_mode: 'markdown' | 'pptx'
  slide_ratio: '16:9' | '4:3'
  title_font: string
  title_font_size: number
  title_bold: boolean
  title_color: string
  body_font: string
  body_font_size: number
  body_bold: boolean
  body_color: string
  bg_color: string
  margin_top: number
  margin_left: number
  margin_right: number
  margin_bottom: number
  created_at: string
  updated_at: string
}

export type SlideConfigUpsert = Omit<SlideConfig, 'id' | 'chapter_id' | 'created_at' | 'updated_at'>

export const DEFAULT_SLIDE_CONFIG: SlideConfigUpsert = {
  output_mode: 'markdown',
  slide_ratio: '16:9',
  title_font: 'Calibri',
  title_font_size: 36,
  title_bold: true,
  title_color: '1F2937',
  body_font: 'Calibri',
  body_font_size: 20,
  body_bold: false,
  body_color: '374151',
  bg_color: 'FFFFFF',
  margin_top: 0.7,
  margin_left: 0.7,
  margin_right: 0.7,
  margin_bottom: 0.7,
}

export const slideConfigsApi = {
  get: (chapterId: number) =>
    client.get<SlideConfig>(`/chapters/${chapterId}/slide-config`).then(r => r.data),
  save: (chapterId: number, data: SlideConfigUpsert) =>
    client.put<SlideConfig>(`/chapters/${chapterId}/slide-config`, data).then(r => r.data),
  exportPptxUrl: (chapterId: number) => `/api/chapters/${chapterId}/export/pptx`,
}
