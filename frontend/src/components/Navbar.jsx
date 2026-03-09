import React, { useState, useEffect, useRef } from 'react'
import '../styles/Navbar.css'

const Navbar = () => {
  const [activeSection, setActiveSection] = useState('home')
  const [isScrolled, setIsScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)
  const navRef = useRef(null)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50)
      if (menuOpen) setMenuOpen(false)
      const sections = ['home', 'about', 'projects', 'education', 'certifications', 'blog', 'contact']
      const scrollPosition = window.scrollY + 100
      for (let i = sections.length - 1; i >= 0; i--) {
        const section = document.getElementById(sections[i])
        if (section && section.offsetTop <= scrollPosition) {
          setActiveSection(sections[i])
          break
        }
      }
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [menuOpen])

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') setMenuOpen(false)
    }
    window.addEventListener('keydown', handleEscape)
    return () => window.removeEventListener('keydown', handleEscape)
  }, [])

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (navRef.current && !navRef.current.contains(e.target)) setMenuOpen(false)
    }
    if (menuOpen) {
      document.body.style.overflow = 'hidden'
      window.addEventListener('click', handleClickOutside)
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
      window.removeEventListener('click', handleClickOutside)
    }
  }, [menuOpen])

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
    setMenuOpen(false)
  }

  const navItems = [
    { id: 'about', label: 'About' },
    { id: 'projects', label: 'Projects' },
    { id: 'education', label: 'Education' },
    { id: 'certifications', label: 'Certifications' },
    { id: 'blog', label: 'Blog' },
    { id: 'contact', label: 'Contact' }
  ]

  return (
    <nav ref={navRef} className={`navbar ${isScrolled ? 'scrolled' : ''} ${menuOpen ? 'menu-open' : ''}`}>
      <div className="navbar-container">
        <div className="navbar-logo" onClick={() => scrollToSection('home')}>
          portfolio.
        </div>
        <button
          type="button"
          className="navbar-hamburger"
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((prev) => !prev)}
        >
          <span className="navbar-hamburger-line" />
          <span className="navbar-hamburger-line" />
          <span className="navbar-hamburger-line" />
        </button>
        <ul className="navbar-menu">
          {navItems.map((item) => (
            <li key={item.id}>
              <a
                href={`#${item.id}`}
                onClick={(e) => {
                  e.preventDefault()
                  scrollToSection(item.id)
                }}
                className={activeSection === item.id ? 'active' : ''}
              >
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </div>
      {menuOpen && (
        <div
          className="navbar-backdrop"
          aria-hidden="true"
          onClick={() => setMenuOpen(false)}
          onKeyDown={(e) => e.key === 'Escape' && setMenuOpen(false)}
        />
      )}
    </nav>
  )
}

export default Navbar

