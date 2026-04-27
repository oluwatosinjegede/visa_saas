import React from 'react'

export default class AppErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, message: '' }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, message: error?.message || 'Unknown rendering error' }
  }

  componentDidCatch(error, errorInfo) {
    console.error('Frontend render crashed:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <main className="homepage">
          <section className="section">
            <h2>We hit a rendering error</h2>
            <p className="status-msg error">
              The app failed to render. Check the browser console for details.
            </p>
            <p className="status-msg">Error: {this.state.message}</p>
          </section>
        </main>
      )
    }

    return this.props.children
  }
}
