import React, { useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import { routes } from '../constants/routes'

export default function ProtectedRoute({ children, navigate }) {
  const { isAuthenticated } = useAuth()

  useEffect(() => {
    if (!isAuthenticated) {
      navigate(routes.login)
    }
  }, [isAuthenticated, navigate])

  if (!isAuthenticated) return null
  return children
}