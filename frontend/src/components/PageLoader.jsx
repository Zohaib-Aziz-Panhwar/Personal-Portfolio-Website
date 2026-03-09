import React from 'react'

const PageLoader = () => (
  <div className="page-loader" style={{
    minHeight: '60vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: '8rem',
  }}>
    <div style={{ textAlign: 'center', color: 'var(--text-secondary)' }}>
      <div style={{
        width: 40,
        height: 40,
        border: '3px solid var(--border-color)',
        borderTopColor: 'var(--accent-primary)',
        borderRadius: '50%',
        animation: 'spin 0.8s linear infinite',
        margin: '0 auto 1rem',
      }} />
      <p style={{ margin: 0, fontSize: '0.95rem' }}>Loading...</p>
    </div>
    <style>{`
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
    `}</style>
  </div>
)

export default PageLoader
