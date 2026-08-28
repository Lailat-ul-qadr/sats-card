// Format currency values
export const formatCurrency = (amount, currency = 'USD') => {
  if (currency === 'sats') {
    return `${Math.floor(amount).toLocaleString()} sats`;
  }
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: currency,
  }).format(amount);
};

// Format date
export const formatDate = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(date));
};

// Format time
export const formatTime = (date) => {
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  }).format(new Date(date));
};

// Format datetime
export const formatDateTime = (date) => {
  return `${formatDate(date)} ${formatTime(date)}`;
};

// Get time ago
export const timeAgo = (date) => {
  const now = new Date();
  const past = new Date(date);
  const diff = now - past;
  const seconds = Math.floor(diff / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) {
    return 'just now';
  } else if (minutes < 60) {
    return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;
  } else if (hours < 24) {
    return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
  } else if (days < 7) {
    return `${days} ${days === 1 ? 'day' : 'days'} ago`;
  } else {
    return formatDate(date);
  }
};

// Validate email
export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

// Validate phone number
export const validatePhone = (phone) => {
  const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
  return re.test(phone);
};

// Mask card number
export const maskCardNumber = (cardNumber) => {
  const last4 = cardNumber.slice(-4);
  return `**** **** **** ${last4}`;
};

// Convert BTC to Sats
export const btcToSats = (btc) => Math.floor(btc * 100000000);

// Convert Sats to BTC
export const satsToBtc = (sats) => sats / 100000000;

// Format BTC value
export const formatBtc = (btc) => {
  if (btc < 0.00001) {
    return `${(btc * 100000000).toFixed(0)} sats`;
  }
  return `${btc.toFixed(8)} BTC`;
};

// Get transaction icon
export const getTransactionIcon = (type) => {
  const icons = {
    topup: '💰',
    payment: '⚡',
    spend: '💳',
    transfer: '↔️',
    receive: '📥',
    send: '📤',
  };
  return icons[type] || '📝';
};

// Get transaction color
export const getTransactionColor = (type) => {
  const colors = {
    topup: '#7AAE8A',
    payment: '#D4A574',
    spend: '#B85C4E',
    transfer: '#6B7F6B',
    receive: '#7AAE8A',
    send: '#B85C4E',
  };
  return colors[type] || '#6B7F6B';
};

// Generate random ID
export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

// Copy to clipboard
export const copyToClipboard = async (text) => {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text);
    } else {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand('copy');
      document.body.removeChild(textarea);
    }
    return true;
  } catch {
    return false;
  }
};

// Delay function (for async simulation)
export const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// API Error handler
export const handleApiError = (error) => {
  if (error.response) {
    return error.response.data.message || 'An error occurred';
  }
  return error.message || 'Network error';
};

// Local storage helpers
export const storage = {
  get: (key) => {
    try {
      return JSON.parse(localStorage.getItem(key));
    } catch {
      return null;
    }
  },
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch {
      console.error('Storage error');
    }
  },
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch {
      console.error('Storage error');
    }
  },
  clear: () => {
    try {
      localStorage.clear();
    } catch {
      console.error('Storage error');
    }
  },
};

// Device detection
export const isMobile = () => /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

export const isTablet = () => /iPad|Android/i.test(navigator.userAgent);

export const isDesktop = () => !isMobile() && !isTablet();
