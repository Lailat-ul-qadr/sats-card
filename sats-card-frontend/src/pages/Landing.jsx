import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Logo } from '../components';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: [0.16, 1, 0.3, 1] } },
};

const RAILS = ['MTN MoMo', 'M-Pesa', 'Airtel Money', 'Orange Money', 'Lightning Network', 'Bitcoin'];

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="bg-noise-grid min-h-screen text-ink overflow-x-hidden">
      {/* Top bar */}
      <header className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between relative z-10">
        <Logo />
        <div className="hidden sm:flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => navigate('/login')}>Login</Button>
          <Button size="sm" onClick={() => navigate('/signup')}>Get Started</Button>
        </div>
      </header>

      {/* HERO */}
      <section className="max-w-6xl mx-auto px-6 pt-10 pb-24 relative">
        <div className="absolute -top-20 right-0 w-[520px] h-[520px] bg-amber/20 rounded-full blur-[140px] pointer-events-none" />
        <div className="absolute top-40 left-0 w-[420px] h-[420px] bg-lime/10 rounded-full blur-[140px] pointer-events-none" />

        <motion.div
          className="relative z-10 grid lg:grid-cols-2 gap-16 items-center"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <div>
            <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-amber/30 bg-amber/10 text-amber text-xs font-semibold uppercase tracking-wider mb-6">
              <span className="w-1.5 h-1.5 rounded-full bg-amber animate-pulseSoft" />
              Live on Lightning
            </motion.div>

            <motion.h1 variants={itemVariants} className="heading-1 mb-6">
              Mobile money in.
              <br />
              <span className="text-gradient">Bitcoin out.</span>
            </motion.h1>

            <motion.p variants={itemVariants} className="text-ink-soft text-lg leading-relaxed max-w-lg mb-10">
              Convert mobile money into Bitcoin instantly via the Lightning Network,
              and spend it anywhere with a virtual card — no bank account, no borders,
              no waiting.
            </motion.p>

            <motion.div variants={itemVariants} className="flex flex-wrap gap-4 mb-12">
              <Button size="lg" onClick={() => navigate('/signup')} className="shadow-glow-amber">
                Start Live Demo ⚡
              </Button>
              <Button size="lg" variant="secondary" onClick={() => navigate('/login')}>
                I have an account
              </Button>
            </motion.div>

            <motion.p variants={itemVariants} className="text-ink-muted text-xs">
              This is a demo. All transactions are simulated for hackathon purposes.
            </motion.p>
          </div>

          {/* Floating card visual */}
          <motion.div variants={itemVariants} className="relative flex justify-center lg:justify-end">
            <motion.div
              animate={{ y: [0, -14, 0] }}
              transition={{ duration: 5, repeat: Infinity, ease: 'easeInOut' }}
              className="relative w-full max-w-sm"
            >
              <div className="absolute inset-0 bg-amber-lime rounded-[28px] blur-2xl opacity-30" />
              <div className="relative panel-elevated p-7 rounded-[28px] border-amber/20">
                <div className="flex justify-between items-start mb-10">
                  <span className="text-xs uppercase tracking-widest text-ink-muted font-semibold">Sats Card</span>
                  <span className="text-2xl bolt-icon">⚡</span>
                </div>
                <div className="mb-8">
                  <p className="text-ink-muted text-xs mb-1">Balance</p>
                  <p className="font-figures text-3xl font-bold text-ink">250,000 <span className="text-lime text-lg">sats</span></p>
                  <p className="text-ink-muted text-sm mt-1">≈ $98.75 USD</p>
                </div>
                <div className="flex justify-between items-end">
                  <div>
                    <p className="text-ink-muted text-[10px] uppercase mb-1">Cardholder</p>
                    <p className="text-ink font-medium text-sm font-figures">DEMO USER</p>
                  </div>
                  <div>
                    <p className="text-ink-muted text-[10px] uppercase mb-1">Network</p>
                    <p className="text-amber font-medium text-sm">Lightning</p>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        </motion.div>
      </section>

      {/* Rails marquee */}
      <div className="border-y border-line bg-surface/40 py-5 overflow-hidden relative">
        <div className="marquee-track">
          {[...RAILS, ...RAILS, ...RAILS].map((rail, i) => (
            <span key={i} className="mx-8 text-ink-muted text-sm font-medium uppercase tracking-wider shrink-0">
              {rail}
            </span>
          ))}
        </div>
      </div>

      {/* Problem / Solution */}
      <section className="max-w-6xl mx-auto px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-80px' }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <p className="text-amber text-xs font-semibold uppercase tracking-widest mb-3">The gap</p>
          <h2 className="heading-2 max-w-2xl mx-auto">
            Billions have mobile money. Almost none have a way into Bitcoin.
          </h2>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: '📵', title: 'Locked to local rails', text: 'Mobile money balances stay trapped in local currency and local networks.' },
            { icon: '🐌', title: 'Slow, costly on-ramps', text: 'Existing crypto exchanges require bank transfers most users don\'t have.' },
            { icon: '🚫', title: 'No way to spend it', text: 'Even those holding Bitcoin have no simple way to actually spend it day to day.' },
          ].map((item, i) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="panel p-7 hover:border-amber/30 transition-colors"
            >
              <div className="text-3xl mb-4">{item.icon}</div>
              <h3 className="heading-4 mb-2">{item.title}</h3>
              <p className="text-ink-soft text-sm leading-relaxed">{item.text}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Flow */}
      <section className="max-w-6xl mx-auto px-6 py-24">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="panel-elevated p-10 md:p-14 relative overflow-hidden"
        >
          <div className="absolute -bottom-32 -right-20 w-80 h-80 bg-lime/10 rounded-full blur-[120px] pointer-events-none" />
          <p className="text-lime text-xs font-semibold uppercase tracking-widest mb-3">How it works</p>
          <h2 className="heading-2 mb-12 max-w-lg">Three steps from cash in hand to spending power.</h2>

          <div className="grid md:grid-cols-3 gap-8 relative">
            {[
              { n: '01', icon: '📱', title: 'Send mobile money', text: 'Pay via MTN, M-Pesa, Airtel, or Orange in your local currency.' },
              { n: '02', icon: '⚡', title: 'Instant Lightning swap', text: 'Funds convert to sats instantly over the Lightning Network.' },
              { n: '03', icon: '💳', title: 'Spend from your card', text: 'Your virtual card balance updates in real time — spend anywhere.' },
            ].map((step, i) => (
              <motion.div
                key={step.n}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.15 }}
              >
                <div className="flex items-center gap-3 mb-4">
                  <span className="font-figures text-amber text-sm font-bold">{step.n}</span>
                  <div className="h-px flex-1 bg-line" />
                  <span className="text-xl">{step.icon}</span>
                </div>
                <h3 className="heading-4 mb-2">{step.title}</h3>
                <p className="text-ink-soft text-sm leading-relaxed">{step.text}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="max-w-6xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: '⚡', title: 'Instant settlement', text: 'Lightning Network payments settle in seconds, not days.' },
            { icon: '🔐', title: 'True ownership', text: 'Your Bitcoin lives on the blockchain — never in our custody.' },
            { icon: '🌍', title: 'Built for everyone', text: 'No bank account required. Just a phone and mobile money.' },
          ].map((f, i) => (
            <motion.div
              key={f.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              className="panel p-7 hover:-translate-y-1 hover:shadow-glow-amber-sm transition-all"
            >
              <div className="w-12 h-12 rounded-xl bg-amber-lime-soft border border-amber/20 flex items-center justify-center text-2xl mb-5">
                {f.icon}
              </div>
              <h3 className="heading-4 mb-2">{f.title}</h3>
              <p className="text-ink-soft text-sm leading-relaxed">{f.text}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-4xl mx-auto px-6 pb-32 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="heading-2 mb-6">Ready to feel the current?</h2>
          <p className="text-ink-soft mb-10 max-w-md mx-auto">
            Try the full flow in under a minute — fund, convert, and spend simulated sats.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button size="lg" onClick={() => navigate('/signup')} className="shadow-glow-amber">
              Launch Demo
            </Button>
            <Button size="lg" variant="outline" onClick={() => navigate('/login')}>
              Login
            </Button>
          </div>
        </motion.div>
      </section>

      <footer className="border-t border-line py-8 text-center text-ink-muted text-xs">
        © {new Date().getFullYear()} Sats Card — Demo product, not affiliated with any mobile money operator.
      </footer>
    </div>
  );
}
