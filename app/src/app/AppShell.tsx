import { NavLink, Outlet } from 'react-router-dom'

import './AppShell.css'

const NAV = [
  { to: '/', label: '문서별 작업', end: true },
  { to: '/changes', label: '변경 이력', end: false },
  { to: '/wireframe', label: '화면', end: false },
]

export function AppShell() {
  return (
    <div className="shell">
      <header className="shell-top">
        <div className="shell-title">
          <p className="shell-eyebrow">기획 문서 상황판</p>
          <h1>아이오더 F&amp;B 플랫폼</h1>
        </div>
        <nav className="shell-nav">
          {NAV.map((n) => (
            <NavLink key={n.to} to={n.to} end={n.end}>
              {n.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="shell-main">
        <Outlet />
      </main>
    </div>
  )
}
