import React from 'react'
import '../styles/AcademicWork.css'

const StatusBadge = ({ status = 'Draft' }) => {
  const statusLower = status.toLowerCase()
  
  return (
    <span className={`status-badge status-badge-${statusLower}`}>
      {status}
    </span>
  )
}

export default StatusBadge

