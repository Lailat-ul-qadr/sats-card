# ⚡ Polar LND Setup Guide for Mobibit Africa

**Set up a local Lightning Network for testing Bitcoin send/receive flows**

> Polar is a desktop app that lets you spin up a local Lightning Network in seconds. It creates a regtest Bitcoin network with LND nodes that you can use for testing without spending real money.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Polar](#2-install-polar)
3. [Create a Network](#3-create-a-network)
4. [Configure LND for Mobibit Africa](#4-configure-lnd-for-mobibit-africa)
5. [Connect Mobibit Africa to LND](#5-connect-mobibit-africa-to-lnd)
6. [Test the Flow](#6-test-the-flow)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| **Docker** | Latest | [docker.com](https://www.docker.com/products/docker-desktop/) |
| **Polar** | v4.0.0+ | [github.com/jamaljsr/polar/releases](https://github.com/jamaljsr/polar/releases) |

### System Requirements

- **RAM:** 4GB minimum (8GB recommended)
- **Disk:** 10GB free space
- **OS:** Windows 10+, macOS 10.15+, or Linux

---

## 2. Install Polar

### Windows

1. Download `polar-win-x.y.z.exe` from [GitHub Releases](https://github.com/jamaljsr/polar/releases)
2. Run the installer
3. Follow the setup wizard
4. Launch Polar

### macOS

1. Download `polar-mac-x.y.z.dmg` from [GitHub Releases](https://github.com/jamaljsr/polar/releases)
2. Open the DMG file
3. Drag Polar to Applications
4. Launch Polar

### Linux

1. Download `polar-linux-x.y.z.deb` (Ubuntu/Debian) or `.AppImage` from [GitHub Releases](https://github.com/jamaljsr/polar/releases)
2. For DEB: `sudo dpkg -i polar-linux-x.y.z.deb`
3. For AppImage: `chmod +x polar-linux-x.y.z.AppImage && ./polar-linux-x.y.z.AppImage`
4. Launch Polar

---

## 3. Create a Network

### Step 1: Open Polar

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    POLAR - Lightning Network                     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │                    Welcome to Polar                      │   │
│  │                                                          │   │
│  │    Create a local Lightning Network for testing         │   │
│  │                                                          │   │
│  │    ┌─────────────────────────────────────────────┐     │   │
│  │    │                                             │     │   │
│  │    │  + Create New Network                       │     │   │
│  │    │                                             │     │   │
│  │    │  Recent Networks:                           │     │   │
│  │    │  (empty)                                    │     │   │
│  │    │                                             │     │   │
│  │    └─────────────────────────────────────────────┘     │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 2: Click "Create New Network"

```
┌─────────────────────────────────────────────────────────────────┐
│                    CREATE NEW NETWORK                            │
│                                                                  │
│  Network Name: [Mobibit Africa Testnet              ]           │
│                                                                  │
│  Lightning Implementation:                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ● LND (Recommended)                                   │   │
│  │  ○ Core Lightning                                      │   │
│  │  ○ Eclair                                              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Number of Nodes: [2] (slider: 1-10)                           │
│                                                                  │
│  Bitcoin Node:                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ● Bitcoin Core (v28.0)                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │    Cancel        │  │   Create         │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Wait for Network to Start

Polar will:
1. Pull Docker images for Bitcoin Core and LND
2. Start Bitcoin Core node
3. Start LND nodes
4. Open channels between nodes

This may take 2-5 minutes on first run.

### Step 4: Network is Ready

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOBIBIT AFRICA TESTNET                         │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │   ┌──────────┐     ┌──────────┐     ┌──────────┐      │   │
│  │   │  LND1    │────>│ Bitcoin  │<────│  LND2    │      │   │
│  │   │          │     │  Core    │     │          │      │   │
│  │   │ ⚡ Ready │     │ 🟢 Running│    │ ⚡ Ready │      │   │
│  │   └──────────┘     └──────────┘     └──────────┘      │   │
│  │        │                                  │            │   │
│  │        └────────── Channel ──────────────┘            │   │
│  │                                                          │   │
│  │   Status: 🟢 All nodes running                          │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Actions:                                                       │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │  Mine Blocks │ │  Open Channel│ │  Create      │           │
│  │              │ │              │ │  Invoice     │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Configure LND for Mobibit Africa

### Step 1: Get LND Credentials

Click on **LND1** node to see its details:

```
┌─────────────────────────────────────────────────────────────────┐
│                    LND1 NODE DETAILS                             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                          │   │
│  │  Node Name: LND1                                        │   │
│  │  Status: 🟢 Running                                     │   │
│  │                                                          │   │
│  │  ── Connection Info ──                                   │   │
│  │                                                          │   │
│  │  REST API:                                               │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  https://localhost:8081                          │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  gRPC:                                                  │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  localhost:10009                                 │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ── Credentials ──                                      │   │
│  │                                                          │   │
│  │  Macaroon:                                              │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  [Show] Click to reveal hex-encoded macaroon     │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  TLS Certificate:                                       │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │  [Show] Click to view TLS cert                  │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                          │   │
│  │  ── Actions ──                                          │   │
│  │                                                          │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │   │
│  │  │  Terminal    │ │  Logs        │ │  Nodes       │   │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 2: Copy Credentials

1. Click **"Show"** next to Macaroon
2. Copy the hex string
3. Click **"Show"** next to TLS Certificate
4. Copy the certificate

### Step 3: Update Mobibit Africa .env

```env
# ── LND Configuration ─────────────────────────────────────────────
# Polar regtest configuration
LND_HOST=localhost
LND_REST_PORT=8081
LND_MACAROON_HEX=<paste-your-macaroon-hex-here>
LND_TLS_CERT_PATH=
LND_NETWORK=regtest
```

---

## 5. Connect Mobibit Africa to LND

### Step 1: Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Start the Frontend

```bash
cd .
npm run dev
```

### Step 3: Create .env file in frontend root

```env
VITE_USE_REAL_API=true
VITE_API_URL=http://localhost:8000/api
```

### Step 4: Verify Connection

Check the backend logs:

```
✅ Database tables ready
🚀 Starting Mobibit Africa API v0.1.0
   Network: regtest
   MTN env: sandbox | Airtel env: sandbox | Orange env: sandbox | MPESA env: sandbox
```

---

## 6. Test the Flow

### Step 1: Fund LND Node with BTC

In Polar, click on **LND1** → **Actions** → **Deposit**

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPOSIT REGTEST BTC                           │
│                                                                  │
│  Amount: [1.0] BTC                                              │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │    Cancel        │  │   Deposit        │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

Or use the terminal in LND1:

```bash
# Open terminal in LND1 node
lncli --network regtest newaddress p2wkh
# Copy the address

# Mine blocks to confirm
# In Polar, click "Mine Blocks" → Mine 6 blocks
```

### Step 2: Mine Blocks

In Polar, click **"Mine Blocks"** button:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MINE BLOCKS                                   │
│                                                                  │
│  Blocks to mine: [6]                                            │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │    Cancel        │  │   Mine           │                    │
│  └──────────────────┘  └──────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 3: Test Receive BTC (Create Invoice)

1. Open Mobibit Africa web app
2. Go to **Receive** page
3. Enter amount: `100000` sats
4. Click **"Generate Invoice"**

```
┌─────────────────────────────────────────────────────────────────┐
│                    RECEIVE BITCOIN                                │
│                                                                  │
│  Amount (sats): [100000]                                        │
│  Description:   [Test Payment]                                  │
│                                                                  │
│  ┌──────────────────────────────┐                               │
│  │      Generate Invoice        │                               │
│  └──────────────────────────────┘                               │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  ⚡ Lightning Invoice                                    │   │
│  │                                                          │   │
│  │  lnbc1000n1p3x90qzpp5...                                │   │
│  │                                                          │   │
│  │  Amount: 100,000 sats                                    │   │
│  │  Expires in: 59 minutes                                  │   │
│  │                                                          │   │
│  │  ┌──────────────────────┐                               │   │
│  │  │   Copy Invoice       │                               │   │
│  │  └──────────────────────┘                               │   │
│  │                                                          │   │
│  │  ⚠️ This is a REAL Lightning invoice                     │   │
│  │     Connect LND for production invoices                 │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Step 4: Pay Invoice from LND2

1. Copy the invoice from Mobibit Africa
2. In Polar, click on **LND2** → **Terminal**
3. Run:

```bash
lncli --network regtest payinvoice <invoice_string>
```

### Step 5: Verify Payment

1. Check Mobibit Africa dashboard - balance should increase
2. In Polar, check LND1 node - should show received payment

---

## 7. Troubleshooting

### Common Issues

#### "Cannot connect to LND"

```
┌─────────────────────────────────────────────────────────────────┐
│  ERROR: Cannot connect to LND                                   │
│                                                                  │
│  Solutions:                                                     │
│  1. Check LND is running in Polar                              │
│  2. Verify LND_REST_PORT is correct (8081 for LND1)           │
│  3. Check LND_MACAROON_HEX is correct                         │
│  4. Ensure Docker is running                                   │
│                                                                  │
│  Test connection:                                               │
│  curl -k https://localhost:8081/v1/getinfo                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### "Invoice already expired"

```
┌─────────────────────────────────────────────────────────────────┐
│  ERROR: Invoice already expired                                │
│                                                                  │
│  Solutions:                                                     │
│  1. Generate a new invoice                                     │
│  2. Pay within the expiry time (default: 1 hour)              │
│  3. Increase expiry when creating invoice                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### "Insufficient funds"

```
┌─────────────────────────────────────────────────────────────────┐
│  ERROR: Insufficient funds                                     │
│                                                                  │
│  Solutions:                                                     │
│  1. Deposit more BTC to LND node                               │
│  2. Mine more blocks (6+ for confirmation)                     │
│  3. Check wallet balance: lncli --network regtest walletbalance│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### "Channel not active"

```
┌─────────────────────────────────────────────────────────────────┐
│  ERROR: Channel not active                                     │
│                                                                  │
│  Solutions:                                                     │
│  1. Open a channel between LND1 and LND2                      │
│  2. In Polar: Click "Open Channel"                             │
│  3. Mine blocks to confirm channel                             │
│  4. Wait for channel to be active (~6 blocks)                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Quick Reference

| Task | Command/Action |
|------|----------------|
| Start network | Polar → Click "Start" on network |
| Stop network | Polar → Click "Stop" on network |
| Mine blocks | Polar → Click "Mine Blocks" |
| Open channel | Polar → Click "Open Channel" |
| Check balance | `lncli --network regtest walletbalance` |
| List invoices | `lncli --network regtest listinvoices` |
| List payments | `lncli --network regtest listpayments` |
| Get node info | `lncli --network regtest getinfo` |

---

## 8. Network Ports Reference

| Node | REST API | gRPC | P2P |
|------|----------|------|-----|
| Bitcoin Core | 18443 | 18444 | — |
| LND1 | 8081 | 10009 | 9735 |
| LND2 | 8082 | 10010 | 9736 |
| CLN (if used) | — | 8534 | 9735 |

---

## 9. Complete Test Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE TEST FLOW                                        │
│                                                                                  │
│  1. START POLAR                                                                 │
│     └── Launch Polar → Create network → Wait for nodes to start                │
│                                                                                  │
│  2. FUND LND NODE                                                               │
│     └── Deposit 1 BTC to LND1 → Mine 6 blocks → Balance: 1 BTC                │
│                                                                                  │
│  3. START MOBIBIT AFRICA                                                        │
│     └── Backend: uvicorn app.main:app --reload                                 │
│     └── Frontend: npm run dev                                                  │
│                                                                                  │
│  4. CREATE USER                                                                 │
│     └── Sign up with phone + PIN → Get JWT token                               │
│                                                                                  │
│  5. RECEIVE BTC (Test Receive Flow)                                             │
│     └── Enter 100,000 sats → Generate invoice → Copy invoice                   │
│     └── In Polar LND2: lncli payinvoice <invoice>                              │
│     └── Check Mobibit Africa: Balance = 100,000 sats                           │
│                                                                                  │
│  6. SEND BTC (Test Send Flow)                                                   │
│     └── In Polar LND2: lncli addinvoice --amt 50000                            │
│     └── Copy invoice from LND2                                                 │
│     └── In Mobibit Africa: Paste invoice → Send 50,000 sats                    │
│     └── Check LND2: Balance = 50,000 sats                                      │
│     └── Check Mobibit Africa: Balance = 50,000 sats                            │
│                                                                                  │
│  7. WITHDRAW BTC (Test Withdraw Flow)                                           │
│     └── In Mobibit Africa: Withdraw 25,000 sats to MPESA                       │
│     └── Check: Balance = 25,000 sats                                            │
│     └── (In production: MPESA sends KES to phone)                              │
│                                                                                  │
│  SUCCESS! All flows working with real Lightning invoices.                       │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

**Polar Version:** v4.0.0+
**LND Version:** v0.18.5+ (recommended)
**Network:** Regtest (local testing only)
**Status:** ✅ Ready for testing
