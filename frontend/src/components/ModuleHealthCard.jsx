import React from 'react'

function formatModuleName(name) {
  if (!name) return 'Unknown'
  return name
    .split('_')
    .map((segment) => segment[0].toUpperCase() + segment.slice(1))
    .join(' ')
}

export default function ModuleHealthCard({ module }) {
  const moduleName = module?.payload?.module ?? module?.name
  return (
    <article className={`card ${module.ok ? 'ok' : 'bad'}`}>
      <h3>{formatModuleName(moduleName)}</h3>
      <p>Status: {module.ok ? 'Healthy' : 'Unavailable'}</p>
      <pre>{JSON.stringify(module.ok ? module.payload : module.error, null, 2)}</pre>
    </article>
  )
}