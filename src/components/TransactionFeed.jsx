import React from 'react'

export default function TransactionFeed({txs=[]}){
  return (
    <div className="tx-feed">
      <h3>Transaction History</h3>
      {txs.length===0 && <p className="muted">No transactions yet. Top up to see activity.</p>}
      <ul className="tx-list">
        {txs.map(tx => (
          <li key={tx.id} className={`tx-item tx-${tx.type}`}>
            <div className="tx-icon">
              {tx.type === 'topup' && '📱'}
              {tx.type === 'spend' && '💳'}
            </div>
            <div className="tx-main">
              <div className="tx-title">
                {tx.type === 'topup' && `${tx.amount} ${tx.currency} → ${tx.sats.toLocaleString()} sats`}
                {tx.type === 'spend' && `Spent ${tx.sats.toLocaleString()} sats`}
              </div>
              {tx.type === 'topup' && <div className="tx-detail">{tx.phone} • ${tx.usd}</div>}
              {tx.type === 'spend' && <div className="tx-detail">{tx.description}</div>}
              <div className="tx-time">{new Date(tx.time).toLocaleString()}</div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
