import { useState, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getScaleById } from '../data/scales'
import { calculateScores, calculateRCSS, calculateAMS_RAI } from '../utils/scoring'
import { submitScale } from '../api'
import { ChartBlock } from '../components/blocks/ChartBlock'

const SESSION_KEY = 'tashan_session_id'

export function ScaleTestPage() {
  const { scaleId } = useParams<{ scaleId: string }>()
  const navigate = useNavigate()
  const scale = scaleId ? getScaleById(scaleId) : undefined
  const [currentIdx, setCurrentIdx] = useState(0)
  const [answers, setAnswers] = useState<Record<string, number>>({})
  const [completed, setCompleted] = useState(false)
  const [saving, setSaving] = useState(false)

  const handleAnswer = useCallback((questionId: string, value: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }))
    if (scale && currentIdx < scale.questions.length - 1) {
      setTimeout(() => setCurrentIdx((i) => i + 1), 200)
    } else if (scale && currentIdx === scale.questions.length - 1) {
      setTimeout(() => setCompleted(true), 200)
    }
  }, [currentIdx, scale])

  const handleSave = async () => {
    if (!scale) return
    const sessionId = localStorage.getItem(SESSION_KEY)
    if (!sessionId) {
      alert('请先在「对话采集」页面建立会话')
      return
    }
    setSaving(true)
    try {
      const scores = calculateScores(scale, answers)
      let resultSummary: Record<string, unknown> = { scores }
      if (scale.id === 'rcss') resultSummary = { ...resultSummary, ...calculateRCSS(scores) }
      if (scale.id === 'ams') resultSummary = { ...resultSummary, ...calculateAMS_RAI(scores) }
      await submitScale(sessionId, scale.id, answers, scores, resultSummary)
      alert('量表结果已保存！')
    } catch (e) {
      alert(`保存失败: ${e instanceof Error ? e.message : String(e)}`)
    } finally {
      setSaving(false)
    }
  }

  if (!scale) {
    return (
      <div className="page-empty">
        <h2>量表不存在</h2>
        <button type="button" onClick={() => navigate('/scales')} className="btn-primary">返回量表列表</button>
      </div>
    )
  }

  if (completed) {
    const scores = calculateScores(scale, answers)
    const dimNames = scale.dimensions.map((d) => d.name)
    const dimValues = scale.dimensions.map((d) => scores[d.id] || 0)
    const maxVal = scale.scoring === 'average' ? scale.max_val : scale.max_val * (scale.dimensions[0]?.question_ids.length || 4)

    return (
      <div className="scale-test-page">
        <div className="scale-result">
          <h2>{scale.name} — 测试完成</h2>

          <ChartBlock
            chartType="radar"
            title="维度得分"
            dimensions={dimNames}
            values={dimValues}
            maxValue={maxVal}
          />

          <div className="score-table">
            {scale.dimensions.map((dim) => (
              <div key={dim.id} className="score-row">
                <span className="score-dim">{dim.name}</span>
                <span className="score-val">{(scores[dim.id] || 0).toFixed(2)}</span>
              </div>
            ))}
          </div>

          {scale.id === 'rcss' && (() => {
            const r = calculateRCSS(scores)
            return (
              <div className="score-summary">
                <p>横向整合分 (I) = {r.I}，垂直深度分 (D) = {r.D}</p>
                <p>认知风格指数 (CSI) = {r.CSI}</p>
                <p className="score-type">类型：<strong>{r.type}</strong></p>
              </div>
            )
          })()}

          {scale.id === 'ams' && (() => {
            const r = calculateAMS_RAI(scores)
            return (
              <div className="score-summary">
                <p>内在动机总分 = {r.intrinsicTotal}</p>
                <p>外在动机总分 = {r.extrinsicTotal}</p>
                <p className="score-type">自主动机指数 (RAI) = <strong>{r.RAI}</strong></p>
              </div>
            )
          })()}

          <div className="scale-result-actions">
            <button type="button" className="btn-primary" onClick={handleSave} disabled={saving}>
              {saving ? '保存中...' : '保存结果'}
            </button>
            <button type="button" className="btn-secondary" onClick={() => navigate('/scales')}>
              返回量表列表
            </button>
            <button type="button" className="btn-secondary" onClick={() => { setCompleted(false); setCurrentIdx(0); setAnswers({}) }}>
              重新测试
            </button>
          </div>
        </div>
      </div>
    )
  }

  const question = scale.questions[currentIdx]
  const progress = ((currentIdx) / scale.questions.length) * 100
  const values: number[] = []
  for (let i = scale.min_val; i <= scale.max_val; i++) values.push(i)

  return (
    <div className="scale-test-page">
      <div className="scale-test-container">
        <header className="scale-test-header">
          <h2>{scale.name}</h2>
          <p className="scale-instructions">{scale.instructions}</p>
        </header>

        <div className="scale-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
          <span className="progress-text">{currentIdx + 1} / {scale.questions.length}</span>
        </div>

        <div className="scale-question-card">
          <p className="scale-question-text">{question.text}</p>
          <div className="scale-rating-row">
            <span className="rating-end-label">{scale.min_label}</span>
            <div className="scale-rating-buttons">
              {values.map((v) => (
                <button
                  key={v}
                  type="button"
                  className={`scale-rating-btn ${answers[question.id] === v ? 'selected' : ''}`}
                  onClick={() => handleAnswer(question.id, v)}
                >
                  {v}
                </button>
              ))}
            </div>
            <span className="rating-end-label">{scale.max_label}</span>
          </div>
        </div>

        <div className="scale-nav">
          <button
            type="button"
            className="btn-secondary"
            onClick={() => setCurrentIdx((i) => Math.max(0, i - 1))}
            disabled={currentIdx === 0}
          >
            ← 上一题
          </button>
          <button
            type="button"
            className="btn-secondary"
            onClick={() => {
              if (currentIdx < scale.questions.length - 1) {
                setCurrentIdx((i) => i + 1)
              } else {
                setCompleted(true)
              }
            }}
            disabled={answers[question.id] == null}
          >
            {currentIdx === scale.questions.length - 1 ? '完成' : '下一题 →'}
          </button>
        </div>
      </div>
    </div>
  )
}
