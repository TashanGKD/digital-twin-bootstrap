import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import type { StructuredProfile } from '../types'
import { getStructuredProfile, getDownloadUrl, getForumDownloadUrl, getProfile } from '../api'
import { ProfileHeader } from '../components/profile/ProfileHeader'
import { CapabilitySection } from '../components/profile/CapabilitySection'
import { NeedsSection } from '../components/profile/NeedsSection'
import { CognitiveStyleSection } from '../components/profile/CognitiveStyleSection'
import { MotivationSection } from '../components/profile/MotivationSection'
import { PersonalitySection } from '../components/profile/PersonalitySection'
import { InterpretationSection } from '../components/profile/InterpretationSection'
import { ScientistMatchSection } from '../components/profile/ScientistMatchSection'
import ReactMarkdown from 'react-markdown'

const SESSION_KEY = 'tashan_session_id'

export function ProfilePage() {
  const [structured, setStructured] = useState<StructuredProfile | null>(null)
  const [forumProfile, setForumProfile] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const sessionId = localStorage.getItem(SESSION_KEY)

  useEffect(() => {
    if (!sessionId) {
      setLoading(false)
      return
    }
    Promise.all([
      getStructuredProfile(sessionId),
      getProfile(sessionId),
    ])
      .then(([sp, raw]) => {
        setStructured(sp)
        setForumProfile(raw.forum_profile)
      })
      .catch((e) => setError(e instanceof Error ? e.message : String(e)))
      .finally(() => setLoading(false))
  }, [sessionId])

  if (loading) return <div className="page-loading">加载中...</div>

  if (!sessionId || error) {
    return (
      <div className="page-empty">
        <h2>尚未建立画像</h2>
        <p>{error || '请先在「对话采集」页面完成基础信息采集。'}</p>
        <Link to="/" className="btn-primary" style={{ marginTop: '1rem', display: 'inline-block' }}>开始构建</Link>
      </div>
    )
  }

  if (!structured) return <div className="page-loading">解析中...</div>

  return (
    <div className="pv-page">
      <ProfileHeader profile={structured} />
      <CapabilitySection capability={structured.capability} />
      <NeedsSection needs={structured.needs} />
      <CognitiveStyleSection data={structured.cognitive_style} />
      <MotivationSection data={structured.motivation} />
      <PersonalitySection data={structured.personality} />
      <InterpretationSection data={structured.interpretation} />

      <ScientistMatchSection sessionId={sessionId} />

      {forumProfile && (
        <section className="pv-section">
          <h3 className="pv-section-title">他山论坛分身</h3>
          <div className="pv-forum-body markdown-content">
            <ReactMarkdown>{forumProfile}</ReactMarkdown>
          </div>
        </section>
      )}

      <div className="pv-bottom-bar no-print">
        <button type="button" className="btn-primary" onClick={() => window.print()}>
          导出 PDF（打印）
        </button>
        <a href={getDownloadUrl(sessionId)} download="profile.md" className="btn-secondary">
          下载 Markdown
        </a>
        {forumProfile && (
          <a href={getForumDownloadUrl(sessionId)} download="forum-profile.md" className="btn-secondary">
            下载论坛分身
          </a>
        )}
        <Link to="/scales" className="btn-secondary">
          量表校对
        </Link>
      </div>
    </div>
  )
}
