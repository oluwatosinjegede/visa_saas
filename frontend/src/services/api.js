const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://visapilot.up.railway.app/api/v1'

const defaultHeaders = {
  'Content-Type': 'application/json',
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
  })

  const contentType = response.headers.get('content-type') || ''
  const payload = contentType.includes('application/json') ? await response.json() : await response.text()

  if (!response.ok) {
    throw new Error(payload?.detail || payload?.message || `Request failed (${response.status})`)
  }

  return payload
}

export const api = {
  apiBaseUrl: API_BASE_URL,
  login: (credentials) => request('/auth/login/', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (data) => request('/auth/register/', { method: 'POST', body: JSON.stringify(data) }),
  getProfile: (token) =>
    request('/auth/profile/', { headers: { Authorization: `Bearer ${token}` } }),
  submitVisaAssessment: (token, data) =>
    request('/scoring/profile/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),
  generateSOP: (token, data) =>
    request('/ai/sop-generator/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),
  analyzeRefusal: (token, data) =>
    request('/ai/refusal-analysis/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),
    initializePayment: (token, data) =>
    request('/payments/initialize/', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { Authorization: `Bearer ${token}` },
    }),
  verifyPayment: (token, reference) =>
    request(`/payments/verify/?reference=${encodeURIComponent(reference)}`, {
      headers: { Authorization: `Bearer ${token}` },
    }),
  currentSubscription: (token) =>
    request('/subscriptions/current/', {
      headers: { Authorization: `Bearer ${token}` },
    }),
}

export function getApiErrorMessage(error, fallback = 'Something went wrong. Please try again.') {
  return error?.message || fallback
}