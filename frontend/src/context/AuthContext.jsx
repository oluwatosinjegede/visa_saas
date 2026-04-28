import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { routes } from '../constants/routes'
import {
  api,
  clearAuthTokens,
  getApiErrorMessage,
  getStoredAccessToken,
  getStoredRefreshToken,
  saveAuthTokens,
  setAuthFailureHandler,
} from '../services/api'

const ACCESS_TOKEN_KEY = 'visapilot_access_token'
const REFRESH_TOKEN_KEY = 'visapilot_refresh_token'
const PROFILE_KEY = 'visapilot_profile'

const AuthContext = createContext(null)

function readJson(key) {
  const raw = localStorage.getItem(key)
  if (!raw) return null
  try {
    return JSON.parse(raw)
  } catch {
    return null
  }
}

function normalizeToken(token) {
  if (typeof token !== 'string') return ''
  const value = token.trim()
  if (!value) return ''
  const lowered = value.toLowerCase()
  if (lowered === 'undefined' || lowered === 'null') return ''
  return value
}

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(() => getStoredAccessToken())
  const [refreshToken, setRefreshToken] = useState(() => getStoredRefreshToken())
  const [profile, setProfile] = useState(() => readJson(PROFILE_KEY))
  const [loading, setLoading] = useState(false)
  const [authError, setAuthError] = useState('')

  const isAuthenticated = Boolean(accessToken)

  const persist = ({ access, refresh, user }) => {
    const normalizedAccess = normalizeToken(access)
    const normalizedRefresh = normalizeToken(refresh)

    setAccessToken(normalizedAccess)
    setRefreshToken(normalizedRefresh)
    setProfile(user)

    saveAuthTokens({ access: normalizedAccess, refresh: normalizedRefresh })
    localStorage.setItem(ACCESS_TOKEN_KEY, normalizedAccess)
    localStorage.setItem(REFRESH_TOKEN_KEY, normalizedRefresh)
    localStorage.setItem(PROFILE_KEY, JSON.stringify(user || {}))
  }

  const clear = (shouldRedirect = false) => {
    setAccessToken('')
    setRefreshToken('')
    setProfile(null)
    clearAuthTokens()
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(PROFILE_KEY)

    if (shouldRedirect && window.location.pathname !== routes.login) {
      window.history.pushState({}, '', routes.login)
      window.dispatchEvent(new PopStateEvent('popstate'))
    }
  }

  useEffect(() => {
    setAuthFailureHandler(() => {
      setAuthError('Your session has expired. Please log in again.')
      clear(true)
    })

    return () => setAuthFailureHandler(null)
  }, [])

  const login = async (credentials) => {
    setLoading(true)
    setAuthError('')
    try {
      const result = await api.login(credentials)
      persist({
        access: result.access || result.access_token || '',
        refresh: result.refresh || result.refresh_token || '',
        user: result.user || result.profile || {},
      })
      return { ok: true }
    } catch (error) {
      const message = getApiErrorMessage(error, 'Login failed')
      setAuthError(message)
      return { ok: false, error: message }
    } finally {
      setLoading(false)
    }
  }

  const register = async (data) => {
    setLoading(true)
    setAuthError('')
    try {
      const result = await api.register(data)
      persist({
        access: result.access || result.access_token || '',
        refresh: result.refresh || result.refresh_token || '',
        user: result.user || result.profile || {},
      })
      return { ok: true }
    } catch (error) {
      const message = getApiErrorMessage(error, 'Registration failed')
      setAuthError(message)
      return { ok: false, error: message }
    } finally {
      setLoading(false)
    }
  }

  const logout = () => clear(true)

  const value = useMemo(
    () => ({
      accessToken,
      refreshToken,
      profile,
      isAuthenticated,
      loading,
      authError,
      login,
      register,
      logout,
    }),
    [accessToken, refreshToken, profile, isAuthenticated, loading, authError],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return ctx
}
