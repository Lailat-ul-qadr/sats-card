import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Loading, StatCard, Skeleton } from '../components';
import { useAuth } from '../context';
import { walletService, transactionService } from '../services';
import { formatCurrency, timeAgo } from '../utils';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.08 } },
};
const itemVariants = {
  hidden: { opacity: 0, y: 12 },
  visible: { opacity: 1, y: 0 },
};

export default function Dashboard() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [balanceData, txsData] = await Promise.all([
          walletService.getBalance(),
          transactionService.getTransactions(),
        ]);
        setBalance(balanceData);
        setTransactions(txsData.slice(0, 5));
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to load dashboard data', error);
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-noise-grid">
        <div className="border-b border-line bg-surface/60 backdrop-blur sticky top-0 z-10">
          <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6">
            <Skeleton height="h-3" className="w-24 mb-2" />
            <Skeleton height="h-8" className="w-48" />
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 space-y-8">
          <div className="grid md:grid-cols-3 gap-5">
            {[1, 2, 3].map(i => (
              <div key={i} className="panel p-6 space-y-4">
                <Skeleton height="h-3" className="w-20" />
                <Skeleton height="h-8" className="w-32" />
                <Skeleton height="h-3" className="w-24" />
              </div>
            ))}
          </div>
          <div className="space-y-3">
            <Skeleton height="h-6" className="w-40" />
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="panel h-24 rounded-2xl" />
              ))}
            </div>
          </div>
          <div className="panel p-4 space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="flex gap-4 items-center">
                <Skeleton height="h-10" className="w-10 rounded-full shrink-0" />
                <div className="flex-1 space-y-2">
                  <Skeleton height="h-4" className="w-40" />
                  <Skeleton height="h-3" className="w-56" />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-noise-grid">
      {/* Header */}
      <div className="border-b border-line bg-surface/60 backdrop-blur sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 py-6">
          <p className="text-ink-muted text-xs uppercase tracking-wider mb-1">Welcome back</p>
          <h1 className="heading-2">{user?.name || 'Demo User'}</h1>
        </div>
      </div>

      <motion.div
        className="max-w-6xl mx-auto px-4 sm:px-6 py-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Balance Cards */}
        <div className="grid md:grid-cols-3 gap-5 mb-10">
          <motion.div variants={itemVariants}>
            <StatCard
              label="Bitcoin Balance"
              value={`${(balance?.sats ?? 0).toLocaleString()} sats`}
              sub={`${balance?.btc?.toFixed(8) ?? '0.00000000'} BTC`}
              accent="amber"
              icon="⚡"
            />
          </motion.div>
          <motion.div variants={itemVariants}>
            <StatCard
              label="USD Equivalent"
              value={formatCurrency(balance?.usd || 0, 'USD')}
              sub="@ 39,500 sats/USD"
              accent="lime"
              icon="$"
            />
          </motion.div>
          <motion.div variants={itemVariants}>
            <StatCard
              label="Account Status"
              value="Active"
              sub="KYC Verified · Tier 2"
              accent="success"
              icon="✓"
            />
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div variants={itemVariants} className="mb-10">
          <h2 className="heading-3 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { to: '/fund', icon: '↓', label: 'Fund Card', primary: true },
              { to: '/card', icon: '▭', label: 'View Card' },
              { to: '/send', icon: '↗', label: 'Send' },
              { to: '/receive', icon: '↙', label: 'Receive' },
            ].map((action) => (
              <button
                key={action.to}
                onClick={() => navigate(action.to)}
                className={`flex flex-col items-center justify-center gap-2 h-24 rounded-2xl border transition-all hover:-translate-y-0.5 ${
                  action.primary
                    ? 'bg-amber-lime text-bg border-transparent shadow-glow-amber-sm'
                    : 'panel text-ink hover:border-amber/40'
                }`}
              >
                <span className="text-xl">{action.icon}</span>
                <span className="text-sm font-semibold">{action.label}</span>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Recent Transactions */}
        <motion.div variants={itemVariants}>
          <div className="flex justify-between items-center mb-4">
            <h2 className="heading-3">Recent Transactions</h2>
            <button
              onClick={() => navigate('/transactions')}
              className="text-amber font-semibold hover:brightness-110 text-sm"
            >
              View All →
            </button>
          </div>

          <div className="panel overflow-hidden">
            {transactions && transactions.length > 0 ? (
              <div className="divide-y divide-line">
                {transactions.map((tx) => (
                  <div
                    key={tx.id}
                    className="p-4 hover:bg-white/5 transition-colors flex justify-between items-center group"
                  >
                    <div className="flex gap-4 items-center min-w-0">
                      <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg shrink-0 transition-colors ${
                        tx.type === 'topup' ? 'bg-success/15 text-success' :
                        tx.type === 'spend' ? 'bg-danger/15 text-danger' :
                        'bg-amber/15 text-amber'
                      }`}>
                        {tx.type === 'topup' ? '↓' : tx.type === 'spend' ? '◆' : '⚡'}
                      </div>
                      <div className="min-w-0">
                        <p className="font-semibold text-ink truncate group-hover:text-amber transition-colors">{tx.title}</p>
                        <p className="text-ink-soft text-sm truncate">{tx.description}</p>
                        <p className="text-ink-muted text-xs mt-1">{timeAgo(tx.timestamp)}</p>
                      </div>
                    </div>
                    <div className="text-right shrink-0 ml-4">
                      <p className={`font-figures font-semibold ${
                        tx.type === 'topup' ? 'text-success' : tx.type === 'spend' ? 'text-danger' : 'text-ink'
                      }`}>
                        {tx.type === 'topup' ? '+' : tx.type === 'spend' ? '-' : ''}{
                        tx.currency === 'sats'
                          ? `${tx.amount.toLocaleString()} sats`
                          : `${tx.currency} ${tx.amount}`}
                      </p>
                      <p className="text-success text-xs capitalize">{tx.status}</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-10 text-center text-ink-muted">
                No transactions yet. Start by funding your card!
              </div>
            )}
          </div>
        </motion.div>
      </motion.div>
    </div>
  );
}
