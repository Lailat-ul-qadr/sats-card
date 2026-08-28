// Mock data for demo
export const mockUser = {
  id: '1',
  name: 'Demo User',
  email: 'demo@mobibitafrica.com',
  phone: '+256701234567',
  country: 'Uganda',
  avatar: null,
  createdAt: new Date('2024-08-01'),
};

export const mockWallet = {
  sats: 250000,
  btc: 0.0025,
  usd: 98.75,
  pendingTransactions: 0,
};

export const mockCard = {
  cardNumber: '4242 4242 4242 4242',
  cardName: 'MOBIBIT AFRICA',
  holder: 'DEMO USER',
  expires: '12/25',
  lastUsed: new Date(Date.now() - 2 * 3600000),
  status: 'active',
};

export const mockTransactions = [
  {
    id: '1',
    type: 'topup',
    title: 'Mobile Money Fund',
    amount: 2.50,
    currency: 'USD',
    sats: 98765,
    status: 'settled',
    timestamp: new Date(Date.now() - 5 * 60000),
    description: 'MTN Mobile Money → BTC',
    provider: 'MTN',
    txHash: 'f' + Math.random().toString(16).substr(2, 60),
  },
  {
    id: '2',
    type: 'payment',
    title: 'Lightning Payment',
    amount: 1000,
    currency: 'sats',
    usd: 39.50,
    status: 'settled',
    timestamp: new Date(Date.now() - 15 * 60000),
    description: 'Invoice payment received',
    invoice: 'lnbc' + Math.random().toString(36).substr(2, 50),
  },
  {
    id: '3',
    type: 'spend',
    title: 'Virtual Card Spend',
    amount: 25.00,
    currency: 'USD',
    sats: 63291,
    status: 'settled',
    timestamp: new Date(Date.now() - 1 * 3600000),
    description: 'Merchant payment',
    merchant: 'Coffee Shop',
  },
  {
    id: '4',
    type: 'topup',
    title: 'Mobile Money Fund',
    amount: 5.00,
    currency: 'USD',
    sats: 197530,
    status: 'settled',
    timestamp: new Date(Date.now() - 2 * 3600000),
    description: 'Airtel Mobile Money → BTC',
    provider: 'Airtel',
  },
];

export const mockNotifications = [
  {
    id: '1',
    type: 'success',
    title: 'Payment Received',
    message: '1000 sats received via Lightning',
    timestamp: new Date(Date.now() - 2 * 60000),
    read: false,
  },
  {
    id: '2',
    type: 'warning',
    title: 'Card Balance Low',
    message: 'Your card balance is below $10',
    timestamp: new Date(Date.now() - 30 * 60000),
    read: false,
  },
  {
    id: '3',
    type: 'success',
    title: 'Mobile Money Received',
    message: 'MTN payment of $5 received and converted',
    timestamp: new Date(Date.now() - 2 * 3600000),
    read: true,
  },
];

export const mockExchangeRates = {
  USDBTC: 0.000025,
  USDSATS: 39500,
  BTCUSD: 39500,
  SATSUSD: 0.000025,
  timestamp: new Date(),
};

export const mockMobileMoneyProviders = [
  { id: 'mtn', name: 'MTN Mobile Money', logo: '📱', color: '#FFCC00' },
  { id: 'airtel', name: 'Airtel Mobile Money', logo: '📱', color: '#FF0000' },
  { id: 'orangemoney', name: 'Orange Money', logo: '📱', color: '#FF9900' },
];

export const mockCountries = [
  { code: 'UG', name: 'Uganda', currency: 'UGX', rate: 3700 },
  { code: 'KE', name: 'Kenya', currency: 'KES', rate: 130 },
  { code: 'TZ', name: 'Tanzania', currency: 'TZS', rate: 2500 },
  { code: 'GH', name: 'Ghana', currency: 'GHS', rate: 12 },
];

export const mockSettings = {
  twoFactorEnabled: false,
  notificationsEnabled: true,
  emailNotifications: true,
  pushNotifications: true,
  dailyLimit: 500,
  monthlyLimit: 5000,
  autoConvert: true,
  preferredCurrency: 'USD',
  language: 'en',
};

export const mockFAQs = [
  {
    id: '1',
    category: 'Getting Started',
    question: 'How do I create an account?',
    answer: 'Download the Mobibit Africa app, click "Sign Up", enter your email and phone number. You\'ll receive a verification code via SMS.',
  },
  {
    id: '2',
    category: 'Funding',
    question: 'What mobile money providers are supported?',
    answer: 'We currently support MTN, Airtel, and Orange Money in Uganda, Kenya, Tanzania, and Ghana.',
  },
  {
    id: '3',
    category: 'Bitcoin',
    question: 'Is my Bitcoin really on the blockchain?',
    answer: 'Yes! Each transaction is settled on the Bitcoin blockchain via the Lightning Network, giving you true Bitcoin ownership.',
  },
  {
    id: '4',
    category: 'Security',
    question: 'Is my mobile money secure?',
    answer: 'All transactions are encrypted end-to-end. Your mobile money provider never sees your Bitcoin, only the converted amount.',
  },
  {
    id: '5',
    category: 'Spending',
    question: 'Can I use the card offline?',
    answer: 'The virtual card requires internet for each transaction to verify your Lightning balance.',
  },
  {
    id: '6',
    category: 'Limits',
    question: 'What are the transaction limits?',
    answer: 'Daily limit: $500, Monthly limit: $5000. These can be increased after KYC verification.',
  },
];
