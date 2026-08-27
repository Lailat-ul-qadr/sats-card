import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, WalletProvider, ThemeProvider } from './context';
import { useAuth } from './context';
import AppShell from './layouts/AppShell';
import './styles.css';

// Import all pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Card from './pages/Card';
import Fund from './pages/Fund';
import Send from './pages/Send';
import Receive from './pages/Receive';
import Spend from './pages/Spend';
import Transactions from './pages/Transactions';
import Profile from './pages/Profile';
import Settings from './pages/Settings';
import Help from './pages/Help';

// Protected Route component — wraps authenticated pages in the app shell
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <AppShell>{children}</AppShell>;
};

// Public Route component
const PublicRoute = ({ children, restricted = false }) => {
  const { isAuthenticated } = useAuth();
  
  if (isAuthenticated && restricted) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

function AppRoutes() {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<PublicRoute><Landing /></PublicRoute>} />
      <Route path="/login" element={<PublicRoute restricted><Login /></PublicRoute>} />
      <Route path="/signup" element={<PublicRoute restricted><Signup /></PublicRoute>} />

      {/* Protected Routes */}
      <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
      <Route path="/card" element={<ProtectedRoute><Card /></ProtectedRoute>} />
      <Route path="/fund" element={<ProtectedRoute><Fund /></ProtectedRoute>} />
      <Route path="/send" element={<ProtectedRoute><Send /></ProtectedRoute>} />
      <Route path="/receive" element={<ProtectedRoute><Receive /></ProtectedRoute>} />
      <Route path="/spend" element={<ProtectedRoute><Spend /></ProtectedRoute>} />
      <Route path="/transactions" element={<ProtectedRoute><Transactions /></ProtectedRoute>} />
      <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
      <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
      <Route path="/help" element={<ProtectedRoute><Help /></ProtectedRoute>} />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <Router>
      <ThemeProvider>
        <AuthProvider>
          <WalletProvider>
            <AppRoutes />
          </WalletProvider>
        </AuthProvider>
      </ThemeProvider>
    </Router>
  );
}
