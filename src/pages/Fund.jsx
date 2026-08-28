import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, PageHeader } from '../components';
import { paymentService, transactionService } from '../services';
import { mockMobileMoneyProviders } from '../data';
import { useCurrencyConversion } from '../hooks';
import { formatCurrency } from '../utils';

export default function Fund() {
  const navigate = useNavigate();
  const { convertUsdToSats } = useCurrencyConversion();
  const [formData, setFormData] = useState({
    phoneNumber: '',
    amount: '',
    provider: 'mtn',
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
    if (!formData.phoneNumber.trim()) {
      newErrors.phoneNumber = 'Phone number is required';
    }
    const amount = parseFloat(formData.amount);
    if (!formData.amount || amount <= 0) {
      newErrors.amount = 'Amount must be greater than 0';
    }
    if (amount > 500) {
      newErrors.amount = 'Amount exceeds daily limit of $500';
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
      const providerName = mockMobileMoneyProviders.find(p => p.id === formData.provider)?.name;

      const result = await paymentService.fundCard(
        formData.phoneNumber,
        parseFloat(formData.amount),
        providerName
      );

      if (result.success) {
        await transactionService.createTransaction({
          type: 'topup',
          title: 'Mobile Money Fund',
          amount: parseFloat(formData.amount),
          currency: 'USD',
          sats: convertUsdToSats(parseFloat(formData.amount)),
          description: `${providerName} → Bitcoin`,
          status: 'settled',
          timestamp: new Date(),
        });

        setSuccess({
          title: 'Funds Added Successfully!',
          message: `${formatCurrency(result.satsReceived, 'sats')} received to your account`,
          transactionId: result.transactionId,
          satsReceived: result.satsReceived,
        });

        setFormData({ phoneNumber: '', amount: '', provider: 'mtn' });

        setTimeout(() => {
          navigate('/card');
        }, 3000);
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Transaction failed' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Fund Your Card" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-12"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {success && (
          <Alert type="success" title={success.title} message={success.message} className="mb-6" />
        )}

        {errors.submit && (
          <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
        )}

        <div className="panel p-8 mb-8">
          <h2 className="heading-3 mb-6">Add Funds via Mobile Money</h2>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="text-xs font-semibold text-ink-muted mb-3 block uppercase tracking-wider">
                Mobile Money Provider
              </label>
              <div className="grid sm:grid-cols-3 gap-3">
                {mockMobileMoneyProviders.map(provider => (
                  <motion.div key={provider.id} whileHover={{ y: -2 }} whileTap={{ scale: 0.98 }}>
                    <input
                      type="radio"
                      id={provider.id}
                      name="provider"
                      value={provider.id}
                      checked={formData.provider === provider.id}
                      onChange={handleChange}
                      className="hidden"
                    />
                    <label
                      htmlFor={provider.id}
                      className={`block p-4 border rounded-xl cursor-pointer transition-all ${
                        formData.provider === provider.id
                          ? 'border-amber bg-amber/10'
                          : 'border-line hover:border-amber/40'
                      }`}
                    >
                      <div className="text-2xl mb-2">{provider.logo}</div>
                      <p className="font-semibold text-ink text-sm">{provider.name.split(' ')[0]}</p>
                    </label>
                  </motion.div>
                ))}
              </div>
            </div>

            <Input
              label="Phone Number"
              type="tel"
              name="phoneNumber"
              value={formData.phoneNumber}
              onChange={handleChange}
              placeholder="+256701234567"
              error={!!errors.phoneNumber}
              helperText={errors.phoneNumber || 'Your mobile money account number'}
            />

            <Input
              label="Amount (USD)"
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              placeholder="10.00"
              min="0.01"
              max="500"
              step="0.01"
              error={!!errors.amount}
              helperText={errors.amount || 'Min: $1, Max: $500 per day'}
            />

            {formData.amount && (
              <motion.div
                className="bg-lime/10 border border-lime/30 rounded-xl p-4"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <p className="text-sm text-ink-soft mb-1">You will receive:</p>
                <p className="heading-3 text-lime">
                  {convertUsdToSats(parseFloat(formData.amount) || 0).toLocaleString()} sats
                </p>
                <p className="text-xs text-ink-muted mt-1">@ 39,500 sats per USD</p>
              </motion.div>
            )}

            <Button
              type="submit"
              disabled={isLoading || !formData.phoneNumber || !formData.amount}
              className="w-full"
              size="lg"
            >
              {isLoading ? 'Processing...' : 'Add Funds'}
            </Button>
          </form>
        </div>

        <div className="space-y-4">
          <div className="bg-info/10 border border-info/20 rounded-xl p-4">
            <h3 className="font-semibold text-info mb-2 text-sm">How it works</h3>
            <ol className="text-sm text-ink-soft space-y-1">
              <li>1. Select your mobile money provider</li>
              <li>2. Enter your phone number and amount</li>
              <li>3. Confirm the transaction</li>
              <li>4. Bitcoin will be deposited to your card instantly</li>
            </ol>
          </div>

          <Alert
            type="info"
            message="All transactions in this demo are simulated. No real money will be transferred."
          />
        </div>
      </motion.div>
    </div>
  );
}
