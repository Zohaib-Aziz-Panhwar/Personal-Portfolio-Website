import React from 'react'
import { useParams, Link, useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Projects.css'
import { projectsAPI } from '../services/api'

const ProjectDetail = () => {
  const { slug } = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const { data: project, isLoading, isError, error } = useQuery({
    queryKey: ['project', slug],
    queryFn: () => projectsAPI.getBySlug(slug),
    enabled: !!slug,
  })

  const getBackLink = () => {
    const from = location.state?.from
    if (from === 'home') {
      return { path: '/', text: '← Back to Home', scrollTo: 'projects' }
    }
    if (from === 'projects') {
      return { path: '/projects', text: '← Back to Projects', scrollTo: null }
    }
    return { path: '/projects', text: '← Back to Projects', scrollTo: null }
  }

  const backLink = getBackLink()

  const handleBackClick = (e) => {
    e.preventDefault()
    navigate(backLink.path)
    if (backLink.scrollTo) {
      setTimeout(() => {
        const element = document.getElementById(backLink.scrollTo)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 100)
    }
  }

  if (isLoading) {
    return (
      <section className="project-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading project...
          </div>
        </div>
      </section>
    )
  }

  if (isError || !project) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load project.'
    return (
      <section className="project-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage || 'Project not found'}
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
          <h1 className="project-detail-title">{project.title}</h1>

          {(project.cover_image || project.image_url) && (
            <div className="project-detail-image-wrapper" style={{ marginBottom: '2rem' }}>
              <img
                src={project.cover_image || project.image_url}
                alt={project.title}
                className="project-detail-image"
              />
            </div>
          )}

          {project.detailed_description && (
            <div className="project-detail-description" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>About the Project</h2>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>{project.detailed_description}</p>
            </div>
          )}

          {project.problem_statement && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>Problem</h2>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>{project.problem_statement}</p>
            </div>
          )}

          {project.solutions && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>Solution</h2>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>{project.solutions}</p>
            </div>
          )}

          {project.system_architecture && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>System Architecture</h2>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>{project.system_architecture}</p>
            </div>
          )}

          {project.challenges && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>Challenges</h2>
              <p style={{ whiteSpace: 'pre-line', lineHeight: '1.8', fontSize: '1.1rem' }}>{project.challenges}</p>
            </div>
          )}

          {project.key_features && project.key_features.length > 0 && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>Key Features</h2>
              <ul className="project-features-list">
                {project.key_features.map((feature, featureIndex) => (
                  <li key={featureIndex} style={{ marginBottom: '0.5rem' }}>{feature}</li>
                ))}
              </ul>
            </div>
          )}

          {project.tech_stack && project.tech_stack.length > 0 && (
            <div className="project-detail-section" style={{ marginBottom: '2rem' }}>
              <h2 style={{ marginBottom: '1rem', fontSize: '1.5rem', color: 'var(--text-primary)' }}>Tech Stack</h2>
              <div className="project-tags">
                {project.tech_stack.map((tag, tagIndex) => (
                  <span key={tagIndex} className="project-tag">{tag}</span>
                ))}
              </div>
            </div>
          )}

          <div className="project-detail-links" style={{ marginTop: '2rem' }}>
            {project.github_link && (
              <a href={project.github_link} target="_blank" rel="noopener noreferrer" className="project-link-btn">
                View on GitHub
              </a>
            )}
            {project.live_demo && (
              <a href={project.live_demo} target="_blank" rel="noopener noreferrer" className="project-link-btn">
                Live Demo
              </a>
            )}
            {project.video_demo && (
              <a href={project.video_demo} target="_blank" rel="noopener noreferrer" className="project-link-btn">
                Video Demo
              </a>
            )}
          </div>
        </article>
      </div>
    </section>
  )
}

export default ProjectDetail
