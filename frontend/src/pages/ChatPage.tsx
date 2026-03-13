import { useState, useRef, useEffect, useCallback } from 'react'
import type { Block, Message } from '../types'
import { BlockRenderer } from '../components/blocks/BlockRenderer'
import { getOrCreateSession, sendMessage, resetSession, getProfile, getModels } from '../api'

const SESSION_KEY = 'tashan_session_id'

export function ChatPage() {
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [initialized, setInitialized] = useState(false)
  const [models, setModels] = useState<{ value: string; label: string }[]>([])
  const [selectedModel, setSelectedModel] = useState('qwen3.5-plus')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const fetchModels = useCallback(async () => {
    try {
      const m = await getModels()
      setModels(m)
      if (m.length > 0 && !m.find((x) => x.value === selectedModel)) {
        setSelectedModel(m[0].value)
      }
    } catch {
      // use default
    }
  }, [selectedModel])

  useEffect(() => {
    async function init() {
      const stored = localStorage.getItem(SESSION_KEY)
      const id = await getOrCreateSession(stored ?? undefined)
      setSessionId(id)
      localStorage.setItem(SESSION_KEY, id)
      await fetchModels()
      setInitialized(true)
    }
    init()
  }, [fetchModels])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = useCallback(async (text: string) => {
    if (!text.trim() || !sessionId || loading) return

    const userMsg: Message = { role: 'user', blocks: [{ type: 'text', content: text }] }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)

    const assistantBlocks: Block[] = []
    const assistantMsg: Message = { role: 'assistant', blocks: [] }
    setMessages((prev) => [...prev, assistantMsg])

    try {
      await sendMessage(sessionId, text, (block) => {
        assistantBlocks.push(block)
        setMessages((prev) => {
          const next = [...prev]
          next[next.length - 1] = { role: 'assistant', blocks: [...assistantBlocks] }
          return next
        })
      }, selectedModel || undefined)
    } catch (e) {
      assistantBlocks.push({
        type: 'text',
        content: `请求失败: ${e instanceof Error ? e.message : String(e)}`,
      })
      setMessages((prev) => {
        const next = [...prev]
        next[next.length - 1] = { role: 'assistant', blocks: [...assistantBlocks] }
        return next
      })
    } finally {
      setLoading(false)
    }
  }, [loading, selectedModel, sessionId])

  const handleBlockRespond = useCallback((text: string) => {
    handleSendMessage(text)
  }, [handleSendMessage])

  const handleReset = async () => {
    if (!sessionId) return
    try {
      await resetSession(sessionId)
      setMessages([])
    } catch (e) {
      alert(`重置失败: ${e instanceof Error ? e.message : String(e)}`)
    }
  }

  if (!initialized) {
    return <div className="page-loading">加载中...</div>
  }

  return (
    <div className="chat-page">
      <div className="chat-container">
        <header className="chat-header">
          <div className="chat-header-left">
            <h2>对话采集</h2>
          </div>
          <div className="chat-header-right">
            <select
              className="model-select"
              value={selectedModel}
              onChange={(e) => setSelectedModel(e.target.value)}
              disabled={loading}
            >
              {models.map((m) => (
                <option key={m.value} value={m.value}>{m.label}</option>
              ))}
            </select>
            <button type="button" className="btn-reset" onClick={handleReset} disabled={loading}>
              重置
            </button>
          </div>
        </header>

        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-welcome">
              <h3>欢迎使用科研数字分身采集助手</h3>
              <p>点击下方按钮开始构建你的数字分身</p>
              <div className="welcome-actions">
                <button
                  type="button"
                  className="welcome-btn"
                  onClick={() => handleSendMessage('帮我建立分身')}
                  disabled={loading}
                >
                  开始构建分身
                </button>
              </div>
            </div>
          )}

          {messages.map((msg, msgIdx) => {
            const isLastAssistant =
              msg.role === 'assistant' && msgIdx === messages.length - 1
            const isResponded = msg.role === 'assistant' && !isLastAssistant

            return (
              <div key={msgIdx} className={`msg-row msg-${msg.role}`}>
                {msg.role === 'assistant' && (
                  <div className="msg-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <rect x="4" y="8" width="16" height="12" rx="2" />
                      <circle cx="9" cy="12" r="1.5" fill="currentColor" />
                      <circle cx="15" cy="12" r="1.5" fill="currentColor" />
                      <path d="M9 15h6" />
                      <path d="M12 4v4" />
                    </svg>
                  </div>
                )}
                <div className="msg-content">
                  {msg.blocks.length === 0 && loading && isLastAssistant && (
                    <div className="loading-dots">
                      <span className="dot" />
                      <span className="dot" />
                      <span className="dot" />
                    </div>
                  )}
                  {msg.blocks.map((block, blockIdx) => (
                    <BlockRenderer
                      key={blockIdx}
                      block={block}
                      onRespond={isLastAssistant && !loading ? handleBlockRespond : undefined}
                      disabled={loading}
                      responded={isResponded}
                    />
                  ))}
                </div>
                {msg.role === 'user' && (
                  <div className="msg-avatar user-avatar">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                      <circle cx="12" cy="8" r="4" />
                      <path d="M4 20c0-4 4-6 8-6s8 2 8 6" />
                    </svg>
                  </div>
                )}
              </div>
            )
          })}
          <div ref={messagesEndRef} />
        </div>
      </div>
    </div>
  )
}
