import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, Logo } from '../components';
import { useAuth } from '../context';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    phone: '',
    pin: '',
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // For PIN, only allow digits and max 4 chars
    if (name === 'pin') {
      const digits = value.replace(/\D/g, '').slice(0, 4);
      setFormData(prev => ({ ...prev, [name]: digits }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\+\d{10,15}$/.test(formData.phone)) {
      newErrors.phone = 'Enter phone in format: +250788123456';
    }
    if (!formData.pin) {
      newErrors.pin = 'PIN is required';
    } else if (formData.pin.length !== 4) {
      newErrors.pin = 'PIN must be 4 digits';
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
      const result = await login(formData.phone, formData.pin);
      if (result.success) {
        navigate('/dashboard');
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Login failed' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-noise-grid flex items-center justify-center px-4 py-12 relative overflow-hidden">
      <div className="absolute top-0 right-0 w-[420px] h-[420px] bg-amber/15 rounded-full blur-[130px] pointer-events-none" />

      <motion.div
        className="w-full max-w-md relative z-10"
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
      >
        <div className="flex justify-center mb-8">
          <button onClick={() => navigate('/')}>
            <Logo size="lg" />
          </button>
        </div>

        <div className="panel-elevated p-8">
          <div className="text-center mb-8">
            <h1 className="heading-2 mb-2">Welcome back</h1>
            <p className="text-ink-soft text-sm">Login with your phone number and PIN</p>
          </div>

          {errors.submit && (
            <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label="Phone Number"
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+250788123456"
              error={!!errors.phone}
              helperText={errors.phone || 'E.164 format with country code'}
            />

            <Input
              label="PIN"
              type="password"
              name="pin"
              value={formData.pin}
              onChange={handleChange}
              placeholder="••••"
              error={!!errors.pin}
              helperText={errors.pin || 'Your 4-digit USSD PIN'}
              maxLength={4}
            />

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full"
              size="lg"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </Button>
          </form>

          <div className="mt-8 p-4 bg-info/10 border border-info/20 rounded-lg space-y-1.5">
            <p className="text-xs font-semibold text-info">Demo Credentials</p>
            <p className="text-xs text-ink-soft">Phone: <code className="bg-white/10 px-1.5 py-0.5 rounded text-ink">+250788123456</code></p>
            <p className="text-xs text-ink-soft">PIN: <code className="bg-white/10 px-1.5 py-0.5 rounded text-ink">1234</code></p>
            <p className="text-xs text-ink-muted">Register first if you haven't</p>
          </div>
        </div>

        <p className="text-center text-ink-soft mt-6 text-sm">
          Don't have an account?{' '}
          <button
            onClick={() => navigate('/signup')}
            className="text-amber font-semibold hover:brightness-110"
          >
            Sign up here
          </button>
        </p>
      </motion.div>
    </div>
  );
}
