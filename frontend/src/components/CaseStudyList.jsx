import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Research.css'
import { caseStudiesAPI } from '../services/api'

const CaseStudyList = () => {
  const navigate = useNavigate()
  const { data: caseStudies = [], isLoading, isError, error } = useQuery({
    queryKey: ['caseStudies'],
    queryFn: async () => {
      const data = await caseStudiesAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  const handleBackToHome = (e) => {
    e.preventDefault()
    sessionStorage.setItem('scrollToSection', 'case-study')
    navigate('/')
  }

  const backLinkStyle = {
    color: 'var(--primary-color, var(--accent-primary))',
    textDecoration: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem'
  }

  if (isLoading) {
    return (
      <section className="research section section-alt" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="research-header">
            <h1 className="section-title">Case Studies</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading case studies...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load case studies.'
    return (
      <section className="research section section-alt" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="research-header">
            <h1 className="section-title">Case Studies</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="research section section-alt" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
      <div className="container">
        <div style={{ marginBottom: '2rem' }}>
          <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>
            ← Back to Home
          </Link>
        </div>
        <div className="research-header">
          <h1 className="section-title">Case Studies</h1>
        </div>
        {caseStudies.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No case studies available at the moment.
          </div>
        ) : (
          <div className="research-list">
            {caseStudies.map((item) => (
              <div key={item.id || item._id} className="research-card">
                <div className="research-content">
                  <h3 className="research-title">{item.title}</h3>
                  <p className="research-description">{item.short_description}</p>
                  <Link
                    to={`/case-studies/${item.slug || item.id || item._id}`}
                    state={{ from: 'case-studies' }}
                    className="research-card-link"
                  >
                    More Info →
                  </Link>
                </div>
                <span className={`research-status research-status-${item.status?.toLowerCase() || 'draft'}`}>
                  {item.status || 'Draft'}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

export default CaseStudyList
