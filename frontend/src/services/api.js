const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://visapilot.up.railway.app/api/v1'

const defaultHeaders = {
  'Content-Type': 'application/json',
}

const ACCESS_TOKEN_KEYS = ['visapilot_access_token', 'access_token', 'accessToken', 'token']
const REFRESH_TOKEN_KEYS = ['visapilot_refresh_token', 'refresh_token', 'refreshToken']
const AUTH_ERROR_MESSAGE = 'Your session has expired. Please log in again.'

let authFailureHandler = null
let refreshPromise = null

class ApiError extends Error {
  constructor(message, { status, payload, fieldErrors, code } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.payload = payload
    this.fieldErrors = fieldErrors || {}
    this.code = code
  }
}

function normalizeToken(value) {
  if (typeof value !== 'string') return ''
  const token = value.trim()
  if (!token) return ''

  const normalized = token.toLowerCase()
  if (normalized === 'undefined' || normalized === 'null') return ''
  return token
}

function decodeJwtPayload(token) {
  const parts = token.split('.')
  if (parts.length < 2) return null

  try {
    const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/')
    const padded = `${base64}${'='.repeat((4 - (base64.length % 4)) % 4)}`
    return JSON.parse(atob(padded))
  } catch {
    return null
  }
}

function getJwtTokenType(token) {
  const payload = decodeJwtPayload(token)
  if (!payload || typeof payload !== 'object') return ''
  return typeof payload.token_type === 'string' ? payload.token_type.toLowerCase() : ''
}

function readToken(keys) {
  for (const key of keys) {
    const token = normalizeToken(localStorage.getItem(key) || sessionStorage.getItem(key) || '')
    if (token) return token
  }
  return ''
}

function writeToken(keys, value) {
  const token = normalizeToken(value)
  for (const key of keys) {
    if (token) {
      localStorage.setItem(key, token)
      sessionStorage.removeItem(key)
    } else {
      localStorage.removeItem(key)
      sessionStorage.removeItem(key)
    }
  }
}

export function getStoredAccessToken() {
  return readToken(ACCESS_TOKEN_KEYS)
}

export function getStoredRefreshToken() {
  return readToken(REFRESH_TOKEN_KEYS)
}

export function saveAuthTokens({ access, refresh }) {
  writeToken(ACCESS_TOKEN_KEYS, access)
  writeToken(REFRESH_TOKEN_KEYS, refresh)
}

export function clearAuthTokens() {
  writeToken(ACCESS_TOKEN_KEYS, '')
  writeToken(REFRESH_TOKEN_KEYS, '')
}

export function setAuthFailureHandler(handler) {
  authFailureHandler = typeof handler === 'function' ? handler : null
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

function isJwtAuthError(payload) {
  const detail = String(payload?.detail || payload?.message || '').toLowerCase()
  const code = String(payload?.code || '').toLowerCase()
  return (
    code === 'token_not_valid' ||
    detail.includes('token not valid') ||
    detail.includes('given token not valid') ||
    detail.includes('token is invalid') ||
    detail.includes('token has expired')
  )
}

function buildMessage(status, payload, fieldErrors) {
  if (isJwtAuthError(payload)) return AUTH_ERROR_MESSAGE
  if (payload?.message) return payload.message
  if (payload?.detail) return String(payload.detail)

  const firstField = Object.keys(fieldErrors)[0]
  if (firstField && fieldErrors[firstField]?.length) {
    return fieldErrors[firstField][0]
  }

  return `Request failed (${status})`
}

async function parseResponsePayload(response) {
  const contentType = response.headers.get('content-type') || ''
  if (contentType.includes('application/json')) {
    try {
      return await response.json()
    } catch {
      return {}
    }
  }

  const text = await response.text()
  return text ? { detail: text } : {}
}

async function refreshAccessToken() {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const refreshToken = getStoredRefreshToken()
      if (!refreshToken || getJwtTokenType(refreshToken) === 'access') {
        throw new ApiError(AUTH_ERROR_MESSAGE, { status: 401, code: 'invalid_refresh_token' })
      }

      const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: defaultHeaders,
        body: JSON.stringify({ refresh: refreshToken }),
      })

      const payload = await parseResponsePayload(response)

      if (!response.ok) {
        throw new ApiError(AUTH_ERROR_MESSAGE, {
          status: response.status,
          payload,
          fieldErrors: normalizeFieldErrors(payload),
          code: 'refresh_failed',
        })
      }

      const access = normalizeToken(payload?.access || payload?.access_token || '')
      if (!access || getJwtTokenType(access) === 'refresh') {
        throw new ApiError(AUTH_ERROR_MESSAGE, { status: 401, payload, code: 'invalid_access_token' })
      }

      saveAuthTokens({ access, refresh: refreshToken })
      return access
    })().finally(() => {
      refreshPromise = null
    })
  }

  return refreshPromise
}

