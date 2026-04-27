import React from 'react'

export default function LoadingSpinner({ label = 'Loading...' }) {
  return <div className="loading-spinner">{label}</div>
}