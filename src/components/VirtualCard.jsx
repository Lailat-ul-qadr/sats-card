import React, { useState, useEffect } from 'react'

function satsToUsd(sats, btcUsd){
  return ((sats / 1e8) * btcUsd).toFixed(2)
}

export default function VirtualCard({sats=0, btcUsd=30000, onSpend}){
  const [displaySats, setDisplaySats] = useState(0)
  const [animating, setAnimating] = useState(false)

  useEffect(() => {
    if(sats !== displaySats){
      setAnimating(true)
      const timer = setTimeout(() => {
        setDisplaySats(sats)
        setAnimating(false)
      }, 600)
      return () => clearTimeout(timer)
    }
  }, [sats, displaySats])

  const handleSimulateSpend = () => {
    const spendAmount = Math.floor(displaySats * 0.2)
    if(spendAmount > 0 && onSpend){
      onSpend(spendAmount)
    }
  }

  return (
    <>
      <div className={`virtual-card ${animating ? 'animating' : ''}`}>
        <div className="card-art" aria-hidden>
          <svg viewBox="0 0 280 170" className="card-bg">
            <defs>
              <linearGradient id="cardGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style={{stopColor:'#E9E6E0',stopOpacity:1}} />
                <stop offset="100%" style={{stopColor:'#D4D0C8',stopOpacity:1}} />
              </linearGradient>
            </defs>
            <rect x="10" y="10" width="260" height="150" rx="14" fill="url(#cardGradient)" stroke="#8AA39B" strokeWidth="0.5"/>
            <circle cx="230" cy="40" r="18" fill="#D29B6A" opacity="0.3"/>
            <circle cx="50" cy="140" r="12" fill="#8AA39B" opacity="0.2"/>
          </svg>
        </div>
        <div className="card-content">
          <div className="card-top">
            <div className="card-label">Sats Card (Demo)</div>
            <div className="chip" aria-hidden>💳</div>
          </div>
          <div className="balance-section">
            <div className="balance-sats">{displaySats.toLocaleString()} sats</div>
            <div className="balance-usd">≈ ${satsToUsd(displaySats, btcUsd)} USD</div>
          </div>
          <div className="card-footer">
            <span className="card-holder">Sats Card User</span>
          </div>
        </div>
      </div>

      {displaySats > 0 && (
        <div className="spend-demo">
          <button onClick={handleSimulateSpend} className="spend-btn">
            💸 Simulate Spend (~20% of balance)
          </button>
          <p className="spend-info">This demonstrates spending the balance on an international purchase.</p>
        </div>
      )}
    </>
  )
}
