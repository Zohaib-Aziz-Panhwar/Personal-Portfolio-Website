import React from 'react'
import { useParams, Link, useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Projects.css'
import '../styles/Research.css'
import { caseStudiesAPI } from '../services/api'

const CaseStudyDetail = () => {
  const { slug } = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const { data: caseStudy, isLoading, isError, error } = useQuery({
    queryKey: ['caseStudy', slug],
    queryFn: () => caseStudiesAPI.getBySlug(slug),
    enabled: !!slug,
  })

  const getBackLink = () => {
    const from = location.state?.from
    if (from === 'home') {
      return { path: '/', text: '← Back to Home', scrollTo: 'case-study' }
    }
    if (from === 'case-studies') {
      return { path: '/case-studies', text: '← Back to Case Studies', scrollTo: null }
    }
    return { path: '/case-studies', text: '← Back to Case Studies', scrollTo: null }
  }

  const backLink = getBackLink()

  const handleBackClick = (e) => {
    e.preventDefault()
    if (backLink.scrollTo) {
      sessionStorage.setItem('scrollToSection', backLink.scrollTo)
    }
    navigate(backLink.path)
  }

  if (isLoading) {
    return (
      <section className="project-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading case study...
          </div>
        </div>
      </section>
    )
  }

  if (isError || !caseStudy) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load case study.'
    return (
      <section className="project-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage || 'Case study not found'}
          </div>
          <div style={{ textAlign: 'center', marginTop: '1rem' }}>
            <Link to={backLink.path} onClick={handleBackClick} style={{ color: 'var(--primary-color)' }}>
              {backLink.text}
            </Link>
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="project-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
      <div className="container">
        <div style={{ marginBottom: '2rem' }}>
          <Link
            to={backLink.path}
            onClick={handleBackClick}
            style={{
              color: 'var(--primary-color)',
              textDecoration: 'none',
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            {backLink.text}
          </Link>
        </div>

        <article className="project-detail-content">
          {caseStudy.cover_image && (
            <div className="project-detail-image-wrapper">
              <img
                src={caseStudy.cover_image}
                alt={caseStudy.title}
                className="project-detail-image"
              />
            </div>
          )}

          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1rem', flexWrap: 'wrap' }}>
            <h1 className="project-detail-title" style={{ margin: 0, flex: 1 }}>{caseStudy.title}</h1>
            <span className={`research-status research-status-${caseStudy.status?.toLowerCase() || 'draft'}`}>
              {caseStudy.status || 'Draft'}
            </span>
          </div>

          {caseStudy.short_description && (
            <div className="project-detail-description">
              <p>{caseStudy.short_description}</p>
            </div>
          )}

          {(caseStudy.author || caseStudy.publication_date) && (
            <div style={{
              display: 'flex',
              gap: '1.5rem',
              marginBottom: '2rem',
              paddingBottom: '1.5rem',
              borderBottom: '1px solid var(--border-color)',
              flexWrap: 'wrap'
            }}>
              {caseStudy.author && (
                <div>
                  <strong style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Author:</strong>
                  <span style={{ marginLeft: '0.5rem', color: 'var(--text-primary)' }}>{caseStudy.author}</span>
                </div>
              )}
              {caseStudy.publication_date && (
                <div>
                  <strong style={{ color: 'var(--text-secondary)', fontSize: 'var(--font-size-sm)' }}>Published:</strong>
                  <span style={{ marginLeft: '0.5rem', color: 'var(--text-primary)' }}>
                    {new Date(caseStudy.publication_date).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}
                  </span>
                </div>
              )}
            </div>
          )}

          {caseStudy.description && (
            <div className="project-detail-section">
              <h3>Description</h3>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8' }}>{caseStudy.description}</p>
            </div>
          )}

          {caseStudy.tags && caseStudy.tags.length > 0 && (
            <div className="project-detail-section">
              <h3>Tags</h3>
              <div className="project-tags">
                {caseStudy.tags.map((tag, tagIndex) => (
                  <span key={tagIndex} className="project-tag">{tag}</span>
                ))}
              </div>
            </div>
          )}
        </article>
      </div>
    </section>
  )
}

export default CaseStudyDetail
