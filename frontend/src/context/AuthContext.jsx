import React, { createContext, useContext, useMemo, useState } from 'react'
import { api, getApiErrorMessage } from '../services/api'

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

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(() => localStorage.getItem(ACCESS_TOKEN_KEY) || '')
  const [refreshToken, setRefreshToken] = useState(() => localStorage.getItem(REFRESH_TOKEN_KEY) || '')
  const [profile, setProfile] = useState(() => readJson(PROFILE_KEY))
  const [loading, setLoading] = useState(false)
  const [authError, setAuthError] = useState('')

  const isAuthenticated = Boolean(accessToken)

  const persist = ({ access, refresh, user }) => {
    setAccessToken(access)
    setRefreshToken(refresh)
    setProfile(user)
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
    localStorage.setItem(PROFILE_KEY, JSON.stringify(user || {}))
  }

  const clear = () => {
    setAccessToken('')
    setRefreshToken('')
    setProfile(null)
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(PROFILE_KEY)
  }

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

  const logout = () => clear()

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
