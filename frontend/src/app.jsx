import { useEffect, useState } from 'react'
import { fetchBackendHealth } from './services/api'
import ModuleHealthCard from './components/ModuleHealthCard'

export default function App() {
  const [modules, setModules] = useState([])

  useEffect(() => {
    fetchBackendHealth().then(setModules)
  }, [])

  const healthyCount = modules.filter((item) => item.ok).length

  return (
    <main className="container">
      <header>
        <h1>Visa SaaS Operational Dashboard</h1>
        <p>
          Backend connectivity: {healthyCount}/{modules.length || 0} modules healthy
        </p>
      </header>

      <section className="grid">
        {modules.map((module) => (
          <ModuleHealthCard key={module.name} module={module} />
        ))}
      </section>
    </main>
  )
}
