import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MobileMoneyForm from '../components/MobileMoneyForm';

// The component fetches the BTC price on mount; stub it at 50,000 USD/BTC
vi.stubGlobal(
  'fetch',
  vi.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ bitcoin: { usd: 50000 } }),
    })
  )
);

describe('MobileMoneyForm', () => {
  let onTopUp;
  let setBtcUsd;

  beforeEach(() => {
    vi.clearAllMocks();
    onTopUp = vi.fn();
    setBtcUsd = vi.fn();
  });

  it('shows a conversion preview in sats as the user types', async () => {
    const user = userEvent.setup();
    render(<MobileMoneyForm onTopUp={onTopUp} setBtcUsd={setBtcUsd} />);

    const amountInput = await screen.findByPlaceholderText('5000');
    await user.clear(amountInput);
    await user.type(amountInput, '100');

    await waitFor(() => {
      // 100 USD at 50,000 USD/BTC = 0.002 BTC = 200,000 sats
      expect(screen.getByText('200,000 sats')).toBeInTheDocument();
    });
  });
});
