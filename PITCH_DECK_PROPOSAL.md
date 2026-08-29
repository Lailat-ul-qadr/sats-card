# 🃏 MOBIBIT AFRICA — Pitch Deck Proposal

## Bitcoin for Everyone. Powered by Mobile Money.

---

## 📋 Table of Contents

1. [The Problem](#1-the-problem)
2. [Our Solution](#2-our-solution)
3. [How It Works](#3-how-it-works)
4. [Market Opportunity](#4-market-opportunity)
5. [Product Demo](#5-product-demo)
6. [Technical Architecture](#6-technical-architecture)
7. [Revenue Model](#7-revenue-model)
8. [Competitive Advantage](#8-competitive-advantage)
9. [Team & Roadmap](#9-team--roadmap)
10. [The Ask](#10-the-ask)

---

## 1. 🎯 The Problem

### Bitcoin Adoption in Emerging Markets is Broken

**1.4 billion people** in Africa are unbanked, yet **60%+ have mobile money accounts**.

| Problem | Impact |
|---------|--------|
| **No fiat-to-Bitcoin bridge** | Mobile money users can't access Bitcoin |
| **Complex onboarding** | Exchanges require KYC, bank accounts, technical knowledge |
| **No spending utility** | Even if you have Bitcoin, you can't spend it locally |
| **High remittance fees** | Sending money across borders costs 8-15% |
| **Volatility risk** | Holders can't protect against BTC price swings |

### The Gap

```
Mobile Money Users (600M+) ←——— GAP ———→ Bitcoin Users (420M+)
        ↑                                         ↑
  Easy to use                              Hard to access
  Widely available                         Requires bank account
  Local currency only                      No spending utility
```

**Nobody is bridging mobile money → Bitcoin → Real-world spending.**

---

## 2. 💡 Our Solution

### Mobibit Africa: The Bitcoin Wallet That Works Like Mobile Money

**Mobibit Africa** is a mobile-first Bitcoin wallet that lets users:

1. **Fund** via mobile money (MTN MoMo, Airtel Money, Orange Money, MPESA)
2. **Convert** fiat to Bitcoin instantly via Lightning Network
3. **Spend** Bitcoin anywhere via a virtual Visa card

### Value Proposition

> "Turn your mobile money into Bitcoin in 3 taps, spend it anywhere with a virtual card."

### Key Benefits

| For Users | For Merchants | For the Bitcoin Ecosystem |
|-----------|---------------|---------------------------|
| ✅ No bank account needed | ✅ Accept BTC payments | ✅ 1.4B new users |
| ✅ Fund with mobile money | ✅ Instant settlement | ✅ Real-world utility |
| ✅ Spend Bitcoin anywhere | ✅ Zero chargebacks | ✅ Lightning adoption |
| ✅ Real-time conversion | ✅ Lower fees | ✅ Emerging market growth |
| ✅ USSD access (feature phones) | ✅ Global reach | ✅ Financial inclusion |

---

## 3. ⚙️ How It Works

### User Flow

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│   Mobile     │───▶│  Mobibit Africa   │───▶│   Lightning   │───▶│  Virtual    │
│   Money      │    │   Backend    │    │   Network     │    │  Card       │
│   (MTN/      │    │   (FastAPI)  │    │   (LND)      │    │  (Visa)     │
│   Airtel/    │    │              │    │              │    │             │
│   Orange)    │    │              │    │              │    │             │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
     Step 1              Step 2              Step 3              Step 4
  User enters         Backend calls       BTC received        User spends
  phone + amount      MoMo API            via Lightning       with virtual card
```

### Step-by-Step

| Step | Action | Technology |
|------|--------|------------|
| **1. Sign Up** | Create account with phone number | SMS OTP via Africa's Talking |
| **2. Fund** | Select mobile money provider, enter amount | MTN MoMo / Airtel / Orange APIs |
| **3. Convert** | Fiat → BTC via Lightning Network | LND (Lightning Network Daemon) |
| **4. Spend** | Use virtual card at any merchant | Visa card issuing API |
| **5. Track** | View transactions in real-time | PostgreSQL + WebSocket |

### USSD Support (Feature Phones)

For users without smartphones:
```
*123# → Send Money → Enter Amount → Enter PIN → Done!
```

---

## 4. 📊 Market Opportunity

### Total Addressable Market (TAM)

| Market | Size | Growth |
|--------|------|--------|
| **Africa Mobile Money** | $700B+ transactions/year | 25% YoY |
| **Bitcoin Users (Global)** | 420M+ | 15% YoY |
| **Africa Remittance** | $100B+ annually | 8% YoY |
| **Unbanked Population** | 1.4 billion | — |

### Target Markets (Phase 1)

| Country | Mobile Money Users | Key Provider | Priority |
|---------|-------------------|--------------|----------|
| 🇷🇼 Rwanda | 8M+ | MTN MoMo | 🔴 High |
| 🇺🇬 Uganda | 28M+ | MTN MoMo | 🔴 High |
| 🇬🇭 Ghana | 20M+ | MTN MoMo | 🟡 Medium |
| 🇰🇪 Kenya | 35M+ | M-Pesa | 🟡 Medium |
| 🇳🇬 Nigeria | 30M+ | MTN MoMo | 🟢 Phase 2 |

### Why Now?

1. **Lightning Network maturity** — Instant, near-zero fees
2. **Mobile money growth** — 25% YoY in Africa
3. **Bitcoin adoption surge** — Post-halving institutional interest
4. **Regulatory clarity** — Rwanda, Uganda progressive on crypto
5. **Smartphone penetration** — Growing rapidly across Africa

---

## 5. 🖥️ Product Demo

### Demo Flow (5 minutes)

| # | Screen | What to Show |
|---|--------|--------------|
| 1 | **Landing Page** | Project overview, problem/solution |
| 2 | **Sign Up** | Create account with phone number |
| 3 | **Dashboard** | Wallet balance, quick actions |
| 4 | **Virtual Card** | Beautiful card design, balance |
| 5 | **Fund Card** | Select MTN → Enter amount → Convert |
| 6 | **Send Bitcoin** | Lightning address → Send sats |
| 7 | **Receive Bitcoin** | Generate invoice → Copy |
| 8 | **Spend** | Simulate card payment |
| 9 | **Transactions** | Full history with filters |
| 10 | **Profile/Settings** | User management |

### Screenshots Preview

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│                     │  │                     │  │                     │
│   MOBIBIT AFRICA         │  │   Dashboard         │  │   Virtual Card      │
│   Bitcoin for       │  │   Balance: 250,000  │  │   ══════════════    │
│   Everyone          │  │   sats ($125.00)    │  │   4532 •••• 7891    │
│                     │  │                     │  │                     │
│   [Get Started]     │  │   [Fund] [Send]     │  │   John Doe          │
│                     │  │   [Receive] [Card]  │  │   12/28             │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
```

---

## 6. 🏗️ Technical Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        FRONTEND (React)                          │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │ Landing │  │Dashboard│  │  Card   │  │  Fund   │  ... 13    │
│  │  Page   │  │         │  │         │  │         │    pages    │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │
└──────────────────────────────────────────────────────────────────┘
                              │
                         REST API
                              │
┌──────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI)                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │  Auth   │  │ Wallet  │  │Payments │  │   USSD  │            │
│  │ Routes  │  │ Routes  │  │ Routes  │  │ Handler │            │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘            │
│  ┌─────────────────────────────────────────────────┐            │
│  │              Service Layer                       │            │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ │            │
│  │  │ Auth │ │Wallet│ │Trans.│ │Rates │ │ SMS  │ │            │
│  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ │            │
│  └─────────────────────────────────────────────────┘            │
│  ┌─────────────────────────────────────────────────┐            │
│  │              Adapters                            │            │
│  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐           │            │
│  │  │ MTN  │ │Airtel│ │Orange│ │LND   │           │            │
│  │  │ MoMo │ │Money │ │Money │ │Light.│           │            │
│  │  └──────┘ └──────┘ └──────┘ └──────┘           │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              ┌─────┴─────┐      ┌─────┴─────┐
              │ PostgreSQL│      │   Redis    │
              │ Database  │      │   Cache    │
              └───────────┘      └───────────┘
```

### Tech Stack

| Layer | Technology | Why |
|-------|------------|-----|
| **Frontend** | React 18 + Vite + Tailwind | Fast, modern, responsive |
| **Backend** | Python FastAPI | Async, fast, well-documented |
| **Database** | PostgreSQL + Alembic | ACID, migrations |
| **Cache** | Redis | Session storage, rate limiting |
| **Lightning** | LND (Lightning Daemon) | Industry standard |
| **Mobile Money** | MTN MoMo / Airtel / Orange | Direct API integration |
| **SMS/USSD** | Africa's Talking | Pan-African coverage |
| **Hosting** | Docker + Render/Railway | Easy deployment |

### Key Integrations

| Integration | Purpose | Status |
|-------------|---------|--------|
| MTN MoMo API | Mobile money payments | ✅ Sandbox ready |
| Airtel Money API | Mobile money payments | ✅ Sandbox ready |
| Orange Money API | Mobile money payments | ✅ Sandbox ready |
| LND (Lightning) | Bitcoin payments | ✅ Testnet ready |
| Africa's Talking | SMS + USSD | ✅ Sandbox ready |
| CoinGecko API | Exchange rates | ✅ Free tier |

---

## 7. 💰 Revenue Model

### Revenue Streams

| Stream | Description | Margin |
|--------|-------------|--------|
| **Transaction Fees** | 1-2% on fiat→BTC conversion | High |
| **Card Spending** | 0.5-1% on virtual card transactions | High |
| **Exchange Rate Spread** | Small spread on BTC/USD rate | Medium |
| **Premium Features** | Higher limits, priority support | High |
| **Merchant Fees** | 1-2% on BTC merchant payments | Medium |

### Unit Economics (Target)

| Metric | Value |
|--------|-------|
| **Average Transaction** | $25 |
| **Fee per Transaction** | $0.50 (2%) |
| **Monthly Active Users (Target)** | 10,000 |
| **Monthly Revenue (Target)** | $50,000 |
| **Customer Acquisition Cost** | $5 |
| **Lifetime Value** | $120 |

---

## 8. 🏆 Competitive Advantage

### Why Mobibit Africa Wins

| Feature | Mobibit Africa | Traditional Exchanges | Other Bitcoin Wallets |
|---------|-----------|----------------------|----------------------|
| **Mobile Money Funding** | ✅ Direct | ❌ No | ❌ No |
| **Lightning Network** | ✅ Instant | ⚠️ Slow | ⚠️ Some |
| **Virtual Card** | ✅ Built-in | ❌ No | ❌ No |
| **USSD Support** | ✅ Yes | ❌ No | ❌ No |
| **No Bank Account** | ✅ Required | ❌ Required | ⚠️ Sometimes |
| **African Focus** | ✅ Primary | ❌ Global | ❌ Global |
| **Real-time Conversion** | ✅ Yes | ⚠️ Delayed | ⚠️ Delayed |

### Moat

1. **Network Effects** — More users → more merchants → more users
2. **Local Partnerships** — Direct MTN/Airtel/Orange integrations
3. **Regulatory Compliance** — Built for African markets
4. **USSD Access** — Reaches feature phone users (70% of Africa)
5. **Lightning-first** — Instant, cheap transactions

---

## 9. 👥 Team & Roadmap

### Team Structure

| Role | Responsibility | Status |
|------|----------------|--------|
| **Frontend Lead** | React app, UI/UX, 13 pages | ✅ Complete |
| **Backend Lead** | FastAPI, DB, API routes | 🔄 In Progress |
| **Mobile Money Lead** | MTN/Airtel/Orange integrations | 🔄 In Progress |
| **Lightning Lead** | LND integration, BTC payments | 🔄 In Progress |
| **DevOps** | Docker, deployment, monitoring | 📋 Planned |

### Roadmap

| Phase | Timeline | Deliverables |
|-------|----------|--------------|
| **Phase 1** | Week 1-2 | ✅ Frontend complete, Backend foundation |
| **Phase 2** | Week 3-4 | 🔄 Mobile money integrations, Lightning |
| **Phase 3** | Week 5-6 | 📋 USSD/SMS, Testing, Security audit |
| **Phase 4** | Week 7-8 | 📋 Launch in Rwanda, User feedback |
| **Phase 5** | Month 3+ | 📋 Expand to Uganda, Ghana, Kenya |

---

## 10. 📣 The Ask

### What We Need

| Need | Details | Priority |
|------|---------|----------|
| **Hackathon Time** | Complete MVP for demo | 🔴 Critical |
| **Sandbox Access** | MTN MoMo, Airtel, Orange APIs | 🔴 Critical |
| **LND Node** | Testnet node for Lightning | 🟡 High |
| **Database** | PostgreSQL instance | 🟡 High |
| **Deployment** | Render/Railway hosting | 🟢 Medium |

### Demo Success Criteria

- [x] Frontend: 13 pages fully functional
- [ ] Backend: API endpoints working
- [ ] Mobile Money: Sandbox integration live
- [ ] Lightning: Testnet payments working
- [ ] End-to-end: Full flow from signup to spending

---

## 📎 Appendix

### A. Project Files

```
mobibit-africa/
├── src/                    # Frontend (React)
│   ├── pages/              # 13 page components
│   ├── components/         # 9+ reusable components
│   ├── services/           # 7 API services
│   ├── context/            # Auth, Wallet, Theme
│   └── hooks/              # 7 custom hooks
│
├── backend/                # Backend (FastAPI)
│   ├── app/
│   │   ├── adapters/       # MTN, Airtel, Orange, LND
│   │   ├── api/            # Route handlers
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── ussd/           # USSD handler
│   └── alembic/            # Database migrations
│
└── docker-compose.yml      # Container orchestration
```

### B. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Create account |
| POST | `/api/auth/login` | Authenticate |
| GET | `/api/wallet/balance` | Get balance |
| POST | `/api/wallet/fund` | Fund via mobile money |
| POST | `/api/payments/send` | Send Bitcoin |
| POST | `/api/payments/receive` | Receive Bitcoin |
| GET | `/api/transactions` | Transaction history |

### C. Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/satscard

# MTN MoMo
MTN_MOMO_API_KEY=your-key
MTN_MOMO_API_USER=your-uuid

# Lightning
LND_HOST=localhost
LND_MACAROON_HEX=your-macaroon

# SMS/USSD
AT_API_KEY=your-africastalking-key
```

---

## 🎯 Summary

**Mobibit Africa** solves the biggest barrier to Bitcoin adoption in emerging markets: **the fiat-to-Bitcoin bridge**.

By connecting mobile money (which 600M+ Africans already use) to Bitcoin via Lightning Network, we create a seamless path from fiat → BTC → real-world spending.

**The frontend is demo-ready. The backend is in progress. The opportunity is massive.**

---

*"The best time to plant a tree was 20 years ago. The second best time is now."*
*— The same is true for Bitcoin adoption in Africa.*

---

**Built with:** React • FastAPI • Lightning Network • Mobile Money APIs
**Status:** 🚀 Demo Ready
**Contact:** [Your Team Email]

---

# ✅ PITCH COMPLETE — Full Project Concept

> This section contains the complete project concept including USSD interaction flows, web app flows, data flow diagrams, system architecture, and file references.

---

## 📋 Complete Concept Index

| Section | Description |
|---------|-------------|
| [User Interfaces](#user-interfaces) | USSD + Web App overview |
| [USSD Interaction Guide](#ussd-interaction-guide) | Feature phone step-by-step flows |
| [Web App Interaction Guide](#web-app-interaction-guide) | Smartphone page-by-page guide |
| [Data Flow Diagrams](#data-flow-diagrams) | Complete system data flows |
| [System Architecture](#system-architecture-full) | Layered architecture diagrams |
| [Database Schema](#database-schema) | Complete SQL schema |
| [File Reference](#complete-file-reference) | Every file and what it does |

---

## User Interfaces

Mobibit Africa provides **two interfaces** to reach all users:

### USSD Interface (Feature Phones — No Internet Needed)

For the 70% of Africans who use basic feature phones without internet access.

```
┌─────────────────────────────────────────────────────┐
│  USER DIALS *123# ON ANY PHONE                       │
│                                                      │
│  ┌─────────────────────────────────┐                 │
│  │ MOBIBIT AFRICA                  │                 │
│  │ Welcome! Select an option:      │                 │
│  │                                 │                 │
│  │ 1. Check Balance                │                 │
│  │ 2. Send BTC                     │                 │
│  │ 3. Fund Account (Buy BTC)       │                 │
│  │ 4. Receive USD                  │                 │
│  │ 5. Convert BTC <-> USD          │                 │
│  │ 6. Help                         │                 │
│  │                                 │                 │
│  │ Reply with a number:            │                 │
│  └─────────────────────────────────┘                 │
│                                                      │
│  Works on: Nokia, Samsung, any basic phone           │
│  Network:  USSD (no internet required)               │
│  Cost:     Standard USSD rates (often free)          │
└─────────────────────────────────────────────────────┘
```

### Web App Interface (Smartphones — Internet Required)

A full 13-page React application for smartphone users.

```
┌─────────────────────────────────────────────────────┐
│  13-PAGE REACT APPLICATION                           │
│                                                      │
│  PUBLIC PAGES:           AUTHENTICATED PAGES:         │
│  ┌──────────────┐       ┌──────────────┐            │
│  │ 🏠 Landing   │       │ 📊 Dashboard │            │
│  │ 🔑 Login     │       │ 💳 Virtual   │            │
│  │ 📝 Signup    │       │    Card      │            │
│  └──────────────┘       │ 💰 Fund Card │            │
│                         │ ⚡ Send BTC   │            │
│                         │ 📥 Receive   │            │
│                         │ 🛒 Spend     │            │
│                         │ 📋 History   │            │
│                         │ 👤 Profile   │            │
│                         │ ⚙️ Settings  │            │
│                         │ ❓ Help      │            │
│                         └──────────────┘            │
│                                                      │
│  Tech: React 18 + Vite + Tailwind + Framer Motion    │
└─────────────────────────────────────────────────────┘
```

---

## USSD Interaction Guide

### Main Menu

When a user dials `*123#`, they see:

```
MOBIBIT AFRICA
Welcome! Select an option:

1. Check Balance
2. Send BTC
3. Fund Account (Buy BTC)
4. Receive USD
5. Convert BTC <-> USD
6. Help

Reply with a number:
```

### Check Balance (Option 1)

```
User: *123# → Selects "1"

MOBIBIT AFRICA BALANCE

BTC: 250,000 sats
   = 0.00250000 BTC
   = $98.75 USD

USD Wallet: $0.00

Reply 0 for main menu.
```

### Send BTC (Option 2)

```
Step 1: Enter recipient phone
┌─────────────────────────────────────┐
│ SEND BTC                            │
│ Enter the recipient's phone number: │
│                                     │
│ Example: +256701234567              │
└─────────────────────────────────────┘

Step 2: Enter amount
┌─────────────────────────────────────┐
│ SEND BTC                            │
│ Recipient: +256701234567            │
│                                     │
│ Enter amount in sats (e.g. 10000):  │
└─────────────────────────────────────┘

Step 3: Confirm
┌─────────────────────────────────────┐
│ SEND BTC - CONFIRM                  │
│ To: +256701234567                   │
│ Amount: 10,000 sats                 │
│ Fee: ~1 sat                         │
│                                     │
│ 1. Confirm & Send                   │
│ 2. Cancel                           │
│                                     │
│ Reply 1 or 2:                       │
└─────────────────────────────────────┘

Step 4: Success
┌─────────────────────────────────────┐
│ BTC SENT!                           │
│                                     │
│ To: +256701234567                   │
│ Amount: 10,000 sats                 │
│ Status: Confirmed                   │
│                                     │
│ Reply 0 for main menu.              │
└─────────────────────────────────────┘
```

### Fund Account / Buy BTC (Option 3)

```
Step 1: Enter amount in local currency
┌─────────────────────────────────────┐
│ FUND ACCOUNT (Buy BTC)              │
│ Enter amount in UGX:                │
│                                     │
│ Min: 1,000 | Max: 500,000          │
└─────────────────────────────────────┘

Step 2: Confirm conversion
┌─────────────────────────────────────┐
│ FUND ACCOUNT - CONFIRM              │
│ Amount: 50,000 UGX                  │
│ You will receive: 1,351 sats        │
│                                     │
│ A payment prompt will be sent       │
│ to your phone.                      │
│                                     │
│ 1. Confirm                          │
│ 2. Cancel                           │
│                                     │
│ Reply 1 or 2:                       │
└─────────────────────────────────────┘

Step 3: MTN PIN prompt (on phone)
┌─────────────────────────────────────┐
│ MTN Mobile Money                    │
│ Enter PIN to confirm payment:       │
│ 50,000 UGX to Mobibit Africa        │
│                                     │
│ [User enters MTN PIN]               │
└─────────────────────────────────────┘

Step 4: Confirmation
┌─────────────────────────────────────┐
│ FUND REQUEST SENT                   │
│                                     │
│ Amount: 50,000 UGX                  │
│ You will receive a payment prompt   │
│ on your phone.                      │
│                                     │
│ Reply 0 for main menu.              │
└─────────────────────────────────────┘

Step 5: SMS confirmation
📱 Mobibit Africa: 50,000 UGX received!
Balance credited: 1,351 sats
Ref: SC-A1B2C3D4E5F6
View: mobibitafrica.com/dashboard
```

### Receive USD (Option 4)

```
Step 1: Enter amount
┌─────────────────────────────────────┐
│ RECEIVE USD                         │
│ Enter amount in USD:                │
│                                     │
│ $1 - $10,000                        │
└─────────────────────────────────────┘

Step 2: Confirm
┌─────────────────────────────────────┐
│ RECEIVE USD - CONFIRM               │
│ Amount: $50.00 USD                  │
│                                     │
│ A payment request will be sent.     │
│                                     │
│ 1. Confirm                          │
│ 2. Cancel                           │
│                                     │
│ Reply 1 or 2:                       │
└─────────────────────────────────────┘

Step 3: Success
┌─────────────────────────────────────┐
│ USD PAYMENT REQUEST SENT            │
│                                     │
│ Amount: $50.00 USD                  │
│ A payment request has been created. │
│ Share the invoice with the sender.  │
│                                     │
│ Reply 0 for main menu.              │
└─────────────────────────────────────┘
```

### Convert BTC ↔ USD (Option 5)

```
Step 1: Choose direction
┌─────────────────────────────────────┐
│ CONVERT BTC <-> USD                 │
│                                     │
│ 1. BTC -> USD                       │
│ 2. USD -> BTC                       │
│                                     │
│ Reply 1 or 2:                       │
└─────────────────────────────────────┘

Step 2: Enter amount (if BTC → USD)
┌─────────────────────────────────────┐
│ SWAP BTC -> USD                     │
│                                     │
│ Enter amount in sats:               │
└─────────────────────────────────────┘

Step 3: Confirm
┌─────────────────────────────────────┐
│ SWAP CONFIRM                        │
│ 50,000 sats -> $12.50 USD           │
│                                     │
│ 1. Confirm Swap                     │
│ 2. Cancel                           │
└─────────────────────────────────────┘

Step 4: Success
┌─────────────────────────────────────┐
│ SWAP COMPLETED                      │
│                                     │
│ 50000 BTC converted successfully.   │
│                                     │
│ Reply 0 for main menu.              │
└─────────────────────────────────────┘
```

### USSD State Machine Diagram

```
                           ┌──────────────────┐
              ┌───────────>│    MAIN MENU     │<───────────┐
              │            │  (Options 1-6)   │            │
              │            └────────┬─────────┘            │
              │                     │                      │
              │     ┌───────────────┼──────────────┐       │
              │     │               │              │       │
              │     ▼               ▼              ▼       │
              │ ┌────────┐   ┌──────────┐   ┌─────────┐  │
              │ │ CHECK  │   │ SEND BTC │   │  FUND   │  │
              │ │ BALANCE│   │  MENU    │   │ ACCOUNT │  │
              │ └───┬────┘   └────┬─────┘   └────┬────┘  │
              │     │             │               │       │
              │     │             ▼               ▼       │
              │     │      ┌──────────┐   ┌──────────┐   │
              │     │      │  ENTER   │   │  ENTER   │   │
              │     │      │ PHONE #  │   │ AMOUNT   │   │
              │     │      └────┬─────┘   └────┬─────┘   │
              │     │           │               │         │
              │     │           ▼               ▼         │
              │     │      ┌──────────┐   ┌──────────┐   │
              │     │      │  ENTER   │   │ CONFIRM  │   │
              │     │      │ AMOUNT   │   │ & SEND   │───┘
              │     │      └────┬─────┘   └──────────┘
              │     │           │
              │     │           ▼
              │     │      ┌──────────┐
              │     │      │ CONFIRM  │
              │     │      │ & SEND   │
              │     │      └────┬─────┘
              │     │           │
              │     │           ▼
              │     │   ┌──────────────┐
              │     └──>│ TRANSACTION  │
              │         │   RESULT     │
              │         └──────┬───────┘
              │                │
              └────────────────┘
                   (Reply 0)
```

### USSD Session Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  DIAL    │     │  MENU    │     │  INPUT   │     │  RESULT  │
│  *123#   │────>│  DISPLAY │────>│  COLLECT │────>│  SHOW    │
│          │     │          │     │          │     │          │
│ AT sends │     │ Backend  │     │ User     │     │ Response │
│ callback │     │ returns  │     │ types    │     │ shown,   │
│ to our   │     │ CON text │     │ number   │     │ END sent │
│ endpoint │     │          │     │          │     │          │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                      │
                                                      │ (or loop
                                                      │  back to
                                                      │  menu)
                                                      ▼
                                               ┌──────────┐
                                               │  SESSION │
                                               │  TIMEOUT │
                                               │ (3 min)  │
                                               └──────────┘
```

---

## Web App Interaction Guide

### Complete Demo Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  STEP 1  │    │  STEP 2  │    │  STEP 3  │    │  STEP 4  │
│          │    │          │    │          │    │          │
│  Sign Up │───>│  Login   │───>│Dashboard │───>│ Fund Card│
│          │    │          │    │          │    │          │
│ Create   │    │ Phone +  │    │ View     │    │ Select   │
│ account  │    │ PIN auth │    │ balance  │    │ MTN/Air  │
│          │    │          │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └────┬─────┘
                                                      │
┌──────────┐    ┌──────────┐    ┌──────────┐         │
│  STEP 8  │    │  STEP 7  │    │  STEP 6  │         │
│          │    │          │    │          │         │
│  Profile │<───│ Settings │<───│Transactns│<────────┘
│          │    │          │    │          │
│ Edit     │    │ Limits,  │    │ View     │
│ info,    │    │ notifs,  │    │ history  │
│ KYC      │    │ currency │    │          │
└──────────┘    └──────────┘    └──────────┘

                    ┌──────────┐
                    │  STEP 5  │
                    │          │
                    │ Send BTC │────> Lightning Payment
                    │          │
                    └──────────┘
```

### Page-by-Page Guide

#### Landing Page (`/`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           MOBIBIT AFRICA                         │
│           Bitcoin for Everyone                   │
│                                                  │
│    Turn your mobile money into Bitcoin           │
│    in 3 taps, spend it anywhere.                 │
│                                                  │
│    ┌──────────────┐  ┌──────────────┐           │
│    │  Get Started  │  │  Learn More  │           │
│    └──────────────┘  └──────────────┘           │
│                                                  │
│    Features:                                     │
│    ✅ Fund with MTN, Airtel, Orange              │
│    ✅ Instant Lightning conversion               │
│    ✅ Virtual Visa card                          │
│    ✅ Works on feature phones                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Signup Page (`/signup`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           CREATE ACCOUNT                         │
│                                                  │
│    Full Name:  [________________]                │
│    Email:      [________________]                │
│    Phone:      [________________]                │
│    Password:   [________________]                │
│    Confirm:    [________________]                │
│                                                  │
│    ┌──────────────────────────────┐              │
│    │         Sign Up              │              │
│    └──────────────────────────────┘              │
│                                                  │
│    Already have an account? Login                │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Dashboard Page (`/dashboard`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           DASHBOARD                              │
│                                                  │
│    ┌──────────────────────────────────┐         │
│    │  Balance                          │         │
│    │  250,000 sats                     │         │
│    │  0.00250000 BTC                   │         │
│    │  ≈ $98.75 USD                     │         │
│    └──────────────────────────────────┘         │
│                                                  │
│    Quick Actions:                                │
│    ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐         │
│    │ Fund │ │ Send │ │Recve │ │ Card │         │
│    └──────┘ └──────┘ └──────┘ └──────┘         │
│                                                  │
│    Recent Transactions:                          │
│    ┌──────────────────────────────────┐         │
│    │ 📥 Received  +50,000 sats  2h ago│         │
│    │ 📤 Sent      -10,000 sats  5h ago│         │
│    │ 💳 Spent     -2,500 sats   1d ago│         │
│    └──────────────────────────────────┘         │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Fund Card Page (`/fund`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           FUND CARD                              │
│                                                  │
│    Select Provider:                              │
│    ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│    │ 🟡 MTN   │ │ 🔴 Airtel│ │ 🟠 Orange│      │
│    │  MoMo    │ │  Money   │ │  Money   │      │
│    └──────────┘ └──────────┘ └──────────┘      │
│                                                  │
│    Phone Number: [________________]              │
│    Amount (UGX): [________________]              │
│                                                  │
│    Conversion Preview:                           │
│    ┌──────────────────────────────────┐         │
│    │  50,000 UGX → 1,351 sats         │         │
│    │  Exchange Rate: 1 USD = 3,700 UGX │         │
│    │  BTC Price: $79,000               │         │
│    └──────────────────────────────────┘         │
│                                                  │
│    ┌──────────────────────────────┐              │
│    │         Fund Card            │              │
│    └──────────────────────────────┘              │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Send Bitcoin Page (`/send`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           SEND BITCOIN                           │
│                                                  │
│    Lightning Address/Invoice:                    │
│    [________________________________________]    │
│                                                  │
│    Amount (sats): [________________]             │
│                                                  │
│    USD Equivalent: ≈ $12.50                      │
│                                                  │
│    Memo (optional): [________________]           │
│                                                  │
│    Network Fee: ~1 sat                           │
│                                                  │
│    ┌──────────────────────────────┐              │
│    │         Send Bitcoin         │              │
│    └──────────────────────────────┘              │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Receive Bitcoin Page (`/receive`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           RECEIVE BITCOIN                        │
│                                                  │
│    Amount (sats): [________________]             │
│    Description:   [________________]             │
│                                                  │
│    ┌──────────────────────────────┐              │
│    │      Generate Invoice        │              │
│    └──────────────────────────────┘              │
│                                                  │
│    ┌──────────────────────────────────┐         │
│    │  Lightning Invoice               │         │
│    │                                  │         │
│    │  lnbc1000000000000000000...      │         │
│    │                                  │         │
│    │  Amount: 100,000 sats            │         │
│    │  Expires in: 58 minutes          │         │
│    │                                  │         │
│    │  ┌──────────────────────┐       │         │
│    │  │   Copy Invoice       │       │         │
│    │  └──────────────────────┘       │         │
│    └──────────────────────────────────┘         │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Virtual Card Page (`/card`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           MOBIBIT AFRICA CARD                    │
│                                                  │
│    ┌──────────────────────────────────┐         │
│    │  ╔═══════════════════════════╗   │         │
│    │  ║  MOBIBIT AFRICA           ║   │         │
│    │  ║                           ║   │         │
│    │  ║  4532 •••• •••• 7891      ║   │         │
│    │  ║                           ║   │         │
│    │  ║  JOHN DOE                 ║   │         │
│    │  ║  12/28                    ║   │         │
│    │  ╚═══════════════════════════╝   │         │
│    └──────────────────────────────────┘         │
│                                                  │
│    Balance: 250,000 sats ($98.75)               │
│    Status: Active                                │
│                                                  │
│    ┌──────────┐ ┌──────────┐                    │
│    │   Fund   │ │  Freeze  │                    │
│    └──────────┘ └──────────┘                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

#### Transactions Page (`/transactions`)
```
┌─────────────────────────────────────────────────┐
│                                                  │
│           TRANSACTIONS                           │
│                                                  │
│    Filters: [All] [Fund] [Payment] [Spend]      │
│                                                  │
│    ┌──────────────────────────────────┐         │
│    │ 📥 Fund    +50,000 sats  2h ago │         │
│    │    MTN MoMo | 50,000 UGX        │         │
│    │    Status: ✅ Settled            │         │
│    ├──────────────────────────────────┤         │
│    │ 📤 Send    -10,000 sats  5h ago │         │
│    │    Lightning | Fee: 1 sat        │         │
│    │    Status: ✅ Settled            │         │
│    ├──────────────────────────────────┤         │
│    │ 💳 Spend   -2,500 sats   1d ago │         │
│    │    Kampala Cafe | $1.00 USD      │         │
│    │    Status: ✅ Settled            │         │
│    └──────────────────────────────────┘         │
│                                                  │
│    Summary:                                      │
│    Total Received: 150,000 sats                  │
│    Total Sent: 12,500 sats                       │
│    Total Spent: 5,000 sats                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Flow 1: USSD → Buy Bitcoin (Mobile Money → BTC)

This is the core flow. A user on a feature phone converts mobile money to Bitcoin:

```
┌──────────┐    ┌──────────┐    ┌──────────────────┐    ┌────────────┐    ┌──────────┐
│  USER'S  │    │ AFRICA'S │    │  MOBIBIT BACKEND  │    │  MOBILE    │    │ LIGHTNING│
│  PHONE   │    │ TALKING  │    │   (FastAPI)       │    │  MONEY     │    │ NETWORK  │
│  (*123#) │    │ GATEWAY  │    │                   │    │  (MTN)     │    │  (LND)   │
└────┬─────┘    └────┬─────┘    └────────┬──────────┘    └─────┬──────┘    └────┬─────┘
     │               │                   │                      │                │
     │  1. Dials *123#                   │                      │                │
     │──────────────>│                   │                      │                │
     │               │  2. POST /api/at/ussd                   │                │
     │               │  {sessionId, phone, text: "3"}          │                │
     │               │──────────────────>│                      │                │
     │               │                   │                      │                │
     │               │  3. "FUND ACCOUNT"│                      │                │
     │               │     Enter amount  │                      │                │
     │               │<──────────────────│                      │                │
     │  4. Shows     │                   │                      │                │
     │  menu         │                   │                      │                │
     │<──────────────│                   │                      │                │
     │               │                   │                      │                │
     │  5. User enters "50000"           │                      │                │
     │──────────────>│                   │                      │                │
     │               │  6. POST /api/at/ussd                   │                │
     │               │  text: "3*50000"  │                      │                │
     │               │──────────────────>│                      │                │
     │               │                   │                      │                │
     │               │                   │  7. Get exchange     │                │
     │               │                   │  rate from           │                │
     │               │                   │  CoinGecko API       │                │
     │               │                   │──────┐               │                │
     │               │                   │<─────┘               │                │
     │               │                   │                      │                │
     │               │  8. "CONFIRM:     │                      │                │
     │               │  50,000 UGX →     │                      │                │
     │               │  1,351 sats"      │                      │                │
     │               │<──────────────────│                      │                │
     │  9. Shows     │                   │                      │                │
     │  confirm      │                   │                      │                │
     │<──────────────│                   │                      │                │
     │               │                   │                      │                │
     │  10. User replies "1" (Confirm)   │                      │                │
     │──────────────>│                   │                      │                │
     │               │  11. POST         │                      │                │
     │               │──────────────────>│                      │                │
     │               │                   │                      │                │
     │               │                   │  12. MTN Adapter:    │                │
     │               │                   │  OAuth2 auth +       │                │
     │               │                   │  Request to Pay      │                │
     │               │                   │─────────────────────>│                │
     │               │                   │                      │                │
     │               │                   │  13. MTN pushes      │                │
     │               │                   │  PIN prompt to       │                │
     │               │                   │  user's phone        │                │
     │               │                   │<─────────────────────│                │
     │               │                   │                      │                │
     │  14. MTN PIN prompt              │                      │                │
     │<─────────────────────────────────────────────────────────│                │
     │               │                   │                      │                │
     │  15. User enters PIN             │                      │                │
     │─────────────────────────────────────────────────────────>│                │
     │               │                   │                      │                │
     │               │                   │  16. Webhook:        │                │
     │               │                   │  payment SUCCESSFUL  │                │
     │               │                   │<─────────────────────│                │
     │               │                   │                      │                │
     │               │                   │  17. Credit wallet:  │                │
     │               │                   │  balance += 1,351 sats               │
     │               │                   │──────┐               │                │
     │               │                   │<─────┘ DB update     │                │
     │               │                   │                      │                │
     │               │                   │  18. Send SMS:       │                │
     │               │                   │  "✅ 50,000 UGX      │                │
     │               │                   │  received!           │                │
     │               │                   │  1,351 sats credited"│                │
     │  19. SMS arrives                 │                      │                │
     │<──────────────────────────────────────────────────────────                │
```

### Flow 2: Web App → Send Bitcoin via Lightning

```
┌──────────┐    ┌──────────────────┐    ┌──────────┐    ┌────────────┐
│  USER'S  │    │  MOBIBIT BACKEND │    │   LND    │    │ RECIPIENT  │
│ BROWSER  │    │   (FastAPI)      │    │ NODE     │    │ (Lightning │
│ (React)  │    │                  │    │          │    │  Wallet)   │
└────┬─────┘    └────────┬─────────┘    └────┬─────┘    └─────┬──────┘
     │                   │                   │                 │
     │  1. POST /api/payments/send           │                 │
     │  {invoice: "lnbc1000...",             │                 │
     │   amount: 50000, memo: "Payment"}     │                 │
     │──────────────────>│                   │                 │
     │                   │                   │                 │
     │                   │  2. Validate JWT  │                 │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │                   │  3. Check wallet  │                 │
     │                   │  balance >= 50000 │                 │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │                   │  4. Reserve sats  │                 │
     │                   │  (hold in pending)│                 │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │                   │  5. LND: Pay Invoice               │
     │                   │──────────────────>│                 │
     │                   │                   │  6. Route       │
     │                   │                   │  payment through│
     │                   │                   │  channels       │
     │                   │                   │────────────────>│
     │                   │                   │                 │
     │                   │  7. Payment SUCCESS + preimage      │
     │                   │<──────────────────│                 │
     │                   │                   │                 │
     │                   │  8. Deduct from wallet + record TX  │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │  9. Response:     │                   │                 │
     │  {success: true,  │                   │                 │
     │   tx_hash, fee}   │                   │                 │
     │<──────────────────│                   │                 │
     │                   │                   │                 │
     │  10. Dashboard shows updated balance  │                 │
```

### Flow 3: Receive Bitcoin → Virtual Card Spend

```
┌──────────┐    ┌──────────────────┐    ┌──────────┐    ┌────────────┐
│  USER'S  │    │  MOBIBIT BACKEND │    │   LND    │    │  VIRTUAL   │
│ BROWSER  │    │   (FastAPI)      │    │ NODE     │    │  CARD      │
│          │    │                  │    │          │    │ (Visa API) │
└────┬─────┘    └────────┬─────────┘    └────┬─────┘    └─────┬──────┘
     │                   │                   │                 │
     │  ── STEP A: RECEIVE BTC ──            │                 │
     │                   │                   │                 │
     │  A1. POST /api/wallet/invoice         │                 │
     │  {amount_sats: 100000}               │                 │
     │──────────────────>│                   │                 │
     │                   │                   │                 │
     │                   │  A2. LND: Create Invoice           │
     │                   │──────────────────>│                 │
     │                   │                   │                 │
     │                   │  A3. BOLT11 invoice string         │
     │                   │<──────────────────│                 │
     │                   │                   │                 │
     │  A4. Invoice + QR code                │                 │
     │<──────────────────│                   │                 │
     │                   │                   │                 │
     │  A5. Sender pays invoice ────────────────────────────>│
     │                   │                   │                 │
     │                   │  A6. Webhook: Payment received      │
     │                   │<──────────────────│                 │
     │                   │                   │                 │
     │                   │  A7. Credit wallet: +100,000 sats   │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │  ── STEP B: SPEND WITH CARD ──        │                 │
     │                   │                   │                 │
     │  B1. POST /api/payments/spend         │                 │
     │  {merchant: "Kampala Cafe",           │                 │
     │   amount_usd: 5.00}                   │                 │
     │──────────────────>│                   │                 │
     │                   │                   │                 │
     │                   │  B2. Convert USD → sats             │
     │                   │  (5.00 → 12,500) │                 │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │                   │  B3. Deduct from wallet             │
     │                   │──────┐            │                 │
     │                   │<─────┘            │                 │
     │                   │                   │                 │
     │                   │  B4. Charge virtual card            │
     │                   │───────────────────────────────────>│
     │                   │                   │                 │
     │                   │  B5. Card auth response             │
     │                   │<───────────────────────────────────│
     │                   │                   │                 │
     │  B6. Transaction confirmed            │                 │
     │<──────────────────│                   │                 │
```

### Flow 4: Currency Conversion Chain

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  Local Fiat │────>│    USD     │────>│    BTC     │────>│    Sats    │
│  (UGX/KES) │     │  (Pivot)   │     │  (Bitcoin) │     │ (Smallest  │
│             │     │            │     │            │     │  Unit)     │
│  50,000 UGX │     │  $13.51    │     │ 0.000171   │     │  17,100    │
│             │     │            │     │ BTC        │     │  sats      │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
       │                  │                  │                  │
       │     CoinGecko    │    1 BTC =       │    1 BTC =       │
       │     Real-time    │    ~$79,000      │    100,000,000   │
       │     rates        │                  │    sats          │
```

### Flow 5: Transaction Lifecycle State Machine

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│  INITIATED  │──>│   PENDING   │──>│ PROCESSING  │──>│   SETTLED   │
│             │   │             │   │             │   │             │
│  TX created │   │ Provider    │   │ User        │   │ Confirmed   │
│  waiting    │   │ acknowledged│   │ approved,   │   │ on Lightning│
│  for API    │   │ prompt sent │   │ being       │   │ /blockchain │
│  call       │   │ to phone    │   │ processed   │   │             │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘
                                          │
                                          ▼
                                    ┌─────────────┐
                                    │   FAILED    │
                                    │             │
                                    │ Provider or │
                                    │ network     │
                                    │ error       │
                                    └──────┬──────┘
                                           │
                                           ▼
                                    ┌─────────────┐
                                    │  REVERSED   │
                                    │             │
                                    │ Refund /    │
                                    │ chargeback  │
                                    └─────────────┘
```

### Flow 6: Webhook Processing Flow

```
┌────────────┐     ┌──────────────────┐     ┌────────────┐     ┌────────────┐
│  MOBILE    │     │  MOBIBIT BACKEND │     │ DATABASE   │     │   USER     │
│  MONEY API │     │   (Webhook)      │     │            │     │            │
└─────┬──────┘     └────────┬─────────┘     └─────┬──────┘     └─────┬──────┘
      │                     │                     │                   │
      │  1. Payment status  │                     │                   │
      │  callback           │                     │                   │
      │────────────────────>│                     │                   │
      │                     │                     │                   │
      │                     │  2. Parse payload   │                   │
      │                     │  Extract reference  │                   │
      │                     │──────┐              │                   │
      │                     │<─────┘              │                   │
      │                     │                     │                   │
      │                     │  3. Find transaction│                   │
      │                     │  by reference       │                   │
      │                     │────────────────────>│                   │
      │                     │                     │                   │
      │                     │  4. Update status   │                   │
      │                     │  (PENDING → SETTLED)│                   │
      │                     │────────────────────>│                   │
      │                     │                     │                   │
      │                     │  5. Credit wallet   │                   │
      │                     │  balance            │                   │
      │                     │────────────────────>│                   │
      │                     │                     │                   │
      │                     │  6. Send SMS        │                   │
      │                     │  confirmation       │                   │
      │                     │──────────────────────────────────────>│
      │                     │                     │                   │
      │  7. 200 OK          │                     │                   │
      │<────────────────────│                     │                   │
```

---

## System Architecture (Full)

### Complete System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                                  │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │  USSD (*123#)│  │  Web App     │  │  SMS Alerts  │                 │
│  │  Feature     │  │  (React)     │  │  (Africa's   │                 │
│  │  Phones      │  │  Smartphones │  │  Talking)    │                 │
│  └──────┬───────┘  └──────┬───────┘  └──────▲───────┘                 │
│         │                 │                  │                          │
└─────────┼─────────────────┼──────────────────┼──────────────────────────┘
          │                 │                  │
          ▼                 ▼                  │
┌─────────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (FastAPI)                                │
│                                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ /api/at/ │ │ /api/    │ │ /api/    │ │ /api/    │ │ /api/    │    │
│  │ ussd     │ │ auth     │ │ wallet   │ │ payments │ │ webhooks │    │
│  │          │ │          │ │          │ │          │ │          │    │
│  │ AT GW    │ │ Register │ │ Balance  │ │ Collect  │ │ /mtn     │    │
│  │ callback │ │ Login    │ │ Invoice  │ │ Send     │ │ /airtel  │    │
│  │          │ │ JWT      │ │ Swap     │ │ Spend    │ │ /orange  │    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘    │
│       │            │            │             │            │            │
└───────┼────────────┼────────────┼─────────────┼────────────┼────────────┘
        │            │            │             │            │
        ▼            ▼            ▼             ▼            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SERVICE LAYER                                     │
│                                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │  USSD    │ │  Auth    │ │ Exchange │ │  LND /   │ │  SMS     │    │
│  │ Handler  │ │ Service  │ │  Rate    │ │  Strike  │ │ Service  │    │
│  │          │ │          │ │ Service  │ │ Service  │ │          │    │
│  │ Menu     │ │ JWT +    │ │ CoinGecko│ │ Create   │ │ Africa's │    │
│  │ State    │ │ PIN Hash │ │ + Cache  │ │ Invoice  │ │ Talking  │    │
│  │ Machine  │ │          │ │          │ │ Pay      │ │          │    │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘    │
│                                                                         │
│  ┌──────────┐ ┌──────────┐                                            │
│  │ Webhook  │ │Transactn │                                            │
│  │ Handler  │ │ Service  │                                            │
│  │          │ │          │                                            │
│  │ Process  │ │ Create + │                                            │
│  │ MTN/AT/  │ │ Status   │                                            │
│  │ Orange   │ │ Lifecycle│                                            │
│  └──────────┘ └──────────┘                                            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
        │            │            │             │
        ▼            ▼            ▼             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      ADAPTER LAYER (External APIs)                       │
│                                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │  MTN     │ │  Airtel  │ │  Orange  │ │  MPESA   │ │  LND     │    │
│  │  MoMo    │ │  Money   │ │  Money   │ │(Safaricom)│ │  Node    │    │
│  │          │ │          │ │          │ │          │ │          │    │
│  │ OAuth2 + │ │ OAuth2 + │ │ OAuth2 + │ │ REST API │ │ Invoice  │    │
│  │ Request  │ │ Customer │ │ Payment  │ │ Macaroon │ │ + Quote  │    │
│  │ to Pay   │ │ Pay      │ │ Init     │ │ Auth     │ │ + Pay    │    │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘    │
│       │            │            │             │            │            │
└───────┼────────────┼────────────┼─────────────┼────────────┼────────────┘
        │            │            │             │            │
        ▼            ▼            ▼             ▼            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                                   │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ MTN Mobile   │  │ Airtel Money │  │ Orange Money │                 │
│  │ Money        │  │              │  │              │                 │
│  │ (Rwanda,     │  │ (Uganda,     │  │ (West Africa │                 │
│  │  Uganda,     │  │  Kenya,      │  │  Senegal,    │                 │
│  │  Ghana)      │  │  Tanzania)   │  │  Cameroon)   │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│  │ Lightning    │  │ CoinGecko    │  │ Africa's     │                 │
│  │ Network      │  │ (BTC Price)  │  │ Talking      │                 │
│  │ (Bitcoin     │  │              │  │ (USSD + SMS) │                 │
│  │  mainnet)    │  │              │  │              │                 │
│  └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
        │            │            │
        ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATA STORE                                        │
│                                                                         │
│  ┌──────────────────────────────────────────┐                          │
│  │           PostgreSQL Database             │                          │
│  │                                           │                          │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────┐ │                          │
│  │  │  users  │  │ wallets  │  │  trans-  │ │                          │
│  │  │         │  │          │  │ actions  │ │                          │
│  │  │ phone   │  │ balance  │  │          │ │                          │
│  │  │ pin     │  │ _sats    │  │ type     │ │                          │
│  │  │ name    │  │ balance  │  │ status   │ │                          │
│  │  │ kyc     │  │ _usd     │  │ amount   │ │                          │
│  │  │         │  │ card_*   │  │ provider │ │                          │
│  │  └─────────┘  └──────────┘  └─────────┘ │                          │
│  │                                           │                          │
│  │  ┌──────────────────┐                    │                          │
│  │  │  ussd_sessions   │                    │                          │
│  │  │                  │                    │                          │
│  │  │ session_id       │                    │                          │
│  │  │ current_screen   │                    │                          │
│  │  │ accumulated_     │                    │                          │
│  │  │   input          │                    │                          │
│  │  └──────────────────┘                    │                          │
│  └──────────────────────────────────────────┘                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Provider Adapter Pattern

```
┌─────────────────────────────────────────────────┐
│           MobileMoneyAdapter (Abstract)          │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  + authenticate() -> str                 │   │
│  │  + collect(PaymentRequest) -> Response   │   │
│  │  + check_status(txn_id) -> Response      │   │
│  │  + validate_phone(phone) -> bool         │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│         ▲              ▲              ▲          │
│         │              │              │          │
│    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐   │
│    │   MTN   │    │ Airtel  │    │ Orange  │   │
│    │  MoMo   │    │ Money   │    │ Money   │   │
│    │         │    │         │    │         │   │
│    │ Country-│    │ Country-│    │ Country-│   │
│    │ specific│    │ specific│    │ specific│   │
│    │ URLs    │    │ URLs    │    │ URLs    │   │
│    └─────────┘    └─────────┘    └─────────┘   │
│                                                  │
│  Adding a new provider = 1 new file              │
│  implementing the abstract methods               │
└─────────────────────────────────────────────────┘
```

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number    VARCHAR(20) UNIQUE NOT NULL,  -- E.164 format
    name            VARCHAR(100) NOT NULL DEFAULT 'User',
    email           VARCHAR(255) UNIQUE,
    pin_hash        VARCHAR(128) NOT NULL,         -- SHA-256 hash
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    kyc_level       VARCHAR(20) DEFAULT 'none',    -- none | tier1 | tier2
    country         VARCHAR(3) DEFAULT 'UG',
    preferred_currency VARCHAR(3) DEFAULT 'UGX',
    daily_limit_usd   FLOAT DEFAULT 500.0,
    monthly_limit_usd FLOAT DEFAULT 5000.0,
    last_login_at   TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);
```

### Wallets Table

```sql
CREATE TABLE wallets (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID UNIQUE REFERENCES users(id),
    balance_sats    BIGINT DEFAULT 0,              -- BTC balance in sats
    reserved_sats   BIGINT DEFAULT 0,              -- Pending transactions
    balance_usd     FLOAT DEFAULT 0.0,             -- USD wallet
    reserved_usd    FLOAT DEFAULT 0.0,
    card_number     VARCHAR(19),                   -- Virtual card (encrypted)
    card_last4      VARCHAR(4),
    card_expiry     VARCHAR(5),                    -- MM/YY
    card_status     VARCHAR(20) DEFAULT 'inactive',
    daily_spent_sats   BIGINT DEFAULT 0,
    monthly_spent_sats BIGINT DEFAULT 0,
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW(),

    CHECK (balance_sats >= 0),
    CHECK (reserved_sats >= 0)
);
```

### Transactions Table

```sql
CREATE TABLE transactions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID REFERENCES users(id),
    type            VARCHAR(20) NOT NULL,          -- fund | send | receive | spend | swap
    status          VARCHAR(20) DEFAULT 'initiated',
    reference       VARCHAR(50) UNIQUE NOT NULL,   -- SC-A1B2C3D4E5F6
    amount_fiat     FLOAT NOT NULL,
    currency_fiat   VARCHAR(3) NOT NULL,
    amount_sats     BIGINT NOT NULL,
    fee_sats        BIGINT DEFAULT 0,
    rate_used       FLOAT NOT NULL,
    provider        VARCHAR(30) NOT NULL,          -- mtn_momo | airtel_money | orange_money | lightning
    provider_txn_id VARCHAR(100),
    phone_number    VARCHAR(20),
    merchant_name   VARCHAR(100),
    description     TEXT,
    payment_hash    VARCHAR(64),                   -- Lightning payment hash
    payment_request TEXT,                          -- BOLT11 invoice
    initiated_at    TIMESTAMP DEFAULT NOW(),
    settled_at      TIMESTAMP,
    failed_at       TIMESTAMP,
    created_at      TIMESTAMP DEFAULT NOW()
);
```

### USSD Sessions Table

```sql
CREATE TABLE ussd_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      VARCHAR(100) UNIQUE NOT NULL,
    phone_number    VARCHAR(20) NOT NULL,
    current_screen  VARCHAR(50) DEFAULT 'main_menu',
    accumulated_input TEXT DEFAULT '{}',
    menu_depth      INTEGER DEFAULT 0,
    user_id         UUID REFERENCES users(id),
    created_at      TIMESTAMP DEFAULT NOW(),
    last_request_at TIMESTAMP DEFAULT NOW()
);
```

---

## Complete File Reference

### Frontend Files (React)

| File | Contains |
|------|----------|
| `src/pages/Landing.jsx` | Landing page with project overview |
| `src/pages/Login.jsx` | Login form (phone + PIN) |
| `src/pages/Signup.jsx` | Account creation form |
| `src/pages/Dashboard.jsx` | Main hub - balance, quick actions, recent txns |
| `src/pages/Card.jsx` | Virtual card display |
| `src/pages/Fund.jsx` | Fund card via MTN/Airtel/Orange |
| `src/pages/Send.jsx` | Send Bitcoin via Lightning |
| `src/pages/Receive.jsx` | Generate Lightning invoice |
| `src/pages/Spend.jsx` | Virtual card spending |
| `src/pages/Transactions.jsx` | Transaction history with filters |
| `src/pages/Profile.jsx` | User profile, KYC status |
| `src/pages/Settings.jsx` | Preferences, limits, notifications |
| `src/pages/Help.jsx` | FAQs, support |
| `src/services/index.js` | All mock API services (7 services) |
| `src/context/index.jsx` | Auth, Wallet, Theme state management |
| `src/components/index.jsx` | Design system (Button, Input, Card, etc.) |
| `src/hooks/index.js` | Custom hooks (useAsync, useForm, etc.) |
| `src/data/index.js` | Mock data (users, wallets, transactions) |
| `src/utils/index.js` | Helper functions (formatCurrency, etc.) |
| `src/App.jsx` | Main routing with protected routes |
| `src/main.jsx` | Entry point |

### Backend Files (FastAPI/Python)

| File | Contains |
|------|----------|
| `backend/app/main.py` | FastAPI app entry point, CORS, routers |
| `backend/app/core/config.py` | All env vars (MTN, Airtel, LND, etc.) |
| `backend/app/core/database.py` | PostgreSQL async connection |
| `backend/app/ussd/handler.py` | **USSD state machine** - all 6 menus |
| `backend/app/api/routes.py` | **Main API** - USSD, payments, wallet, webhooks |
| `backend/app/api/auth_routes.py` | Register, login, JWT auth |
| `backend/app/api/at_ussd_routes.py` | Africa's Talking USSD callback |
| `backend/app/api/lightning_routes.py` | Lightning payment routes |
| `backend/app/adapters/base.py` | **Abstract adapter interface** |
| `backend/app/adapters/mtn.py` | **MTN MoMo adapter** - OAuth2 + Request to Pay |
| `backend/app/adapters/airtel.py` | **Airtel Money adapter** |
| `backend/app/adapters/orange.py` | **Orange Money adapter** |
| `backend/app/adapters/lightning.py` | **Strike API adapter** for Lightning |
| `backend/app/adapters/africastalking.py` | Africa's Talking USSD + SMS adapter |
| `backend/app/models/user.py` | **User model** - phone, PIN, KYC |
| `backend/app/models/wallet.py` | **Wallet model** - BTC sats + USD balance |
| `backend/app/models/transaction.py` | **Transaction model** - lifecycle states |
| `backend/app/models/ussd_session.py` | USSD session persistence |
| `backend/app/services/auth.py` | **JWT + PIN auth service** |
| `backend/app/services/lnd.py` | **LND Lightning service** - create/pay invoices |
| `backend/app/services/exchange_rate.py` | **CoinGecko price oracle** with caching |
| `backend/app/services/sms.py` | **SMS notifications** via Africa's Talking |
| `backend/app/services/webhook.py` | **Webhook handler** - MTN/Airtel/Orange callbacks |
| `backend/app/services/transaction.py` | Transaction lifecycle manager |

### Key Files by Concept

```
USSD Flow:        backend/app/ussd/handler.py + backend/app/api/at_ussd_routes.py
Buy BTC Flow:     backend/app/api/routes.py (POST /api/payments/collect)
Send BTC Flow:    backend/app/api/routes.py + backend/app/services/lnd.py
Card Spend:       backend/app/api/routes.py + backend/app/adapters/lightning.py
Mobile Money:     backend/app/adapters/mtn.py, airtel.py, orange.py
Webhooks:         backend/app/services/webhook.py + backend/app/api/routes.py
Auth:             backend/app/services/auth.py + backend/app/api/auth_routes.py
Exchange Rates:   backend/app/services/exchange_rate.py
Database Models:  backend/app/models/user.py, wallet.py, transaction.py
```

### Config & Infrastructure Files

| File | Contains |
|------|----------|
| `package.json` | Frontend dependencies (React, Vite, Tailwind) |
| `vite.config.js` | Vite build configuration |
| `tailwind.config.js` | Custom colors, fonts, animations |
| `backend/requirements.txt` | Python dependencies (FastAPI, SQLAlchemy, etc.) |
| `backend/alembic.ini` | Database migration configuration |
| `docker-compose.yml` | Container orchestration |
| `render.yaml` | Deployment configuration |
| `.env` / `.env.example` | Environment variables template |

---

## Environment Variables Reference

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mobibitafrica

# JWT
SECRET_KEY=your-secret-key-here

# MTN MoMo
MTN_MOMO_API_KEY=your-key
MTN_MOMO_API_USER=your-uuid
MTN_MOMO_API_SECRET=your-secret
MTN_MOMO_SUBSCRIPTION_KEY=your-subscription-key
MTN_MOMO_ENVIRONMENT=sandbox

# Airtel Money
AIRTEL_CLIENT_ID=your-client-id
AIRTEL_CLIENT_SECRET=your-client-secret

# Orange Money
ORANGE_MONEY_CLIENT_ID=your-client-id
ORANGE_MONEY_CLIENT_SECRET=your-client-secret

# Lightning Network
LND_HOST=localhost
LND_REST_PORT=8080
LND_MACAROON_HEX=your-macaroon-hex

# Africa's Talking (USSD + SMS)
AT_API_KEY=your-at-api-key
AT_USERNAME=sandbox

# Strike API (alternative Lightning)
STRIKE_API_KEY=your-strike-key
```

---

## Summary

**Mobibit Africa** solves the biggest barrier to Bitcoin adoption in emerging markets: **the fiat-to-Bitcoin bridge**.

By connecting mobile money (which 600M+ Africans already use) to Bitcoin via Lightning Network, we create a seamless path from fiat → BTC → real-world spending.

### Key Differentiators

| Feature | Mobibit Africa | Traditional Exchanges | Other Bitcoin Wallets |
|---------|-----------|----------------------|----------------------|
| **Mobile Money Funding** | ✅ Direct | ❌ No | ❌ No |
| **Lightning Network** | ✅ Instant | ⚠️ Slow | ⚠️ Some |
| **Virtual Card** | ✅ Built-in | ❌ No | ❌ No |
| **USSD Support** | ✅ Yes | ❌ No | ❌ No |
| **No Bank Account** | ✅ Required | ❌ Required | ⚠️ Sometimes |
| **African Focus** | ✅ Primary | ❌ Global | ❌ Global |

### The Moat

1. **Network Effects** — More users → more merchants → more users
2. **Local Partnerships** — Direct MTN/Airtel/Orange integrations
3. **Regulatory Compliance** — Built for African markets
4. **USSD Access** — Reaches feature phone users (70% of Africa)
5. **Lightning-first** — Instant, cheap transactions

---

**Built with:** React • FastAPI • Lightning Network • Mobile Money APIs
**Status:** 🚀 Demo Ready
**Target Markets:** Rwanda 🇷🇼 → Uganda 🇺🇬 → Ghana 🇬🇭 → Kenya 🇰🇪
**Contact:** [Your Team Email]
