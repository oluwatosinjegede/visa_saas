import React from 'react'

export default function FormInput({ label, as = 'input', children, ...props }) {
  const Element = as
  return (
    <label className="form-input">
      <span>{label}</span>
      <Element {...props}>{children}</Element>
    </label>
  )
}