import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, Input, Alert, Logo } from '../components';
import { useAuth } from '../context';

export default function Signup() {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [formData, setFormData] = useState({
    fullName: '',
    phone: '',
    pin: '',
    confirmPin: '',
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    // For PIN fields, only allow digits and max 4 chars
    if (name === 'pin' || name === 'confirmPin') {
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

    if (!formData.fullName.trim()) {
      newErrors.fullName = 'Name is required';
    }
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
    if (formData.pin !== formData.confirmPin) {
      newErrors.confirmPin = 'PINs do not match';
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
      // Backend expects: phone, pin, name, country
      const result = await signup(formData.phone, formData.pin, formData.fullName);
      if (result.success) {
        setSuccessMessage('Account created! Redirecting to dashboard...');
        setTimeout(() => navigate('/dashboard'), 2000);
      }
    } catch (error) {
      setErrors({ submit: error.message || 'Signup failed' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-noise-grid flex items-center justify-center px-4 py-12 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-[420px] h-[420px] bg-lime/15 rounded-full blur-[130px] pointer-events-none" />

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
            <h1 className="heading-2 mb-2">Create account</h1>
            <p className="text-ink-soft text-sm">Join millions using mobile money to own Bitcoin</p>
          </div>

          {successMessage && (
            <Alert type="success" title="Success!" message={successMessage} className="mb-6" />
          )}

          {errors.submit && (
            <Alert type="error" title="Error" message={errors.submit} className="mb-6" />
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              label="Full Name"
              type="text"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              placeholder="Jean Paul"
              error={!!errors.fullName}
              helperText={errors.fullName}
            />

            <Input
              label="Phone Number"
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="+250788123456"
              error={!!errors.phone}
              helperText={errors.phone || 'Your mobile money phone number'}
            />

            <Input
              label="Create 4-Digit PIN"
              type="password"
              name="pin"
              value={formData.pin}
              onChange={handleChange}
              placeholder="••••"
              error={!!errors.pin}
              helperText={errors.pin || 'This is your login PIN'}
              maxLength={4}
            />

            <Input
              label="Confirm PIN"
              type="password"
              name="confirmPin"
              value={formData.confirmPin}
              onChange={handleChange}
              placeholder="••••"
              error={!!errors.confirmPin}
              helperText={errors.confirmPin}
              maxLength={4}
            />

            <Button
              type="submit"
              disabled={isLoading}
              className="w-full"
              size="lg"
            >
              {isLoading ? 'Creating account...' : 'Create Account'}
            </Button>
          </form>

          <div className="mt-8 p-4 bg-warning/10 border border-warning/20 rounded-lg">
            <p className="text-xs text-warning">
              <strong>Note:</strong> Your phone number is your identity. Use the same number for your mobile money account.
            </p>
          </div>
        </div>

        <p className="text-center text-ink-soft mt-6 text-sm">
          Already have an account?{' '}
          <button
            onClick={() => navigate('/login')}
            className="text-amber font-semibold hover:brightness-110"
          >
            Login here
          </button>
        </p>
      </motion.div>
    </div>
  );
}
