import React from 'react'

export default function ServiceCard({ title, description, cta, onClick }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <p>{description}</p>
      {cta ? (
        <button className="secondary-btn" type="button" onClick={onClick}>
          {cta}
        </button>
      ) : null}
    </article>
  )
}