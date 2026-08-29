import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, PageHeader, Toast } from '../components';
import { paymentService, walletService } from '../services';
import { useCurrencyConversion } from '../hooks';
import { formatCurrency } from '../utils';

export default function Send() {
  const navigate = useNavigate();
  const { convertSatsToUsd } = useCurrencyConversion();
  const [activeTab, setActiveTab] = useState('p2p');
  const [formData, setFormData] = useState({
    recipient: '',
    amount: '',
    memo: '',
  });
  const [balance, setBalance] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ visible: false, message: '' });

  // Load balance on mount
  useEffect(() => {
    const loadBalance = async () => {
      try {
        const data = await walletService.getBalance();
        setBalance(data);
      } catch (err) {
        // Silently fail — balance display is optional
      }
    };
    loadBalance();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateP2P = () => {
    const newErrors = {};
    if (!formData.recipient.trim()) {
      newErrors.recipient = 'Phone number is required';
    } else if (!/^\+\d{10,15}$/.test(formData.recipient.trim())) {
      newErrors.recipient = 'Use country code, e.g. +256701234567';
    }
    const amount = parseInt(formData.amount);
    if (!formData.amount || amount <= 0) {
      newErrors.amount = 'Enter an amount';
    } else if (amount < 100) {
      newErrors.amount = 'Minimum is 100 sats';
    } else if (balance && amount > balance.sats) {
      newErrors.amount = `Insufficient balance. You have ${balance.sats.toLocaleString()} sats`;
    }
    return newErrors;
  };

  const validateLightning = () => {
    const newErrors = {};
    if (!formData.recipient.trim()) {
      newErrors.recipient = 'Paste a Lightning invoice (starts with lnbc)';
    } else if (!formData.recipient.trim().startsWith('lnbc')) {
      newErrors.recipient = 'Lightning invoice should start with "lnbc"';
    }
    const amount = parseInt(formData.amount);
    if (!formData.amount || amount <= 0) {
      newErrors.amount = 'Enter an amount';
    } else if (balance && amount > balance.sats) {
      newErrors.amount = `Insufficient balance. You have ${balance.sats.toLocaleString()} sats`;
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});
    setSuccess(null);

    const newErrors = activeTab === 'p2p' ? validateP2P() : validateLightning();
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    try {
      let result;
      const amount = parseInt(formData.amount);

      if (activeTab === 'p2p') {
        result = await paymentService.transferToUser(
          formData.recipient.trim(),
          amount,
          formData.memo
        );
      } else {
        result = await paymentService.sendBitcoin(
          formData.recipient.trim(),
          amount,
          formData.memo
        );
      }

      if (!result || !result.success) {
        throw new Error(result?.message || 'Transfer failed. Please try again.');
      }

      // Refresh balance after successful send
      try {
        const newBalance = await walletService.getBalance();
        setBalance(newBalance);
      } catch (_) {
        // Balance refresh failed — not critical
      }

      // Show success
      setSuccess(activeTab === 'p2p'
        ? {
            title: '✅ Transfer Sent!',
            message: `${amount.toLocaleString()} sats sent to ${result.recipientName || formData.recipient}`,
            details: [
              { label: 'Recipient', value: result.recipientName || 'User' },
              { label: 'Phone', value: result.recipientPhone },
              { label: 'Amount', value: `${amount.toLocaleString()} sats` },
              { label: 'Fee', value: `${result.feeSats} sats` },
              { label: 'Your Balance', value: `${result.senderNewBalance?.toLocaleString() || '—'} sats` },
            ],
            reference: result.reference,
          }
        : {
            title: '✅ Payment Sent!',
            message: `${amount.toLocaleString()} sats sent via Lightning`,
            details: [
              { label: 'Amount', value: `${result.amount?.toLocaleString() || amount.toLocaleString()} sats` },
              { label: 'Status', value: result.status || 'paid' },
              { label: 'Card Balance', value: `${result.cardBalance?.toLocaleString() || '—'} sats` },
            ],
            reference: result.transactionHash,
          }
      );

      setFormData({ recipient: '', amount: '', memo: '' });
    } catch (error) {
      // Parse backend error messages into user-friendly text
      let msg = error.message || 'Transfer failed';

      if (msg.includes('Insufficient balance')) {
        msg = '💰 ' + msg;
      } else if (msg.includes('not found') || msg.includes('not registered')) {
        msg = '👤 ' + msg + '\n\nAsk them to create an account first.';
      } else if (msg.includes('Cannot transfer to yourself')) {
        msg = '🚫 You cannot send sats to yourself.';
      } else if (msg.includes('Session expired') || error.status === 401) {
        msg = '🔑 Your session expired. Please log in again.';
        setTimeout(() => navigate('/login'), 2000);
      } else if (msg.includes('connect') || msg.includes('fetch') || msg.includes('NetworkError') || msg.includes('Cannot connect')) {
        msg = '📡 Cannot connect to server. Make sure the backend is running on port 8000.';
      } else if (msg.includes('Invalid')) {
        msg = '⚠️ ' + msg;
      } else if (msg.includes('Lightning') || msg.includes('invoice')) {
        msg = '⚡ ' + msg;
      }

      setErrors({ submit: msg });
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setSuccess(null);
    setErrors({});
    // Refresh balance after reset
    walletService.getBalance().then(setBalance).catch(() => {});
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Send Bitcoin" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* ═══ CURRENT BALANCE ═══ */}
        {balance && !success && (
          <motion.div
            className="panel p-4 mb-6 flex justify-between items-center"
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div>
              <p className="text-xs text-ink-muted">Your Balance</p>
              <p className="heading-3 text-ink font-figures">{balance.sats.toLocaleString()} sats</p>
            </div>
            <button
              onClick={async () => {
                try {
                  const data = await walletService.getBalance();
                  setBalance(data);
                  setToast({ visible: true, message: 'Balance refreshed' });
                } catch (_) {}
              }}
              className="text-amber text-sm font-semibold hover:brightness-110"
            >
              🔄 Refresh
            </button>
          </motion.div>
        )}

        {/* ═══ SUCCESS SCREEN ═══ */}
        {success && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="mb-6">
            <div className="panel-elevated p-8 border-lime/20">
              <div className="text-center mb-6">
                <div className="w-16 h-16 rounded-full bg-success/15 flex items-center justify-center text-3xl mx-auto mb-4">
                  ✓
                </div>
                <h2 className="heading-3 text-lime">{success.title}</h2>
                <p className="text-ink-soft mt-2">{success.message}</p>
              </div>

              <div className="panel p-4 space-y-3">
                {success.details && success.details.map((detail, i) => (
                  <div key={i} className="flex justify-between text-sm">
                    <span className="text-ink-soft">{detail.label}</span>
                    <span className="font-semibold text-ink font-figures">{detail.value}</span>
                  </div>
                ))}
                {success.reference && (
                  <div className="pt-3 border-t border-line">
                    <p className="text-xs text-ink-muted mb-1">Reference</p>
                    <code className="text-xs bg-elevated px-2 py-1 rounded block break-all font-figures text-ink-soft">
                      {success.reference}
                    </code>
                  </div>
                )}
              </div>

              {balance && (
                <div className="mt-4 p-3 bg-success/10 border border-success/20 rounded-xl text-center">
                  <p className="text-xs text-ink-muted">Your new balance</p>
                  <p className="heading-4 text-success font-figures">{balance.sats.toLocaleString()} sats</p>
                </div>
              )}

              <div className="flex gap-3 mt-6">
                <Button onClick={resetForm} className="flex-1" variant="secondary">
                  Send More
                </Button>
                <Button onClick={() => navigate('/dashboard')} className="flex-1">
                  Dashboard
                </Button>
              </div>
            </div>
          </motion.div>
        )}

        {/* ═══ ERROR DISPLAY ═══ */}
        {errors.submit && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
            <Alert type="error" title="Transfer Failed" message={errors.submit} />
            <button
              onClick={() => setErrors({})}
              className="w-full mt-3 text-sm text-ink-muted hover:text-ink transition-colors"
            >
              Dismiss
            </button>
          </motion.div>
        )}

        {/* ═══ SEND FORM ═══ */}
        {!success && (
          <div className="panel p-8 mb-8">
            {/* Tab Selector */}
            <div className="flex gap-2 mb-6 bg-elevated rounded-xl p-1">
              <button
                onClick={() => {
                  setActiveTab('p2p');
                  setErrors({});
                  setFormData({ recipient: '', amount: '', memo: '' });
                }}
                className={`flex-1 py-3 px-4 rounded-lg text-sm font-semibold transition-all ${
                  activeTab === 'p2p'
                    ? 'bg-amber text-black'
                    : 'text-ink-soft hover:text-ink'
                }`}
              >
                📱 Send to User
              </button>
              <button
                onClick={() => {
                  setActiveTab('lightning');
                  setErrors({});
                  setFormData({ recipient: '', amount: '', memo: '' });
                }}
                className={`flex-1 py-3 px-4 rounded-lg text-sm font-semibold transition-all ${
                  activeTab === 'lightning'
                    ? 'bg-amber text-black'
                    : 'text-ink-soft hover:text-ink'
                }`}
              >
                ⚡ Lightning
              </button>
            </div>

            {activeTab === 'p2p' ? (
              <>
                <h2 className="heading-3 mb-2">Send to Another User</h2>
                <p className="text-sm text-ink-soft mb-6">
                  Send Bitcoin instantly to any registered user by phone number.
                </p>
              </>
            ) : (
              <>
                <h2 className="heading-3 mb-2">Lightning Payment</h2>
                <p className="text-sm text-ink-soft mb-6">
                  Send Bitcoin to any Lightning address or paste an invoice.
                </p>
              </>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <Input
                  label={activeTab === 'p2p' ? 'Recipient Phone Number' : 'Lightning Invoice (lnbc...)'}
                  type="text"
                  name="recipient"
                  value={formData.recipient}
                  onChange={handleChange}
                  placeholder={activeTab === 'p2p' ? '+256701234567' : 'lnbc1000u1p...'}
                  error={!!errors.recipient}
                  helperText={errors.recipient}
                  disabled={isLoading}
                />
              </div>

              <div>
                <Input
                  label="Amount (sats)"
                  type="number"
                  name="amount"
                  value={formData.amount}
                  onChange={handleChange}
                  placeholder="10000"
                  min="1"
                  step="1"
                  error={!!errors.amount}
                  helperText={errors.amount}
                  disabled={isLoading}
                />
              </div>

              {formData.amount && parseInt(formData.amount) > 0 && (
                <motion.div
                  className="bg-amber/10 border border-amber/30 rounded-xl p-4"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-ink-soft">USD Equivalent</span>
                    <span className="heading-3 text-amber">
                      {formatCurrency(convertSatsToUsd(parseInt(formData.amount) || 0), 'USD')}
                    </span>
                  </div>
                  {activeTab === 'p2p' && (
                    <div className="flex justify-between items-center mt-2 pt-2 border-t border-amber/20">
                      <span className="text-xs text-ink-muted">Network Fee (0.5%)</span>
                      <span className="text-xs text-ink-muted font-figures">
                        {Math.max(1, Math.floor(parseInt(formData.amount) * 0.005))} sats
                      </span>
                    </div>
                  )}
                  {balance && (
                    <div className="flex justify-between items-center mt-2 pt-2 border-t border-amber/20">
                      <span className="text-xs text-ink-muted">After send, you'll have</span>
                      <span className="text-xs text-ink-muted font-figures">
                        {Math.max(0, balance.sats - parseInt(formData.amount) - Math.floor(parseInt(formData.amount) * 0.005)).toLocaleString()} sats
                      </span>
                    </div>
                  )}
                </motion.div>
              )}

              <Input
                label="Memo (Optional)"
                type="text"
                name="memo"
                value={formData.memo}
                onChange={handleChange}
                placeholder="e.g. Lunch money"
                helperText=""
                disabled={isLoading}
              />

              <Button
                type="submit"
                disabled={isLoading || !formData.recipient || !formData.amount}
                className="w-full"
                size="lg"
              >
                {isLoading ? (
                  <span className="flex items-center justify-center gap-2">
                    <span className="animate-spin">⏳</span>
                    Sending...
                  </span>
                ) : activeTab === 'p2p' ? (
                  'Send to User'
                ) : (
                  'Send Bitcoin'
                )}
              </Button>
            </form>
          </div>
        )}

        {/* ═══ INFO ALERTS ═══ */}
        {!success && activeTab === 'p2p' && (
          <Alert
            type="info"
            title="How it works"
            message="Enter the recipient's phone number with country code. They must have a Mobibit Africa account. Transfer is instant with 0.5% fee."
          />
        )}

        {!success && activeTab === 'lightning' && (
          <Alert
            type="info"
            title="Lightning Network"
            message="Paste a BOLT11 invoice (starts with lnbc). Payment settles instantly on the Lightning Network."
          />
        )}

        {/* ═══ QUICK ACTIONS ═══ */}
        {!success && (
          <div className="flex gap-3 mt-6">
            <Button
              onClick={() => navigate('/receive')}
              variant="secondary"
              className="flex-1"
            >
              ↙ Receive
            </Button>
            <Button
              onClick={() => navigate('/transactions')}
              variant="secondary"
              className="flex-1"
            >
              📋 History
            </Button>
          </div>
        )}
      </motion.div>

      <Toast message={toast.message} visible={toast.visible} onDismiss={() => setToast({ visible: false, message: '' })} />
    </div>
  );
}
