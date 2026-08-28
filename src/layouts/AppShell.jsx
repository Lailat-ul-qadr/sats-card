import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Logo } from '../components';
import { useAuth } from '../context';

const NAV_ITEMS = [
  { to: '/dashboard', label: 'Dashboard', icon: '◈' },
  { to: '/card', label: 'Card', icon: '▭' },
  { to: '/fund', label: 'Fund', icon: '↓' },
  { to: '/send', label: 'Send', icon: '↗' },
  { to: '/receive', label: 'Receive', icon: '↙' },
  { to: '/spend', label: 'Spend', icon: '◆' },
  { to: '/transactions', label: 'Activity', icon: '≡' },
];

const SECONDARY_ITEMS = [
  { to: '/profile', label: 'Profile', icon: '◎' },
  { to: '/settings', label: 'Settings', icon: '⚙' },
  { to: '/help', label: 'Help', icon: '?' },
];

export default function AppShell({ children }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const navLinkClass = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-colors group ${
      isActive
        ? 'bg-amber/10 text-amber border border-amber/30'
        : 'text-ink-soft border border-transparent hover:bg-white/5 hover:text-ink'
    }`;

  const SidebarContent = () => (
    <>
      <div className="px-2 mb-8">
        <Logo />
      </div>

      <nav className="flex-1 flex flex-col gap-1 px-0">
        {NAV_ITEMS.map(item => (
          <NavLink key={item.to} to={item.to} className={navLinkClass} onClick={() => setMobileOpen(false)}>
            <span className="w-5 text-center opacity-80">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="divider my-4" />

      <div className="flex flex-col gap-1">
        {SECONDARY_ITEMS.map(item => (
          <NavLink key={item.to} to={item.to} className={navLinkClass} onClick={() => setMobileOpen(false)}>
            <span className="w-5 text-center opacity-80">{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </div>

      <div className="mt-6 panel p-4 flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-amber-lime flex items-center justify-center text-bg font-bold text-sm shrink-0">
          {(user?.name || 'D U').split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          <p className="text-sm font-semibold text-ink truncate">{user?.name || 'Demo User'}</p>
          <button onClick={handleLogout} className="text-xs text-ink-muted hover:text-danger transition-colors">
            Log out
          </button>
        </div>
      </div>
    </>
  );

  return (
    <div className="min-h-screen bg-noise-grid text-ink flex">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex flex-col w-64 shrink-0 border-r border-line px-4 py-6 sticky top-0 h-screen">
        <SidebarContent />
      </aside>

      {/* Mobile top bar */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3 bg-surface/90 backdrop-blur border-b border-line">
        <Logo size="sm" />
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          className="w-9 h-9 rounded-lg border border-line flex items-center justify-center text-ink"
          aria-label="Toggle menu"
        >
          {mobileOpen ? '✕' : '☰'}
        </button>
      </div>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <div className="lg:hidden fixed inset-0 z-20 pt-16">
            <motion.div
              className="absolute inset-0 bg-black/70"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={() => setMobileOpen(false)}
            />
            <motion.aside
              className="relative w-72 h-full bg-surface border-r border-line px-4 py-6 flex flex-col overflow-y-auto"
              initial={{ x: -288 }}
              animate={{ x: 0 }}
              exit={{ x: -288 }}
              transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            >
              <SidebarContent />
            </motion.aside>
          </div>
        )}
      </AnimatePresence>

      {/* Main content */}
      <main className="flex-1 min-w-0 pt-16 lg:pt-0">
        {children}
      </main>
    </div>
  );
}
