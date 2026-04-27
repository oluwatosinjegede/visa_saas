import React from 'react'
import { routes } from '../constants/routes'

const links = [
  ['Dashboard', routes.dashboard],
  ['Visa Assessment', routes.visaAssessment],
  ['Document Checklist', routes.documentChecklist],
  ['Documents', routes.documents],
  ['SOP Generator', routes.sopGenerator],
  ['Refusal Analysis', routes.refusalAnalysis],
  ['Study Placement', routes.studyPlacement],
  ['Job Relocation', routes.jobRelocation],
  ['Pricing', routes.pricing],
  ['Payment', routes.payment],
  ['Profile', routes.profile],
  ['Consultant', routes.consultantDashboard],
  ['Admin', routes.adminDashboard],
]

export default function Sidebar({ navigate }) {
  return (
    <aside className="sidebar">
      {links.map(([label, path]) => (
        <button key={path} type="button" className="ghost-btn sidebar-link" onClick={() => navigate(path)}>
          {label}
        </button>
      ))}
    </aside>
  )
}
