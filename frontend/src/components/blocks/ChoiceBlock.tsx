import { useState } from 'react'
import type { ChoiceOption } from '../../types'

interface ChoiceBlockProps {
  question: string
  options: ChoiceOption[]
  onSelect?: (option: ChoiceOption) => void
  disabled?: boolean
}

export function ChoiceBlock({ question, options, onSelect, disabled }: ChoiceBlockProps) {
  const [selected, setSelected] = useState<string | null>(null)

  const handleClick = (opt: ChoiceOption) => {
    if (disabled || selected) return
    setSelected(opt.id)
    onSelect?.(opt)
  }

  return (
    <div className="block-choice">
      <p className="block-question">{question}</p>
      <div className="choice-options">
        {options.map((opt) => (
          <button
            key={opt.id}
            type="button"
            className={`choice-btn ${selected === opt.id ? 'selected' : ''} ${disabled || selected ? 'disabled' : ''}`}
            onClick={() => handleClick(opt)}
            disabled={!!(disabled || selected)}
          >
            <span className="choice-label">{opt.label}</span>
            {opt.description && <span className="choice-desc">{opt.description}</span>}
          </button>
        ))}
      </div>
    </div>
  )
}
