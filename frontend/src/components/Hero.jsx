import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { siteSettingsAPI, techStackAPI } from '../services/api'
import '../styles/Hero.css'

const DEFAULT_HERO = {
  welcome_label: 'WELCOME',
  hero_name: 'Zohaib Aziz Panhwar',
  hero_tagline: 'Developer · Researcher · Problem Solver',
  hero_description: "I'm a Computer Science student with a strong interest in AI automation and software development. I enjoy building practical solutions that simplify workflows, improve efficiency, and solve real-world problems."
}

const Hero = () => {
  const { data: siteData } = useQuery({
    queryKey: ['siteSettings'],
    queryFn: () => siteSettingsAPI.get(),
  })
  const { data: techData } = useQuery({
    queryKey: ['techStack'],
    queryFn: () => techStackAPI.getAll(),
  })

  const settings = siteData && (siteData.hero_tagline || siteData.hero_name)
    ? {
        welcome_label: siteData.welcome_label ?? DEFAULT_HERO.welcome_label,
        hero_name: siteData.hero_name ?? DEFAULT_HERO.hero_name,
        hero_tagline: siteData.hero_tagline ?? DEFAULT_HERO.hero_tagline,
        hero_description: siteData.hero_description ?? DEFAULT_HERO.hero_description
      }
    : DEFAULT_HERO
  const techStack = Array.isArray(techData) ? techData : []

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  const downloadResume = () => {
    const link = document.createElement('a')
    link.href = '/resume.pdf'
    link.download = 'Zohaib_Aziz_Panhwar_Resume.pdf'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <section id="home" className="hero">
      <div className="container">
        <div className="hero-content">
          <div className="hero-text">
            <span className="hero-label animate-fade-in">{settings.welcome_label}</span>
            <h1 className="hero-name animate-slide-up">{settings.hero_name}</h1>
            <p className="hero-role animate-fade-in-delay">{settings.hero_tagline}</p>
            <p className="hero-description animate-fade-in-delay-2">
              {settings.hero_description}
            </p>
            {techStack.length > 0 && (
              <div className="hero-tech-stack animate-fade-in-delay-2">
                <span className="hero-tech-stack-label">TECH STACK</span>
                <div className="hero-tech-stack-logos">
                  {techStack.slice(0, 5).map((item) => (
                    <div key={item.id || item.name} className="hero-tech-stack-item" title={item.name}>
                      <img src={item.logo_url} alt={item.name} />
                      <span>{item.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="hero-buttons animate-fade-in-delay-3">
              <button
                className="btn btn-primary"
                onClick={downloadResume}
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M10 12.5V2.5M10 12.5L6.66667 9.16667M10 12.5L13.3333 9.16667" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M2.5 15.8333V16.6667C2.5 17.5871 3.24619 18.3333 4.16667 18.3333H15.8333C16.7538 18.3333 17.5 17.5871 17.5 16.6667V15.8333" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Download Resume
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => scrollToSection('contact')}
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M2.5 5.83333L10 10.8333L17.5 5.83333M2.5 5.83333L10 10.8333M2.5 5.83333V14.1667L10 19.1667M17.5 5.83333V14.1667L10 19.1667M10 19.1667V10.8333" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
                Contact Me
              </button>
            </div>
          </div>
          <div className="hero-image animate-slide-in-right">
            <div className="hero-image-wrapper">
              <div className="hero-image-bg animate-float"></div>
              <div className="hero-image-bg-2 animate-float-delay"></div>
              <div className="hero-image-main animate-float-slow">
                <img
                  src="/Picture.jpg"
                  alt="ZOHAIB AZIZ PANHWAR"
                />
              </div>
            </div>
          </div>
        </div>
        <div
          className="hero-scroll-indicator"
          onClick={() => scrollToSection('about')}
          role="button"
          tabIndex={0}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              scrollToSection('about')
            }
          }}
          aria-label="Scroll to About section"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M7 10L12 15L17 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </div>
      </div>
    </section>
  )
}

export default Hero
