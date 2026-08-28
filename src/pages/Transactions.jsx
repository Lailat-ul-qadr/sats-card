import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Loading, PageHeader, Badge } from '../components';
import { transactionService } from '../services';
import { formatDateTime, timeAgo } from '../utils';

export default function Transactions() {
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState(null);
  const [filter, setFilter] = useState('all');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const data = await transactionService.getTransactions();
        setTransactions(data);
        setIsLoading(false);
      } catch (error) {
        console.error('Failed to load transactions', error);
        setIsLoading(false);
      }
    };

    loadTransactions();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  const filteredTransactions = filter === 'all'
    ? transactions
    : transactions.filter(tx => tx.type === filter);

  const getTypeIcon = (type) => {
    const icons = { topup: '↓', payment: '⚡', spend: '◆' };
    return icons[type] || '≡';
  };

  const getStatusBadge = (status) => {
    if (status === 'settled') return 'success';
    if (status === 'pending') return 'warning';
    return 'error';
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Transaction History" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-4xl mx-auto px-4 sm:px-6 py-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Filters */}
        <div className="mb-6 flex gap-2 flex-wrap">
          {['all', 'topup', 'payment', 'spend'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-4 py-2 rounded-xl font-medium text-sm transition-all ${
                filter === f
                  ? 'bg-amber-lime text-bg'
                  : 'panel text-ink-soft hover:border-amber/40'
              }`}
            >
              {f === 'all' ? 'All' : f === 'topup' ? '↓ Fund' : f === 'payment' ? '⚡ Payment' : '◆ Spend'}
            </button>
          ))}
        </div>

        {/* Transactions List */}
        <div className="space-y-3">
          {filteredTransactions && filteredTransactions.length > 0 ? (
            filteredTransactions.map((tx, index) => (
              <motion.div
                key={tx.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.04 }}
                className="panel p-4 hover:border-amber/30 transition-colors"
              >
                <div className="flex items-center justify-between gap-4">
                  <div className="flex gap-4 items-start flex-1 min-w-0">
                    <div className="w-11 h-11 bg-elevated rounded-full flex items-center justify-center text-lg shrink-0">
                      {getTypeIcon(tx.type)}
                    </div>
                    <div className="min-w-0">
                      <h3 className="font-semibold text-ink truncate">{tx.title}</h3>
                      <p className="text-sm text-ink-soft truncate">{tx.description}</p>
                      <p className="text-xs text-ink-muted mt-1">
                        {formatDateTime(tx.timestamp)} · {timeAgo(tx.timestamp)}
                      </p>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <p className="font-figures font-semibold text-ink">
                      {tx.currency === 'sats'
                        ? `${tx.amount.toLocaleString()} sats`
                        : `${tx.currency} ${tx.amount}`}
                    </p>
                    <p className="text-sm text-ink-muted">
                      {tx.currency === 'sats' && tx.usd
                        ? `≈ $${tx.usd}`
                        : tx.currency === 'USD' && tx.sats
                        ? `≈ ${tx.sats.toLocaleString()} sats`
                        : ''}
                    </p>
                    <div className="mt-1.5">
                      <Badge variant={getStatusBadge(tx.status)}>{tx.status}</Badge>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))
          ) : (
            <div className="panel p-12 text-center">
              <p className="text-ink text-lg">No transactions found</p>
              <p className="text-ink-muted text-sm mt-2">Start by funding your card or making a payment</p>
            </div>
          )}
        </div>

        {/* Summary */}
        {transactions && transactions.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="mt-8 panel p-6 grid md:grid-cols-3 gap-6"
          >
            <div>
              <p className="text-ink-muted text-xs uppercase tracking-wider mb-2">Total Transactions</p>
              <p className="heading-3">{transactions.length}</p>
            </div>
            <div>
              <p className="text-ink-muted text-xs uppercase tracking-wider mb-2">Total Funded</p>
              <p className="heading-3 text-success">
                ${transactions
                  .filter(t => t.type === 'topup')
                  .reduce((sum, t) => sum + t.amount, 0)
                  .toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-ink-muted text-xs uppercase tracking-wider mb-2">Current Balance</p>
              <p className="heading-3 text-amber">
                {transactions
                  .filter(t => t.currency === 'sats')
                  .reduce((sum, t) => {
                    if (t.type === 'topup' || t.type === 'payment') return sum + t.sats;
                    if (t.type === 'spend') return sum - t.sats;
                    return sum;
                  }, 250000)
                  .toLocaleString()} sats
              </p>
            </div>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
