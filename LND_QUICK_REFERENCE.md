# ⚡ LND Quick Reference Card

**Common commands for testing Mobibit Africa with Polar**

---

## 🚀 Quick Start

```bash
# 1. Check LND node status
lncli --network regtest getinfo

# 2. Check wallet balance
lncli --network regtest walletbalance

# 3. Create invoice (receive BTC)
lncli --network regtest addinvoice --amt 100000

# 4. Pay invoice (send BTC)
lncli --network regtest payinvoice <invoice_string>

# 5. List invoices
lncli --network regtest listinvoices

# 6. List payments
lncli --network regtest listpayments
```

---

## 📥 Receive BTC (Create Invoice)

### Basic Invoice
```bash
lncli --network regtest addinvoice --amt 100000
```

**Output:**
```
{
    "r_hash": "abc123...",
    "payment_request": "lnbc1000n1p3x90qzpp5...",
    "add_index": "1"
}
```

### Invoice with Memo
```bash
lncli --network regtest addinvoice --amt 100000 --memo "Mobibit Top-Up"
```

### Invoice with Expiry (2 hours)
```bash
lncli --network regtest addinvoice --amt 100000 --expiry 7200
```

### Zero-Amount Invoice (Any Amount)
```bash
lncli --network regtest addinvoice
```

---

## 📤 Send BTC (Pay Invoice)

### Pay Invoice
```bash
lncli --network regtest payinvoice <payment_request>
```

### Pay Invoice with Amount (for zero-amount invoices)
```bash
lncli --network regtest payinvoice <payment_request> --amt 100000
```

### Pay Invoice without Confirmation
```bash
lncli --network regtest payinvoice <payment_request> --force
```

---

## 💰 Wallet Operations

### Check Balance
```bash
lncli --network regtest walletbalance
```

### New Address (to receive on-chain BTC)
```bash
lncli --network regtest newaddress p2wkh
```

### List Channels
```bash
lncli --network regtest listchannels
```

### Channel Balance
```bash
lncli --network regtest channelbalance
```

---

## 🔍 Query Operations

### List Invoices
```bash
lncli --network regtest listinvoices
```

### List Payments
```bash
lncli --network regtest listpayments
```

### Get Invoice by Payment Hash
```bash
lncli --network regtest lookupinvoice <r_hash>
```

### Get Payment by Hash
```bash
lncli --network regtest lookuptxns <payment_hash>
```

---

## 🌐 Node Information

### Get Node Info
```bash
lncli --network regtest getinfo
```

### List Peers
```bash
lncli --network regtest listpeers
```

### Describe Graph
```bash
lncli --network regtest describegraph
```

---

## 🔗 Channel Operations

### Open Channel
```bash
lncli --network regtest openchannel --node_key <pubkey> --local_amt 500000
```

### Close Channel
```bash
lncli --network regtest closechannel --channel_point <txid>:<index>
```

### List Pending Channels
```bash
lncli --network regtest pendingchannels
```

---

## 🧪 Testing Commands

### Create and Pay Invoice (Full Flow)
```bash
# Step 1: Create invoice on LND1
INVOICE=$(lncli --network regtest addinvoice --amt 100000 --memo "Test" | grep payment_request | cut -d'"' -f4)
echo "Invoice: $INVOICE"

# Step 2: Pay invoice from LND2 (use different terminal)
lncli --network regtest payinvoice $INVOICE

# Step 3: Check balances
echo "LND1 Balance:"
lncli --network regtest walletbalance
echo "LND2 Balance:"
lncli --network regtest walletbalance
```

### Test Multiple Payments
```bash
# Create 5 invoices and pay them
for i in {1..5}; do
    AMOUNT=$((10000 + RANDOM % 90000))
    INVOICE=$(lncli --network regtest addinvoice --amt $AMOUNT --memo "Test $i" | grep payment_request | cut -d'"' -f4)
    echo "Paying $AMOUNT sats..."
    lncli --network regtest payinvoice $INVOICE --force
done
```

---

## 🐛 Debugging

### Check LND Logs
```bash
# In Polar, click on node → Logs
# Or check Docker logs:
docker logs polar-lnd-1
```

### Restart LND Node
```bash
# In Polar, click on node → Stop → Start
# Or via Docker:
docker restart polar-lnd-1
```

### Reset Network
```bash
# In Polar, click on network → Delete → Recreate
```

---

## 📊 Common Amounts

| Amount | Sats | BTC | USD (approx) |
|--------|------|-----|--------------|
| 1,000 sats | 1,000 | 0.00001 | $0.79 |
| 10,000 sats | 10,000 | 0.0001 | $7.90 |
| 100,000 sats | 100,000 | 0.001 | $79.00 |
| 1,000,000 sats | 1,000,000 | 0.01 | $790.00 |

---

## 🔗 Useful Links

- **Polar GitHub:** https://github.com/jamaljsr/polar
- **LND Documentation:** https://github.com/lightningnetwork/lnd/blob/master/docs/README.md
- **Lightning Network:** https://lightning.network/
- **BOLT11 Spec:** https://github.com/lightning/bolts/blob/master/11-payment-encoding.md

---

**Network:** Regtest (local testing only)
**Last Updated:** August 28, 2026
