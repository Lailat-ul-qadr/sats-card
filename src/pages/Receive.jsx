import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Alert, Input, PageHeader, Toast } from '../components';
import { paymentService } from '../services';
import { copyToClipboard, formatDateTime } from '../utils';

export default function Receive() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
  });
  const [invoice, setInvoice] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ visible: false, message: '' });
  const [timeLeft, setTimeLeft] = useState('');
  const [pollStatus, setPollStatus] = useState('waiting'); // waiting | paid | expired

  // Countdown timer for invoice expiry
  useEffect(() => {
    if (!invoice?.expiresAt) return;
    const updateCountdown = () => {
      const diff = new Date(invoice.expiresAt) - new Date();
      if (diff <= 0) {
        setTimeLeft('Expired');
        return;
      }
      const mins = Math.floor(diff / 60000);
      const secs = Math.floor((diff % 60000) / 1000);
      setTimeLeft(`${mins}:${secs.toString().padStart(2, '0')}`);
    };
    updateCountdown();
    const id = setInterval(updateCountdown, 1000);
    return () => clearInterval(id);
  }, [invoice?.expiresAt]);

  // Poll for invoice payment every 3 seconds
  useEffect(() => {
    if (!invoice?.paymentId || pollStatus === 'paid') return;

    const pollForPayment = async () => {
      try {
        const result = await paymentService.checkInvoicePaid(invoice.paymentId);
        if (result.paid) {
          // Deposit sats to card after payment confirmed
          try {
            await paymentService.depositSats(invoice.paymentId);
          } catch (_) {}
          setPollStatus('paid');
        }
      } catch (err) {
        // Silently continue polling
      }
    };

    // Start polling immediately, then every 3 seconds
    pollForPayment();
    const pollId = setInterval(pollForPayment, 3000);
    return () => clearInterval(pollId);
  }, [invoice?.paymentId, invoice?.rHash, pollStatus]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    const amount = parseFloat(formData.amount);
    if (!formData.amount || amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }
    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validate();

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setIsLoading(true);
    try {
      const result = await paymentService.receiveBitcoin(
        parseInt(formData.amount),
        formData.description || 'Payment'
      );

      if (result.success) {
        setInvoice(result);
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Failed to generate invoice' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Receive Bitcoin" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {invoice && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="mb-8">
            <div className="panel-elevated p-8 border-lime/20">
              {pollStatus === 'paid' ? (
                <div className="text-center">
                  <div className="w-16 h-16 rounded-full bg-success/15 flex items-center justify-center text-3xl mx-auto mb-4">✓</div>
                  <h2 className="heading-3 text-success mb-2">Payment Received!</h2>
                  <p className="text-ink-soft">{Number(formData.amount).toLocaleString()} sats has been credited to your wallet.</p>
                  <Button onClick={() => navigate('/dashboard')} className="w-full mt-6">View Dashboard</Button>
                  <Button variant="secondary" onClick={() => { setInvoice(null); setPollStatus('waiting'); setFormData({ amount: '', description: '' }); }} className="w-full mt-2">Create Another</Button>
                </div>
              ) : (
                <h2 className="heading-3 mb-6">Lightning Invoice Generated</h2>
              )}

              <div className="space-y-4 mb-6">
                <div>
                  <p className="text-xs text-ink-muted mb-2">Amount</p>
                  <p className="heading-3 text-lime">{Number(formData.amount).toLocaleString()} sats</p>
                </div>

                <div className="panel p-4">
                  <p className="text-xs text-ink-muted mb-2">Invoice</p>
                  <div className="flex gap-2 items-start">
                    <code className="text-xs bg-elevated px-3 py-2 rounded flex-1 break-all font-figures text-ink-soft">
                      {invoice.invoice.slice(0, 50)}...
                    </code>
                    <button
                      onClick={async () => {
                        const ok = await copyToClipboard(invoice.invoice);
                        if (ok) setToast({ visible: true, message: 'Invoice copied to clipboard!' });
                      }}
                      className="px-3 py-2 bg-amber-lime text-bg rounded-lg text-xs font-semibold hover:brightness-110 transition-all shrink-0"
                    >
                      Copy
                    </button>
                  </div>
                </div>

                {formData.description && (
                  <div>
                    <p className="text-xs text-ink-muted mb-1">Description</p>
                    <p className="text-ink text-sm">{formData.description}</p>
                  </div>
                )}

                <div>
                  <p className="text-xs text-ink-muted mb-1">Expires</p>
                  <div className="flex items-center gap-2">
                    <p className="text-ink text-sm font-figures">{timeLeft}</p>
                    <span className="text-ink-muted text-xs">({formatDateTime(invoice.expiresAt)})</span>
                  </div>
                </div>

                {pollStatus === 'waiting' && (
                  <div className="flex items-center gap-2 text-amber">
                    <span className="animate-pulse">⏳</span>
                    <span className="text-sm">Waiting for payment...</span>
                  </div>
                )}
              </div>

              {pollStatus === 'paid' ? (
                <Alert type="success" title="Payment confirmed!" message="The sats have been added to your wallet balance." />
              ) : (
                <Alert
                  type="info"
                  title="Waiting for payment..."
                  message="Share this invoice. The page will update automatically when payment arrives."
                />
              )}

              {pollStatus !== 'paid' && (
                <div className="flex gap-4 mt-6">
                  <Button onClick={() => navigate('/dashboard')} className="flex-1">
                    Done
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => {
                      setInvoice(null);
                      setPollStatus('waiting');
                      setFormData({ amount: '', description: '' });
                    }}
                    className="flex-1"
                  >
                    Create Another
                  </Button>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {errors.submit && (
          <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
        )}

        {!invoice && (
          <div className="panel p-8 mb-8">
            <h2 className="heading-3 mb-6">Request Bitcoin Payment</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Amount (sats)"
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                placeholder="50000"
                min="1"
                step="1"
                error={!!errors.amount}
                helperText={errors.amount || 'Amount you want to receive'}
              />

              <Input
                label="Description (Optional)"
                type="text"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="e.g., Payment for services"
                helperText="Help the sender remember what this payment is for"
              />

              <Button
                type="submit"
                disabled={isLoading || !formData.amount}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Generating Invoice...' : 'Generate Invoice'}
              </Button>
            </form>

            <Alert
              type="info"
              title="How it works"
              message="Generate a Lightning invoice and share it with the sender. Payment will settle instantly once they pay."
              className="mt-6"
            />
          </div>
        )}

        <div className="space-y-4">
          <Alert
            type="info"
            title="Lightning Network"
            message="Invoices expire after 1 hour. Generate a new one if needed."
          />
        </div>
      </motion.div>

      <Toast message={toast.message} visible={toast.visible} onDismiss={() => setToast({ visible: false, message: '' })} />
    </div>
  );
}
