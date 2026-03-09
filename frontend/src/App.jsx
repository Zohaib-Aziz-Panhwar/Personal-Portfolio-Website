import React, { useState, useEffect, Suspense, lazy } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import Navbar from './components/Navbar'
import ScrollToTop from './components/ScrollToTop'
import Hero from './components/Hero'
import About from './components/About'
import Projects from './components/Projects'
import Education from './components/Education'
import Certifications from './components/Certifications'
import Blog from './components/Blog'
import Contact from './components/Contact'
import Footer from './components/Footer'
import PageLoader from './components/PageLoader'
import './styles/App.css'

// Lazy-load route-only components for faster initial load and smaller bundles
const ProjectsList = lazy(() => import('./components/ProjectsList'))
const ProjectDetail = lazy(() => import('./components/ProjectDetail'))
const CertificationsList = lazy(() => import('./components/CertificationsList'))
const BlogList = lazy(() => import('./components/BlogList'))
const BlogDetail = lazy(() => import('./components/BlogDetail'))
const AdminLogin = lazy(() => import('./components/admin/AdminLogin'))
const AdminDashboard = lazy(() => import('./components/admin/AdminDashboard'))

function HomePage() {
  const location = useLocation()

  useEffect(() => {
    const scrollToSection = sessionStorage.getItem('scrollToSection')
    if (scrollToSection) {
      sessionStorage.removeItem('scrollToSection')
      setTimeout(() => {
        const element = document.getElementById(scrollToSection)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      }, 300)
    }
  }, [location])

  return (
    <>
      <Hero />
      <About />
      <Projects />
      <Education />
      <Certifications />
      <Blog />
      <Contact />
    </>
  )
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const authStatus = localStorage.getItem('adminAuthenticated')
    setIsAuthenticated(authStatus === 'true')
  }, [])

  const PrivateRoute = ({ children }) => {
    return isAuthenticated ? children : <Navigate to="/admin" replace />
  }

  return (
    <Router>
      <ScrollToTop />
      <div className="App">
        <Navbar />
        <main>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/projects" element={<ProjectsList />} />
              <Route path="/projects/:slug" element={<ProjectDetail />} />
              <Route path="/certificates" element={<CertificationsList />} />
              <Route path="/blog" element={<BlogList />} />
              <Route path="/blog/:slug" element={<BlogDetail />} />
              <Route
                path="/admin"
                element={
                  isAuthenticated ? (
                    <Navigate to="/admin/dashboard" replace />
                  ) : (
                    <AdminLogin onLogin={setIsAuthenticated} />
                  )
                }
              />
              <Route
                path="/admin/dashboard"
                element={
                  <PrivateRoute>
                    <AdminDashboard onLogout={() => setIsAuthenticated(false)} />
                  </PrivateRoute>
                }
              />
            </Routes>
          </Suspense>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App
