import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, PageHeader } from '../components';
import { paymentService, transactionService } from '../services';
import { useCurrencyConversion } from '../hooks';
import { formatCurrency } from '../utils';

export default function Spend() {
  const navigate = useNavigate();
  const { convertSatsToUsd } = useCurrencyConversion();
  const [formData, setFormData] = useState({
    merchant: '',
    amount: '',
    cardLast4: '4242',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(null);
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.merchant.trim()) {
      newErrors.merchant = 'Merchant name is required';
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
      const satsAmount = Math.floor(parseFloat(formData.amount) * 39500);

      const result = await paymentService.spendCard(
        formData.merchant,
        parseFloat(formData.amount),
        formData.cardLast4
      );

      if (result.success) {
        await transactionService.createTransaction({
          type: 'spend',
          title: 'Virtual Card Spend',
          amount: parseFloat(formData.amount),
          currency: 'USD',
          sats: satsAmount,
          description: `Payment at ${formData.merchant}`,
          status: 'settled',
          merchant: formData.merchant,
          timestamp: new Date(),
        });

        setSuccess({
          title: 'Payment Approved!',
          message: `${formatCurrency(parseFloat(formData.amount), 'USD')} spent at ${formData.merchant}`,
          transactionId: result.transactionId,
          satsSpent: satsAmount,
        });

        setFormData({ merchant: '', amount: '', cardLast4: '4242' });
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Payment failed' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Spend with Card" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {success && (
          <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
            <Alert type="success" title={success.title} message={success.message} />
            <div className="panel p-4 mt-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-ink-soft text-sm">Transaction ID</span>
                <span className="font-figures text-sm text-ink">{success.transactionId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-ink-soft text-sm">Sats Spent</span>
                <span className="font-semibold text-ink font-figures text-sm">{success.satsSpent.toLocaleString()}</span>
              </div>
            </div>
            <div className="flex gap-4 mt-4">
              <Button onClick={() => navigate('/dashboard')} className="flex-1">
                Dashboard
              </Button>
              <Button
                variant="secondary"
                onClick={() => {
                  setSuccess(null);
                  setFormData({ merchant: '', amount: '', cardLast4: '4242' });
                }}
                className="flex-1"
              >
                Another Transaction
              </Button>
            </div>
          </motion.div>
        )}

        {errors.submit && (
          <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
        )}

        {!success && (
          <div className="panel p-8 mb-8">
            <h2 className="heading-3 mb-6">Complete Purchase</h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Merchant Name"
                type="text"
                name="merchant"
                value={formData.merchant}
                onChange={handleChange}
                placeholder="e.g., Coffee Shop, Electronics Store"
                error={!!errors.merchant}
                helperText={errors.merchant}
              />

              <Input
                label="Amount (USD)"
                type="number"
                name="amount"
                value={formData.amount}
                onChange={handleChange}
                placeholder="25.99"
                min="0.01"
                step="0.01"
                error={!!errors.amount}
                helperText={errors.amount}
              />

              {formData.amount && (
                <motion.div
                  className="bg-danger/10 border border-danger/30 rounded-xl p-4"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <p className="text-sm text-ink-soft mb-1">Sats Deducted</p>
                  <p className="heading-3 text-danger">
                    {Math.floor(parseFloat(formData.amount) * 39500).toLocaleString()} sats
                  </p>
                </motion.div>
              )}

              <div>
                <label className="text-xs font-semibold text-ink-muted mb-3 block uppercase tracking-wider">
                  Card
                </label>
                <div className="flex items-center gap-3 p-4 bg-elevated border border-line rounded-xl">
                  <span className="text-2xl">💳</span>
                  <div>
                    <p className="font-semibold text-ink text-sm">Mobibit Africa</p>
                    <p className="text-sm text-ink-soft font-figures">**** **** **** {formData.cardLast4}</p>
                  </div>
                </div>
              </div>

              <Button
                type="submit"
                disabled={isLoading || !formData.merchant || !formData.amount}
                className="w-full"
                size="lg"
              >
                {isLoading ? 'Processing...' : 'Complete Payment'}
              </Button>
            </form>

            <Alert
              type="info"
              title="Demo Mode"
              message="This is a simulated card transaction. In production, this would connect to a real payment processor."
              className="mt-6"
            />
          </div>
        )}
      </motion.div>
    </div>
  );
}
