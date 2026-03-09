import React from 'react'
import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import '../styles/Blog.css'
import { blogAPI } from '../services/api'

const Blog = () => {
  const { data: blogs = [], isLoading, isError, error } = useQuery({
    queryKey: ['blog'],
    queryFn: async () => {
      const data = await blogAPI.getAll()
      return Array.isArray(data) ? data : []
    },
  })

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
      <section id="blog" className="blog section section-alt">
        <div className="container">
          <div className="blog-header">
            <span className="section-label">WRITING</span>
            <h2 className="section-title">Latest Posts</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            Loading blogs...
          </div>
        </div>
      </section>
    )
  }

  if (isError) {
    const errorMessage = error?.response?.data?.detail || error?.message || 'Failed to load blogs. Please check if the backend server is running.'
    return (
      <section id="blog" className="blog section section-alt">
        <div className="container">
          <div className="blog-header">
            <span className="section-label">WRITING</span>
            <h2 className="section-title">Latest Posts</h2>
          </div>
          <div style={{ textAlign: 'center', padding: '2rem', color: '#ef4444' }}>
            {errorMessage}
          </div>
        </div>
      </section>
    )
  }

  const displayedBlogs = blogs.slice(0, 6)
  const hasMoreBlogs = blogs.length > 6

  return (
    <section id="blog" className="blog section section-alt">
      <div className="container">
        <div className="blog-header">
          <span className="section-label">WRITING</span>
          <h2 className="section-title">Latest Posts</h2>
        </div>
        {displayedBlogs.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No blog posts available at the moment.
          </div>
        ) : (
          <>
            <div className="blog-grid">
              {displayedBlogs.map((blog) => (
                <div key={blog.id || blog._id} className="blog-card">
                  {blog.cover_image_url && (
                    <div className="blog-image-wrapper">
                      <img
                        src={blog.cover_image_url}
                        alt={blog.title}
                        className="blog-image"
                      />
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
                      state={{ from: 'home' }}
                      className="blog-more-info-link"
                    >
                      More Info →
                    </Link>
                  </div>
                </div>
              ))}
            </div>
            {hasMoreBlogs && (
              <div style={{ textAlign: 'center', marginTop: '3rem' }}>
                <Link to="/blog" className="view-more-blogs-btn">
                  View More Blogs +{blogs.length - 6}
                </Link>
              </div>
            )}
          </>
        )}
      </div>
    </section>
  )
}

export default Blog
