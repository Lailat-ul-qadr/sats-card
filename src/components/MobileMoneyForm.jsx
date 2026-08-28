import React, { useState, useEffect } from 'react'

const FX_RATES = { KES: 0.007, NGN: 0.0026, GHS: 0.17, USD: 1 }

const convertToSats = (amount, currency, btcPrice) => {
  const usd = parseFloat(amount) * (FX_RATES[currency] || 1)
  const sats = Math.round((usd / btcPrice) * 1e8)
  return { usd, sats }
}

export default function MobileMoneyForm({ onTopUp, setBtcUsd }){
  const [phone, setPhone] = useState('+254700000000')
  const [amount, setAmount] = useState('5000')
  const [currency, setCurrency] = useState('KES')
  const [busy, setBusy] = useState(false)
  const [preview, setPreview] = useState(null)
  const [btcPrice, setBtcPrice] = useState(30000)

  useEffect(() => {
    fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
      .then(r => r.json())
      .then(j => {
        const price = j.bitcoin?.usd || 30000
        setBtcPrice(price)
        setBtcUsd(price)
      })
      .catch(e => console.error(e))
  }, [setBtcUsd])

  const updatePreview = (val, curr) => {
    if(!val || !btcPrice) return setPreview(null)
    const { usd, sats } = convertToSats(val, curr, btcPrice)
    setPreview({ usd: usd.toFixed(2), sats })
  }

  const handleAmountChange = (e) => {
    setAmount(e.target.value)
    updatePreview(e.target.value, currency)
  }

  const handleCurrencyChange = (e) => {
    setCurrency(e.target.value)
    updatePreview(amount, e.target.value)
  }

  async function handleSubmit(e){
    e.preventDefault()
    if(!amount || !phone) return
    setBusy(true)
    try{
      const { usd, sats } = convertToSats(amount, currency, btcPrice)

      const invoiceId = `lnbc${sats}n_${Date.now().toString(36).toUpperCase()}`

      const tx = {
        id: Date.now(),
        type: 'topup',
        phone,
        currency,
        amount: parseFloat(amount),
        usd: Number(usd.toFixed(2)),
        sats,
        time: new Date().toISOString()
      }

      const invoice = {
        timestamp: new Date().toISOString(),
        event: 'INVOICE_CREATED',
        invoice: invoiceId,
        amount: sats,
        currency: 'sats'
      }

      await new Promise(r => setTimeout(r, 500))

      const payment = {
        timestamp: new Date(Date.now() + 800).toISOString(),
        event: 'PAYMENT_SETTLED',
        invoice: invoiceId,
        amount: sats,
        status: 'SUCCESS',
        node: 'Exchange → Card Wallet (regtest)'
      }

      onTopUp(tx, invoice)
      await new Promise(r => setTimeout(r, 400))
      onTopUp(null, payment)

      setPhone('')
      setAmount('')
      setPreview(null)
    }catch(err){
      console.error(err)
      alert('Failed to fetch rate')
    }finally{setBusy(false)}
  }

  return (
    <form className="mm-form" onSubmit={handleSubmit}>
      <h3>Send Mobile Money</h3>

      <label>Phone Number
        <input value={phone} onChange={e=>setPhone(e.target.value)} placeholder="+254700000000" />
      </label>

      <label>Currency
        <select value={currency} onChange={handleCurrencyChange}>
          <option>KES</option>
          <option>NGN</option>
          <option>GHS</option>
          <option>USD</option>
        </select>
      </label>

      <label>Amount
        <input value={amount} onChange={handleAmountChange} placeholder="5000" type="number" />
      </label>

      {preview && (
        <div className="preview">
          <div className="preview-row">
            <span>{amount} {currency}</span>
            <span className="arrow">≈</span>
            <span>${preview.usd}</span>
          </div>
          <div className="preview-row highlight">
            <span>${preview.usd}</span>
            <span className="arrow">≈</span>
            <span className="sats">{preview.sats.toLocaleString()} sats</span>
          </div>
        </div>
      )}

      <button type="submit" disabled={busy} className="submit-btn">
        {busy? '⏳ Processing via Lightning...':'✨ Top Up'}
      </button>
    </form>
  )
}

