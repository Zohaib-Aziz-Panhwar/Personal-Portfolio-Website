import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import '../../styles/Admin.css'

const AdminLogin = ({ onLogin }) => {
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const storedPassword = localStorage.getItem('adminPassword')
      const correctPassword = storedPassword || import.meta.env.VITE_ADMIN_PASSWORD || 'admin123'

      if (password === correctPassword) {
        localStorage.setItem('adminPassword', password)
        localStorage.setItem('adminAuthenticated', 'true')
        onLogin(true)
        navigate('/admin/dashboard')
      } else {
        setError('Invalid password. Please try again.')
      }
    } catch (err) {
      setError('An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="admin-login-container">
      <div className="admin-login-card">
        <h1 className="admin-login-title">Admin Login</h1>
        <p className="admin-login-subtitle">Enter password to access admin panel</p>
        
        <form onSubmit={handleSubmit} className="admin-login-form">
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter admin password"
              required
              autoFocus
            />
          </div>

          {error && (
            <div className="error-message">{error}</div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary admin-login-btn"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default AdminLogin

