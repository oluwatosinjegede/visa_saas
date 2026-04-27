import React from 'react'

export default function PlanCard({ plan, onSelect }) {
  return (
    <article className="card">
      <h3>{plan.name}</h3>
      <p className="plan-price">{plan.price}</p>
      <ul>
        {plan.features.map((feature) => (
          <li key={feature}>{feature}</li>
        ))}
      </ul>
      <button className="primary-btn" type="button" onClick={() => onSelect(plan)}>
        Choose {plan.name}
      </button>
    </article>
  )
}