import React from 'react'
import { routes } from '../constants/routes'
import { useAuth } from '../context/AuthContext'

const publicLinks = [
  ['Home', routes.home],
  ['Pricing', routes.pricing],
  ['Visa Assessment', routes.visaAssessment],
  ['Study Placement', routes.studyPlacement],
  ['Job Relocation', routes.jobRelocation],
  ['SOP Generator', routes.sopGenerator],
  ['Refusal Analysis', routes.refusalAnalysis],
]

export default function Navbar({ navigate }) {
  const { isAuthenticated, logout } = useAuth()

  return (
    <nav className="navbar">
      <button className="brand" onClick={() => navigate(routes.home)} type="button">
        VisaPilot
      </button>
      <div className="nav-links">
        {publicLinks.map(([label, path]) => (
          <button key={path} className="ghost-btn" type="button" onClick={() => navigate(path)}>
            {label}
          </button>
        ))}
      </div>
      <div className="nav-links">
        {!isAuthenticated ? (
          <>
            <button className="ghost-btn" type="button" onClick={() => navigate(routes.login)}>
              Login
            </button>
            <button className="primary-btn" type="button" onClick={() => navigate(routes.register)}>
              Register
            </button>
          </>
        ) : (
          <>
            <button className="ghost-btn" type="button" onClick={() => navigate(routes.dashboard)}>
              Dashboard
            </button>
            <button
              className="ghost-btn"
              type="button"
              onClick={() => {
                logout()
                navigate(routes.login)
              }}
            >
              Logout
            </button>
          </>
        )}
      </div>
    </nav>
  )
}
