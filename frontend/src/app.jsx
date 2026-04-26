import { useEffect, useState } from 'react'
import { fetchBackendHealth } from './services/api'
import ModuleHealthCard from './components/ModuleHealthCard'

const highlights = [
  {
    title: 'Smart visa pathways',
    description: 'Get personalized route suggestions for study, work, family, and relocation goals.'
  },
  {
    title: 'Document readiness',
    description: 'Track required paperwork, expiry dates, and review status from one timeline.'
  },
  {
    title: 'Risk-aware scoring',
    description: 'See an AI-powered readiness score with clear next steps to improve outcomes.'
  }
]

const steps = [
  'Tell us where you are, where you are going, and your intended visa category.',
  'Upload documents and complete the guided compliance checklist.',
  'Collaborate with advisors and monitor milestones until submission.'
]

export default function App() {
  const [modules, setModules] = useState([])

  useEffect(() => {
    fetchBackendHealth().then(setModules)
  }, [])

  const healthyCount = modules.filter((item) => item.ok).length

  return (
    <main className="homepage">
      <section className="hero">
        <nav className="topbar">
          <p className="brand">VisaFlow</p>
          <button className="ghost-btn">Sign in</button>
        </nav>

        <div className="hero-content">
          <p className="eyebrow">Global Mobility Platform</p>
          <h1>Move across borders with confidence.</h1>
          <p className="subtitle">
            VisaFlow helps applicants, teams, and advisors plan visa journeys, prepare compliant
            submissions, and stay ahead of every deadline.
          </p>

          <div className="cta-row">
            <button className="primary-btn">Start your visa plan</button>
            <button className="secondary-btn">Explore pathways</button>
          </div>

          <div className="stats">
            <article>
              <strong>98%</strong>
              <span>on-time document completion</span>
            </article>
            <article>
              <strong>42+</strong>
              <span>supported visa pathways</span>
            </article>
            <article>
              <strong>24/7</strong>
              <span>workflow and notification coverage</span>
            </article>
          </div>
        </div>
      </section>

      <section className="section">
        <h2>Everything you need for a successful visa application</h2>
        <div className="feature-grid">
          {highlights.map((item) => (
            <article key={item.title} className="feature-card">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section process">
        <h2>How it works</h2>
        <ol>
          {steps.map((step) => (
            <li key={step}>{step}</li>
          ))}
        </ol>
      </section>

      <section className="section system-status">
        <div className="status-head">
          <h2>System reliability</h2>
          <p>
            Backend connectivity: <strong>{healthyCount}</strong> / <strong>{modules.length || 0}</strong>{' '}
            services healthy
          </p>
        </div>
        <div className="grid">
          {modules.map((module) => (
            <ModuleHealthCard key={module.name} module={module} />
          ))}
        </div>
      </section>
    </main>
  )
}
