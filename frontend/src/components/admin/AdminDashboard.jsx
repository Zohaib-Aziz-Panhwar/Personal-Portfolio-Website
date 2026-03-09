import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { projectsAPI, blogAPI, certificatesAPI, educationAPI, siteSettingsAPI, techStackAPI } from '../../services/api'
import '../../styles/Admin.css'

const AdminDashboard = ({ onLogout }) => {
  const [activeTab, setActiveTab] = useState('projects') // 'projects', 'blogs', 'certificates', or 'education'
  
  // Projects state
  const [projects, setProjects] = useState([])
  const [projectsLoading, setProjectsLoading] = useState(true)
  
  // Blogs state
  const [blogs, setBlogs] = useState([])
  const [blogsLoading, setBlogsLoading] = useState(true)
  
  // Certificates state
  const [certificates, setCertificates] = useState([])
  const [certificatesLoading, setCertificatesLoading] = useState(true)
  
  // Education state
  const [education, setEducation] = useState([])
  const [educationLoading, setEducationLoading] = useState(true)
  
  // Site settings (landing) & tech stack state
  const [siteSettings, setSiteSettings] = useState(null)
  const [siteSettingsLoading, setSiteSettingsLoading] = useState(false)
  const [techStack, setTechStack] = useState([])
  const [techStackLoading, setTechStackLoading] = useState(false)
  const [editingTechItem, setEditingTechItem] = useState(null)
  const [siteFormData, setSiteFormData] = useState({
    welcome_label: '',
    hero_name: '',
    hero_tagline: '',
    hero_description: '',
    about_paragraph_1: '',
    about_paragraph_2: ''
  })
  const [techStackFormData, setTechStackFormData] = useState({ name: '', logo_url: '' })
  
  const [error, setError] = useState('')
  const [showAddForm, setShowAddForm] = useState(false)
  const [editingProject, setEditingProject] = useState(null)
  const [editingBlog, setEditingBlog] = useState(null)
  const [editingCertificate, setEditingCertificate] = useState(null)
  const [editingEducation, setEditingEducation] = useState(null)
  const navigate = useNavigate()

  const [projectFormData, setProjectFormData] = useState({
    title: '',
    slug: '',
    short_description: '',
    detailed_description: '',
    tech_stack: '',
    tools: '',
    github_link: '',
    live_demo: '',
    video_demo: '',
    key_features: '',
    cover_image: '',
    problem: '',
    solution: '',
    system_architecture: '',
    challenges: ''
  })

  const [blogFormData, setBlogFormData] = useState({
    title: '',
    slug: '',
    short_description: '',
    cover_image_url: '',
    tags: '',
    author: '',
    published_date: '',
    reading_time: '',
    content: ''
  })

  const [certificateFormData, setCertificateFormData] = useState({
    title: '',
    company: '',
    completion_month: '',
    completion_year: '',
    short_description: '',
    certificate_url: ''
  })

  const [educationFormData, setEducationFormData] = useState({
    degree: '',
    institution: '',
    start_year: '',
    end_year: '',
    details: ''
  })

  useEffect(() => {
    fetchProjects()
    fetchBlogs()
    fetchCertificates()
    fetchEducation()
    fetchSiteSettings()
    fetchTechStack()
  }, [])

  const fetchSiteSettings = async () => {
    try {
      setSiteSettingsLoading(true)
      const data = await siteSettingsAPI.get()
      setSiteSettings(data || null)
      if (data) {
        setSiteFormData({
          welcome_label: data.welcome_label ?? '',
          hero_name: data.hero_name ?? '',
          hero_tagline: data.hero_tagline ?? '',
          hero_description: data.hero_description ?? '',
          about_paragraph_1: data.about_paragraph_1 ?? '',
          about_paragraph_2: data.about_paragraph_2 ?? ''
        })
      }
    } catch (err) {
      console.error('Error fetching site settings:', err)
      setError('Failed to load site settings')
    } finally {
      setSiteSettingsLoading(false)
    }
  }

  const fetchTechStack = async () => {
    try {
      setTechStackLoading(true)
      const data = await techStackAPI.getAll()
      setTechStack(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Error fetching tech stack:', err)
      setError('Failed to load tech stack')
    } finally {
      setTechStackLoading(false)
    }
  }

  const fetchProjects = async () => {
    try {
      setProjectsLoading(true)
      setError('') // Clear any previous errors
      const data = await projectsAPI.getAll()
      // Ensure data is always an array
      setProjects(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : [])
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError('Failed to load projects: ' + errorMsg)
      console.error('Error fetching projects:', err)
      setProjects([]) // Set empty array on error
    } finally {
      setProjectsLoading(false)
    }
  }

  const fetchBlogs = async () => {
    try {
      setBlogsLoading(true)
      setError('') // Clear any previous errors
      const data = await blogAPI.getAll()
      // Ensure data is always an array
      setBlogs(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : [])
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError('Failed to load blogs: ' + errorMsg)
      console.error('Error fetching blogs:', err)
      setBlogs([]) // Set empty array on error
    } finally {
      setBlogsLoading(false)
    }
  }

  const fetchCertificates = async () => {
    try {
      setCertificatesLoading(true)
      setError('') // Clear any previous errors
      const data = await certificatesAPI.getAll()
      // Ensure data is always an array
      setCertificates(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : [])
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError('Failed to load certificates: ' + errorMsg)
      console.error('Error fetching certificates:', err)
      setCertificates([]) // Set empty array on error
    } finally {
      setCertificatesLoading(false)
    }
  }

  const fetchEducation = async () => {
    try {
      setEducationLoading(true)
      setError('') // Clear any previous errors
      const data = await educationAPI.getAll()
      // Ensure data is always an array
      setEducation(Array.isArray(data) ? data : Array.isArray(data?.data) ? data.data : [])
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError('Failed to load education: ' + errorMsg)
      console.error('Error fetching education:', err)
      setEducation([]) // Set empty array on error
    } finally {
      setEducationLoading(false)
    }
  }

  const handleProjectInputChange = (e) => {
    const { name, value } = e.target
    setProjectFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleBlogInputChange = (e) => {
    const { name, value } = e.target
    setBlogFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleCertificateInputChange = (e) => {
    const { name, value } = e.target
    setCertificateFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleEducationInputChange = (e) => {
    const { name, value } = e.target
    setEducationFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  // Helper function to convert error responses to strings
  const formatError = (error) => {
    if (!error) return 'An unknown error occurred'
    
    // If it's already a string, return it
    if (typeof error === 'string') return error
    
    // If it's an array (FastAPI validation errors)
    if (Array.isArray(error)) {
      return error.map(err => {
        if (typeof err === 'string') return err
        if (err.msg) return err.msg
        if (err.message) return err.message
        return JSON.stringify(err)
      }).join(', ')
    }
    
    // If it's an object
    if (typeof error === 'object') {
      if (error.message) return error.message
      if (error.msg) return error.msg
      if (error.detail) {
        // Recursively handle nested detail
        return formatError(error.detail)
      }
      return JSON.stringify(error)
    }
    
    return String(error)
  }

  // Auto-generate slug from title
  const generateSlug = (title) => {
    return title
      .toLowerCase()
      .trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/[\s_-]+/g, '-')
      .replace(/^-+|-+$/g, '')
  }

  const handleProjectTitleChange = (e) => {
    const title = e.target.value
    setProjectFormData(prev => ({
      ...prev,
      title,
      slug: prev.slug || generateSlug(title)
    }))
  }

  const handleBlogTitleChange = (e) => {
    const title = e.target.value
    setBlogFormData(prev => ({
      ...prev,
      title,
      slug: prev.slug || generateSlug(title)
    }))
  }

  const handleProjectSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      const projectData = {
        title: projectFormData.title.trim(),
        slug: projectFormData.slug.trim(),
        short_description: projectFormData.short_description.trim(),
        detailed_description: projectFormData.detailed_description?.trim() || null,
        tech_stack: projectFormData.tech_stack ? projectFormData.tech_stack.split(',').map(t => t.trim()).filter(t => t) : [],
        tools: projectFormData.tools ? projectFormData.tools.split(',').map(t => t.trim()).filter(t => t) : [],
        github_link: projectFormData.github_link?.trim() || null,
        live_demo: projectFormData.live_demo?.trim() || null,
        video_demo: projectFormData.video_demo?.trim() || null,
        key_features: projectFormData.key_features ? projectFormData.key_features.split(',').map(f => f.trim()).filter(f => f) : [],
        cover_image: projectFormData.cover_image?.trim() || null,
        problem_statement: projectFormData.problem?.trim() || null,
        solutions: projectFormData.solution?.trim() || null,
        system_architecture: projectFormData.system_architecture?.trim() || null,
        challenges: projectFormData.challenges?.trim() || null
      }

      if (editingProject) {
        await projectsAPI.update(editingProject.id || editingProject._id, projectData, adminPassword)
      } else {
        await projectsAPI.create(projectData, adminPassword)
      }

      setProjectFormData({
        title: '',
        slug: '',
        short_description: '',
        detailed_description: '',
        tech_stack: '',
        tools: '',
        github_link: '',
        live_demo: '',
        video_demo: '',
        key_features: '',
        cover_image: '',
        problem: '',
        solution: '',
        system_architecture: '',
        challenges: ''
      })
      setShowAddForm(false)
      setEditingProject(null)
      await fetchProjects() // Use await to ensure it completes
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to save project')
      console.error(err)
    }
  }

  const handleBlogSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      const blogData = {
        title: blogFormData.title.trim(),
        slug: blogFormData.slug.trim(),
        short_description: blogFormData.short_description.trim(),
        cover_image_url: blogFormData.cover_image_url?.trim() || null,
        tags: blogFormData.tags ? blogFormData.tags.split(',').map(t => t.trim()).filter(t => t) : [],
        author: blogFormData.author?.trim() || null,
        published_date: blogFormData.published_date?.trim() || null,
        reading_time: blogFormData.reading_time?.trim() || null,
        content: blogFormData.content.trim()
      }

      if (editingBlog) {
        await blogAPI.update(editingBlog.slug, blogData, adminPassword)
      } else {
        await blogAPI.create(blogData, adminPassword)
      }

      setBlogFormData({
        title: '',
        slug: '',
        short_description: '',
        cover_image_url: '',
        tags: '',
        author: '',
        published_date: '',
        reading_time: '',
        content: ''
      })
      setShowAddForm(false)
      setEditingBlog(null)
      await fetchBlogs() // Use await to ensure it completes
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to save blog')
      console.error(err)
    }
  }

  const handleEditProject = (project) => {
    setEditingProject(project)
    setEditingBlog(null)
    setProjectFormData({
      title: project.title || '',
      slug: project.slug || '',
      short_description: project.short_description || '',
      detailed_description: project.detailed_description || '',
      tech_stack: (project.tech_stack || []).join(', '),
      tools: (project.tools || []).join(', '),
      github_link: project.github_link || '',
      live_demo: project.live_demo || '',
      video_demo: project.video_demo || '',
      key_features: (project.key_features || []).join(', '),
      cover_image: project.cover_image || '',
      problem: project.problem_statement || '',
      solution: project.solutions || '',
      system_architecture: project.system_architecture || '',
      challenges: project.challenges || ''
    })
    setShowAddForm(true)
  }

  const handleEditBlog = (blog) => {
    setEditingBlog(blog)
    setEditingProject(null)
    setBlogFormData({
      title: blog.title || '',
      slug: blog.slug || '',
      short_description: blog.short_description || '',
      cover_image_url: blog.cover_image_url || '',
      tags: (blog.tags || []).join(', '),
      author: blog.author || '',
      published_date: blog.published_date || '',
      reading_time: blog.reading_time || '',
      content: blog.content || ''
    })
    setShowAddForm(true)
  }

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm('Are you sure you want to delete this project?')) {
      return
    }

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      await projectsAPI.delete(projectId, adminPassword)
      fetchProjects()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to delete project')
      console.error(err)
    }
  }

  const handleDeleteBlog = async (slug) => {
    if (!window.confirm('Are you sure you want to delete this blog?')) {
      return
    }

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      await blogAPI.delete(slug, adminPassword)
      fetchBlogs()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to delete blog')
      console.error(err)
    }
  }

  const handleCertificateSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      const certificateData = {
        title: certificateFormData.title.trim(),
        company: certificateFormData.company.trim(),
        completion_month: parseInt(certificateFormData.completion_month),
        completion_year: parseInt(certificateFormData.completion_year),
        short_description: certificateFormData.short_description.trim(),
        certificate_url: certificateFormData.certificate_url.trim()
      }

      if (editingCertificate) {
        await certificatesAPI.update(editingCertificate.id || editingCertificate._id, certificateData, adminPassword)
      } else {
        await certificatesAPI.create(certificateData, adminPassword)
      }

      setCertificateFormData({
        title: '',
        company: '',
        completion_month: '',
        completion_year: '',
        short_description: '',
        certificate_url: ''
      })
      setShowAddForm(false)
      setEditingCertificate(null)
      fetchCertificates()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to save certificate')
      console.error(err)
    }
  }

  const handleEditCertificate = (certificate) => {
    setEditingCertificate(certificate)
    setEditingProject(null)
    setEditingBlog(null)
    setCertificateFormData({
      title: certificate.title || '',
      company: certificate.company || '',
      completion_month: certificate.completion_month || '',
      completion_year: certificate.completion_year || '',
      short_description: certificate.short_description || '',
      certificate_url: certificate.certificate_url || ''
    })
    setShowAddForm(true)
  }

  const handleDeleteCertificate = async (certificateId) => {
    if (!window.confirm('Are you sure you want to delete this certificate?')) {
      return
    }

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      await certificatesAPI.delete(certificateId, adminPassword)
      fetchCertificates()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to delete certificate')
      console.error(err)
    }
  }

  const handleEducationSubmit = async (e) => {
    e.preventDefault()
    setError('')

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      const educationData = {
        degree: educationFormData.degree.trim(),
        institution: educationFormData.institution.trim(),
        start_year: parseInt(educationFormData.start_year),
        end_year: educationFormData.end_year ? parseInt(educationFormData.end_year) : null,
        details: educationFormData.details?.trim() || null
      }

      if (editingEducation) {
        await educationAPI.update(editingEducation.id || editingEducation._id, educationData, adminPassword)
      } else {
        await educationAPI.create(educationData, adminPassword)
      }

      setEducationFormData({
        degree: '',
        institution: '',
        start_year: '',
        end_year: '',
        details: ''
      })
      setShowAddForm(false)
      setEditingEducation(null)
      await fetchEducation()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to save education entry')
      console.error(err)
    }
  }

  const handleEditEducation = (edu) => {
    setEditingEducation(edu)
    setEditingProject(null)
    setEditingBlog(null)
    setEditingCertificate(null)
    setEducationFormData({
      degree: edu.degree || '',
      institution: edu.institution || '',
      start_year: edu.start_year || '',
      end_year: edu.end_year || '',
      details: edu.details || ''
    })
    setShowAddForm(true)
  }

  const handleDeleteEducation = async (educationId) => {
    if (!window.confirm('Are you sure you want to delete this education entry?')) {
      return
    }

    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }

    try {
      await educationAPI.delete(educationId, adminPassword)
      fetchEducation()
      setError('')
    } catch (err) {
      const errorMsg = formatError(err.response?.data?.detail || err.message || err)
      setError(errorMsg || 'Failed to delete education entry')
      console.error(err)
    }
  }

  const handleSiteSettingsSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }
    try {
      await siteSettingsAPI.update({
        welcome_label: siteFormData.welcome_label.trim(),
        hero_name: siteFormData.hero_name.trim(),
        hero_tagline: siteFormData.hero_tagline.trim(),
        hero_description: siteFormData.hero_description.trim(),
        about_paragraph_1: siteFormData.about_paragraph_1.trim(),
        about_paragraph_2: siteFormData.about_paragraph_2.trim()
      }, adminPassword)
      await fetchSiteSettings()
      setError('')
      alert('Landing page content saved.')
    } catch (err) {
      setError(formatError(err.response?.data?.detail || err.message || err) || 'Failed to save site settings')
    }
  }

  const handleTechStackSubmit = async (e) => {
    e.preventDefault()
    setError('')
    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated. Please login again.')
      return
    }
    try {
      if (editingTechItem) {
        await techStackAPI.update(editingTechItem.id || editingTechItem._id, {
          name: techStackFormData.name.trim(),
          logo_url: techStackFormData.logo_url.trim()
        }, adminPassword)
      } else {
        await techStackAPI.create({
          name: techStackFormData.name.trim(),
          logo_url: techStackFormData.logo_url.trim()
        }, adminPassword)
      }
      setTechStackFormData({ name: '', logo_url: '' })
      setEditingTechItem(null)
      setShowAddForm(false)
      await fetchTechStack()
      setError('')
    } catch (err) {
      setError(formatError(err.response?.data?.detail || err.message || err) || 'Failed to save tech stack item')
    }
  }

  const handleEditTechItem = (item) => {
    setEditingTechItem(item)
    setTechStackFormData({ name: item.name || '', logo_url: item.logo_url || '' })
    setShowAddForm(true)
  }

  const handleDeleteTechItem = async (itemId) => {
    if (!window.confirm('Delete this tech stack item?')) return
    const adminPassword = localStorage.getItem('adminPassword')
    if (!adminPassword) {
      setError('Not authenticated.')
      return
    }
    try {
      await techStackAPI.delete(itemId, adminPassword)
      await fetchTechStack()
      setEditingTechItem(null)
      setShowAddForm(false)
      setError('')
    } catch (err) {
      setError(formatError(err.response?.data?.detail || err.message || err) || 'Failed to delete')
    }
  }

  const handleCancel = () => {
    setShowAddForm(false)
    setEditingProject(null)
    setEditingBlog(null)
    setEditingCertificate(null)
    setEditingEducation(null)
    setEditingTechItem(null)
    setTechStackFormData({ name: '', logo_url: '' })
    setProjectFormData({
      title: '',
      slug: '',
      short_description: '',
      tech_stack: '',
      tools: '',
      github_link: '',
      live_demo: '',
      video_demo: '',
      key_features: '',
      cover_image: '',
      problem: '',
      solution: '',
      system_architecture: '',
      challenges: ''
    })
    setBlogFormData({
      title: '',
      slug: '',
      short_description: '',
      cover_image_url: '',
      tags: '',
      author: '',
      published_date: '',
      reading_time: '',
      content: ''
    })
    setCertificateFormData({
      title: '',
      company: '',
      completion_month: '',
      completion_year: '',
      short_description: '',
      certificate_url: ''
    })
    setEducationFormData({
      degree: '',
      institution: '',
      start_year: '',
      end_year: '',
      details: ''
    })
  }

  const handleLogout = () => {
    localStorage.removeItem('adminPassword')
    localStorage.removeItem('adminAuthenticated')
    onLogout()
    navigate('/')
  }

  // Debug: Log state when form should show
  if (showAddForm && activeTab === 'projects') {
    console.log('Form should be visible:', { showAddForm, activeTab, projectFormData })
  }

  return (
    <div className="admin-dashboard-container">
      <div className="admin-header">
        <h1>Admin Dashboard</h1>
        <button onClick={handleLogout} className="btn btn-secondary">
          Logout
        </button>
      </div>

      {error && !showAddForm && (
        <div className="error-message">{error}</div>
      )}

      {/* Tabs */}
      <div className="admin-tabs" style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', borderBottom: '2px solid var(--border-color)' }}>
        <button
          onClick={() => {
            setActiveTab('projects')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
          }}
          className={`btn ${activeTab === 'projects' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'projects' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Projects ({projects.length})
        </button>
        <button
          onClick={() => {
            setActiveTab('blogs')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
          }}
          className={`btn ${activeTab === 'blogs' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'blogs' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Blogs ({blogs.length})
        </button>
        <button
          onClick={() => {
            setActiveTab('certificates')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
          }}
          className={`btn ${activeTab === 'certificates' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'certificates' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Certificates ({certificates.length})
        </button>
        <button
          onClick={() => {
            setActiveTab('education')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
            setEditingTechItem(null)
          }}
          className={`btn ${activeTab === 'education' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'education' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Education ({education.length})
        </button>
        <button
          onClick={() => {
            setActiveTab('landing')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
            setEditingTechItem(null)
          }}
          className={`btn ${activeTab === 'landing' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'landing' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Landing
        </button>
        <button
          onClick={() => {
            setActiveTab('tech-stack')
            setShowAddForm(false)
            setEditingProject(null)
            setEditingBlog(null)
            setEditingCertificate(null)
            setEditingEducation(null)
            setEditingTechItem(null)
          }}
          className={`btn ${activeTab === 'tech-stack' ? 'btn-primary' : 'btn-secondary'}`}
          style={{ borderBottom: activeTab === 'tech-stack' ? '2px solid var(--accent-primary)' : 'none', borderRadius: 0 }}
        >
          Tech Stack ({techStack.length})
        </button>
      </div>

      <div className="admin-actions">
        {activeTab === 'tech-stack' && !showAddForm && (
          <button
            onClick={() => {
              setEditingTechItem(null)
              setTechStackFormData({ name: '', logo_url: '' })
              setShowAddForm(true)
            }}
            className="btn btn-primary"
          >
            + Add Tech Stack Item
          </button>
        )}
        {!showAddForm && activeTab !== 'landing' && activeTab !== 'tech-stack' && (
          <button 
            onClick={() => {
              // Reset all editing states
              setEditingProject(null)
              setEditingBlog(null)
              setEditingCertificate(null)
              setEditingEducation(null)
              
              // Clear any errors
              setError('')
              
              // Reset form data based on active tab and show form
              if (activeTab === 'projects') {
                setProjectFormData({
                  title: '',
                  slug: '',
                  short_description: '',
                  detailed_description: '',
                  tech_stack: '',
                  tools: '',
                  github_link: '',
                  live_demo: '',
                  video_demo: '',
                  key_features: '',
                  cover_image: '',
                  problem: '',
                  solution: '',
                  system_architecture: '',
                  challenges: ''
                })
                setShowAddForm(true)
              } else if (activeTab === 'blogs') {
                setBlogFormData({
                  title: '',
                  slug: '',
                  short_description: '',
                  cover_image_url: '',
                  tags: '',
                  author: '',
                  published_date: '',
                  reading_time: '',
                  content: ''
                })
                setShowAddForm(true)
              } else if (activeTab === 'certificates') {
                setCertificateFormData({
                  title: '',
                  company: '',
                  completion_month: '',
                  completion_year: '',
                  short_description: '',
                  certificate_url: ''
                })
                setShowAddForm(true)
              } else if (activeTab === 'education') {
                setEducationFormData({
                  degree: '',
                  institution: '',
                  start_year: '',
                  end_year: '',
                  details: ''
                })
                setShowAddForm(true)
              }
            }}
            className="btn btn-primary"
          >
            + Add New {activeTab === 'projects' ? 'Project' : activeTab === 'blogs' ? 'Blog' : activeTab === 'certificates' ? 'Certificate' : 'Education Entry'}
          </button>
        )}
      </div>

      {/* Landing page (hero) settings */}
      {activeTab === 'landing' && (
        <div className="admin-form-card">
          <h2>Landing Page Content</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>Edit the hero section text shown on the main page.</p>
          {siteSettingsLoading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}
              <form onSubmit={handleSiteSettingsSubmit} className="admin-form">
                <div className="form-group">
                  <label>Welcome label</label>
                  <input
                    type="text"
                    value={siteFormData.welcome_label}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, welcome_label: e.target.value }))}
                    placeholder="WELCOME"
                  />
                </div>
                <div className="form-group">
                  <label>Hero name</label>
                  <input
                    type="text"
                    value={siteFormData.hero_name}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, hero_name: e.target.value }))}
                    placeholder="Your name"
                  />
                </div>
                <div className="form-group">
                  <label>Tagline (e.g. Developer · Researcher · Problem Solver)</label>
                  <input
                    type="text"
                    value={siteFormData.hero_tagline}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, hero_tagline: e.target.value }))}
                    placeholder="Developer · Researcher · Problem Solver"
                  />
                </div>
                <div className="form-group">
                  <label>Short description</label>
                  <textarea
                    value={siteFormData.hero_description}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, hero_description: e.target.value }))}
                    rows="4"
                    placeholder="Brief intro about you..."
                  />
                </div>
                <hr style={{ margin: '1.5rem 0', borderColor: 'var(--border)' }} />
                <h3 style={{ marginBottom: '0.75rem', fontSize: '1rem' }}>About section (2 paragraphs)</h3>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>These two paragraphs appear in the About section below the hero. Cards stay fixed.</p>
                <div className="form-group">
                  <label>About paragraph 1</label>
                  <textarea
                    value={siteFormData.about_paragraph_1}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, about_paragraph_1: e.target.value }))}
                    rows="4"
                    placeholder="First paragraph about you..."
                  />
                </div>
                <div className="form-group">
                  <label>About paragraph 2</label>
                  <textarea
                    value={siteFormData.about_paragraph_2}
                    onChange={(e) => setSiteFormData(prev => ({ ...prev, about_paragraph_2: e.target.value }))}
                    rows="4"
                    placeholder="Second paragraph about you..."
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn btn-primary">Save landing content</button>
                </div>
              </form>
            </>
          )}
        </div>
      )}

      {/* Tech stack add/edit form */}
      {showAddForm && activeTab === 'tech-stack' && (
        <div className="admin-form-card">
          <h2>{editingTechItem ? 'Edit Tech Stack Item' : 'Add Tech Stack Item'}</h2>
          {error && <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>}
          <form onSubmit={handleTechStackSubmit} className="admin-form">
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                value={techStackFormData.name}
                onChange={(e) => setTechStackFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="e.g. Python, JavaScript, N8N"
                required
              />
            </div>
            <div className="form-group">
              <label>Logo URL *</label>
              <input
                type="url"
                value={techStackFormData.logo_url}
                onChange={(e) => setTechStackFormData(prev => ({ ...prev, logo_url: e.target.value }))}
                placeholder="https://example.com/logo.svg"
                required
              />
              <small style={{ color: 'var(--text-secondary)' }}>Use a direct link to an image (SVG or PNG).</small>
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">{editingTechItem ? 'Update' : 'Add'}</button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      )}

      {/* Tech stack list */}
      {activeTab === 'tech-stack' && !showAddForm && (
        <div className="admin-projects-list">
          <h2>Tech Stack ({techStack.length})</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>These logos appear in the hero section. Add 2–4 items for best display.</p>
          {techStackLoading ? (
            <div className="loading">Loading...</div>
          ) : techStack.length === 0 ? (
            <div className="empty-state">No tech stack items. Add your first item (e.g. Python, JS, N8N).</div>
          ) : (
            <div className="projects-table">
              {techStack.map((item) => (
                <div key={item.id || item._id} className="project-row">
                  <div className="project-row-content">
                    {item.logo_url && (
                      <img src={item.logo_url} alt={item.name} className="project-row-image" style={{ width: 48, height: 48, objectFit: 'contain' }} />
                    )}
                    <div className="project-row-info">
                      <h3>{item.name}</h3>
                      <p style={{ fontSize: '0.85rem', wordBreak: 'break-all' }}>{item.logo_url}</p>
                    </div>
                  </div>
                  <div className="project-row-actions">
                    <button onClick={() => handleEditTechItem(item)} className="btn btn-small btn-secondary">Edit</button>
                    <button onClick={() => handleDeleteTechItem(item.id || item._id)} className="btn btn-small btn-danger">Delete</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Debug: Show when form should be visible */}
      {showAddForm && activeTab === 'projects' && console.log('Rendering project form', { showAddForm, activeTab, projectFormData })}
      
      {showAddForm && activeTab === 'projects' && (
        <div className="admin-form-card" style={{ display: 'block', visibility: 'visible', opacity: 1, minHeight: '400px', position: 'relative', zIndex: 1 }}>
          <h2>{editingProject ? 'Edit Project' : 'Add New Project'}</h2>
          {error && (
            <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>
          )}
          <form onSubmit={handleProjectSubmit} className="admin-form">
            <div className="form-row">
              <div className="form-group">
                <label>Title *</label>
                <input
                  type="text"
                  name="title"
                  value={projectFormData.title}
                  onChange={handleProjectTitleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Slug (URL-friendly) *</label>
              <input
                type="text"
                name="slug"
                value={projectFormData.slug}
                onChange={handleProjectInputChange}
                placeholder="ai-resume-analyzer"
                pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$"
                required
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                Auto-generated from title. Use lowercase letters, numbers, and hyphens only.
              </small>
            </div>

            <div className="form-group">
              <label>Short Description *</label>
              <textarea
                name="short_description"
                value={projectFormData.short_description}
                onChange={handleProjectInputChange}
                rows="2"
                required
              />
            </div>

            <div className="form-group">
              <label>Detailed Description</label>
              <textarea
                name="detailed_description"
                value={projectFormData.detailed_description}
                onChange={handleProjectInputChange}
                rows="6"
                placeholder="Provide a detailed description of the project..."
              />
            </div>

            <div className="form-group">
              <label>Tech Stack (comma-separated) *</label>
              <input
                type="text"
                name="tech_stack"
                value={projectFormData.tech_stack}
                onChange={handleProjectInputChange}
                placeholder="React, Python, FastAPI, MongoDB"
                required
              />
            </div>

            <div className="form-group">
              <label>Tools (comma-separated)</label>
              <input
                type="text"
                name="tools"
                value={projectFormData.tools}
                onChange={handleProjectInputChange}
                placeholder="VS Code, Docker, Git, Postman"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>GitHub Link</label>
                <input
                  type="url"
                  name="github_link"
                  value={projectFormData.github_link}
                  onChange={handleProjectInputChange}
                />
              </div>
              <div className="form-group">
                <label>Live Demo</label>
                <input
                  type="url"
                  name="live_demo"
                  value={projectFormData.live_demo}
                  onChange={handleProjectInputChange}
                />
              </div>
            </div>

            <div className="form-group">
              <label>Video Demo</label>
              <input
                type="url"
                name="video_demo"
                value={projectFormData.video_demo}
                onChange={handleProjectInputChange}
              />
            </div>

            <div className="form-group">
              <label>Cover Image URL</label>
              <input
                type="url"
                name="cover_image"
                value={projectFormData.cover_image}
                onChange={handleProjectInputChange}
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div className="form-group">
              <label>Key Features (comma-separated)</label>
              <textarea
                name="key_features"
                value={projectFormData.key_features}
                onChange={handleProjectInputChange}
                rows="3"
                placeholder="Feature 1, Feature 2, Feature 3"
              />
            </div>

            <div className="form-group">
              <label>Problem</label>
              <textarea
                name="problem"
                value={projectFormData.problem}
                onChange={handleProjectInputChange}
                rows="4"
                placeholder="Describe the problem this project addresses..."
              />
            </div>

            <div className="form-group">
              <label>Solution</label>
              <textarea
                name="solution"
                value={projectFormData.solution}
                onChange={handleProjectInputChange}
                rows="4"
                placeholder="Describe the solution approach..."
              />
            </div>

            <div className="form-group">
              <label>System Architecture</label>
              <textarea
                name="system_architecture"
                value={projectFormData.system_architecture}
                onChange={handleProjectInputChange}
                rows="4"
                placeholder="Describe the system architecture (e.g. diagram description, components)..."
              />
            </div>

            <div className="form-group">
              <label>Challenges</label>
              <textarea
                name="challenges"
                value={projectFormData.challenges}
                onChange={handleProjectInputChange}
                rows="4"
                placeholder="Key challenges faced and how they were addressed..."
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                {editingProject ? 'Update Project' : 'Create Project'}
              </button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {showAddForm && activeTab === 'blogs' && blogFormData && (
        <div className="admin-form-card">
          <h2>{editingBlog ? 'Edit Blog' : 'Add New Blog'}</h2>
          {error && (
            <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>
          )}
          <form onSubmit={handleBlogSubmit} className="admin-form">
            <div className="form-row">
              <div className="form-group">
                <label>Title *</label>
                <input
                  type="text"
                  name="title"
                  value={blogFormData.title}
                  onChange={handleBlogTitleChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Slug (URL-friendly) *</label>
              <input
                type="text"
                name="slug"
                value={blogFormData.slug}
                onChange={handleBlogInputChange}
                placeholder="my-blog-post"
                pattern="^[a-z0-9]+(?:-[a-z0-9]+)*$"
                required
              />
              <small style={{ color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
                Auto-generated from title. Use lowercase letters, numbers, and hyphens only.
              </small>
            </div>

            <div className="form-group">
              <label>Short Description *</label>
              <textarea
                name="short_description"
                value={blogFormData.short_description}
                onChange={handleBlogInputChange}
                rows="2"
                required
              />
            </div>

            <div className="form-group">
              <label>Cover Image URL</label>
              <input
                type="url"
                name="cover_image_url"
                value={blogFormData.cover_image_url}
                onChange={handleBlogInputChange}
                placeholder="https://images.unsplash.com/photo-..."
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Tags (comma-separated)</label>
                <input
                  type="text"
                  name="tags"
                  value={blogFormData.tags}
                  onChange={handleBlogInputChange}
                  placeholder="React, Node.js, MongoDB"
                />
              </div>
              <div className="form-group">
                <label>Author</label>
                <input
                  type="text"
                  name="author"
                  value={blogFormData.author}
                  onChange={handleBlogInputChange}
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Published Date</label>
                <input
                  type="date"
                  name="published_date"
                  value={blogFormData.published_date}
                  onChange={handleBlogInputChange}
                />
              </div>
              <div className="form-group">
                <label>Reading Time</label>
                <input
                  type="text"
                  name="reading_time"
                  value={blogFormData.reading_time}
                  onChange={handleBlogInputChange}
                  placeholder="5 min read"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Content (Full Blog Text) *</label>
              <textarea
                name="content"
                value={blogFormData.content}
                onChange={handleBlogInputChange}
                rows="15"
                required
                placeholder="Write your blog content here..."
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                {editingBlog ? 'Update Blog' : 'Create Blog'}
              </button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {activeTab === 'projects' && !showAddForm && (
        <div className="admin-projects-list">
          <h2>All Projects ({projects.length})</h2>
          {projectsLoading ? (
            <div className="loading">Loading projects...</div>
          ) : projects.length === 0 ? (
            <div className="empty-state">No projects found. Add your first project!</div>
          ) : (
            <div className="projects-table">
              {projects.map((project) => (
                <div key={project.id || project._id} className="project-row">
                  <div className="project-row-content">
                    {project.cover_image && (
                      <img src={project.cover_image} alt={project.title} className="project-row-image" />
                    )}
                    <div className="project-row-info">
                      <h3>{project.title}</h3>
                      <p>{project.short_description}</p>
                      <div className="project-row-tech">
                        {(project.tech_stack || []).slice(0, 3).map((tech, i) => (
                          <span key={i} className="tech-tag">{tech}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="project-row-actions">
                    <button 
                      onClick={() => handleEditProject(project)}
                      className="btn btn-small btn-secondary"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDeleteProject(project.id || project._id)}
                      className="btn btn-small btn-danger"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {showAddForm && activeTab === 'certificates' && certificateFormData && (
        <div className="admin-form-card">
          <h2>{editingCertificate ? 'Edit Certificate' : 'Add New Certificate'}</h2>
          {error && (
            <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>
          )}
          <form onSubmit={handleCertificateSubmit} className="admin-form">
            <div className="form-row">
              <div className="form-group">
                <label>Title *</label>
                <input
                  type="text"
                  name="title"
                  value={certificateFormData.title}
                  onChange={handleCertificateInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Company/Issuer *</label>
              <input
                type="text"
                name="company"
                value={certificateFormData.company}
                onChange={handleCertificateInputChange}
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Completion Month (1-12) *</label>
                <input
                  type="number"
                  name="completion_month"
                  value={certificateFormData.completion_month}
                  onChange={handleCertificateInputChange}
                  min="1"
                  max="12"
                  required
                />
              </div>
              <div className="form-group">
                <label>Completion Year *</label>
                <input
                  type="number"
                  name="completion_year"
                  value={certificateFormData.completion_year}
                  onChange={handleCertificateInputChange}
                  min="1900"
                  max="2100"
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label>Short Description *</label>
              <textarea
                name="short_description"
                value={certificateFormData.short_description}
                onChange={handleCertificateInputChange}
                rows="3"
                required
              />
            </div>

            <div className="form-group">
              <label>Certificate URL *</label>
              <input
                type="url"
                name="certificate_url"
                value={certificateFormData.certificate_url}
                onChange={handleCertificateInputChange}
                placeholder="https://example.com/certificate.pdf"
                required
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                {editingCertificate ? 'Update Certificate' : 'Create Certificate'}
              </button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {activeTab === 'blogs' && !showAddForm && (
        <div className="admin-projects-list">
          <h2>All Blogs ({blogs.length})</h2>
          {blogsLoading ? (
            <div className="loading">Loading blogs...</div>
          ) : blogs.length === 0 ? (
            <div className="empty-state">No blogs found. Add your first blog!</div>
          ) : (
            <div className="projects-table">
              {blogs.map((blog) => (
                <div key={blog.id || blog._id} className="project-row">
                  <div className="project-row-content">
                    {blog.cover_image_url && (
                      <img src={blog.cover_image_url} alt={blog.title} className="project-row-image" />
                    )}
                    <div className="project-row-info">
                      <h3>{blog.title}</h3>
                      <p>{blog.short_description}</p>
                      <div className="project-row-tech">
                        <span className="tech-tag" style={{ fontSize: '0.85rem' }}>Slug: {blog.slug}</span>
                        {blog.reading_time && (
                          <span className="tech-tag" style={{ fontSize: '0.85rem' }}>{blog.reading_time}</span>
                        )}
                        {(blog.tags || []).slice(0, 2).map((tag, i) => (
                          <span key={i} className="tech-tag">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                  <div className="project-row-actions">
                    <button 
                      onClick={() => handleEditBlog(blog)}
                      className="btn btn-small btn-secondary"
                    >
                      Edit
                    </button>
                    <button 
                      onClick={() => handleDeleteBlog(blog.slug)}
                      className="btn btn-small btn-danger"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'certificates' && !showAddForm && (
        <div className="admin-projects-list">
          <h2>All Certificates ({certificates.length})</h2>
          {certificatesLoading ? (
            <div className="loading">Loading certificates...</div>
          ) : certificates.length === 0 ? (
            <div className="empty-state">No certificates found. Add your first certificate!</div>
          ) : (
            <div className="projects-table">
              {certificates.map((cert) => {
                const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
                const dateStr = `${monthNames[cert.completion_month - 1]} ${cert.completion_year}`
                return (
                  <div key={cert.id || cert._id} className="project-row">
                    <div className="project-row-content">
                      <div className="project-row-info">
                        <h3>{cert.title}</h3>
                        <p>{cert.company} - {dateStr}</p>
                        <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                          {cert.short_description}
                        </p>
                      </div>
                    </div>
                    <div className="project-row-actions">
                      <button 
                        onClick={() => handleEditCertificate(cert)}
                        className="btn btn-small btn-secondary"
                      >
                        Edit
                      </button>
                      <button 
                        onClick={() => handleDeleteCertificate(cert.id || cert._id)}
                        className="btn btn-small btn-danger"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {showAddForm && activeTab === 'education' && educationFormData && (
        <div className="admin-form-card">
          <h2>{editingEducation ? 'Edit Education Entry' : 'Add New Education Entry'}</h2>
          {error && (
            <div className="error-message" style={{ marginBottom: '1rem' }}>{error}</div>
          )}
          <form onSubmit={handleEducationSubmit} className="admin-form">
            <div className="form-group">
              <label>Degree *</label>
              <input
                type="text"
                name="degree"
                value={educationFormData.degree}
                onChange={handleEducationInputChange}
                placeholder="B.S Computer Science"
                required
              />
            </div>

            <div className="form-group">
              <label>Institution *</label>
              <input
                type="text"
                name="institution"
                value={educationFormData.institution}
                onChange={handleEducationInputChange}
                placeholder="DHA Suffa University, Karachi"
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Start Year *</label>
                <input
                  type="number"
                  name="start_year"
                  value={educationFormData.start_year}
                  onChange={handleEducationInputChange}
                  min="1900"
                  max="2100"
                  required
                />
              </div>
              <div className="form-group">
                <label>End Year (leave empty for present)</label>
                <input
                  type="number"
                  name="end_year"
                  value={educationFormData.end_year}
                  onChange={handleEducationInputChange}
                  min="1900"
                  max="2100"
                />
              </div>
            </div>

            <div className="form-group">
              <label>Details</label>
              <textarea
                name="details"
                value={educationFormData.details}
                onChange={handleEducationInputChange}
                rows="2"
                placeholder="Focus: AI Automation and ML"
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                {editingEducation ? 'Update Education Entry' : 'Create Education Entry'}
              </button>
              <button type="button" onClick={handleCancel} className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {activeTab === 'education' && !showAddForm && (
        <div className="admin-projects-list">
          <h2>All Education Entries ({education.length})</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Note: Only the 3 latest entries are displayed. Adding a new entry will automatically remove the oldest one.
          </p>
          {educationLoading ? (
            <div className="loading">Loading education entries...</div>
          ) : education.length === 0 ? (
            <div className="empty-state">No education entries found. Add your first entry!</div>
          ) : (
            <div className="projects-table">
              {education.map((edu) => {
                const period = edu.end_year 
                  ? `${edu.start_year} – ${edu.end_year}` 
                  : `${edu.start_year} – PRESENT`
                return (
                  <div key={edu.id || edu._id} className="project-row">
                    <div className="project-row-content">
                      <div className="project-row-info">
                        <h3>{edu.degree}</h3>
                        <p>{edu.institution} - {period}</p>
                        {edu.details && (
                          <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                            {edu.details}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="project-row-actions">
                      <button 
                        onClick={() => handleEditEducation(edu)}
                        className="btn btn-small btn-secondary"
                      >
                        Edit
                      </button>
                      <button 
                        onClick={() => handleDeleteEducation(edu.id || edu._id)}
                        className="btn btn-small btn-danger"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default AdminDashboard


