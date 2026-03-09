import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Projects.css'
import { projectsAPI } from '../services/api'

const Projects = () => {
  const { data: projects = [], isLoading, isError, error } = useQuery({
    queryKey: ['projects'],
    queryFn: async () => {
      const data = await projectsAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  if (isLoading) {
    return (
      <section id="projects" className="projects section">
        <div className="container">
          <div className="projects-header">
            <span className="section-label">WORK</span>
            <h2 className="section-title">Selected Projects</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading projects...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load projects. Please check if the backend server is running.'
    return (
      <section id="projects" className="projects section">
        <div className="container">
          <div className="projects-header">
            <span className="section-label">WORK</span>
            <h2 className="section-title">Selected Projects</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  const displayedProjects = projects.slice(0, 6)
  const hasMoreProjects = projects.length > 6
  const moreProjectsCount = projects.length - 6

  return (
    <section id="projects" className="projects section">
      <div className="container">
        <div className="projects-header">
          <span className="section-label">WORK</span>
          <h2 className="section-title">Selected Projects</h2>
        </div>
        {displayedProjects.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No projects available at the moment.
          </div>
        ) : (
          <>
            <div className="projects-grid">
              {displayedProjects.map((project) => {
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
                        state={{ from: 'home' }}
                        className="project-more-info-link"
                      >
                        More Info →
                      </Link>
                    </div>
                  </div>
                )
              })}
            </div>
            {hasMoreProjects && (
              <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <Link to="/projects" className="view-more-projects-btn">
                  View More Projects +{moreProjectsCount}
                </Link>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}

export default Projects
