import { Routes, Route, Link, useLocation } from 'react-router-dom'
import { ChatPage } from './pages/ChatPage'
import { ProfilePage } from './pages/ProfilePage'
import { ScalesPage } from './pages/ScalesPage'
import { ScaleTestPage } from './pages/ScaleTestPage'
import './App.css'

function TopNav() {
  const location = useLocation()
  const isActive = (path: string) => location.pathname === path

  return (
    <nav className="top-nav">
      <div className="top-nav-inner">
        <Link to="/" className="nav-brand">他山数字分身</Link>
        <div className="nav-links">
          <Link to="/" className={`nav-link ${isActive('/') ? 'active' : ''}`}>
            对话采集
          </Link>
          <Link to="/profile" className={`nav-link ${isActive('/profile') ? 'active' : ''}`}>
            我的画像
          </Link>
          <Link to="/scales" className={`nav-link ${isActive('/scales') || location.pathname.startsWith('/scales/') ? 'active' : ''}`}>
            量表测试
          </Link>
        </div>
      </div>
    </nav>
  )
}

function App() {
  return (
    <>
      <TopNav />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/scales" element={<ScalesPage />} />
          <Route path="/scales/:scaleId" element={<ScaleTestPage />} />
        </Routes>
      </main>
    </>
  )
}

export default App
