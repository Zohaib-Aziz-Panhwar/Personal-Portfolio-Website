import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Projects.css'
import { projectsAPI } from '../services/api'

const ProjectsList = () => {
  const navigate = useNavigate()
  const { data: projects = [], isLoading, isError, error } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const data = await projectsAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  const handleBackToHome = (e) => {
    e.preventDefault()
    navigate('/')
    setTimeout(() => {
      const element = document.getElementById('projects')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }
    }, 100)
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
      <section className="projects section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="projects-header">
            <h1 className="section-title">Projects</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading projects...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load projects.'
    return (
      <section className="projects section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="projects-header">
            <h1 className="section-title">Projects</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="projects section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
      <div className="container">
        <div style={{ marginBottom: '2rem' }}>
          <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>
            ← Back to Home
          </Link>
        </div>
        <div className="projects-header">
          <h1 className="section-title">Projects</h1>
        </div>
        {projects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No projects available at the moment.
          </div>
        ) : (
          <div className="projects-grid">
            {projects.map((project) => {
              const techStack = project.tech_stack || project.tags || []
              const displayedTags = techStack.slice(0, 4)

              return (
                <div key={project.id || project._id} className="project-card">
                  {(project.cover_image || project.image_url) && (
                    <div className="project-image-wrapper">
                      <img
                        src={project.cover_image || project.image_url}
                        alt={project.title}
                        className="project-image"
                      />
                    </div>
                  )}
                  <h3 className="project-title">{project.title}</h3>
                  <p className="project-description">{project.short_description || project.description}</p>
                  <div className="project-card-bottom">
                    {displayedTags.length > 0 && (
                      <div className="project-tags">
                        {displayedTags.map((tag, tagIndex) => (
                          <span key={tagIndex} className="project-tag">{tag}</span>
                        ))}
                        {techStack.length > 4 && (
                          <span className="project-tag" style={{ opacity: 0.7 }}>
                            +{techStack.length - 4} more
                          </span>
                        )}
                      </div>
                    )}
                    <Link
                      to={`/projects/${project.slug || project.id || project._id}`}
                      state={{ from: 'projects' }}
                      className="project-more-info-link"
                    >
                      More Info →
                    </Link>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </section>
  )
}

export default ProjectsList
