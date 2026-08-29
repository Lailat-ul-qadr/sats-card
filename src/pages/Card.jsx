import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Alert, Loading, PageHeader } from '../components';
import { walletService } from '../services';
import { formatCurrency } from '../utils';

export default function Card() {
  const navigate = useNavigate();
  const [card, setCard] = useState(null);
  const [balance, setBalance] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showFullNumber, setShowFullNumber] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [cardData, balanceData] = await Promise.all([
          walletService.getCardInfo(),
          walletService.getBalance(),
        ]);
        setCard(cardData);
        setBalance(balanceData);
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to load card data', error);
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Mobibit Africa" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Virtual Card */}
        <div className="mb-10">
          <motion.div
            className="relative rounded-[28px] p-8 overflow-hidden bg-elevated border border-amber/20 shadow-card"
            whileHover={{ y: -6 }}
            transition={{ duration: 0.3 }}
          >
            {/* Ambient glows */}
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-amber/25 rounded-full blur-[90px] pointer-events-none" />
            <div className="absolute -bottom-24 -left-16 w-56 h-56 bg-lime/15 rounded-full blur-[90px] pointer-events-none" />
            {/* Subtle grid texture */}
            <div className="absolute inset-0 opacity-[0.04] bg-grid-lines bg-grid pointer-events-none" />

            <div className="relative z-10">
              <div className="flex justify-between items-start mb-14">
                <div className="w-12 h-9 rounded-md bg-amber-lime flex items-center justify-center text-lg">
                  ⚡
                </div>
                <span className="text-ink-muted text-xs uppercase tracking-widest font-semibold">Virtual</span>
              </div>

              <div className="mb-14">
                <p className="text-ink-muted text-xs uppercase mb-2 font-semibold tracking-wider">Card Number</p>
                <p className="font-figures text-xl sm:text-2xl tracking-widest text-ink">
                  {showFullNumber
                    ? card?.cardNumber
                    : card?.cardNumber?.split(' ').map((seg, i) => i === 0 || i === 3 ? seg : '••••').join(' ')
                  }
                </p>
                <button
                  onClick={() => setShowFullNumber(!showFullNumber)}
                  className="text-xs text-amber hover:brightness-110 mt-2 underline underline-offset-2"
                >
                  {showFullNumber ? 'Hide' : 'Show'} number
                </button>
              </div>

              <div className="flex justify-between items-end">
                <div>
                  <p className="text-ink-muted text-[10px] uppercase mb-1 font-semibold tracking-wider">Cardholder</p>
                  <p className="text-ink font-semibold font-figures">{card?.holder}</p>
                </div>
                <div>
                  <p className="text-ink-muted text-[10px] uppercase mb-1 font-semibold tracking-wider">Expires</p>
                  <p className="text-ink font-semibold font-figures">{card?.expires}</p>
                </div>
              </div>
            </div>
          </motion.div>
        </div>

        {/* Balance Section */}
        <div className="mb-10">
          <h2 className="heading-3 mb-4">Balance</h2>
          <div className="grid sm:grid-cols-2 gap-5">
            <div className="panel p-6">
              <p className="text-ink-muted text-xs font-semibold uppercase tracking-wider mb-2">Satoshis</p>
              <h3 className="font-figures text-2xl font-bold text-amber">{balance?.sats.toLocaleString()}</h3>
              <p className="text-ink-muted text-sm mt-2">Bitcoin units</p>
            </div>

            <div className="panel p-6">
              <p className="text-ink-muted text-xs font-semibold uppercase tracking-wider mb-2">USD Equivalent</p>
              <h3 className="font-figures text-2xl font-bold text-lime">
                {formatCurrency(balance?.usd || 0, 'USD')}
              </h3>
              <p className="text-ink-muted text-sm mt-2">@ 39,500 sats/USD</p>
            </div>
          </div>
        </div>

        {/* Card Details */}
        <div className="mb-10">
          <h2 className="heading-3 mb-4">Card Details</h2>
          <div className="panel p-6 space-y-4">
            {[
              { label: 'Card Status', value: 'Active', badge: true },
              { label: 'Card Type', value: 'Virtual Mastercard' },
              { label: 'Currency', value: 'Bitcoin (Sats)' },
              { label: 'Daily Limit', value: '$500', last: true },
            ].map((row) => (
              <div key={row.label} className={`flex justify-between items-center ${!row.last ? 'pb-4 border-b border-line' : ''}`}>
                <span className="text-ink-soft text-sm">{row.label}</span>
                {row.badge ? (
                  <span className="px-3 py-1 bg-success/10 text-success border border-success/30 rounded-full text-xs font-semibold">
                    {row.value}
                  </span>
                ) : (
                  <span className="font-semibold text-ink text-sm">{row.value}</span>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <Button onClick={() => navigate('/fund')} className="flex-1">
            Add Funds
          </Button>
          <Button onClick={() => navigate('/spend')} variant="secondary" className="flex-1">
            Spend Sats
          </Button>
        </div>

        <Alert
          type="info"
          title="Security"
          message="Your virtual card is secured with end-to-end encryption. Never share your card number with anyone."
          className="mt-8"
        />
      </motion.div>
    </div>
  );
}
