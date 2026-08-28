/**
 * API Client — connects the React frontend to the FastAPI backend.
 *
 * All service methods go through this client which handles:
 *   - Base URL configuration
 *   - JWT token injection (from localStorage)
 *   - Response parsing and error handling
 *   - Token refresh on 401
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// ── Token Management ──────────────────────────────────────────────────

function getAccessToken() {
  return localStorage.getItem('auth_token');
}

function getRefreshToken() {
  return localStorage.getItem('refresh_token');
}

function setTokens(accessToken, refreshToken) {
  localStorage.setItem('auth_token', accessToken);
  if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
}

function clearTokens() {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
}

// ── HTTP Client ───────────────────────────────────────────────────────

async function request(endpoint, options = {}) {
  const url = `${API_BASE}${endpoint}`;
  const token = getAccessToken();

  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle token expiry — try refresh
    if (response.status === 401 && token && getRefreshToken()) {
      const refreshed = await refreshAccessToken();
      if (refreshed) {
        headers['Authorization'] = `Bearer ${getAccessToken()}`;
        const retryResponse = await fetch(url, { ...options, headers });
        return handleResponse(retryResponse);
      }
      // Refresh failed — redirect to login
      clearTokens();
      window.location.href = '/login';
      throw new Error('Session expired');
    }

    return handleResponse(response);
  } catch (error) {
    if (error.message === 'Failed to fetch') {
      throw new Error('Cannot connect to server. Please check your connection.');
    }
    throw error;
  }
}

async function handleResponse(response) {
  let data;
  try {
    data = await response.json();
  } catch {
    // Response isn't JSON (e.g. HTML error page)
    throw new Error(`Server error (${response.status}). Is the backend running?`);
  }

  if (!response.ok) {
    // Build a clear error message from backend response
    let msg = data.detail || data.message || 'Request failed';

    // Add status code context for common errors
    if (response.status === 404) {
      msg = msg.includes('not found') ? msg : `${msg} (resource not found)`;
    } else if (response.status === 401) {
      msg = 'Session expired. Please log in again.';
    } else if (response.status === 403) {
      msg = 'You do not have permission to do this.';
    } else if (response.status === 422) {
      msg = msg.includes('Validation error') ? msg : `Invalid input: ${msg}`;
    } else if (response.status >= 500) {
      msg = 'Server error. Please try again later.';
    }

    const error = new Error(msg);
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}

async function refreshAccessToken() {
  try {
    const refreshToken = getRefreshToken();
    if (!refreshToken) return false;

    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) return false;

    const data = await response.json();
    setTokens(data.access_token, data.refresh_token);
    return true;
  } catch {
    return false;
  }
}

// ── Auth API ──────────────────────────────────────────────────────────

export const authAPI = {
  register: async (phone, pin, name = 'User', country = 'UG') => {
    const data = await request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ phone, pin, name, country }),
    });
    setTokens(data.tokens.access_token, data.tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },

  login: async (phone, pin) => {
    const data = await request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ phone, pin }),
    });
    setTokens(data.tokens.access_token, data.tokens.refresh_token);
    localStorage.setItem('user', JSON.stringify(data.user));
    return data;
  },

  logout: async () => {
    clearTokens();
    return { success: true };
  },

  getMe: async () => {
    return request('/auth/me');
  },
};

// ── Wallet API ────────────────────────────────────────────────────────

export const walletAPI = {
  getBalance: async () => {
    return request('/card_balance');
  },

  createInvoice: async (amountSats, memo = 'Mobibit Top-Up') => {
    return request('/create_invoice', {
      method: 'POST',
      body: JSON.stringify({ amount_sats: amountSats, memo }),
    });
  },

  payInvoice: async (paymentRequest) => {
    return request('/card_payment', {
      method: 'POST',
      body: JSON.stringify({
        payment_request: paymentRequest,
      }),
    });
  },

  checkInvoice: async (paymentId) => {
    return request(`/check_payment/${paymentId}`);
  },

  deposit: async (paymentId) => {
    return request(`/deposit/${paymentId}`, {
      method: 'POST',
    });
  },
};

// ── Payment API ───────────────────────────────────────────────────────

export const paymentAPI = {
  collect: async (phoneNumber, amount, currency, provider, description = '') => {
    return request('/payments/collect', {
      method: 'POST',
      body: JSON.stringify({
        phone_number: phoneNumber,
        amount,
        currency,
        provider,
        description,
      }),
    });
  },

  checkStatus: async (providerTxnId, provider = 'mtn_momo') => {
    return request(`/payments/${providerTxnId}/status?provider=${provider}`);
  },

  transfer: async (recipientPhone, amountSats, memo = '') => {
    return request('/payments/transfer', {
      method: 'POST',
      body: JSON.stringify({
        recipient_phone: recipientPhone,
        amount_sats: amountSats,
        memo,
      }),
    });
  },
};

// ── Exchange Rate API ─────────────────────────────────────────────────

export const rateAPI = {
  getRate: async (fromCurrency = 'UGX', to = 'BTC') => {
    return request(`/rates/${fromCurrency}?to=${to}`);
  },

  convert: async (amount, fromCurrency, toCurrency = 'sats') => {
    return request('/rates/convert', {
      method: 'POST',
      body: JSON.stringify({
        amount,
        from_currency: fromCurrency,
        to_currency: toCurrency,
      }),
    });
  },
};

// ── USSD API ──────────────────────────────────────────────────────────

export const ussdAPI = {
  sendInput: async (sessionId, phoneNumber, userInput, serviceCode = '*123#') => {
    return request('/ussd', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        phone_number: phoneNumber,
        user_input: userInput,
        service_code: serviceCode,
      }),
    });
  },
};

export default { authAPI, walletAPI, paymentAPI, rateAPI, ussdAPI };
