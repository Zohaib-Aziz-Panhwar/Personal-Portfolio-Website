import React from 'react'
import { useParams, Link, useLocation, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Blog.css'
import { blogAPI } from '../services/api'

const BlogDetail = () => {
  const { slug } = useParams()
  const location = useLocation()
  const navigate = useNavigate()

  const { data: blog, isLoading, isError, error } = useQuery({
    queryKey: ['blogPost', slug],
    queryFn: () => blogAPI.getBySlug(slug),
    enabled: !!slug,
  })

  const getBackLink = () => {
    const from = location.state?.from
    if (from === 'home') {
      return { path: '/', text: '← Back to Home', scrollTo: 'blog' }
    }
    if (from === 'blog') {
      return { path: '/blog', text: '← Back to Blogs', scrollTo: null }
    }
    return { path: '/blog', text: '← Back to Blogs', scrollTo: null }
  }

  const backLink = getBackLink()

  const handleBackClick = (e) => {
    e.preventDefault()
    if (backLink.scrollTo) {
      sessionStorage.setItem('scrollToSection', backLink.scrollTo)
    }
    navigate(backLink.path)
  }

  const formatDate = (dateString) => {
    if (!dateString) return ''
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      })
    } catch {
      return dateString
    }
  }

  if (isLoading) {
    return (
      <section className="blog-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading blog...
          </div>
        </div>
      </section>
    )
  }

  if (isError || !blog) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load blog.'
    return (
      <section className="blog-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
        <div className="container">
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage || 'Blog not found'}
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
    <section className="blog-detail section" style={{ minHeight: '60vh', paddingTop: '8rem' }}>
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

        <article className="blog-detail-content">
          {blog.cover_image_url && (
            <div className="blog-detail-image-wrapper">
              <img src={blog.cover_image_url} alt={blog.title} className="blog-detail-image" />
            </div>
          )}

          <div className="blog-detail-meta">
            <span className="blog-detail-date">
              {formatDate(blog.published_date || blog.created_at)}
            </span>
            {blog.reading_time && (
              <span className="blog-detail-reading-time">• {blog.reading_time}</span>
            )}
            {blog.author && (
              <span className="blog-detail-author">• By {blog.author}</span>
            )}
          </div>

          <h1 className="blog-detail-title">{blog.title}</h1>

          <div className="blog-detail-content-text">
            <div style={{ whiteSpace: 'pre-wrap' }}>{blog.content}</div>
          </div>

          {blog.tags && blog.tags.length > 0 && (
            <div className="blog-detail-section">
              <h3>Tags</h3>
              <div className="blog-tags">
                {blog.tags.map((tag, tagIndex) => (
                  <span key={tagIndex} className="blog-tag">{tag}</span>
                ))}
              </div>
            </div>
          )}
        </article>
      </div>
    </section>
  )
}

export default BlogDetail
