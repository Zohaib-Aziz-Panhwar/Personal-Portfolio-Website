import React from 'react'
import { Link } from 'react-router-dom'
import StatusBadge from './StatusBadge'
import '../styles/AcademicWork.css'

const ResearchCard = ({ caseStudy }) => {
  return (
    <div className="research-card">
      <div className="research-card-content">
        <h3 className="research-card-title">{caseStudy.title}</h3>
        <p className="research-card-description">{caseStudy.short_description}</p>
        <Link 
          to={`/case-studies/${caseStudy.slug || caseStudy.id || caseStudy._id}`}
          state={{ from: 'home' }}
          className="research-card-link"
        >
          More Info →
        </Link>
      </div>
      <StatusBadge status={caseStudy.status || 'Draft'} />
    </div>
  )
}

export default ResearchCard