function handleAuthFailure() {
  clearAuthTokens()
  if (authFailureHandler) authFailureHandler()
}

async function request(path, options = {}) {
  const {
    requiresAuth = false,
    skipAuthRetry = false,
    skipAuthHeader = false,
    headers: customHeaders = {},
    ...restOptions
  } = options

  const headers = {
    ...defaultHeaders,
    ...customHeaders,
  }

  if (requiresAuth && !skipAuthHeader) {
    const accessToken = getStoredAccessToken()
    const tokenType = getJwtTokenType(accessToken)
    if (!accessToken || tokenType === 'refresh') {
      handleAuthFailure()
      throw new ApiError(AUTH_ERROR_MESSAGE, { status: 401, code: 'invalid_or_missing_access_token' })
    }
    headers.Authorization = `Bearer ${accessToken}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...restOptions,
    headers,
  })

  const payload = await parseResponsePayload(response)

  if (!response.ok) {
    const fieldErrors = normalizeFieldErrors(payload)

     if (requiresAuth && !skipAuthRetry && response.status === 401 && isJwtAuthError(payload)) {
      try {
        await refreshAccessToken()
        return request(path, { ...options, skipAuthRetry: true })
      } catch {
        handleAuthFailure()
        throw new ApiError(AUTH_ERROR_MESSAGE, { status: 401, payload, fieldErrors, code: 'session_expired' })
      }
    }

    const message = buildMessage(response.status, payload, fieldErrors)
    throw new ApiError(message, { status: response.status, payload, fieldErrors })
  }

  return payload
}

export const api = {
  apiBaseUrl: API_BASE_URL,
  login: (credentials = {}) => {
    const normalizedEmail = (credentials.email || credentials.username || '').trim().toLowerCase()
    const password = credentials.password || ''
    return request('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({
        email: normalizedEmail,
        password,
      }),
      requiresAuth: false,
    })
  },
  register: (data = {}) => {
  const normalizedEmail = (data.email || '').trim().toLowerCase()

    return request('/auth/register/', {
      method: 'POST',
      body: JSON.stringify({
        full_name: data.full_name?.trim(),
        email: normalizedEmail,
        password: data.password,
        password_confirm: data.password_confirm || '',
      }),
      requiresAuth: false,
    })
  },
  refreshToken: () => refreshAccessToken(),
  getProfile: () => request('/auth/profile/', { requiresAuth: true }),
  submitVisaAssessment: (_token, data) =>
    request('/scoring/assessment/', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),
  generateSOP: (_token, data) =>
    request('/ai/sop-generator/', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),
  analyzeRefusal: (_token, data) =>
    request('/ai/refusal-analysis/', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),
  initializePayment: (_token, data) =>
    request('/payments/initialize/', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
    }),
  verifyPayment: (_token, reference) =>
    request(`/payments/verify/?reference=${encodeURIComponent(reference)}`, {
      requiresAuth: true,
    }),
  currentSubscription: () =>
    request('/payments/current-subscription/', {
      requiresAuth: true,
    }),
  adminOverview: () =>
    request('/admin/overview/', {
      requiresAuth: true,
    }),
  adminListUsers: (_token, params = {}) => {
    const query = new URLSearchParams(params).toString()
    return request(`/admin/users/${query ? `?${query}` : ''}`, {
      requiresAuth: true,
    })
  },
  adminCreateUser: (_token, data) =>
    request('/admin/users/', {
      method: 'POST',
      body: JSON.stringify(data),
      requiresAuth: true,
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
  const rawMessage = String(error?.message || '')
  const lowered = rawMessage.toLowerCase()
  if (
    error?.status === 401 ||
    error?.code === 'session_expired' ||
    lowered.includes('given token not valid') ||
    lowered.includes('token not valid')
  ) {
    return AUTH_ERROR_MESSAGE
  }

  if (error?.fieldErrors && Object.keys(error.fieldErrors).length) {
    return formatFieldErrors(error.fieldErrors)
  }
  return rawMessage || fallback
}

export { ApiError, AUTH_ERROR_MESSAGE }