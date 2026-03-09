import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Certifications.css'
import { certificatesAPI } from '../services/api'

const Certifications = () => {
  const { data: certificates = [], isLoading, isError, error } = useQuery({
    queryKey: ['certificates'],
    queryFn: async () => {
      const data = await certificatesAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  const formatDate = (month, year) => {
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December']
    return `${monthNames[month - 1]} ${year}`
  }

  if (isLoading) {
    return (
      <section id="certifications" className="certifications section section-alt">
        <div className="container">
          <div className="certifications-header">
            <span className="section-label">CERTIFICATIONS</span>
            <h2 className="section-title">Professional Certifications</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading certificates...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load certificates. Please check if the backend server is running.'
    return (
      <section id="certifications" className="certifications section section-alt">
        <div className="container">
          <div className="certifications-header">
            <span className="section-label">CERTIFICATIONS</span>
            <h2 className="section-title">Professional Certifications</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  const displayedCertificates = certificates.slice(0, 3)
  const hasMoreCertificates = certificates.length > 3

  return (
    <section id="certifications" className="certifications section section-alt">
      <div className="container">
        <div className="certifications-header">
          <span className="section-label">CERTIFICATIONS</span>
          <h2 className="section-title">Professional Certifications</h2>
        </div>
        {displayedCertificates.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No certificates available at the moment.
          </div>
        ) : (
          <>
            <div className="certifications-grid">
              {displayedCertificates.map((cert) => (
                <div key={cert.id || cert._id} className="certification-card">
                  <div className="certification-icon">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      <circle cx="12" cy="12" r="2" fill="currentColor"/>
                    </svg>
                  </div>
                  <div className="certification-content">
                    <h3 className="certification-title">{cert.title}</h3>
                    <p className="certification-issuer">{cert.company}</p>
                    <p className="certification-date">
                      {formatDate(cert.completion_month, cert.completion_year)}
                    </p>
                    <p className="certification-description">{cert.short_description}</p>
                    <a
                      href={cert.certificate_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="certification-link"
                    >
                      <span>View Certificate</span>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M7 17L17 7M7 7H17V17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                      </svg>
                    </a>
                  </div>
                </div>
              ))}
            </div>
            {hasMoreCertificates && (
              <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <Link to="/certificates" className="view-more-projects-btn">
                  View More Certificates +{certificates.length - 3}
                </Link>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}

export default Certifications
