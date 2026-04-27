import React from 'react'

export default function AlertMessage({ type = 'info', message }) {
  if (!message) return null
  return <p className={`alert alert-${type}`}>{message}</p>
}