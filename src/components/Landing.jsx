import React from 'react'

export default function Landing({onStart}){
  return (
    <div className="landing">
      <div className="landing-bg" aria-hidden />
      <div className="landing-content">
        <div className="landing-header">
          <h1>Mobibit Africa</h1>
          <p className="subtitle">Lightning-Powered Bitcoin Card, Funded by Mobile Money</p>
        </div>

        <section className="problem">
          <h2>The Problem</h2>
          <ul>
            <li>Across Africa, mobile money (M-Pesa, MTN MoMo, Airtel Money) is how people transact daily.</li>
            <li>But mobile money balances are locked to local currency and local rails.</li>
            <li>There's no simple bridge from <strong>"money I already have on my phone"</strong> to <strong>"a spendable balance I can use internationally."</strong></li>
            <li>Existing crypto on-ramps are slow, require bank transfers, or aren't built for mobile-money-first users.</li>
          </ul>
        </section>

        <section className="solution">
          <h2>Our Solution</h2>
          <p>Convert mobile money directly into Bitcoin via the <strong>Lightning Network</strong> for instant settlement, and load it onto a virtual card balance you can spend from — <strong>no bank account required.</strong></p>
          <div className="flow">
            <span className="flow-step">Mobile Money</span>
            <span className="flow-arrow">→</span>
            <span className="flow-step">BTC/Sats (Lightning)</span>
            <span className="flow-arrow">→</span>
            <span className="flow-step">Virtual Card Balance</span>
          </div>
        </section>

        <section className="targets">
          <h2>For Whom</h2>
          <ul>
            <li>Freelancers/gig workers paid internationally but only with mobile money access locally</li>
            <li>Small business owners paying for international tools and subscriptions</li>
            <li>Anyone underbanked who wants Bitcoin exposure without complex exchange onboarding</li>
          </ul>
        </section>

        <button className="cta" onClick={onStart}>
          ✨ Start Live Demo
        </button>
      </div>
    </div>
  )
}
