import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, PageHeader, Toast } from '../components';
import { paymentService, transactionService } from '../services';
import { useCurrencyConversion } from '../hooks';
import { copyToClipboard, formatCurrency } from '../utils';

export default function Send() {
  const navigate = useNavigate();
  const { convertSatsToUsd } = useCurrencyConversion();
  const [formData, setFormData] = useState({
    recipient: '',
    amount: '',
    memo: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [errors, setErrors] = useState({});
  const [toast, setToast] = useState({ visible: false, message: '' });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.recipient.trim()) {
      newErrors.recipient = 'Lightning address or invoice is required';
    }
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
      const result = await paymentService.sendBitcoin(
        formData.recipient,
        parseInt(formData.amount),
        formData.memo
      );

      if (result.success) {
        await transactionService.createTransaction({
          type: 'payment',
          title: 'Lightning Payment Sent',
          amount: parseInt(formData.amount),
          currency: 'sats',
          usd: convertSatsToUsd(parseInt(formData.amount)),
          description: formData.memo || 'Payment sent via Lightning',
          status: 'settled',
          timestamp: new Date(),
        });

        setSuccess({
          title: 'Payment Sent!',
          message: `${parseInt(formData.amount).toLocaleString()} sats sent successfully`,
          txHash: result.transactionHash,
          fee: result.fee,
        });

        setFormData({ recipient: '', amount: '', memo: '' });
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Payment failed' });
    } finally {
      setIsLoading(false);
    }
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
        {success && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
            <Alert type="success" title={success.title} message={success.message} />
            <div className="panel p-4 mt-4 space-y-3">
              <div>
                <p className="text-xs text-ink-muted">Transaction Hash</p>
                <div className="flex items-center gap-2 mt-1">
                  <code className="text-xs bg-elevated px-2 py-1 rounded flex-1 break-all font-figures text-ink-soft">
                    {success.txHash.slice(0, 20)}...
                  </code>
                  <button
                    onClick={async () => {
                      const ok = await copyToClipboard(success.txHash);
                      if (ok) setToast({ visible: true, message: 'Transaction hash copied!' });
                    }}
                    className="text-xs text-amber hover:brightness-110 font-semibold"
                  >
                    Copy
                  </button>
                </div>
              </div>
              <div className="flex justify-between text-sm pt-3 border-t border-line">
                <span className="text-ink-soft">Network Fee</span>
                <span className="font-semibold text-ink font-figures">{success.fee} sats</span>
              </div>
            </div>
            <Button onClick={() => navigate('/transactions')} className="w-full mt-4">
              View Transactions
            </Button>
          </motion.div>
        )}

        {errors.submit && (
          <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
        )}

        <div className="panel p-8 mb-8">
          <h2 className="heading-3 mb-6">Send Bitcoin via Lightning</h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            <Input
              label="Lightning Address or Invoice"
              type="text"
              name="recipient"
              value={formData.recipient}
              onChange={handleChange}
              placeholder="lnbc1000u1p..."
              error={!!errors.recipient}
              helperText={errors.recipient || 'Paste a Lightning invoice or address'}
            />

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
            />

            {formData.amount && (
              <motion.div
                className="bg-amber/10 border border-amber/30 rounded-xl p-4"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <p className="text-sm text-ink-soft mb-1">USD Equivalent</p>
                <p className="heading-3 text-amber">
                  {formatCurrency(convertSatsToUsd(parseInt(formData.amount) || 0), 'USD')}
                </p>
              </motion.div>
            )}

            <Input
              label="Memo (Optional)"
              type="text"
              name="memo"
              value={formData.memo}
              onChange={handleChange}
              placeholder="Payment for..."
              helperText="Add a note to remember what this payment was for"
            />

            <Button
              type="submit"
              disabled={isLoading || !formData.recipient || !formData.amount}
              className="w-full"
              size="lg"
            >
              {isLoading ? 'Sending...' : 'Send Bitcoin'}
            </Button>
          </form>
        </div>

        <Alert
          type="info"
          title="Lightning Network"
          message="Payments settle instantly on the Lightning Network with minimal fees."
        />
      </motion.div>

      <Toast message={toast.message} visible={toast.visible} onDismiss={() => setToast({ visible: false, message: '' })} />
    </div>
  );
}
