const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

const MODULES = [
  ['auth', '/auth/health/'],
  ['visa', '/visa/health/'],
  ['documents', '/documents/health/'],
  ['ai', '/ai/health/'],
  ['relocation', '/relocation/health/'],
  ['study', '/study/health/'],
  ['analytics', '/analytics/health/'],
  ['payments', '/payments/health/'],
  ['admin', '/admin/health/'],
  ['notifications', '/notifications/health/'],
  ['compliance', '/compliance/health/'],
]

export async function fetchBackendHealth() {
  const results = await Promise.all(
    MODULES.map(async ([name, path]) => {
      try {
        const response = await fetch(`${API_BASE}${path}`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const payload = await response.json()
        return { name, ok: true, payload }
      } catch (error) {
        return { name, ok: false, error: error.message }
      }
    }),
  )

  return results
}
