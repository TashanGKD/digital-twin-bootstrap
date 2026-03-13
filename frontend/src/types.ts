export interface ChoiceOption {
  id: string
  label: string
  description?: string
}

export interface ActionButton {
  id: string
  label: string
  href?: string
  style?: 'primary' | 'secondary'
}

export type Block =
  | { type: 'text'; content: string }
  | { type: 'choice'; id: string; question: string; options: ChoiceOption[] }
  | { type: 'text_input'; id: string; question: string; placeholder?: string; multiline?: boolean }
  | { type: 'rating'; id: string; question: string; min_val: number; max_val: number; min_label?: string; max_label?: string }
  | { type: 'chart'; chart_type: 'radar' | 'bar'; title: string; dimensions: string[]; values: number[]; max_value?: number }
  | { type: 'actions'; message?: string; buttons: ActionButton[] }
  | { type: 'copyable'; title?: string; content: string }

export interface Message {
  role: 'user' | 'assistant'
  blocks: Block[]
}

// ── 结构化画像 ──────────────────────────

export interface ProcessScore {
  score: number | null
  description: string
}

export interface TechItem {
  category: string
  tech: string
  level: string
}

export interface NeedItem {
  item?: string
  desc?: string
  feeling?: string
  issue?: string
  detail?: string
  help_type?: string
}

export interface PersonalityDim {
  score: number
  level: string
}

export interface StructuredProfile {
  name: string
  meta: { created_at: string; updated_at: string; stage: string; source: string }
  identity: {
    research_stage: string
    primary_field: string
    secondary_field: string
    cross_field: string
    method: string
    institution: string
    network: string
  }
  capability: {
    tech_stack: TechItem[]
    process: Record<string, ProcessScore>
    outputs: string
  }
  needs: {
    time_occupation: NeedItem[]
    pain_points: NeedItem[]
    want_to_change: string
  }
  cognitive_style: {
    integration?: number
    depth?: number
    csi?: number
    type?: string
    source?: string
  }
  motivation: {
    dimensions: Record<string, number>
    intrinsic_total: number | null
    extrinsic_total: number | null
    rai: number | null
    source: string
  }
  personality: Record<string, PersonalityDim | string>
  interpretation: {
    core_driver: string
    risks: string
    path: string
  }
  completion: Record<string, boolean>
}

// ── 量表 ────────────────────────────────

export interface ScaleQuestion {
  id: string
  text: string
  dimension: string
  reverse?: boolean
}

export interface ScaleDefinition {
  id: string
  name: string
  description: string
  instructions: string
  min_val: number
  max_val: number
  min_label: string
  max_label: string
  questions: ScaleQuestion[]
  dimensions: { id: string; name: string; question_ids: string[] }[]
  scoring: 'average' | 'sum'
}
