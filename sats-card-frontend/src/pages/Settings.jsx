import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Button, PageHeader, Toast } from '../components';
import { mockSettings } from '../data';

const Toggle = ({ checked, onChange }) => (
  <button
    onClick={onChange}
    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors shrink-0 ${
      checked ? 'bg-amber' : 'bg-elevated border border-line'
    }`}
  >
    <span
      className={`inline-block h-4 w-4 transform rounded-full bg-bg transition-transform ${
        checked ? 'translate-x-6 bg-bg' : 'translate-x-1 bg-ink-muted'
      }`}
    />
  </button>
);

const selectClass = "w-full px-4 py-3 bg-surface border border-line rounded-xl text-ink focus:outline-none";
const inputClass = "w-full px-4 py-3 bg-surface border border-line rounded-xl text-ink focus:outline-none";

export default function Settings() {
  const navigate = useNavigate();
  const [settings, setSettings] = useState(mockSettings);
  const [toast, setToast] = useState({ visible: false, message: '' });
  const [saveCount, setSaveCount] = useState(0);

  const handleToggle = (key) => {
    setSettings(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: value }));
  };

  return (
    <div className="min-h-screen bg-noise-grid">
      <PageHeader title="Settings" onBack={() => navigate(-1)} />

      <motion.div
        className="max-w-2xl mx-auto px-4 sm:px-6 py-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Notifications */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">Notifications</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-4 border-b border-line">
              <div>
                <p className="font-semibold text-ink">Push Notifications</p>
                <p className="text-sm text-ink-soft mt-1">Get alerts on your phone</p>
              </div>
              <Toggle checked={settings.pushNotifications} onChange={() => handleToggle('pushNotifications')} />
            </div>

            <div className="flex items-center justify-between pb-4 border-b border-line">
              <div>
                <p className="font-semibold text-ink">Email Notifications</p>
                <p className="text-sm text-ink-soft mt-1">Receive updates via email</p>
              </div>
              <Toggle checked={settings.emailNotifications} onChange={() => handleToggle('emailNotifications')} />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-semibold text-ink">All Notifications</p>
                <p className="text-sm text-ink-soft mt-1">Enable all notification types</p>
              </div>
              <Toggle checked={settings.notificationsEnabled} onChange={() => handleToggle('notificationsEnabled')} />
            </div>
          </div>
        </div>

        {/* Limits */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">Transaction Limits</h2>
          <div className="space-y-5">
            <div>
              <label className="text-xs font-semibold text-ink-muted block mb-2 uppercase tracking-wider">Daily Limit (USD)</label>
              <input
                type="number"
                name="dailyLimit"
                value={settings.dailyLimit}
                onChange={handleChange}
                className={inputClass}
              />
              <p className="text-xs text-ink-muted mt-1.5">Current: ${settings.dailyLimit}</p>
            </div>

            <div>
              <label className="text-xs font-semibold text-ink-muted block mb-2 uppercase tracking-wider">Monthly Limit (USD)</label>
              <input
                type="number"
                name="monthlyLimit"
                value={settings.monthlyLimit}
                onChange={handleChange}
                className={inputClass}
              />
              <p className="text-xs text-ink-muted mt-1.5">Current: ${settings.monthlyLimit}</p>
            </div>
          </div>
        </div>

        {/* Preferences */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">Preferences</h2>
          <div className="space-y-5">
            <div>
              <label className="text-xs font-semibold text-ink-muted block mb-2 uppercase tracking-wider">Preferred Currency</label>
              <select name="preferredCurrency" value={settings.preferredCurrency} onChange={handleChange} className={selectClass}>
                <option value="USD">USD</option>
                <option value="EUR">EUR</option>
                <option value="GBP">GBP</option>
                <option value="BTC">Bitcoin</option>
              </select>
            </div>

            <div>
              <label className="text-xs font-semibold text-ink-muted block mb-2 uppercase tracking-wider">Language</label>
              <select name="language" value={settings.language} onChange={handleChange} className={selectClass}>
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="sw">Swahili</option>
              </select>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-line">
              <div>
                <p className="font-semibold text-ink">Auto Convert to Bitcoin</p>
                <p className="text-sm text-ink-soft mt-1">Automatically convert received fiat to Bitcoin</p>
              </div>
              <Toggle checked={settings.autoConvert} onChange={() => handleToggle('autoConvert')} />
            </div>
          </div>
        </div>

        {/* Data & Privacy */}
        <div className="panel p-8 mb-6">
          <h2 className="heading-3 mb-6">Data & Privacy</h2>
          <div className="space-y-3">
            {[
              { title: 'Download Your Data', sub: 'Export all your personal data' },
              { title: 'Privacy Policy', sub: 'Review our privacy policy' },
              { title: 'Terms of Service', sub: 'Review our terms' },
            ].map(item => (
              <button
                key={item.title}
                className="w-full text-left px-4 py-3 hover:bg-white/5 rounded-xl transition-colors border border-line"
              >
                <p className="font-semibold text-ink text-sm">{item.title}</p>
                <p className="text-sm text-ink-muted mt-1">{item.sub}</p>
              </button>
            ))}
          </div>
        </div>

        <Button className="w-full" size="lg" onClick={() => {
          setSaveCount(c => c + 1);
          setToast({ visible: true, message: 'Settings saved successfully!' });
        }}>
          Save Settings
        </Button>

        <Toast message={toast.message} visible={toast.visible} onDismiss={() => setToast({ visible: false, message: '' })} />
      </motion.div>
    </div>
  );
}
