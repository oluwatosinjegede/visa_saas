import React, { useEffect, useMemo, useState } from 'react'

const highlights = [
  {
    title: 'Smart visa pathways',
    description: 'Get personalized route suggestions for study, work, family, and relocation goals.',
  },
  {
    title: 'Document readiness',
    description: 'Track required paperwork, expiry dates, and review status from one timeline.',
  },
  {
    title: 'Risk-aware scoring',
    description: 'See an AI-powered readiness score with clear next steps to improve outcomes.',
  },
]

const steps = [
  'Tell us where you are, where you are going, and your intended visa category.',
  'Upload documents and complete the guided compliance checklist.',
  'Collaborate with advisors and monitor milestones until submission.',
]

const modulePages = [
  {
    slug: 'accounts',
    title: 'Accounts',
    description: 'Manage applicant profiles, family members, and linked advisor access controls.',
    bullets: ['Profile completion progress', 'Team and family member roles', 'Identity verification status'],
  },
  {
    slug: 'visa',
    title: 'Visa',
    description: 'Track active cases and compare eligibility paths based on your destination goals.',
    bullets: ['Country and category matrix', 'Readiness score overview', 'Milestone-based case timeline'],
  },
  {
    slug: 'documents',
    title: 'Documents',
    description: 'Upload, classify, and validate forms, IDs, and supporting evidence in one workspace.',
    bullets: ['Required document checklist', 'Expiry and renewal tracking', 'Advisor review queue'],
  },
  {
    slug: 'ai-assistant',
    title: 'AI Assistant',
    description: 'Get contextual guidance for missing requirements, deadlines, and filing strategy.',
    bullets: ['Intent-aware question prompts', 'Draft response suggestions', 'Policy and evidence reminders'],
  },
  {
    slug: 'relocation',
    title: 'Relocation',
    description: 'Coordinate travel, housing, onboarding, and dependents with timeline-first planning.',
    bullets: ['Move planning checklist', 'Destination onboarding tasks', 'Family relocation sequencing'],
  },
  {
    slug: 'study',
    title: 'Study',
    description: 'Prepare education-focused pathways including institution docs and permit timelines.',
    bullets: ['Admission and enrollment status', 'Student permit requirement map', 'Scholarship and funding tracker'],
  },
  {
    slug: 'analytics',
    title: 'Analytics',
    description: 'Monitor pipeline health, case velocity, and completion risk across all applicants.',
    bullets: ['Live application funnel', 'Deadline risk indicators', 'Advisor workload dashboard'],
  },
  {
    slug: 'payments',
    title: 'Payments',
    description: 'Track government fees, advisor invoices, and payment milestones per case.',
    bullets: ['Fee schedule visibility', 'Invoice and receipt history', 'Pending payment alerts'],
  },
  {
    slug: 'admin-portal',
    title: 'Admin Portal',
    description: 'Configure platform settings, roles, governance rules, and organization-wide controls.',
    bullets: ['Role and permission policies', 'Workflow configuration', 'Environment and audit settings'],
  },
  {
    slug: 'notifications',
    title: 'Notifications',
    description: 'Deliver updates for approvals, requests, deadlines, and team mentions in real time.',
    bullets: ['Multi-channel notification rules', 'Escalation and reminder cadence', 'Case activity digest preferences'],
  },
  {
    slug: 'compliance',
    title: 'Compliance',
    description: 'Keep your program aligned with jurisdiction policies, internal controls, and audits.',
    bullets: ['Regulation checklist tracking', 'Policy acknowledgement records', 'Audit trail and exception log'],
  },
]

  const pageMap = Object.fromEntries(modulePages.map((page) => [page.slug, page]))

  function ModulePage({ page, onBack }) {
  return (
    <section className="section module-page">
      <button className="ghost-btn" type="button" onClick={onBack}>
        ← Back to home
      </button>

      <h2>{page.title}</h2>
      <p className="module-description">{page.description}</p>

      <div className="module-grid">
        {page.bullets.map((bullet) => (
          <article key={bullet} className="feature-card">
            <h3>{bullet}</h3>
            <p>
              This section of the {page.title} module is now connected to the homepage for quick
              navigation.
            </p>
          </article>
        ))}
      </div>
    </section>
  )
}

function HomePage({ onNavigate }) {
  return (
    <>
      <section className="hero">
        <nav className="topbar">
          <p className="brand">VisaPilot</p>
          <div className="topbar-actions">
            <button className="ghost-btn" type="button" onClick={() => onNavigate('accounts')}>
              Dashboard
            </button>
            <button className="ghost-btn" type="button" onClick={() => onNavigate('admin-portal')}>
              Admin
            </button>
            <button className="ghost-btn" type="button" onClick={() => onNavigate('ai-assistant')}>
              Sign in
            </button>
          </div>
        </nav>

        <div className="hero-content">
          <p className="eyebrow">Global Mobility Platform</p>

          <h1>Move across borders with confidence.</h1>

          <p className="subtitle">
            VisaPilot helps applicants, teams, and advisors plan visa journeys, prepare compliant
            submissions, and stay ahead of every deadline.
          </p>

          <div className="cta-row">
            <button className="primary-btn" type="button" onClick={() => onNavigate('visa')}>
              Start your visa plan
            </button>
            <button className="secondary-btn" type="button" onClick={() => onNavigate('documents')}>
              Explore pathways
            </button>
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

       <section className="section">
        <h2>Explore app modules</h2>
        <p className="module-description">
          Open each page directly from the homepage. Every major module is now available and linked.
        </p>

        <div className="module-grid">
          {modulePages.map((page) => (
            <article key={page.slug} className="feature-card module-card">
              <h3>{page.title}</h3>
              <p>{page.description}</p>
              <button className="secondary-btn" type="button" onClick={() => onNavigate(page.slug)}>
                Open {page.title}
              </button>
            </article>
          ))}
        </div>
        </section>
    </>
  )
}

        export default function App() {
  const [route, setRoute] = useState(() => window.location.hash.replace('#/', '') || 'home')


        useEffect(() => {
    function handleHashChange() {
      setRoute(window.location.hash.replace('#/', '') || 'home')
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  const currentPage = useMemo(() => pageMap[route], [route])

  function navigate(nextRoute) {
    window.location.hash = nextRoute === 'home' ? '/' : `/${nextRoute}`
  }

  return (
    <main className="homepage">
      {currentPage ? (
        <ModulePage page={currentPage} onBack={() => navigate('home')} />
      ) : (
        <HomePage onNavigate={navigate} />
      )}
    </main>
  )
}