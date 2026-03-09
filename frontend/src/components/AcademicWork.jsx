import React from 'react'
import { Link } from 'react-router-dom'
import ResearchCard from './ResearchCard'
import { useQuery } from '@tanstack/react-query'
import { caseStudiesAPI } from '../services/api'
import '../styles/AcademicWork.css'

const AcademicWork = () => {
  const { data: caseStudies = [], isLoading, isError, error } = useQuery({
    queryKey: ['caseStudies'],
    queryFn: async () => {
      const data = await caseStudiesAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  if (isLoading) {
    return (
      <section id="case-study" className="academic-work section section-alt">
        <div className="container">
          <div className="academic-work-header">
            <span className="section-label">CASE STUDY</span>
            <h2 className="section-title">Academic Work</h2>
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
      <section id="case-study" className="academic-work section section-alt">
        <div className="container">
          <div className="academic-work-header">
            <span className="section-label">CASE STUDY</span>
            <h2 className="section-title">Academic Work</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  const displayedCaseStudies = caseStudies.slice(0, 3)
  const hasMoreCaseStudies = caseStudies.length > 3
  const moreCaseStudiesCount = caseStudies.length - 3

  return (
    <section id="case-study" className="academic-work section section-alt">
      <div className="container">
        <div className="academic-work-header">
          <span className="section-label">CASE STUDY</span>
          <h2 className="section-title">Academic Work</h2>
        </div>
        {caseStudies.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No case studies available at the moment.
          </div>
        ) : (
          <>
            <div className="research-cards-grid">
              {displayedCaseStudies.map((item) => (
                <ResearchCard key={item.id || item._id} caseStudy={item} />
              ))}
            </div>
            {hasMoreCaseStudies && (
              <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <Link to="/case-studies" className="view-more-projects-btn">
                  View More Case Studies +{moreCaseStudiesCount}
                </Link>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}

export default AcademicWork
