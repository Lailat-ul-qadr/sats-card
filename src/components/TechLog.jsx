import React from 'react'

export default function TechLog({logs=[]}){
  return (
    <div className="tech-log">
      <h3>Lightning Events (for judges)</h3>
      <p className="log-info">Real invoice + payment simulation</p>
      {logs.length===0 && <p className="muted">Awaiting first Lightning event...</p>}
      <ul className="log-list">
        {logs.map((log, i) => (
          <li key={i} className={`log-entry log-${log.event.toLowerCase()}`}>
            <div className="log-header">
              <span className="log-event">{log.event}</span>
              <span className="log-time">{new Date(log.timestamp).toLocaleTimeString()}</span>
            </div>
            <div className="log-details">
              {log.invoice && <div><strong>Invoice:</strong> {log.invoice}</div>}
              {log.amount && <div><strong>Amount:</strong> {log.amount.toLocaleString()} {log.currency || 'sats'}</div>}
              {log.node && <div><strong>Route:</strong> {log.node}</div>}
              {log.status && <div><strong>Status:</strong> <span className={`status-${log.status.toLowerCase()}`}>{log.status}</span></div>}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
