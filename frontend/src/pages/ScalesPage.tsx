import { Link } from 'react-router-dom'
import { ALL_SCALES } from '../data/scales'

export function ScalesPage() {
  return (
    <div className="scales-page">
      <header className="scales-header">
        <h2>量表测试</h2>
        <p>通过标准化量表精确评估你的科研认知风格、学术动机和人格特征。结果独立保存，可用于校对 AI 推断。</p>
      </header>

      <div className="scales-grid">
        {ALL_SCALES.map((scale) => (
          <Link key={scale.id} to={`/scales/${scale.id}`} className="scale-card">
            <h3>{scale.name}</h3>
            <p>{scale.description}</p>
            <span className="scale-card-action">开始测试 →</span>
          </Link>
        ))}
      </div>
    </div>
  )
}
