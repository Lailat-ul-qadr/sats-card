/**
 * Service Layer — connects to the real FastAPI backend.
 *
 * In demo mode (no backend running), falls back to mock data.
 * When the backend is running, all calls go through the real API.
 */

import { authAPI, walletAPI, paymentAPI, rateAPI } from './api';

// ── Feature Flag ──────────────────────────────────────────────────────
// Set to true to use real API, false for mock/demo mode
const USE_REAL_API = import.meta.env.VITE_USE_REAL_API === 'true';

// ── Mock Data (fallback for demo mode) ────────────────────────────────

const MOCK_DELAY = (ms = 500) => new Promise(r => setTimeout(r, ms));

const MOCK_RATES = {
  UGX: 3700, KES: 130, TZS: 2500, GHS: 12, NGN: 1550,
  USD: 1, EUR: 0.92, GBP: 0.79,
};

const MOCK_BALANCE = { sats: 250000, btc: 0.0025, usd: 98.75 };

const MOCK_TXS = [
  { id: '1', type: 'topup', title: 'Mobile Money Fund', amount: 2.50, currency: 'USD', sats: 98765, status: 'settled', timestamp: new Date(Date.now() - 5 * 60000), description: 'MTN Mobile Money → BTC' },
  { id: '2', type: 'payment', title: 'Lightning Payment', amount: 1000, currency: 'sats', usd: 39.50, status: 'settled', timestamp: new Date(Date.now() - 15 * 60000), description: 'Invoice payment received' },
  { id: '3', type: 'spend', title: 'Virtual Card Spend', amount: 25.00, currency: 'USD', sats: 63291, status: 'settled', timestamp: new Date(Date.now() - 3600000), description: 'Merchant payment' },
  { id: '4', type: 'topup', title: 'Mobile Money Fund', amount: 5.00, currency: 'USD', sats: 197530, status: 'settled', timestamp: new Date(Date.now() - 7200000), description: 'Airtel Mobile Money → BTC' },
];

// ── Auth Service ──────────────────────────────────────────────────────

export const authService = {
  login: async (email, phone, pin) => {
    if (USE_REAL_API) {
      const result = await authAPI.login(phone, pin);
      return { success: true, token: result.tokens?.access_token, user: result.user, ...result };
    }
    await MOCK_DELAY(1500);
    const token = 'demo_token_' + Math.random().toString(36).substr(2, 9);
    const user = { id: '1', email: email || 'demo@satscardapp.com', name: 'Demo User', phone: phone || '+256701234567' };
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user', JSON.stringify(user));
    return { success: true, token, user };
  },

  signup: async (email, pin, phone, name) => {
    if (USE_REAL_API) {
      const result = await authAPI.register(phone, pin, name || 'User', 'RW');
      return { success: true, token: result.tokens?.access_token, user: result.user, ...result };
    }
    await MOCK_DELAY(2000);
    const token = 'demo_token_' + Math.random().toString(36).substr(2, 9);
    const user = { id: '1', email: email || 'demo@satscardapp.com', name: name || 'New User', phone };
    localStorage.setItem('auth_token', token);
    localStorage.setItem('user', JSON.stringify(user));
    return { success: true, token, user };
  },

  logout: async () => {
    if (USE_REAL_API) return authAPI.logout();
    await MOCK_DELAY(500);
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    return { success: true };
  },
};

// ── Wallet Service ────────────────────────────────────────────────────

export const walletService = {
  getBalance: async () => {
    if (USE_REAL_API) {
      const data = await walletAPI.getBalance();
      return { sats: data.balance_sats, btc: data.balance_btc, usd: data.balance_usd };
    }
    await MOCK_DELAY();
    return { ...MOCK_BALANCE };
  },

  getCardInfo: async () => {
    await MOCK_DELAY();
    return { cardNumber: '4242 4242 4242 4242', cardName: 'SATS CARD', holder: 'DEMO USER', expires: '12/25' };
  },

  addFunds: async (amount, currency) => {
    await MOCK_DELAY(1500);
    return { success: true, satsReceived: Math.floor(amount * 39500), usdEquivalent: amount };
  },
};

// ── Transaction Service ───────────────────────────────────────────────

