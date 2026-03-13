import type { Block, StructuredProfile } from './types'

const API_BASE = '/api'

export async function getOrCreateSession(existingId?: string): Promise<string> {
  const url = existingId
    ? `${API_BASE}/session?session_id=${encodeURIComponent(existingId)}`
    : `${API_BASE}/session`
  const res = await fetch(url)
  const data = await res.json()
  return data.session_id
}

/**
 * Block 协议：每个 SSE 事件是一个 Block JSON。
 * onBlock 回调在收到每个 Block 时触发。
 */
export async function sendMessage(
  sessionId: string,
  message: string,
  onBlock: (block: Block) => void,
  model?: string | null,
): Promise<void> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId, message, model: model || undefined }),
  })
  if (!res.ok) throw new Error(`请求失败: ${res.status}`)
  const reader = res.body?.getReader()
  if (!reader) throw new Error('无法读取响应流')
  const decoder = new TextDecoder()
  let buffer = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n\n')
    buffer = lines.pop() ?? ''
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const payload = line.slice(6)
        if (payload === '[DONE]') continue
        try {
          const block = JSON.parse(payload) as Block
          onBlock(block)
        } catch {
          // ignore
        }
      }
    }
  }
}

export async function getProfile(sessionId: string): Promise<{
  profile: string
  forum_profile: string
}> {
  const res = await fetch(`${API_BASE}/profile/${sessionId}`)
  if (!res.ok) throw new Error(`获取画像失败: ${res.status}`)
  return res.json()
}

export async function getStructuredProfile(sessionId: string): Promise<StructuredProfile> {
  const res = await fetch(`${API_BASE}/profile/${sessionId}/structured`)
  if (!res.ok) throw new Error(`获取结构化画像失败: ${res.status}`)
  return res.json()
}

export function getDownloadUrl(sessionId: string): string {
  return `${API_BASE}/download/${sessionId}`
}

export function getPdfDownloadUrl(sessionId: string): string {
  return `${API_BASE}/download/${sessionId}/pdf`
}

export function getForumDownloadUrl(sessionId: string): string {
  return `${API_BASE}/download/${sessionId}/forum`
}

export async function resetSession(sessionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/session/reset/${sessionId}`, { method: 'POST' })
  if (!res.ok) throw new Error(`重置失败: ${res.status}`)
}

export async function getModels(): Promise<{ value: string; label: string }[]> {
  const res = await fetch(`${API_BASE}/models`)
  const data = await res.json()
  return data.models
}

export async function submitScale(
  sessionId: string,
  scaleName: string,
  answers: Record<string, number>,
  scores: Record<string, number>,
  resultSummary?: Record<string, unknown>,
): Promise<void> {
  const res = await fetch(`${API_BASE}/scales/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      scale_name: scaleName,
      answers,
      scores,
      result_summary: resultSummary,
    }),
  })
  if (!res.ok) throw new Error(`提交失败: ${res.status}`)
}

export interface FamousMatch {
  name: string
  name_en: string
  field: string
  era: string
  similarity: number
  reason: string
  signature: string
  csi: number
  rai: number
}

export interface ScatterPoint {
  name: string
  name_en: string
  csi: number
  rai: number
  is_top3: boolean
}

export interface FieldRecommendation {
  name: string
  name_en: string
  institution: string
  field: string
  reason: string
}

export interface FamousMatchResult {
  top3: FamousMatch[]
  scatter_data: ScatterPoint[]
  user_point: { csi: number; rai: number }
}

export async function getFamousMatches(sessionId: string): Promise<FamousMatchResult> {
  const res = await fetch(`${API_BASE}/profile/${sessionId}/scientists/famous`)
  if (!res.ok) throw new Error(`获取匹配失败: ${res.status}`)
  return res.json()
}

export async function getFieldRecommendations(sessionId: string): Promise<FieldRecommendation[]> {
  const res = await fetch(`${API_BASE}/profile/${sessionId}/scientists/field`)
  if (!res.ok) throw new Error(`获取推荐失败: ${res.status}`)
  const data = await res.json()
  return data.recommendations
}

export async function getScales(sessionId: string): Promise<Record<string, unknown>> {
  const res = await fetch(`${API_BASE}/scales/${sessionId}`)
  if (!res.ok) throw new Error(`获取量表失败: ${res.status}`)
  const data = await res.json()
  return data.scales
}
