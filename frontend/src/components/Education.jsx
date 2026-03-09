import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { educationAPI } from '../services/api'
import '../styles/Education.css'

const Education = () => {
  const { data: educationItems = [], isLoading } = useQuery({
    queryKey: ['education'],
    queryFn: async () => {
      const data = await educationAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  const formatPeriod = (startYear, endYear) => {
    if (!endYear) {
      return `${startYear} – PRESENT`
    }
    return `${startYear} – ${endYear}`
  }

  if (isLoading) {
    return (
      <section id="education" className="education section">
        <div className="container">
          <div className="education-header">
            <span className="section-label">EDUCATION</span>
            <h2 className="section-title">Academic Background</h2>
          </div>
          <div className="loading">Loading education...</div>
        </div>
      </section>
    )
  }

  return (
    <section id="education" className="education section">
      <div className="container">
        <div className="education-header">
          <span className="section-label">EDUCATION</span>
          <h2 className="section-title">Academic Background</h2>
        </div>
        <div className="education-timeline">
          {educationItems.length === 0 ? (
            <div className="empty-state">No education entries found.</div>
          ) : (
            educationItems.map((item, index) => (
              <div key={item.id || index} className="timeline-item">
                <div className="timeline-dot"></div>
                <div className="timeline-content">
                  <span className="timeline-period">
                    {formatPeriod(item.start_year, item.end_year)}
                  </span>
                  <h3 className="timeline-degree">{item.degree}</h3>
                  <p className="timeline-institution">{item.institution}</p>
                  {item.details && <p className="timeline-details">{item.details}</p>}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  )
}

export default Education