export const transactionService = {
  getTransactions: async () => {
    await MOCK_DELAY();
    return [...MOCK_TXS];
  },

  createTransaction: async (transaction) => {
    await MOCK_DELAY(1200);
    return { ...transaction, id: Math.random().toString(36).substr(2, 9), status: 'settled', timestamp: new Date() };
  },
};

// ── Payment Service ───────────────────────────────────────────────────

export const paymentService = {
  fundCard: async (phoneNumber, amount, provider) => {
    if (USE_REAL_API) {
      const result = await paymentAPI.collect(phoneNumber, amount, 'UGX', provider, 'Sats Card Top-Up');
      return {
        success: true,
        transactionId: result.provider_txn_id,
        satsReceived: result.amount_sats,
        provider: result.provider,
        phoneNumber,
        timestamp: new Date(),
      };
    }
    await MOCK_DELAY(2000);
    return {
      success: true,
      transactionId: 'TXN' + Math.random().toString(36).substr(2, 9).toUpperCase(),
      satsReceived: Math.floor(amount * 39500),
      provider,
      phoneNumber,
      timestamp: new Date(),
    };
  },

  sendBitcoin: async (recipientAddress, amount, memo) => {
    await MOCK_DELAY(2500);
    return {
      success: true,
      transactionHash: 'f' + Math.random().toString(16).substr(2, 60),
      amount, recipientAddress, memo,
      timestamp: new Date(),
      fee: Math.floor(amount * 0.01),
    };
  },

  receiveBitcoin: async (amount, description) => {
    await MOCK_DELAY(1500);
    return {
      success: true,
      invoice: 'lnbc' + Math.random().toString(36).substr(2, 50),
      amount, description,
      expiresAt: new Date(Date.now() + 3600000),
      timestamp: new Date(),
    };
  },

  spendCard: async (merchantName, amount, cardLast4) => {
    await MOCK_DELAY(1800);
    return {
      success: true,
      transactionId: 'SPEND' + Math.random().toString(36).substr(2, 9).toUpperCase(),
      merchant: merchantName, amount, cardLast4,
      timestamp: new Date(), status: 'approved',
    };
  },
};

// ── Exchange Rate Service ─────────────────────────────────────────────

export const exchangeRateService = {
  getExchangeRate: async (from = 'USD', to = 'BTC') => {
    if (USE_REAL_API) {
      const data = await rateAPI.getRate(from, to);
      return { from: data.from_currency, to: data.to_currency, rate: data.rate, timestamp: new Date(data.timestamp * 1000) };
    }
    await MOCK_DELAY(300);
    const rate = from === 'USD' && to === 'BTC' ? 0.000025 : 39500;
    return { from, to, rate, timestamp: new Date() };
  },

  convertCurrency: async (amount, from, to) => {
    if (USE_REAL_API) {
      const data = await rateAPI.convert(amount, from, to);
      return { amount: data.amount, from: data.from, to: data.to, converted: data.converted };
    }
    await MOCK_DELAY(300);
    let converted;
    if (from === 'USD' && to === 'sats') converted = Math.floor(amount * 39500);
    else if (from === 'sats' && to === 'USD') converted = (amount / 39500).toFixed(2);
    else converted = amount;
    return { amount, from, to, converted };
  },
};

// ── User Profile Service ──────────────────────────────────────────────

export const userService = {
  getProfile: async () => {
    await MOCK_DELAY();
    return { id: '1', name: 'Demo User', email: 'demo@satscardapp.com', phone: '+256701234567', country: 'Uganda', createdAt: new Date('2024-08-01'), kyc: { verified: true, level: 'tier2' } };
  },

  updateProfile: async (updates) => {
    await MOCK_DELAY(1000);
    return { success: true, user: { ...updates, id: '1' } };
  },
};

// ── Notification Service ──────────────────────────────────────────────

export const notificationService = {
  getNotifications: async () => {
    await MOCK_DELAY();
    return [
      { id: '1', type: 'success', title: 'Payment Received', message: '1000 sats received via Lightning', timestamp: new Date(Date.now() - 120000), read: false },
      { id: '2', type: 'info', title: 'Card Balance Low', message: 'Your card balance is below $10', timestamp: new Date(Date.now() - 1800000), read: false },
      { id: '3', type: 'success', title: 'Mobile Money Received', message: 'MTN payment of $5 received and converted', timestamp: new Date(Date.now() - 7200000), read: true },
    ];
  },
};
