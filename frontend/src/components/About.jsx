import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { siteSettingsAPI } from '../services/api'
import '../styles/About.css'

const About = () => {
  const { data } = useQuery({
    queryKey: ['siteSettings'],
    queryFn: () => siteSettingsAPI.get(),
  })

  const paragraph1 = (data?.about_paragraph_1 || '').trim()
  const paragraph2 = (data?.about_paragraph_2 || '').trim()

  const skills = [
    {
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M8 8C8 8 10 6 12 8C14 10 16 8 16 8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M8 12C8 12 10 10 12 12C14 14 16 12 16 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M8 16C8 16 10 14 12 16C14 18 16 16 16 16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
        </svg>
      ),
      title: 'AI Automation',
      subtitle: 'Workflow automation, AI agents, task optimization'
    },
    {
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2"/>
          <path d="M3 9H21M3 15H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <path d="M9 3V21M15 3V21" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.5"/>
          <circle cx="7" cy="7" r="1" fill="currentColor"/>
          <circle cx="17" cy="7" r="1" fill="currentColor"/>
          <circle cx="7" cy="17" r="1" fill="currentColor"/>
          <circle cx="17" cy="17" r="1" fill="currentColor"/>
        </svg>
      ),
      title: 'Full-Stack Development',
      subtitle: 'React, Node, APIs'
    },
    {
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2"/>
          <path d="M8 8H16M8 12H16M8 16H12" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
          <circle cx="6" cy="6" r="1" fill="currentColor"/>
          <circle cx="18" cy="6" r="1" fill="currentColor"/>
          <circle cx="6" cy="18" r="1" fill="currentColor"/>
          <circle cx="18" cy="18" r="1" fill="currentColor"/>
          <path d="M12 4V8M12 16V20M4 12H8M16 12H20" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" opacity="0.4"/>
        </svg>
      ),
      title: 'Tools & Stack',
      subtitle: 'Python, JavaScript, Git, MongoDB, SQL, APIs'
    },
    {
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          <circle cx="12" cy="12" r="1.5" fill="currentColor"/>
          <circle cx="12" cy="7" r="1.5" fill="currentColor"/>
          <circle cx="12" cy="17" r="1.5" fill="currentColor"/>
        </svg>
      ),
      title: 'Open Source',
      subtitle: 'Contributor & collaborative development'
    }
  ]

  return (
    <section id="about" className="about section">
      <div className="container">
        <div className="about-content">
          <div className="about-text">
            <span className="section-label">ABOUT</span>
            <h2 className="section-title">A bit about me</h2>
            {(paragraph1 || paragraph2) ? (
              <div className="about-description">
                {paragraph1 ? <p>{paragraph1}</p> : null}
                {paragraph2 ? <p>{paragraph2}</p> : null}
              </div>
            ) : null}
          </div>
          <div className="about-skills">
            {skills.map((skill, index) => (
              <div key={index} className="skill-card">
                <div className="skill-icon">{skill.icon}</div>
                <h3 className="skill-title">{skill.title}</h3>
                <p className="skill-subtitle">{skill.subtitle}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default About
