const API_BASE = import.meta.env.VITE_API_BASE_URL || '/api/v1'
const REQUEST_TIMEOUT_MS = 5000

const MODULES = [
  ['accounts', '/auth/health/'],
  ['visa', '/visa/health/'],
  ['documents', '/documents/health/'],
  ['ai_assistant', '/ai/health/'],
  ['relocation', '/relocation/health/'],
  ['study', '/study/health/'],
  ['analytics', '/analytics/health/'],
  ['payments', '/payments/health/'],
  ['admin_portal', '/admin/health/'],
  ['notifications', '/notifications/health/'],
  ['compliance', '/compliance/health/'],
]

async function fetchWithTimeout(url) {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS)

  try {
    return await fetch(url, { signal: controller.signal })
  } finally {
    clearTimeout(timeout)
  }
}

export async function fetchBackendHealth() {
  const results = await Promise.all(
    MODULES.map(async ([name, path]) => {
      try {
        const response = await fetchWithTimeout(`${API_BASE}${path}`)
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const payload = await response.json()
        return { name, ok: true, payload }
      } catch (error) {
        return { name, ok: false, error: error.message || 'Request failed' }
      }
    }),
  )

  return results
}
