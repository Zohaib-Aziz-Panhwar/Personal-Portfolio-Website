import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor for adding auth tokens if needed
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized
      localStorage.removeItem('authToken')
    }
    return Promise.reject(error)
  }
)

// API Services
export const contactAPI = {
  sendMessage: async (data) => {
    const response = await apiClient.post('/contact', data)
    return response.data
  },
}

export const projectsAPI = {
  getAll: async () => {
    const response = await apiClient.get('/projects')
    return response.data
  },
  getById: async (id) => {
    const response = await apiClient.get(`/projects/${id}`)
    return response.data
  },
  getBySlug: async (slug) => {
    const response = await apiClient.get(`/projects/${slug}`)
    return response.data
  },
  create: async (projectData, adminPassword) => {
    const response = await apiClient.post('/projects', projectData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  update: async (id, projectData, adminPassword) => {
    const response = await apiClient.put(`/projects/${id}`, projectData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  delete: async (id, adminPassword) => {
    const response = await apiClient.delete(`/projects/${id}`, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export const blogAPI = {
  getAll: async () => {
    const response = await apiClient.get('/blog')
    return response.data
  },
  getBySlug: async (slug) => {
    const response = await apiClient.get(`/blog/${slug}`)
    return response.data
  },
  create: async (blogData, adminPassword) => {
    const response = await apiClient.post('/blog', blogData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  update: async (slug, blogData, adminPassword) => {
    const response = await apiClient.put(`/blog/${slug}`, blogData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  delete: async (slug, adminPassword) => {
    const response = await apiClient.delete(`/blog/${slug}`, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export const certificatesAPI = {
  getAll: async () => {
    const response = await apiClient.get('/certificates')
    return response.data
  },
  getById: async (id) => {
    const response = await apiClient.get(`/certificates/${id}`)
    return response.data
  },
  create: async (certificateData, adminPassword) => {
    const response = await apiClient.post('/certificates', certificateData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  update: async (id, certificateData, adminPassword) => {
    const response = await apiClient.put(`/certificates/${id}`, certificateData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  delete: async (id, adminPassword) => {
    const response = await apiClient.delete(`/certificates/${id}`, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export const siteSettingsAPI = {
  get: async () => {
    const response = await apiClient.get('/site-settings')
    return response.data
  },
  update: async (data, adminPassword) => {
    const response = await apiClient.put('/site-settings', data, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export const techStackAPI = {
  getAll: async () => {
    const response = await apiClient.get('/tech-stack')
    return response.data
  },
  create: async (item, adminPassword) => {
    const response = await apiClient.post('/tech-stack', item, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  update: async (id, item, adminPassword) => {
    const response = await apiClient.put(`/tech-stack/${id}`, item, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  delete: async (id, adminPassword) => {
    const response = await apiClient.delete(`/tech-stack/${id}`, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export const educationAPI = {
  getAll: async () => {
    const response = await apiClient.get('/education')
    return response.data
  },
  getById: async (id) => {
    const response = await apiClient.get(`/education/${id}`)
    return response.data
  },
  create: async (educationData, adminPassword) => {
    const response = await apiClient.post('/education', educationData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  update: async (id, educationData, adminPassword) => {
    const response = await apiClient.put(`/education/${id}`, educationData, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
  delete: async (id, adminPassword) => {
    const response = await apiClient.delete(`/education/${id}`, {
      headers: {
        'X-Admin-Password': adminPassword
      }
    })
    return response.data
  },
}

export default apiClient

