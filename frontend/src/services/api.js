const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://visapilot.up.railway.app/api/v1'

const defaultHeaders = {
  'Content-Type': 'application/json',
}

class ApiError extends Error {
  constructor(message, { status, payload, fieldErrors } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.payload = payload
    this.fieldErrors = fieldErrors || {}
  }
}

function normalizeFieldErrors(payload) {
  if (!payload || typeof payload !== 'object') return {}

  if (payload.errors && typeof payload.errors === 'object') {
    return payload.errors
  }

  if (payload.detail) {
    return { detail: [String(payload.detail)] }
  }

  return Object.entries(payload).reduce((acc, [key, value]) => {
    if (Array.isArray(value)) {
      acc[key] = value.map((item) => String(item))
      return acc
    }

    if (typeof value === 'string') {
      acc[key] = [value]
      return acc
    }

    return acc
  }, {})
}

function buildMessage(status, payload, fieldErrors) {
  if (payload?.message) return payload.message
  if (payload?.detail) return String(payload.detail)

  const firstField = Object.keys(fieldErrors)[0]
  if (firstField && fieldErrors[firstField]?.length) {
    return fieldErrors[firstField][0]
  }

  return `Request failed (${status})`
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
    const fieldErrors = normalizeFieldErrors(payload)
    const message = buildMessage(response.status, payload, fieldErrors)
    throw new ApiError(message, { status: response.status, payload, fieldErrors })
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
    request('/payments/current-subscription/', {
      headers: { Authorization: `Bearer ${token}` },
    }),
}

export function formatFieldErrors(fieldErrors = {}) {
  const label = (field) => {
    if (!field || field === 'non_field_errors' || field === 'detail') return ''
    return field
      .split('_')
      .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
      .join(' ')
  }

  return Object.entries(fieldErrors)
    .flatMap(([field, messages]) =>
      (messages || []).map((msg) => {
        const cleanLabel = label(field)
        return cleanLabel ? `${cleanLabel}: ${msg}` : String(msg)
      }),
    )
    .join('\n')
}

export function getApiErrorMessage(error, fallback = 'Something went wrong. Please try again.') {
  if (error?.fieldErrors && Object.keys(error.fieldErrors).length) {
    return formatFieldErrors(error.fieldErrors)
  }
  return error?.message || fallback
}

export { ApiError }