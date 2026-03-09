import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Blog.css'
import { blogAPI } from '../services/api'

const BlogList = () => {
  const navigate = useNavigate()
  const { data: blogs = [], isLoading, isError, error } = useQuery({
    queryKey: ['blog'],
    queryFn: async () => {
      const data = await blogAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

  const handleBackToHome = (e) => {
    e.preventDefault()
    sessionStorage.setItem('scrollToSection', 'blog')
    navigate('/')
  }

  const backLinkStyle = {
    color: 'var(--primary-color, var(--accent-primary))',
    textDecoration: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    gap: '0.5rem'
  }

  const formatDate = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    } catch {
      return dateString
    }
  }

  if (isLoading) {
    return (
      <section className="blog section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="blog-header">
            <h1 className="section-title">Blog Posts</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading blogs...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load blogs.'
    return (
      <section className="blog section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ marginBottom: '2rem' }}>
            <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>← Back to Home</Link>
          </div>
          <div className="blog-header">
            <h1 className="section-title">Blog Posts</h1>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  return (
    <section className="blog section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
      <div className="container">
        <div style={{ marginBottom: '2rem' }}>
          <Link to="/" onClick={handleBackToHome} style={backLinkStyle}>
            ← Back to Home
          </Link>
        </div>
        <div className="blog-header">
          <h1 className="section-title">Blog Posts</h1>
        </div>
        {blogs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No blog posts available at the moment.
          </div>
        ) : (
          <div className="blog-grid">
            {blogs.map((blog) => (
              <div key={blog.id || blog._id} className="blog-card">
                {blog.cover_image_url && (
                  <div className="blog-image-wrapper">
                    <img src={blog.cover_image_url} alt={blog.title} className="blog-image" />
                  </div>
                )}
                <div className="blog-card-content">
                  <div className="blog-meta">
                    <span className="blog-date">
                      {formatDate(blog.published_date || blog.created_at)}
                    </span>
                    {blog.reading_time && (
                      <span className="blog-reading-time">{blog.reading_time}</span>
                    )}
                  </div>
                  <h3 className="blog-title">{blog.title}</h3>
                  <p className="blog-description">{blog.short_description}</p>
                  {blog.tags && blog.tags.length > 0 && (
                    <div className="blog-tags">
                      {blog.tags.slice(0, 3).map((tag, tagIndex) => (
                        <span key={tagIndex} className="blog-tag">{tag}</span>
                      ))}
                    </div>
                  )}
                  <Link
                    to={`/blog/${blog.slug}`}
                    state={{ from: 'blog' }}
                    className="blog-more-info-link"
                  >
                    More Info →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

export default BlogList
