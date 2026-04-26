export default function ModuleHealthCard({ module }) {
  return (
    <article className={`card ${module.ok ? 'ok' : 'bad'}`}>
      <h3>{module.name}</h3>
      <p>Status: {module.ok ? 'Healthy' : 'Unavailable'}</p>
      <pre>{JSON.stringify(module.ok ? module.payload : module.error, null, 2)}</pre>
    </article>
  )
}