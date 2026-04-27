import React from 'react'

export default function DashboardCard({ title, value, note }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <p className="metric">{value}</p>
      {note ? <p>{note}</p> : null}
    </article>
  )
}