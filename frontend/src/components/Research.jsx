import React from 'react'
import '../styles/Research.css'

const Research = () => {
  const researchItems = [
    {
      title: 'Efficient Attention Mechanisms for Low-Resource NLP',
      description: 'Proposes a lightweight attention variant reducing memory footprint by 40% while maintaining competitive accuracy on benchmark tasks.',
      status: 'Published',
      statusType: 'published'
    },
    {
      title: 'Graph-Based Approaches to Code Vulnerability Detection',
      description: 'Explores using graph neural networks to identify security vulnerabilities in source code repositories at scale.',
      status: 'Ongoing',
      statusType: 'ongoing'
    },
    {
      title: 'Federated Learning for Privacy-Preserving Health Data',
      description: 'Investigating decentralized model training techniques for sensitive medical datasets across institutions.',
      status: 'Ongoing',
      statusType: 'ongoing'
    }
  ]

  return (
    <section id="research" className="research section section-alt">
      <div className="container">
        <div className="research-header">
          <span className="section-label">RESEARCH</span>
          <h2 className="section-title">Academic Work</h2>
        </div>
        <div className="research-list">
          {researchItems.map((item, index) => (
            <div key={index} className="research-card">
              <div className="research-content">
                <h3 className="research-title">{item.title}</h3>
                <p className="research-description">{item.description}</p>
              </div>
              <span className={`research-status research-status-${item.statusType}`}>
                {item.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default Research

