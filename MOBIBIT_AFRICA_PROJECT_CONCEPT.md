# 🃏 MOBIBIT AFRICA — Complete Project Concept Document

**Bitcoin for Everyone. Powered by Mobile Money.**

> A Lightning-Powered Bitcoin Card MVP that bridges mobile money (600M+ users in Africa) to Bitcoin via Lightning Network, enabling users to convert local currency to BTC and spend it using a virtual card — all accessible through USSD on feature phones or a web app on smartphones.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Solution Overview](#3-solution-overview)
4. [User Interfaces](#4-user-interfaces)
5. [USSD Interaction Guide](#5-ussd-interaction-guide)
6. [Web App Interaction Guide](#6-web-app-interaction-guide)
7. [Data Flow Diagrams](#7-data-flow-diagrams)
8. [System Architecture](#8-system-architecture)
9. [Technical Stack](#9-technical-stack)
10. [API Reference](#10-api-reference)
11. [Database Schema](#11-database-schema)
12. [Security & Auth](#12-security--auth)

---

## 1. Executive Summary

**Mobibit Africa** solves the biggest barrier to Bitcoin adoption in emerging markets: **the fiat-to-Bitcoin bridge**.

By connecting mobile money (which 600M+ Africans already use) to Bitcoin via Lightning Network, we create a seamless path:

```
Mobile Money (Fiat) → Lightning Network (BTC) → Virtual Card (Spending)
```

### Key Numbers

| Metric | Value |
|--------|-------|
| Target Market (Africa Mobile Money) | $700B+ transactions/year |
| Unbanked Population in Africa | 1.4 billion |
| Mobile Money Users in Africa | 600M+ |
| Bitcoin Users Globally | 420M+ |
| Target Countries | Rwanda, Uganda, Ghana, Kenya |
| Growth Rate (Mobile Money) | 25% YoY |

---

## 2. Problem Statement

### Bitcoin Adoption in Emerging Markets is Broken

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE GAP                                       │
│                                                                  │
│  Mobile Money Users (600M+)  ←———— GAP ————→  Bitcoin Users     │
│        ↑                                    ↑                   │
│  Easy to use                          Hard to access            │
│  Widely available                     Requires bank account     │
│  Local currency only                  No spending utility       │
│                                                                  │
│  ══════════════════════════════════════════════════════════════  │
│  Nobody is bridging mobile money → Bitcoin → Real-world spending │
└─────────────────────────────────────────────────────────────────┘
```

### Problems We Solve

| Problem | Impact | Our Solution |
|---------|--------|--------------|
| No fiat-to-Bitcoin bridge | Mobile money users can't access Bitcoin | Direct MTN/Airtel/Orange → BTC conversion |
| Complex onboarding | Exchanges require KYC, bank accounts | Phone number + 4-digit PIN only |
| No spending utility | Bitcoin can't be spent locally | Virtual Visa card |
| High remittance fees | Cross-border costs 8-15% | Lightning Network (<1 cent fees) |
| Volatility risk | Holders can't protect against swings | Instant BTC ↔ USD swap |

---

## 3. Solution Overview

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

## 4. User Interfaces

Mobibit Africa provides **two interfaces** to reach all users:

### 4.1 USSD Interface (Feature Phones — No Internet Needed)

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

**USSD Features Available:**
- Check BTC/USD balance
- Send BTC to another phone number
- Fund account (Buy BTC with mobile money)
- Receive USD payments
- Convert BTC ↔ USD
- Get help and support info

### 4.2 Web App Interface (Smartphones — Internet Required)

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

**Web App Features:**
- Account creation and login
- Wallet management and balance viewing
- Funding via mobile money
- Sending/receiving Bitcoin via Lightning
- Virtual card spending
- Transaction history tracking
- User profile and settings management
- Real-time currency conversions

---

## 5. USSD Interaction Guide

### 5.1 Main Menu

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

### 5.2 Check Balance (Option 1)

```
User: *123# → Selects "1"

MOBIBIT AFRICA BALANCE

BTC: 250,000 sats
   = 0.00250000 BTC
   = $98.75 USD

USD Wallet: $0.00

Reply 0 for main menu.
```

### 5.3 Send BTC (Option 2)

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

### 5.4 Fund Account / Buy BTC (Option 3)

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

### 5.5 Receive USD (Option 4)

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

### 5.6 Convert BTC ↔ USD (Option 5)

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

### 5.7 USSD State Machine Diagram

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

### 5.8 USSD Session Lifecycle

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

## 6. Web App Interaction Guide

### 6.1 Complete Demo Flow

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

### 6.2 Page-by-Page Guide

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

## 7. Data Flow Diagrams

### 7.1 USSD → Buy Bitcoin (Mobile Money → BTC)

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

### 7.2 Web App → Send Bitcoin via Lightning

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

### 7.3 Receive Bitcoin → Virtual Card Spend

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

### 7.4 Currency Conversion Chain

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

### 7.5 Transaction Lifecycle State Machine

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

### 7.6 Webhook Processing Flow

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

## 8. System Architecture

### 8.1 Complete System Architecture

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
│  │  MTN     │ │  Airtel  │ │  Orange  │ │  LND     │ │ Strike   │    │
│  │  MoMo    │ │  Money   │ │  Money   │ │  Node    │ │ API      │    │
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

### 8.2 Provider Adapter Pattern

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

### 8.3 Project File Structure

```
mobibit-africa/
├── src/                          # Frontend (React)
│   ├── pages/                    # 13 page components
│   │   ├── Landing.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Card.jsx
│   │   ├── Fund.jsx
│   │   ├── Send.jsx
│   │   ├── Receive.jsx
│   │   ├── Spend.jsx
│   │   ├── Transactions.jsx
│   │   ├── Profile.jsx
│   │   ├── Settings.jsx
│   │   └── Help.jsx
│   ├── components/               # Reusable UI components
│   ├── services/                 # API abstraction layer
│   ├── context/                  # State management (Auth, Wallet, Theme)
│   ├── hooks/                    # Custom React hooks
│   ├── data/                     # Mock data objects
│   ├── types/                    # JSDoc type definitions
│   ├── utils/                    # Helper functions
│   ├── App.jsx                   # Main routing
│   └── styles.css                # Global styles (Tailwind)
│
├── backend/                      # Backend (FastAPI)
│   ├── app/
│   │   ├── adapters/             # MTN, Airtel, Orange, Lightning
│   │   │   ├── base.py           # Abstract adapter interface
│   │   │   ├── mtn.py            # MTN MoMo adapter
│   │   │   ├── airtel.py         # Airtel Money adapter
│   │   │   ├── orange.py         # Orange Money adapter
│   │   │   └── lightning.py      # Lightning Network adapter
│   │   ├── api/                  # Route handlers
│   │   │   ├── routes.py         # USSD, payments, wallet, webhooks
│   │   │   ├── auth_routes.py    # Register, login, JWT
│   │   │   └── at_ussd_routes.py # Africa's Talking USSD callback
│   │   ├── core/                 # Config, database setup
│   │   ├── models/               # SQLAlchemy models
│   │   │   ├── user.py           # User (phone-first auth)
│   │   │   ├── wallet.py         # Wallet (BTC + USD balances)
│   │   │   ├── transaction.py    # Transaction lifecycle
│   │   │   └── ussd_session.py   # USSD session state
│   │   ├── services/             # Business logic
│   │   │   ├── auth.py           # JWT + PIN authentication
│   │   │   ├── lnd.py            # Lightning Network daemon
│   │   │   ├── exchange_rate.py  # CoinGecko price oracle
│   │   │   ├── sms.py            # SMS notifications
│   │   │   ├── webhook.py        # Payment confirmation handler
│   │   │   └── transaction.py    # Transaction lifecycle manager
│   │   └── ussd/                 # USSD menu state machine
│   │       └── handler.py
│   └── alembic/                  # Database migrations
│
└── docker-compose.yml            # Container orchestration
```

---

## 9. Technical Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **USSD Gateway** | Africa's Talking | Feature phone access (no internet) |
| **Web Frontend** | React 18 + Vite + Tailwind | Smartphone web app (13 pages) |
| **Backend API** | Python FastAPI | Async REST API + webhooks |
| **Database** | PostgreSQL + Alembic | Users, wallets, transactions |
| **Lightning** | LND (or Strike API) | Bitcoin payments via Lightning |
| **Mobile Money** | MTN MoMo / Airtel / Orange | Fiat payment collection |
| **Exchange Rates** | CoinGecko API | Real-time BTC prices |
| **SMS** | Africa's Talking | Transaction confirmations |
| **Auth** | JWT + 4-digit PIN | Phone-number-first auth |
| **Animations** | Framer Motion | Smooth UI transitions |
| **Deployment** | Docker + Render/Railway | Containerized deployment |

---

## 10. API Reference

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create account with phone + PIN |
| POST | `/api/auth/login` | Login with phone + PIN |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Get current user profile |

### USSD

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/at/ussd` | Africa's Talking USSD callback |
| POST | `/api/at/ussd/test` | Test USSD flow (JSON API) |
| POST | `/api/at/sms` | Send SMS notification |

### Wallet

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/wallet/balance` | Get BTC + USD balance |
| POST | `/api/wallet/invoice` | Create Lightning invoice |
| POST | `/api/wallet/swap` | Swap BTC ↔ USD |

### Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/collect` | Initiate mobile money collection |
| GET | `/api/payments/{txn_id}/status` | Check payment status |
| POST | `/api/payments/send` | Send Bitcoin via Lightning |
| POST | `/api/payments/spend` | Spend with virtual card |

### Exchange Rates

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/rates/{currency}` | Get live exchange rate |
| POST | `/api/rates/convert` | Convert between currencies |

### Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/webhooks/mtn` | MTN MoMo callback |
| POST | `/api/webhooks/airtel` | Airtel Money callback |
| POST | `/api/webhooks/orange` | Orange Money callback |
| POST | `/api/webhooks/test/simulate` | Simulate webhook for testing |

---

## 11. Database Schema

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
    status          VARCHAR(20) DEFAULT 'initiated', -- initiated | pending | processing | settled | failed | reversed
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
    created_at      TIMESTAMP DEFAULT NOW(),

    INDEX idx_tx_user_created (user_id, created_at),
    INDEX idx_tx_status (status),
    INDEX idx_tx_reference (reference),
    INDEX idx_tx_provider_txn (provider_txn_id)
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

## 12. Security & Auth

### Authentication Flow

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  USER    │     │  BACKEND │     │  JWT     │     │  DATABASE│
│          │     │          │     │          │     │          │
└────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘
     │                │                │                 │
     │  1. Register   │                │                 │
     │  phone + PIN   │                │                 │
     │───────────────>│                │                 │
     │                │  2. Hash PIN   │                 │
     │                │──────┐         │                 │
     │                │<─────┘         │                 │
     │                │                │                 │
     │                │  3. Store user │                 │
     │                │  + create      │                 │
     │                │  wallet        │                 │
     │                │────────────────────────────────>│
     │                │                │                 │
     │                │  4. Generate   │                 │
     │                │  JWT tokens    │                 │
     │                │──────┐         │                 │
     │                │<─────┘         │                 │
     │                │                │                 │
     │  5. Return     │                │                 │
     │  tokens        │                │                 │
     │<───────────────│                │                 │
     │                │                │                 │
     │  6. Login      │                │                 │
     │  phone + PIN   │                │                 │
     │───────────────>│                │                 │
     │                │  7. Verify PIN │                 │
     │                │────────────────────────────────>│
     │                │                │                 │
     │  8. Return     │                │                 │
     │  tokens        │                │                 │
     │<───────────────│                │                 │
     │                │                │                 │
     │  9. API call   │                │                 │
     │  + Bearer JWT  │                │                 │
     │───────────────>│                │                 │
     │                │  10. Validate  │                 │
     │                │  JWT           │                 │
     │                │──────┐         │                 │
     │                │<─────┘         │                 │
     │                │                │                 │
     │  11. Response  │                │                 │
     │<───────────────│                │                 │
```

### Security Features

| Feature | Implementation |
|---------|---------------|
| **Password Hashing** | SHA-256 with salt (via passlib) |
| **JWT Tokens** | Access (1hr) + Refresh (30 days) |
| **Phone-First Auth** | Phone number IS identity (no email required) |
| **4-Digit PIN** | USSD-friendly authentication |
| **Webhook Signatures** | HMAC-SHA256 verification |
| **Rate Limiting** | Redis-based (planned) |
| **KYC Levels** | Tier 1 (phone) → Tier 2 (ID verification) |
| **Transaction Limits** | Daily ($500) + Monthly ($5000) defaults |

### Environment Variables

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
| **Mobile Money Funding** | ✅ Direct (MTN, Airtel, Orange, MPESA) | ❌ No | ❌ No |
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
