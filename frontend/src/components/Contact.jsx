import React, { useState } from 'react'
import { contactAPI } from '../services/api'
import '../styles/Contact.css'

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [submitStatus, setSubmitStatus] = useState(null)
  const [showSuccessDialog, setShowSuccessDialog] = useState(false)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    // Prevent the default form reload
    e.preventDefault()
    
    setIsSubmitting(true)
    setSubmitStatus(null)

    try {
      const data = await contactAPI.sendMessage(formData)

      if (data.status === 'success') {
        setFormData({ name: '', email: '', message: '' })
        setShowSuccessDialog(true)
      } else {
        alert('Failed to send message')
      }
    } catch (error) {
      console.error('Error sending message:', error)
      alert('Failed to send message')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <section id="contact" className="contact section">
      {showSuccessDialog && (
        <div 
          className="contact-success-overlay" 
          onClick={() => setShowSuccessDialog(false)}
          role="dialog"
          aria-modal="true"
          aria-labelledby="success-dialog-title"
        >
          <div className="contact-success-dialog" onClick={(e) => e.stopPropagation()}>
            <div className="contact-success-tick-wrap">
              <svg className="contact-success-tick" viewBox="0 0 52 52" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <circle className="contact-success-circle" cx="26" cy="26" r="24" stroke="currentColor" strokeWidth="2"/>
                <path className="contact-success-check" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M14 26l8 8 16-18"/>
              </svg>
            </div>
            <h3 id="success-dialog-title" className="contact-success-title">Message sent!</h3>
            <p className="contact-success-message">
              Thank you for reaching out! Your message has been successfully sent.
              I appreciate you taking the time to contact me and will get back to you as soon as possible.
            </p>
            <button 
              type="button" 
              className="btn btn-primary contact-success-close"
              onClick={() => setShowSuccessDialog(false)}
            >
              Done
            </button>
          </div>
        </div>
      )}
      <div className="container">
        <div className="contact-content">
          <div className="contact-form-wrapper">
            <h2 className="contact-title">Get in Touch</h2>
            <form className="contact-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <input
                  type="text"
                  name="name"
                  placeholder="Name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <input
                  type="email"
                  name="email"
                  placeholder="Email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="form-input"
                />
              </div>
              <div className="form-group">
                <textarea
                  name="message"
                  placeholder="Message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows="6"
                  className="form-input form-textarea"
                ></textarea>
              </div>
              {submitStatus && (
                <div className={`form-status form-status-${submitStatus.type}`}>
                  {submitStatus.message}
                </div>
              )}
              <button 
                type="submit" 
                className="btn btn-primary"
                disabled={isSubmitting}
              >
                {isSubmitting ? 'Sending...' : 'Send Message'}
              </button>
            </form>
          </div>
          <div className="contact-info">
            <p className="contact-description">
              I'm always open to conversations about interesting projects, research collaborations, or just a friendly hello.
            </p>
            <p className="contact-location">
              Based in Karachi, Pakistan · Open to remote work
            </p>
            <div className="contact-social">
              <a 
                href="https://github.com/Zohaib-Aziz-Panhwar" 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link" 
                aria-label="GitHub"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C6.477 2 2 6.477 2 12C2 16.42 4.865 20.335 8.862 21.69C9.362 21.79 9.562 21.42 9.562 21.09C9.562 20.79 9.552 19.67 9.542 18.45C7.142 18.95 6.742 17.57 6.742 17.57C6.342 16.33 5.682 16.01 5.682 16.01C4.802 15.35 5.762 15.37 5.762 15.37C6.742 15.45 7.222 16.41 7.222 16.41C8.082 17.87 9.422 17.45 9.582 17.33C9.662 16.89 9.862 16.61 10.082 16.45C7.662 16.21 5.102 15.29 5.102 11.29C5.102 10.13 5.502 9.17 6.222 8.41C6.122 8.15 5.722 6.97 6.402 5.37C6.402 5.37 7.342 5.01 9.562 6.41C10.462 6.15 11.422 6.03 12.382 6.03C13.342 6.03 14.302 6.15 15.202 6.41C17.422 5 18.362 5.37 18.362 5.37C19.042 6.97 18.642 8.15 18.542 8.41C19.262 9.17 19.662 10.13 19.662 11.29C19.662 15.31 17.082 16.21 14.662 16.45C14.942 16.69 15.182 17.15 15.182 17.89C15.182 19.05 15.172 20.01 15.172 21.09C15.172 21.42 15.372 21.8 15.872 21.69C19.868 20.335 22.732 16.418 22.732 12C22.732 6.477 18.255 2 12.732 2H12Z" fill="currentColor"/>
                </svg>
              </a>
              <a 
                href="https://www.linkedin.com/in/zohaib-aziz-panhwar-a86822265/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link" 
                aria-label="LinkedIn"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M16 8C17.5913 8 19.1174 8.63214 20.2426 9.75736C21.3679 10.8826 22 12.4087 22 14V21H18V14C18 13.4696 17.7893 12.9609 17.4142 12.5858C17.0391 12.2107 16.5304 12 16 12C15.4696 12 14.9609 12.2107 14.5858 12.5858C14.2107 12.9609 14 13.4696 14 14V21H10V14C10 12.4087 10.6321 10.8826 11.7574 9.75736C12.8826 8.63214 14.4087 8 16 8Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <path d="M6 9H2V21H6V9Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                  <circle cx="4" cy="4" r="2" stroke="currentColor" strokeWidth="2"/>
                </svg>
              </a>
              <a 
                href="https://x.com/AzizZohaib78463" 
                target="_blank" 
                rel="noopener noreferrer"
                className="social-link" 
                aria-label="X (Twitter)"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" fill="currentColor"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}

export default Contact

