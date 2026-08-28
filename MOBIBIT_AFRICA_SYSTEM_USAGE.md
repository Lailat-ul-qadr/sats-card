# 📱 MOBIBIT AFRICA — System Usage Document

**How the System Works: User Interaction & Data Flow**

> This document explains how Mobibit Africa works end-to-end — from the moment a user picks up their phone to the moment Bitcoin arrives in their wallet and is spent at a merchant.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [User Types](#2-user-types)
3. [USSD Usage Guide (Feature Phones)](#3-ussd-usage-guide-feature-phones)
4. [Web App Usage Guide (Smartphones)](#4-web-app-usage-guide-smartphones)
5. [Complete Data Flow Diagrams](#5-complete-data-flow-diagrams)
6. [Transaction Lifecycle](#6-transaction-lifecycle)
7. [Error Handling & Edge Cases](#7-error-handling--edge-cases)
8. [Security & Authentication](#8-security--authentication)

---

## 1. System Overview

### What is Mobibit Africa?

Mobibit Africa is a **Bitcoin wallet** that connects **mobile money** to **Bitcoin** via the **Lightning Network**. It allows users in Africa to:

1. **Deposit** local currency (UGX, KES, etc.) using mobile money (MTN MoMo, Airtel Money, Orange Money, MPESA)
2. **Convert** it to Bitcoin instantly via Lightning Network
3. **Send** Bitcoin to anyone with a phone number
4. **Receive** Bitcoin from anyone worldwide
5. **Spend** Bitcoin using a virtual Visa card
6. **Swap** between Bitcoin and USD
7. **Withdraw** Bitcoin back to mobile money (BTC → Fiat)

### Supported Mobile Money Providers

| Provider | Countries | Currencies | API | Logo | Status |
|----------|-----------|------------|-----|------|--------|
| **MTN MoMo** | Rwanda 🇷🇼, Uganda 🇺🇬, Ghana 🇬🇭, Cameroon 🇨🇲 | RWF, UGX, GHS, XAF | MTN MoMo Collection API v2.0 | 🟡 Official MTN Logo | ✅ Integrated |
| **Airtel Money** | Uganda 🇺🇬, Kenya 🇰🇪, Tanzania 🇹🇿, Rwanda 🇷🇼 | UGX, KES, TZS, RWF | Airtel Africa Payment API | 🔴 Official Airtel Logo | ✅ Integrated |
| **Orange Money** | Senegal 🇸🇳, Cameroon 🇨🇲, Mali 🇲🇱, Ivory Coast 🇨🇮 | XOF, XAF | Orange Money Web Payment API | 🟠 Official Orange Logo | ✅ Integrated |
| **MPESA** | Kenya 🇰🇪, Tanzania 🇹🇿, Mozambique 🇲🇿, DRC 🇨🇩 | KES, TZS, MZN, CDF | Safaricom Daraja API | 🟢 Official Safaricom Logo | ✅ Integrated |

> **Note:** All official provider logos are displayed during the onboarding and account creation process. When a user selects a mobile money provider, the official logo is shown to build trust and recognition. The logos are sourced from official brand guidelines and are displayed at 200x200px minimum resolution.

### Two Ways to Access the System

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    MOBIBIT AFRICA SYSTEM                         │
│                                                                  │
│  ┌─────────────────────┐      ┌─────────────────────┐          │
│  │                     │      │                     │          │
│  │   USSD INTERFACE    │      │    WEB INTERFACE    │          │
│  │                     │      │                     │          │
│  │  For feature phones │      │  For smartphones    │          │
│  │  No internet needed │      │  Internet required  │          │
│  │  Dial *123#         │      │  mobibitafrica.com  │          │
│  │                     │      │                     │          │
│  │  ┌───────────────┐  │      │  ┌───────────────┐  │          │
│  │  │  Nokia 105    │  │      │  │  iPhone/      │  │          │
│  │  │  Samsung B310 │  │      │  │  Android      │  │          │
│  │  │  Any basic    │  │      │  │  Browser      │  │          │
│  │  └───────────────┘  │      │  └───────────────┘  │          │
│  │                     │      │                     │          │
│  └──────────┬──────────┘      └──────────┬──────────┘          │
│             │                            │                      │
│             └──────────┬─────────────────┘                      │
│                        │                                        │
│                        ▼                                        │
│              ┌─────────────────┐                                │
│              │  SAME BACKEND   │                                │
│              │  (FastAPI)      │                                │
│              │                 │                                │
│              │  Same wallet    │                                │
│              │  Same BTC       │                                │
│              │  Same features  │                                │
│              └─────────────────┘                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### What Happens Behind the Scenes

When a user interacts with Mobibit Africa, the following systems work together:

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  USER    │     │  API     │     │  SERVICE │     │ ADAPTER  │     │ EXTERNAL │
│          │     │  LAYER   │     │  LAYER   │     │  LAYER   │     │ SERVICES │
│          │     │          │     │          │     │          │     │          │
│ Phone/   │────>│ FastAPI  │────>│ Business │────>│ MTN/     │────>│ MTN MoMo │
│ Browser  │     │ Routes   │     │ Logic    │     │ Airtel/  │     │ Airtel   │
│          │     │          │     │          │     │ Orange/  │     │ Orange   │
│          │<────│ JWT Auth │<────│ Exchange │<────│ MPESA/   │     │ MPESA    │
│          │     │          │     │ Rates    │     │ LND      │<────│ Lightning│
│          │     │          │     │          │     │          │     │ CoinGecko│
└──────────┘     └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

### Onboarding & Brand Trust

During account creation and the funding process, official mobile money provider logos are displayed to:

1. **Build User Trust** — Recognizable brands (MTN, Airtel, Orange, Safaricom) signal a legitimate platform
2. **Guide Provider Selection** — Users see their provider's official logo and know it's supported
3. **Ensure Brand Compliance** — Only official logos from brand guidelines are used (200x200px minimum)
4. **Local Relevance** — Providers are shown based on the user's country/phone code

---

## 2. User Types

### Who Uses the System?

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER TYPES                                │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  MOBILE MONEY   │  │  BITCOIN        │  │  MERCHANT       │ │
│  │  USER           │  │  USER           │  │                  │ │
│  │                 │  │                 │  │                  │ │
│  │  Has MTN/Airtel/│  │  Has Lightning  │  │  Accepts BTC    │ │
│  │  Orange/MPESA   │  │  wallet or      │  │  payments via   │ │
│  │  wallet with    │  │  exchange       │  │  virtual card   │ │
│  │  local currency │  │                 │  │                  │ │
│  │                 │  │                 │  │                  │ │
│  │  Wants to:      │  │  Wants to:      │  │  Wants to:      │ │
│  │  Buy BTC        │  │  Send/Receive   │  │  Receive BTC    │ │
│  │  Send BTC       │  │  Convert to fiat│  │  Convert to fiat│ │
│  │  Spend BTC      │  │  Spend BTC      │  │  Accept payments│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                  │
│  Most users in Africa are MOBILE MONEY USERS who become         │
│  BITCOIN USERS through Mobibit Africa.                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Mobile Money Providers

### Supported Providers & Countries

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        MOBILE MONEY PROVIDERS                                    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │ 🟡 MTN MOBILE MONEY (MoMo)                                      │   │   │
│  │  │                                                                  │   │   │
│  │  │  [OFFICIAL MTN LOGO]                                            │   │   │
│  │  │                                                                  │   │   │
│  │  │  Countries: Rwanda 🇷🇼, Uganda 🇺🇬, Ghana 🇬🇭, Cameroon 🇨🇲      │   │   │
│  │  │  Currencies: RWF, UGX, GHS, XAF                                │   │   │
│  │  │  API: MTN MoMo Collection API v2.0                             │   │   │
│  │  │  Docs: https://momodeveloper.mtn.com/api-documentation         │   │   │
│  │  │                                                                  │   │   │
│  │  │  Flow: OAuth2 Auth → Request to Pay → Webhook Callback          │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │ 🔴 AIRTEL MONEY                                                 │   │   │
│  │  │                                                                  │   │   │
│  │  │  [OFFICIAL AIRTEL LOGO]                                         │   │   │
│  │  │                                                                  │   │   │
│  │  │  Countries: Uganda 🇺🇬, Kenya 🇰🇪, Tanzania 🇹🇿, Rwanda 🇷🇼       │   │   │
│  │  │  Currencies: UGX, KES, TZS, RWF                                 │   │   │
│  │  │  API: Airtel Africa Payment API                                  │   │   │
│  │  │  Docs: https://developers.airtel.africa/documentation           │   │   │
│  │  │                                                                  │   │   │
│  │  │  Flow: OAuth2 Auth → CustomerPay → Transaction Status           │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │ 🟠 ORANGE MONEY                                                 │   │   │
│  │  │                                                                  │   │   │
│  │  │  [OFFICIAL ORANGE LOGO]                                         │   │   │
│  │  │                                                                  │   │   │
│  │  │  Countries: Senegal 🇸🇳, Cameroon 🇨🇲, Mali 🇲🇱, Ivory Coast 🇨🇮  │   │   │
│  │  │  Currencies: XOF, XAF                                           │   │   │
│  │  │  API: Orange Money Web Payment API                              │   │   │
│  │  │  Docs: https://developer.orange.com/apis/om-webpay             │   │   │
│  │  │                                                                  │   │   │
│  │  │  Flow: OAuth2 Auth → Payment Init → Webhook Callback            │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │ 🟢 MPESA (Safaricom)                                            │   │   │
│  │  │                                                                  │   │   │
│  │  │  [OFFICIAL SAFARICOM/MPESA LOGO]                                │   │   │
│  │  │                                                                  │   │   │
│  │  │  Countries: Kenya 🇰🇪, Tanzania 🇹🇿, Mozambique 🇲🇿, DRC 🇨🇩      │   │   │
│  │  │  Currencies: KES, TZS, MZN, CDF                                 │   │   │
│  │  │  API: Safaricom Daraja API                                       │   │   │
│  │  │  Docs: https://developer.safaricom.co.ke/APIs                                     │   │   │
│  │  │                                                                  │   │   │
│  │  │  Flow: OAuth2 Auth → STK Push (Lipa Na M-Pesa) → Callback       │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ALL LOGOS: Official brand assets, 200x200px minimum, no modifications         │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Provider Selection Flow (Web App)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PROVIDER SELECTION FLOW                                   │
│                                                                                  │
│  User clicks "Fund Card"                                                         │
│         │                                                                        │
│         ▼                                                                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                          │   │
│  │  SELECT YOUR MOBILE MONEY PROVIDER                                      │   │
│  │                                                                          │   │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                    │   │
│  │  │  🟡 MTN MoMo         │  │  🔴 Airtel Money     │                    │   │
│  │  │                      │  │                      │                    │   │
│  │  │  [MTN Official Logo] │  │  [Airtel Official    │                    │   │
│  │  │                      │  │   Logo]              │                    │   │
│  │  │  Rwanda, Uganda,     │  │  Uganda, Kenya,      │                    │   │
│  │  │  Ghana, Cameroon     │  │  Tanzania, Rwanda    │                    │   │
│  │  └──────────────────────┘  └──────────────────────┘                    │   │
│  │                                                                          │   │
│  │  ┌──────────────────────┐  ┌──────────────────────┐                    │   │
│  │  │  🟠 Orange Money     │  │  🟢 MPESA            │                    │   │
│  │  │                      │  │                      │                    │   │
│  │  │  [Orange Official    │  │  [Safaricom Official │                    │   │
│  │  │   Logo]              │  │   Logo]              │                    │   │
│  │  │  Senegal, Cameroon,  │  │  Kenya, Tanzania,    │                    │   │
│  │  │  Mali, Ivory Coast   │  │  Mozambique, DRC     │                    │   │
│  │  └──────────────────────┘  └──────────────────────┘                    │   │
│  │                                                                          │   │
│  │  💡 Providers shown based on your phone number country code             │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│         │                                                                        │
│         ▼                                                                        │
│  User selects provider → Enter phone → Enter amount → Confirm                   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Country → Provider Mapping

| Country | Currency | Primary Provider | Alternative |
|---------|----------|------------------|-------------|
| 🇷🇼 Rwanda | RWF | MTN MoMo 🟡 | Airtel Money 🔴 |
| 🇺🇬 Uganda | UGX | MTN MoMo 🟡 | Airtel Money 🔴 |
| 🇬🇭 Ghana | GHS | MTN MoMo 🟡 | — |
| 🇰🇪 Kenya | KES | MPESA 🟢 | Airtel Money 🔴 |
| 🇹🇿 Tanzania | TZS | MPESA 🟢 | Airtel Money 🔴 |
| 🇨🇲 Cameroon | XAF | MTN MoMo 🟡 | Orange Money 🟠 |
| 🇸🇳 Senegal | XOF | Orange Money 🟠 | — |
| 🇲🇱 Mali | XOF | Orange Money 🟠 | — |
| 🇨🇮 Ivory Coast | XOF | Orange Money 🟠 | — |
| 🇲🇿 Mozambique | MZN | MPESA 🟢 | — |
| 🇨🇩 DRC | CDF | MPESA 🟢 | — |

---

## 4. USSD Usage Guide (Feature Phones)

### How to Start

1. Pick up any feature phone (Nokia, Samsung, etc.)
2. Dial `*123#`
3. The Mobibit Africa menu appears
4. Reply with a number to select an option

### Complete USSD Menu Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    USSD MENU STRUCTURE                           │
│                                                                  │
│  *123# (Dial)                                                    │
│  │                                                               │
│  ├── 1. Check Balance ─────────────────────────────────────────>│\n│  │   └── Shows BTC, sats, USD equivalent                       │\n│  │                                                               │\n│  ├── 2. Send BTC ──────────────────────────────────────────────>│\n│  │   ├── Enter recipient phone (+256701234567)                  │\n│  │   ├── Enter amount (sats)                                    │\n│  │   ├── Confirm (1=Yes, 2=No)                                  │\n│  │   └── Success message                                        │\n│  │                                                               │\n│  ├── 3. Fund Account (Buy BTC) ───────────────────────────────>│\n│  │   ├── Enter amount in UGX                                    │\n│  │   ├── Shows conversion (UGX → sats)                          │\n│  │   ├── Confirm (1=Yes, 2=No)                                  │\n│  │   ├── MTN PIN prompt on phone                                │\n│  │   └── Success + SMS confirmation                             │\n│  │                                                               │\n│  ├── 4. Receive USD ──────────────────────────────────────────>│\n│  │   ├── Enter amount in USD                                    │\n│  │   ├── Confirm (1=Yes, 2=No)                                  │\n│  │   └── Invoice created                                        │\n│  │                                                               │\n│  ├── 5. Convert BTC <-> USD ──────────────────────────────────>│\n│  │   ├── Choose direction (1=BTC→USD, 2=USD→BTC)               │\n│  │   ├── Enter amount                                           │\n│  │   ├── Confirm (1=Yes, 2=No)                                  │\n│  │   └── Swap completed                                         │\n│  │                                                               │\n│  ├── 6. Help ─────────────────────────────────────────────────>│\n│  │   └── How it works + support info                            │\n│  │                                                               │\n│  └── 0 (at any screen) ──── Return to Main Menu                 │\n│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### USSD Flow 1: Check Balance

```
┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. Dial *123#                │
     │──────────────────────────────>│
     │                               │
     │  2. "MOBIBIT AFRICA           │
     │      Welcome! Select option:  │
     │      1. Check Balance         │
     │      2. Send BTC              │
     │      3. Fund Account          │
     │      4. Receive USD           │
     │      5. Convert BTC <-> USD   │
     │      6. Help"                 │
     │<──────────────────────────────│
     │                               │
     │  3. Reply "1"                 │
     │──────────────────────────────>│
     │                               │
     │  4. "BALANCE                  │
     │      BTC: 250,000 sats        │
     │      = 0.00250000 BTC         │
     │      = $98.75 USD             │
     │      USD Wallet: $0.00        │
     │      Reply 0 for main menu"   │
     │<──────────────────────────────│
     │                               │
     │  5. Reply "0"                 │
     │──────────────────────────────>│
     │                               │
     │  [Returns to Main Menu]       │
     │                               │
```

### USSD Flow 2: Send BTC

```
┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. Dial *123#                │
     │──────────────────────────────>│
     │                               │
     │  2. Main Menu                 │
     │<──────────────────────────────│
     │                               │
     │  3. Reply "2" (Send BTC)      │
     │──────────────────────────────>│
     │                               │
     │  4. "SEND BTC                 │
     │      Enter recipient's phone: │
     │      Example: +256701234567"  │
     │<──────────────────────────────│
     │                               │
     │  5. Reply "+256781234567"     │
     │──────────────────────────────>│
     │                               │
     │  6. "SEND BTC                 │
     │      Recipient: +256781234567 │
     │      Enter amount in sats:"   │
     │<──────────────────────────────│
     │                               │
     │  7. Reply "10000"             │
     │──────────────────────────────>│
     │                               │
     │  8. "SEND BTC - CONFIRM       │
     │      To: +256781234567        │
     │      Amount: 10,000 sats      │
     │      Fee: ~1 sat              │
     │      1. Confirm & Send        │
     │      2. Cancel"               │
     │<──────────────────────────────│
     │                               │
     │  9. Reply "1" (Confirm)       │
     │──────────────────────────────>│
     │                               │
     │  10. [System sends BTC        │
     │       via Lightning Network]  │
     │                               │
     │  11. "BTC SENT!               │
     │       To: +256781234567       │
     │       Amount: 10,000 sats     │
     │       Status: Confirmed       │
     │       Reply 0 for main menu"  │
     │<──────────────────────────────│
     │                               │
```

### USSD Flow 3: Fund Account (Buy BTC)

**Supported Providers:** MTN MoMo 🟡 | Airtel Money 🔴 | Orange Money 🟠 | MPESA 🟢

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │                    │ PROVIDER │
│          │                    │          │                    │(MTN/     │
│          │                    │          │                    │Airtel/   │
│          │                    │          │                    │Orange/   │
│          │                    │          │                    │MPESA)    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Dial *123#                │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │  2. Main Menu                 │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  3. Reply "3" (Fund Account)  │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │  4. "FUND ACCOUNT             │                               │
     │      Enter amount in UGX:     │                               │
     │      Min: 1,000 | Max: 500,000"                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  5. Reply "50000"             │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                               │  6. Get exchange rate         │
     │                               │  from CoinGecko               │
     │                               │──────────────┐                │
     │                               │<─────────────┘                │
     │                               │                               │
     │  7. "FUND ACCOUNT - CONFIRM   │                               │
     │      Amount: 50,000 UGX       │                               │
     │      You will receive:        │                               │
     │      1,351 sats               │                               │
     │      A payment prompt will    │                               │
     │      be sent to your phone.   │                               │
     │      1. Confirm               │                               │
     │      2. Cancel"               │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  8. Reply "1" (Confirm)       │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                               │  9. Call MTN MoMo API         │
     │                               │  (Request to Pay)             │
     │                               │──────────────────────────────>│
     │                               │                               │
     │                               │                               │ 10. Push PIN
     │                               │                               │ prompt to
     │                               │                               │ user's phone
     │  11. MTN PIN prompt           │                               │
     │  "Enter PIN to confirm        │                               │
     │   50,000 UGX payment"         │                               │
     │<──────────────────────────────────────────────────────────────│
     │                               │                               │
     │  12. User enters MTN PIN      │                               │
     │──────────────────────────────────────────────────────────────>│
     │                               │                               │
     │                               │  13. Webhook:                 │
     │                               │  payment SUCCESSFUL           │
     │                               │<──────────────────────────────│
     │                               │                               │
     │                               │  14. Credit wallet            │
     │                               │  balance += 1,351 sats        │
     │                               │──────┐                        │
     │                               │<─────┘                        │
     │                               │                               │
     │                               │  15. Send SMS                 │
     │                               │  "✅ 50,000 UGX received!     │
     │                               │  1,351 sats credited"         │
     │                               │                               │
     │  16. "FUND REQUEST SENT       │                               │
     │       Amount: 50,000 UGX      │                               │
     │       Reply 0 for main menu"  │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  17. SMS arrives on phone     │                               │
     │<──────────────────────────────────────────────────────────────│
     │                               │                               │
```

### USSD Flow 4: Receive USD

```
┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. Dial *123#                │
     │──────────────────────────────>│
     │                               │
     │  2. Main Menu                 │
     │<──────────────────────────────│
     │                               │
     │  3. Reply "4" (Receive USD)   │
     │──────────────────────────────>│
     │                               │
     │  4. "RECEIVE USD              │
     │      Enter amount in USD:     │
     │      $1 - $10,000"            │
     │<──────────────────────────────│
     │                               │
     │  5. Reply "50"                │
     │──────────────────────────────>│
     │                               │
     │  6. "RECEIVE USD - CONFIRM    │
     │      Amount: $50.00 USD       │
     │      A payment request will   │
     │      be sent.                 │
     │      1. Confirm               │
     │      2. Cancel"               │
     │<──────────────────────────────│
     │                               │
     │  7. Reply "1" (Confirm)       │
     │──────────────────────────────>│
     │                               │
     │  8. [System creates Lightning │
     │       invoice for $50]        │
     │                               │
     │  9. "USD PAYMENT REQUEST SENT │
     │      Amount: $50.00 USD       │
     │      A payment request has    │
     │      been created.            │
     │      Share the invoice with   │
     │      the sender.              │
     │      Reply 0 for main menu"   │
     │<──────────────────────────────│
     │                               │
```

### USSD Flow 5: Convert BTC ↔ USD

```
┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │
└────┬─────┘                    └────┬─────┘
     │                               │
     │  1. Dial *123#                │
     │──────────────────────────────>│
     │                               │
     │  2. Main Menu                 │
     │<──────────────────────────────│
     │                               │
     │  3. Reply "5" (Convert)       │
     │──────────────────────────────>│
     │                               │
     │  4. "CONVERT BTC <-> USD      │
     │      1. BTC -> USD            │
     │      2. USD -> BTC            │
     │      Reply 1 or 2:"           │
     │<──────────────────────────────│
     │                               │
     │  5. Reply "1" (BTC → USD)     │
     │──────────────────────────────>│
     │                               │
     │  6. "SWAP BTC -> USD          │
     │      Enter amount in sats:"   │
     │<──────────────────────────────│
     │                               │
     │  7. Reply "50000"             │
     │──────────────────────────────>│
     │                               │
     │  8. [System calculates        │
     │       50,000 sats → $12.50]   │
     │                               │
     │  9. "SWAP CONFIRM             │
     │      50,000 sats ->           │
     │      $12.50 USD               │
     │      1. Confirm Swap          │
     │      2. Cancel"               │
     │<──────────────────────────────│
     │                               │
     │  10. Reply "1" (Confirm)      │
     │──────────────────────────────>│
     │                               │
     │  11. [System updates wallet:  │
     │       BTC -50,000 sats        │
     │       USD +$12.50]            │
     │                               │
     │  12. "SWAP COMPLETED          │
     │       50000 BTC converted     │
     │       successfully.           │
     │       Reply 0 for main menu"  │
     │<──────────────────────────────│
     │                               │
```

### USSD Flow 6: Withdraw Bitcoin to Mobile Money (BTC → Fiat)

This flow converts Bitcoin back to local currency and sends it to the user's mobile money wallet.

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  SYSTEM  │                    │ LIGHTNING│                    │ MOBILE   │
│          │                    │          │                    │  NETWORK │                    │  MONEY   │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Dial *123#                │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Main Menu                 │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  3. Reply "7" (Withdraw BTC)  │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  4. "WITHDRAW BTC TO          │                               │                               │
     │      MOBILE MONEY             │                               │                               │
     │      Select provider:         │                               │                               │
     │      1. MTN MoMo              │                               │                               │
     │      2. Airtel Money          │                               │                               │
     │      3. Orange Money          │                               │                               │
     │      4. MPESA                 │                               │                               │
     │      Reply 1-4:"              │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  5. Reply "4" (MPESA)         │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  6. "WITHDRAW BTC TO MPESA    │                               │                               │
     │      Enter amount in sats:"   │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  7. Reply "50000"             │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  8. Get exchange rate         │                               │
     │                               │  BTC → USD → KES              │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │                               │  9. Calculate:                │                               │
     │                               │  50,000 sats = $12.50 USD     │
     │                               │  $12.50 = 1,625 KES           │
     │                               │  Fee: ~$0.25 (2%)             │
     │                               │  Net: 1,593 KES               │
     │                               │                               │
     │  10. "WITHDRAW CONFIRM        │                               │
     │       Amount: 50,000 sats     │                               │
     │       You will receive:       │                               │
     │       1,593 KES               │                               │
     │       Fee: 32 KES ($0.25)     │                               │
     │       To: MPESA +254712345678 │                               │
     │                               │                               │
     │       1. Confirm Withdraw     │                               │
     │       2. Cancel"              │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  11. Reply "1" (Confirm)      │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  12. Deduct from wallet       │                               │
     │                               │  balance -= 50,000 sats       │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │                               │  13. Sell BTC via exchange    │                               │
     │                               │  (BTC → USD → KES)            │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │                               │  14. Initiate mobile money    │                               │
     │                               │  disbursement to user         │                               │
     │                               │──────────────────────────────────────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │  15. MPESA sends              │
     │                               │                               │  1,593 KES to                 │
     │                               │                               │  +254712345678                │
     │                               │                               │                               │
     │                               │  16. Webhook:                 │                               │
     │                               │  Disbursement SUCCESSFUL      │                               │
     │                               │<──────────────────────────────────────────────────────────────│
     │                               │                               │                               │
     │                               │  17. Update transaction       │                               │
     │                               │  status → SETTLED             │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │  18. "WITHDRAWAL SUCCESSFUL   │                               │                               │
     │       50,000 sats withdrawn   │                               │                               │
     │       1,593 KES sent to       │                               │                               │
     │       MPESA +254712345678     │                               │                               │
     │       Reply 0 for main menu"  │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  19. SMS confirmation         │                               │                               │
     │<──────────────────────────────────────────────────────────────────────────────────────────────│
     │                               │                               │                               │
```

### Web App Flow: Withdraw Bitcoin to Mobile Money

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │                    │ MOBILE   │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│                    │  MONEY   │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Click "Withdraw"          │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Withdraw page loads       │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  3. Select provider:          │                               │                               │
     │  ┌─────────────────────────┐ │                               │                               │
     │  │ 🟡 MTN MoMo  [LOGO]    │ │                               │                               │
     │  │ 🔴 Airtel    [LOGO]    │ │                               │                               │
     │  │ 🟠 Orange     [LOGO]    │ │                               │                               │
     │  │ 🟢 MPESA      [LOGO]    │ │                               │                               │
     │  └─────────────────────────┘ │                               │                               │
     │  User selects: MPESA 🟢      │                               │                               │
     │  Enter phone: +254712345678  │                               │                               │
     │  Enter amount: 50,000 sats   │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │
     │                               │  4. Preview conversion        │                               │
     │                               │  50,000 sats → 1,593 KES     │
     │                               │  (after 2% fee)              │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │  5. Conversion preview shows  │                               │                               │
     │  ┌─────────────────────────┐ │                               │                               │
     │  │ Provider: MPESA 🟢      │ │                               │                               │
     │  │ Amount: 50,000 sats     │ │                               │                               │
     │  │ Fee: 1,000 sats (2%)    │ │                               │                               │
     │  │ You receive: 1,593 KES  │ │                               │                               │
     │  │ Phone: +254712345678    │ │                               │                               │
     │  └─────────────────────────┘ │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │
     │  6. Click "Withdraw"          │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │
     │                               │  7. POST /api/payments/withdraw│                               │
     │                               │  {sats, provider, phone}      │                               │
     │                               │──────────────────────────────>│                               │
     │                               │                               │
     │                               │                               │ 8. Check wallet balance       │
     │                               │                               │ >= 50,000 sats                │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 9. Deduct from wallet         │
     │                               │                               │ balance -= 50,000 sats        │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 10. Sell BTC via exchange     │
     │                               │                               │ (BTC → USD → KES)             │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 11. Initiate disbursement     │
     │                               │                               │ to MPESA                      │
     │                               │                               │──────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │                               │ 12. MPESA
     │                               │                               │                               │ sends KES
     │                               │                               │                               │ to phone
     │                               │                               │                               │
     │                               │                               │ 13. Webhook:                  │
     │                               │                               │ Disbursement SUCCESSFUL       │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │                               │ 14. Update transaction        │
     │                               │                               │ status → SETTLED              │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │  15. {success, kes_amount}    │                               │
     │                               │<──────────────────────────────│                               │
     │                               │                               │                               │
     │  16. Success!                 │                               │                               │
     │  "50,000 sats withdrawn      │                               │                               │
     │   1,593 KES sent to           │                               │                               │
     │   MPESA +254712345678"        │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
```

### Bitcoin → Fiat Conversion Chain

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        BITCOIN → FIAT CONVERSION                                 │
│                                                                                  │
│  When a user withdraws 50,000 sats to MPESA (Kenya):                            │
│                                                                                  │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐       │
│  │    Sats    │     │    BTC     │     │    USD     │     │    KES     │       │
│  │  50,000    │────>│ 0.000500   │────>│   $39.50   │────>│  5,135     │       │
│  │  sats      │     │ BTC        │     │            │     │  KES       │       │
│  └────────────┘     └────────────┘     └────────────┘     └────────────┘       │
│       │                  │                  │                  │                │
│       │    ÷ 100,000,000 │    × 79,000      │    × 130         │                │
│       │                  │                  │                  │                │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  FEE BREAKDOWN:                                                        │   │
│  │  - Network fee: ~1 sat ($0.00008)                                      │   │
│  │  - Exchange spread: ~0.5% ($0.20)                                      │   │
│  │  - Platform fee: ~1.5% ($0.59)                                         │   │
│  │  - Mobile money fee: ~$0.10                                             │   │
│  │  - Total fee: ~$0.89 (2.25%)                                           │   │
│  │  - User receives: 5,102 KES (net)                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Withdrawal Data Journey

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        WITHDRAWAL DATA JOURNEY                                   │
│                                                                                  │
│  When a user withdraws 50,000 sats to MPESA:                                    │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  1. USER INPUT                                                         │   │
│  │     Amount: 50,000 sats                                                │   │
│  │     Provider: MPESA                                                    │   │
│  │     Phone: +254712345678                                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  2. BACKEND PROCESSING                                                  │   │
│  │     - Verify user has sufficient balance (>= 50,000 sats)              │   │
│  │     - Generate reference: WD-A1B2C3D4E5F6                              │   │
│  │     - Fetch exchange rate: 1 BTC = $79,000 USD                         │   │
│  │     - Calculate USD: 50,000 / 100,000,000 × 79,000 = $39.50           │   │
│  │     - Calculate KES: $39.50 × 130 = 5,135 KES                         │   │
│  │     - Deduct fees: 5,135 × 0.02 = 103 KES fee                         │   │
│  │     - Net amount: 5,032 KES                                            │   │
│  │     - Reserve sats in wallet (hold)                                     │   │
│  │     - Create transaction record in database                            │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  3. SELL BTC                                                           │   │
│  │     - Convert sats to USD via exchange                                  │   │
│  │     - USD held in platform's exchange account                           │   │
│  │     - Record BTC sale transaction                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  4. MOBILE MONEY DISBURSEMENT                                          │   │
│  │     - Call MPESA Disbursement API                                       │   │
│  │     - Send 5,032 KES to +254712345678                                  │   │
│  │     - MPESA processes and delivers funds                                │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  5. CONFIRMATION                                                        │   │
│  │     - MPESA webhook confirms delivery                                   │   │
│  │     - Update transaction status: SETTLED                                │   │
│  │     - Deduct sats from wallet (finalize)                                │   │
│  │     - Send SMS: "✅ 50,000 sats withdrawn! 5,032 KES sent to MPESA"     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Web App Usage Guide (Smartphones)

### How to Start

1. Open a web browser (Chrome, Safari, Firefox)
2. Go to `mobibitafrica.com`
3. Sign up or log in
4. Access your dashboard

### Onboarding Experience (Account Creation)

When a new user creates an account, they see the official mobile money provider logos to build trust:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ONBOARDING - ACCOUNT CREATION                             │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                          │   │
│  │                    MOBIBIT AFRICA                                        │   │
│  │                    Bitcoin for Everyone                                  │   │
│  │                                                                          │   │
│  │                    ┌─────────────────────┐                              │   │
│  │                    │  MOBIBIT AFRICA     │                              │   │
│  │                    │  Official Logo      │                              │   │
│  │                    │  (200x200px)        │                              │   │
│  │                    └─────────────────────┘                              │   │
│  │                                                                          │   │
│  │  CREATE YOUR ACCOUNT                                                     │   │
│  │                                                                          │   │
│  │  Full Name:  [________________]                                        │   │
│  │  Email:      [________________]                                        │   │
│  │  Phone:      [________________]  (+256...)                             │   │
│  │  Password:   [________________]                                        │   │
│  │  Confirm:    [________________]                                        │   │
│  │                                                                          │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │   │
│  │  │                    FUND YOUR ACCOUNT WITH                        │   │   │
│  │  │                                                                  │   │   │
│  │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │   │   │
│  │  │  │ 🟡 MTN   │  │ 🔴 Airtel│  │ 🟠 Orange│  │ 🟢 MPESA │       │   │   │
│  │  │  │  MoMo    │  │  Money   │  │  Money   │  │          │       │   │   │
│  │  │  │          │  │          │  │          │  │          │       │   │   │
│  │  │  │ [LOGO]   │  │ [LOGO]   │  │ [LOGO]   │  │ [LOGO]   │       │   │   │
│  │  │  │ Official │  │ Official │  │ Official │  │ Official │       │   │   │
│  │  │  │ MTN      │  │ Airtel   │  │ Orange   │  │ Safaricom│       │   │   │
│  │  │  │ Brand    │  │ Brand    │  │ Brand    │  │ Brand    │       │   │   │
│  │  │  │ Logo     │  │ Logo     │  │ Logo     │  │ Logo     │       │   │   │
│  │  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │   │   │
│  │  │                                                                  │   │   │
│  │  │  All logos are official brand assets displayed at 200x200px    │   │   │
│  │  │  minimum resolution for trust and recognition.                 │   │   │
│  │  └─────────────────────────────────────────────────────────────────┘   │   │
│  │                                                                          │   │
│  │  ┌──────────────────────────────┐                                      │   │
│  │  │         Sign Up              │                                      │   │
│  │  └──────────────────────────────┘                                      │   │
│  │                                                                          │   │
│  │  Already have an account? Login                                          │   │
│  │                                                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  IMPORTANT: Official provider logos are shown during onboarding to:            │
│  1. Build user trust - recognizable brands = safe platform                    │
│  2. Guide provider selection - users see their provider's logo                 │
│  3. Ensure brand compliance - official logos only, no modifications            │
│  4. Local relevance - users see providers available in their country           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Provider Logo Display Rules

| Provider | Logo Source | Display Size | Location |
|----------|-------------|--------------|----------|
| MTN MoMo | Official MTN Brand Assets | 200x200px min | Onboarding, Fund page, USSD menu |
| Airtel Money | Official Airtel Africa Brand | 200x200px min | Onboarding, Fund page, USSD menu |
| Orange Money | Official Orange Brand | 200x200px min | Onboarding, Fund page, USSD menu |
| MPESA | Official Safaricom Brand | 200x200px min | Onboarding, Fund page, USSD menu |

> All logos must be sourced from official brand guidelines. No modifications, stretching, or color changes allowed.

### Complete Web App Navigation

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEB APP NAVIGATION                            │
│                                                                  │
│  PUBLIC PAGES:                                                   │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  / (Landing)  →  /login  →  /signup                     │    │
│  └─────────────────────────────────────────────────────────┘    │
│                          │                                       │
│                          ▼                                       │
│  AUTHENTICATED PAGES:                                            │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │  /dashboard ────────────────────────────────────────┐   │    │
│  │       │                                             │   │    │
│  │       ├── /card (Virtual Card)                      │   │    │
│  │       │     └── View card, balance, freeze          │   │    │
│  │       │                                             │   │    │
│  │       ├── /fund (Fund Card)                         │   │    │
│  │       │     └── Select provider → Enter amount →    │   │    │
│  │       │         Confirm → Payment prompt → Done     │   │    │
│  │       │                                             │   │    │
│  │       ├── /send (Send Bitcoin)                      │   │    │
│  │       │     └── Enter invoice → Amount → Confirm →  │   │    │
│  │       │         BTC sent via Lightning              │   │    │
│  │       │                                             │   │    │
│  │       ├── /receive (Receive Bitcoin)                │   │    │
│  │       │     └── Enter amount → Generate invoice →   │   │    │
│  │       │         Copy/share invoice → Wait for       │   │    │
│  │       │         payment → BTC credited              │   │    │
│  │       │                                             │   │    │
│  │       ├── /spend (Spend with Card)                  │   │    │
│  │       │     └── Enter merchant → Amount → Confirm → │   │    │
│  │       │         Card charged → BTC deducted         │   │    │
│  │       │                                             │   │    │
│  │       ├── /transactions (History)                   │   │    │
│  │       │     └── View all transactions, filter       │   │    │
│  │       │                                             │   │    │
│  │       ├── /profile (User Profile)                   │   │    │
│  │       │     └── Edit info, KYC status, security     │   │    │
│  │       │                                             │   │    │
│  │       ├── /settings (Settings)                      │   │    │
│  │       │     └── Notifications, limits, preferences  │   │    │
│  │       │                                             │   │    │
│  │       └── /help (Help & Support)                    │   │    │
│  │             └── FAQs, contact, documentation        │   │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Web App Flow 1: Sign Up

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│
└────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │
     │  1. Visit mobibitafrica.com   │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │  2. Landing page loads        │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  3. Click "Get Started"       │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │  4. Signup form appears       │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
     │  5. Fill form:                │                               │
     │  - Name: John Doe             │                               │
     │  - Email: john@email.com      │                               │
     │  - Phone: +256701234567       │                               │
     │  - Password: ****             │                               │
     │──────────────────────────────>│                               │
     │                               │                               │
     │                               │  6. POST /api/auth/register   │
     │                               │  {phone, pin, name, email}    │
     │                               │──────────────────────────────>│
     │                               │                               │
     │                               │                               │ 7. Create
     │                               │                               │ user +
     │                               │                               │ wallet
     │                               │                               │──────┐
     │                               │                               │<─────┘
     │                               │                               │
     │                               │                               │ 8. Generate
     │                               │                               │ JWT tokens
     │                               │                               │──────┐
     │                               │                               │<─────┘
     │                               │                               │
     │                               │  9. {user, tokens}            │
     │                               │<──────────────────────────────│
     │                               │                               │
     │                               │  10. Store tokens in          │
     │                               │      localStorage             │
     │                               │──────┐                        │
     │                               │<─────┘                        │
     │                               │                               │
     │  11. Redirect to /dashboard   │                               │
     │<──────────────────────────────│                               │
     │                               │                               │
```

### Web App Flow 2: Fund Card (Mobile Money → BTC)

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │                    │ MTN MOMO │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│                    │   API    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Click "Fund Card"         │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Fund page loads           │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
│  3. Select provider:          │                               │                               │
│  ┌─────────────────────────┐ │                               │                               │
│  │ 🟡 MTN MoMo  [LOGO]    │ │                               │                               │
│  │ 🔴 Airtel    [LOGO]    │ │                               │                               │
│  │ 🟠 Orange     [LOGO]    │ │                               │                               │
│  │ 🟢 MPESA      [LOGO]    │ │                               │                               │
│  └─────────────────────────┘ │                               │                               │
│  User selects: MPESA 🟢      │                               │                               │
│  Enter phone: +254712345678  │                               │                               │
│  Enter amount: 5,000 KES     │                               │                               │
│──────────────────────────────>│                               │                               │
│                               │                               │                               │
│                               │  4. Preview conversion        │                               │
│                               │  5,000 KES → 384 sats         │                               │
│                               │  (1 USD = 130 KES)           │                               │
│                               │──────┐                        │                               │
│                               │<─────┘                        │                               │
│                               │                               │                               │
│  5. Conversion preview shows  │                               │                               │
│  ┌─────────────────────────┐ │                               │                               │
│  │ Provider: MPESA 🟢      │ │                               │                               │
│  │ Amount: 5,000 KES       │ │                               │                               │
│  │ You receive: 384 sats   │ │                               │                               │
│  │ Fee: ~$0.10             │ │                               │                               │
│  └─────────────────────────┘ │                               │                               │
│<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  6. Click "Fund Card"         │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  7. POST /api/payments/collect│                               │
     │                               │  {phone, amount, provider}    │                               │
     │                               │──────────────────────────────>│                               │
     │                               │                               │                               │
     │                               │                               │ 8. Get exchange rate          │
     │                               │                               │ from CoinGecko                │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 9. Create transaction         │
     │                               │                               │ record in DB                  │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 10. Call MTN MoMo API         │
     │                               │                               │ (Request to Pay)              │
     │                               │                               │──────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │                               │ 11. Push
     │                               │                               │                               │ PIN prompt
     │                               │                               │                               │ to phone
     │  12. "Payment prompt sent     │                               │                               │
     │       to your phone"          │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  13. MTN PIN prompt on phone  │                               │                               │
     │<──────────────────────────────────────────────────────────────────────────────────────────────│
     │                               │                               │                               │
     │  14. User enters PIN          │                               │                               │
     │──────────────────────────────────────────────────────────────────────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │ 15. Webhook:                  │
     │                               │                               │ payment SUCCESSFUL            │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │                               │ 16. Update transaction        │
     │                               │                               │ status → SETTLED              │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 17. Credit wallet             │
     │                               │                               │ balance += 1,351 sats         │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 18. Send SMS                  │
     │                               │                               │ confirmation                  │
     │                               │                               │                               │
     │  19. Success! Balance updated │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
```

### Web App Flow 3: Send Bitcoin via Lightning

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │                    │  LND     │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│                    │  NODE    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Click "Send Bitcoin"      │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Send page loads           │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  3. Enter Lightning invoice:  │                               │                               │
     │  lnbc10000000000000...        │                               │                               │
     │  Amount: 50,000 sats          │                               │                               │
     │  Memo: "Payment"              │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  4. Validate invoice format   │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │  5. Shows USD equivalent:     │                               │                               │
     │  ≈ $12.50                     │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  6. Click "Send Bitcoin"      │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  7. POST /api/payments/send   │                               │
     │                               │  {invoice, amount, memo}      │                               │
     │                               │──────────────────────────────>│                               │
     │                               │                               │                               │
     │                               │                               │ 8. Validate JWT               │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 9. Check wallet balance       │
     │                               │                               │ >= 50,000 sats                │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 10. Reserve sats              │
     │                               │                               │ (hold in pending)             │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 11. LND: Pay Invoice          │
     │                               │                               │──────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │                               │ 12. Route
     │                               │                               │                               │ payment
     │                               │                               │                               │ through
     │                               │                               │                               │ channels
     │                               │                               │                               │
     │                               │                               │ 13. Payment SUCCESS           │
     │                               │                               │ + preimage                    │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │                               │ 14. Deduct from wallet        │
     │                               │                               │ + record TX                   │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │  15. {success, tx_hash, fee}  │                               │
     │                               │<──────────────────────────────│                               │
     │                               │                               │                               │
     │  16. Success!                 │                               │                               │
     │  "50,000 sats sent!           │                               │                               │
     │   Fee: 1 sat"                 │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
```

### Web App Flow 4: Receive Bitcoin

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │                    │  LND     │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│                    │  NODE    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Click "Receive Bitcoin"   │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Receive page loads        │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  3. Enter amount:             │                               │                               │
     │  100,000 sats                 │                               │                               │
     │  Description: "Payment"       │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  4. POST /api/wallet/invoice  │                               │
     │                               │  {amount_sats, memo}          │                               │
     │                               │──────────────────────────────>│                               │
     │                               │                               │                               │
     │                               │                               │ 5. LND: Create Invoice        │
     │                               │                               │──────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │                               │ 6. Generate
     │                               │                               │                               │ BOLT11
     │                               │                               │                               │ invoice
     │                               │                               │                               │
     │                               │                               │ 7. Invoice + payment hash     │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │  8. {invoice, qr_code}        │                               │
     │                               │<──────────────────────────────│                               │
     │                               │                               │                               │
     │  9. Shows invoice + QR code   │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  10. Shares invoice with      │                               │                               │
     │      sender                   │                               │                               │
     │                               │                               │                               │
     │  ... time passes ...          │                               │                               │
     │                               │                               │                               │
     │                               │                               │ 11. Webhook:                  │
     │                               │                               │ Payment received              │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │                               │ 12. Credit wallet             │
     │                               │                               │ +100,000 sats                 │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │  13. Balance updated!         │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
```

### Web App Flow 5: Spend with Virtual Card

```
┌──────────┐                    ┌──────────┐                    ┌──────────┐                    ┌──────────┐
│  USER    │                    │  WEB APP │                    │ BACKEND  │                    │  CARD    │
│ BROWSER  │                    │ (React)  │                    │ (FastAPI)│                    │   API    │
└────┬─────┘                    └────┬─────┘                    └────┬─────┘                    └────┬─────┘
     │                               │                               │                               │
     │  1. Click "Spend"             │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │  2. Spend page loads          │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  3. Enter:                    │                               │                               │
     │  Merchant: "Kampala Cafe"     │                               │                               │
     │  Amount: $5.00 USD            │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  4. Convert USD → sats        │                               │
     │                               │  $5.00 → 12,500 sats          │                               │
     │                               │──────┐                        │                               │
     │                               │<─────┘                        │                               │
     │                               │                               │                               │
     │  5. Shows: "$5.00 = 12,500    │                               │                               │
     │     sats"                     │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
     │  6. Click "Spend"             │                               │                               │
     │──────────────────────────────>│                               │                               │
     │                               │                               │                               │
     │                               │  7. POST /api/payments/spend  │                               │
     │                               │  {merchant, amount_usd}       │                               │
     │                               │──────────────────────────────>│                               │
     │                               │                               │                               │
     │                               │                               │ 8. Check wallet balance       │
     │                               │                               │ >= 12,500 sats                │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 9. Deduct from wallet         │
     │                               │                               │ balance -= 12,500 sats        │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │                               │ 10. Charge virtual card       │
     │                               │                               │──────────────────────────────>│
     │                               │                               │                               │
     │                               │                               │                               │ 11. Card
     │                               │                               │                               │ authorized
     │                               │                               │                               │
     │                               │                               │ 12. Card auth response        │
     │                               │                               │<──────────────────────────────│
     │                               │                               │                               │
     │                               │                               │ 13. Record transaction        │
     │                               │                               │──────┐                        │
     │                               │                               │<─────┘                        │
     │                               │                               │                               │
     │                               │  14. {success, tx_id}         │                               │
     │                               │<──────────────────────────────│                               │
     │                               │                               │                               │
     │  15. Success!                 │                               │                               │
     │  "Spent $5.00 at Kampala Cafe │                               │                               │
     │   12,500 sats deducted"       │                               │                               │
     │<──────────────────────────────│                               │                               │
     │                               │                               │                               │
```

---

## 5. Complete Data Flow Diagrams

### 5.1 End-to-End Data Flow: Mobile Money → Bitcoin → Spending

This is the complete journey of money through the system:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        COMPLETE DATA FLOW                                        │
│                                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ STEP 1   │    │ STEP 2   │    │ STEP 3   │    │ STEP 4   │    │ STEP 5   │ │
│  │          │    │          │    │          │    │          │    │          │ │
│  │ DEPOSIT  │───>│ CONVERT  │───>│ STORE    │───>│ SEND     │───>│ SPEND    │ │
│  │          │    │          │    │          │    │          │    │          │ │
│  │ User     │    │ Backend  │    │ Wallet   │    │ Lightning│    │ Virtual  │ │
│  │ sends    │    │ converts │    │ holds    │    │ Network  │    │ Card     │ │
│  │ mobile   │    │ fiat to  │    │ BTC in   │    │ routes   │    │ charges  │ │
│  │ money    │    │ sats     │    │ sats     │    │ payment  │    │ merchant │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │               │               │               │               │         │
│       ▼               ▼               ▼               ▼               ▼         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ 50,000   │    │ 1,351    │    │ 1,351    │    │ -10,000  │    │ -2,500   │ │
│  │ UGX      │───>│ sats     │───>│ sats in  │───>│ sats     │───>│ sats     │ │
│  │ (fiat)   │    │ (BTC)    │    │ wallet   │    │ sent     │    │ spent    │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                                  │
│  Each step involves different external services:                                │
│  Step 1: MTN/Airtel/Orange API                                                  │
│  Step 2: CoinGecko exchange rate API                                            │
│  Step 3: PostgreSQL database                                                    │
│  Step 4: LND Lightning node                                                     │
│  Step 5: Visa/card issuing API                                                  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Currency Conversion Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        CURRENCY CONVERSION FLOW                                  │
│                                                                                  │
│  When a user deposits 50,000 UGX:                                               │
│                                                                                  │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐       │
│  │  UGX       │     │    USD     │     │    BTC     │     │    Sats    │       │
│  │  50,000    │────>│   $13.51   │────>│ 0.000171   │────>│  1,351     │       │
│  │            │     │            │     │ BTC        │     │  sats      │       │
│  └────────────┘     └────────────┘     └────────────┘     └────────────┘       │
│       │                  │                  │                  │                │
│       │     ÷ 3,700      │    ÷ 79,000      │    × 100,000,000  │                │
│       │     (UGX/USD)    │    (USD/BTC)     │    (BTC/sats)    │                │
│       │                  │                  │                  │                │
│       │     CoinGecko    │    CoinGecko     │    Fixed         │                │
│       │     provides     │    provides      │    conversion    │                │
│       │     rate         │    rate          │                  │                │
│                                                                                  │
│  Reverse (spending 2,500 sats):                                                 │
│                                                                                  │
│  ┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐       │
│  │    Sats    │     │    BTC     │     │    USD     │     │   UGX      │       │
│  │  2,500     │────>│ 0.000025   │────>│   $1.98    │────>│  7,315     │       │
│  │  sats      │     │ BTC        │     │            │     │  UGX       │       │
│  └────────────┘     └────────────┘     └────────────┘     └────────────┘       │
│       │                  │                  │                  │                │
│       │    ÷ 100,000,000 │    × 79,000      │    × 3,700       │                │
│       │                  │                  │                  │                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.3 Lightning Network Payment Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        LIGHTNING NETWORK PAYMENT FLOW                            │
│                                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│  │  SENDER  │     │  LND     │     │ ROUTING  │     │ RECEIVER │              │
│  │  (User)  │     │  NODE    │     │  NODES   │     │ (Merchant│              │
│  │          │     │          │     │          │     │  /User)  │              │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘              │
│       │                │                │                │                     │
│       │  1. Create     │                │                │                     │
│       │  Payment       │                │                │                     │
│       │───────────────>│                │                │                     │
│       │                │                │                │                     │
│       │                │  2. Find route │                │                     │
│       │                │  to receiver   │                │                     │
│       │                │───────────────>│                │                     │
│       │                │                │                │                     │
│       │                │  3. Route      │                │                     │
│       │                │  confirmed     │                │                     │
│       │                │<───────────────│                │                     │
│       │                │                │                │                     │
│       │                │  4. Forward    │                │                     │
│       │                │  payment       │                │                     │
│       │                │───────────────────────────────>│                     │
│       │                │                │                │                     │
│       │                │                │  5. Payment   │                     │
│       │                │                │  received     │                     │
│       │                │                │<───────────────│                     │
│       │                │                │                │                     │
│       │                │  6. Preimage   │                │                     │
│       │                │  (proof)       │                │                     │
│       │                │<───────────────────────────────│                     │
│       │                │                │                │                     │
│       │  7. Payment    │                │                │                     │
│       │  CONFIRMED     │                │                │                     │
│       │<───────────────│                │                │                     │
│       │                │                │                │                     │
│                                                                                  │
│  Total time: < 1 second                                                          │
│  Total fee: ~1 sat (less than $0.001)                                           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.4 Webhook Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        WEBHOOK PROCESSING FLOW                                   │
│                                                                                  │
│  When MTN confirms a payment, they send a webhook to our system:                │
│                                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│  │  MTN     │     │  WEBHOOK │     │  BUSINESS│     │DATABASE  │              │
│  │  API     │     │  HANDLER │     │  LOGIC   │     │          │              │
│  │          │     │          │     │          │     │          │              │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘              │
│       │                │                │                │                     │
│       │  1. POST       │                │                │                     │
│       │  /webhooks/mtn │                │                │                     │
│       │  {externalId,  │                │                │                     │
│       │   status:      │                │                │                     │
│       │   SUCCESSFUL,  │                │                │                     │
│       │   amount:      │                │                │                     │
│       │   "50000"}     │                │                │                     │
│       │───────────────>│                │                │                     │
│       │                │                │                │                     │
│       │                │  2. Parse      │                │                     │
│       │                │  payload       │                │                     │
│       │                │──────┐         │                │                     │
│       │                │<─────┘         │                │                     │
│       │                │                │                │                     │
│       │                │  3. Find       │                │                     │
│       │                │  transaction   │                │                     │
│       │                │  by reference  │                │                     │
│       │                │───────────────────────────────>│                     │
│       │                │                │                │                     │
│       │                │  4. Transaction│                │                     │
│       │                │  found         │                │                     │
│       │                │<───────────────────────────────│                     │
│       │                │                │                │                     │
│       │                │  5. Update     │                │                     │
│       │                │  status:       │                │                     │
│       │                │  PENDING →     │                │                     │
│       │                │  SETTLED       │                │                     │
│       │                │───────────────────────────────>│                     │
│       │                │                │                │                     │
│       │                │  6. Credit     │                │                     │
│       │                │  wallet:       │                │                     │
│       │                │  +1,351 sats   │                │                     │
│       │                │───────────────────────────────>│                     │
│       │                │                │                │                     │
│       │                │  7. Send SMS   │                │                     │
│       │                │  confirmation  │                │                     │
│       │                │──────┐         │                │                     │
│       │                │<─────┘         │                │                     │
│       │                │                │                │                     │
│       │  8. 200 OK     │                │                │                     │
│       │<───────────────│                │                │                     │
│       │                │                │                │                     │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Authentication Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION FLOW                                       │
│                                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐              │
│  │  USER    │     │  WEB APP │     │  BACKEND │     │DATABASE  │              │
│  │          │     │          │     │          │     │          │              │
│  └────┬─────┘     └────┬─────┘     └────┬─────┘     └────┬─────┘              │
│       │                │                │                │                     │
│       │  1. Login      │                │                │                     │
│       │  phone + PIN   │                │                │                     │
│       │───────────────>│                │                │                     │
│       │                │                │                │                     │
│       │                │  2. POST       │                │                     │
│       │                │  /api/auth/    │                │                     │
│       │                │  login         │                │                     │
│       │                │───────────────>│                │                     │
│       │                │                │                │                     │
│       │                │                │  3. Find user  │                     │
│       │                │                │  by phone      │                     │
│       │                │                │───────────────>│                     │
│       │                │                │                │                     │
│       │                │                │  4. User found │                     │
│       │                │                │<───────────────│                     │
│       │                │                │                │                     │
│       │                │                │  5. Verify PIN │                     │
│       │                │                │  (SHA-256)     │                     │
│       │                │                │──────┐         │                     │
│       │                │                │<─────┘         │                     │
│       │                │                │                │                     │
│       │                │                │  6. Generate   │                     │
│       │                │                │  JWT tokens    │                     │
│       │                │                │  (access +     │                     │
│       │                │                │   refresh)     │                     │
│       │                │                │──────┐         │                     │
│       │                │                │<─────┘         │                     │
│       │                │                │                │                     │
│       │                │  7. {user,     │                │                     │
│       │                │    tokens}     │                │                     │
│       │                │<───────────────│                │                     │
│       │                │                │                │                     │
│       │                │  8. Store in   │                │                     │
│       │                │  localStorage  │                │                     │
│       │                │──────┐         │                │                     │
│       │                │<─────┘         │                │                     │
│       │                │                │                │                     │
│       │  9. Dashboard  │                │                │                     │
│       │  loads         │                │                │                     │
│       │<───────────────│                │                │                     │
│       │                │                │                │                     │
│       │  10. API call  │                │                │                     │
│       │  + Bearer JWT  │                │                │                     │
│       │───────────────>│                │                │                     │
│       │                │                │                │                     │
│       │                │  11. Validate  │                │                     │
│       │                │  JWT signature │                │                     │
│       │                │──────┐         │                │                     │
│       │                │<─────┘         │                │                     │
│       │                │                │                │                     │
│       │                │  12. Extract   │                │                     │
│       │                │  user ID       │                │                     │
│       │                │───────────────>│                │                     │
│       │                │                │                │                     │
│       │  13. Response  │                │                │                     │
│       │<───────────────│                │                │                     │
│       │                │                │                │                     │
│                                                                                  │
│  JWT Token Structure:                                                            │
│  {                                                                              │
│    "sub": "user-uuid-here",                                                     │
│    "phone": "+256701234567",                                                    │
│    "type": "access",                                                            │
│    "exp": 1724812800,                                                           │
│    "iat": 1724809200                                                            │
│  }                                                                              │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Transaction Lifecycle

### Transaction States

Every transaction in Mobibit Africa goes through these states:

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

### State Transitions by Transaction Type

| Transaction Type | Start | Normal Flow | Error Flow |
|-----------------|-------|-------------|------------|
| **Fund (Buy BTC)** | INITIATED → PENDING → SETTLED | MTN prompt sent → User approves → Wallet credited | MTN prompt failed → FAILED |
| **Send BTC** | INITIATED → PROCESSING → SETTLED | LND pays invoice → Preimage received → Wallet deducted | LND payment failed → FAILED, wallet unreserved |
| **Receive BTC** | INITIATED → PENDING → SETTLED | Invoice created → Sender pays → Wallet credited | Invoice expired → FAILED |
| **Spend (Card)** | INITIATED → PROCESSING → SETTLED | Card charged → Merchant paid → Wallet deducted | Card declined → FAILED, wallet unreserved |
| **Swap (BTC↔USD)** | INITIATED → SETTLED | Rate locked → Balances updated | Rate unavailable → FAILED |

### Transaction Data Journey

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        TRANSACTION DATA JOURNEY                                  │
│                                                                                  │
│  When a user funds their account with 50,000 UGX via MTN:                       │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  1. USER INPUT                                                         │   │
│  │     Phone: +256701234567                                               │   │
│  │     Amount: 50,000 UGX                                                 │   │
│  │     Provider: MTN MoMo                                                 │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  2. BACKEND PROCESSING                                                  │   │
│  │     - Generate reference: SC-A1B2C3D4E5F6                              │   │
│  │     - Fetch exchange rate: 1 USD = 3,700 UGX                           │   │
│  │     - Fetch BTC price: $79,000                                         │   │
│  │     - Calculate sats: 50,000 / 3,700 × 100,000,000 / 79,000 = 1,351   │   │
│  │     - Create transaction record in database                            │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  3. PROVIDER CALL                                                       │   │
│  │     MTN MoMo API: Request to Pay                                        │   │
│  │     - Amount: 50,000 UGX                                               │   │
│  │     - Payer: +256701234567                                             │   │
│  │     - Reference: SC-A1B2C3D4E5F6                                       │   │
│  │     - Callback URL: https://mobibitafrica.com/api/webhooks/mtn         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  4. USER ACTION                                                         │   │
│  │     - Receives PIN prompt on phone                                      │   │
│  │     - Enters MTN PIN                                                    │   │
│  │     - Payment approved                                                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  5. WEBHOOK CONFIRMATION                                                │   │
│  │     MTN sends POST to our webhook:                                      │   │
│  │     {                                                                   │   │
│  │       "externalId": "SC-A1B2C3D4E5F6",                                 │   │
│  │       "status": "SUCCESSFUL",                                          │   │
│  │       "amount": "50000",                                               │   │
│  │       "currency": "UGX",                                               │   │
│  │       "financialTransactionId": "MTN-TX-123456"                        │   │
│  │     }                                                                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  6. WALLET UPDATE                                                       │   │
│  │     - Find transaction by reference                                     │   │
│  │     - Update status: PENDING → SETTLED                                  │   │
│  │     - Credit wallet: balance_sats += 1,351                             │   │
│  │     - Record settled_at timestamp                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                      │                                          │
│                                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  7. NOTIFICATION                                                        │   │
│  │     SMS sent to +256701234567:                                          │   │
│  │     "✅ Mobibit Africa: 50,000 UGX received!                            │   │
│  │      Balance credited: 1,351 sats                                       │   │
│  │      Ref: SC-A1B2C3D4E5F6"                                             │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Error Handling & Edge Cases

### What Happens When Things Go Wrong

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ERROR HANDLING FLOWS                                       │
│                                                                                  │
│  SCENARIO 1: User enters wrong MTN PIN                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  MTN API returns: {"status": "FAILED", "reason": "Wrong PIN"}          │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Update transaction status → FAILED                                  │   │
│  │  2. Do NOT deduct from wallet                                           │   │
│  │  3. Send SMS: "❌ Payment failed. Wrong PIN. Try again."                │   │
│  │  4. User can retry from main menu                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  SCENARIO 2: User has insufficient balance                                      │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  User tries to send 50,000 sats but only has 25,000 sats               │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Check wallet balance before processing                              │   │
│  │  2. Return error: "Insufficient balance. You have 25,000 sats."        │   │
│  │  3. Do NOT create transaction                                           │   │
│  │  4. Suggest: "Top up your account first."                               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  SCENARIO 3: Lightning network timeout                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LND payment takes too long (> 30 seconds)                             │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Transaction stays in PROCESSING state                               │   │
│  │  2. Background worker checks status every 5 seconds                     │   │
│  │  3. If still pending after 60s → mark as FAILED                         │   │
│  │  4. Unreserve sats in wallet                                            │   │
│  │  5. Send SMS: "⚠️ Payment timed out. Funds returned."                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  SCENARIO 4: Exchange rate unavailable                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  CoinGecko API is down or returning errors                             │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Use last cached rate (valid for 30 seconds)                         │   │
│  │  2. If cache is empty → use fallback rate                               │   │
│  │  3. Log warning: "Exchange rate fetch failed, using fallback"           │   │
│  │  4. Continue with transaction                                           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  SCENARIO 5: Session timeout (USSD)                                             │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  User dials *123# but doesn't respond for 3 minutes                    │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Session expires after 180 seconds                                   │   │
│  │  2. USSD session marked as ended                                        │   │
│  │  3. Any incomplete transaction remains in INITIATED state               │   │
│  │  4. User must start over by dialing *123# again                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  SCENARIO 6: Webhook not received                                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  MTN sends webhook but our server is down                              │   │
│  │                                                                          │   │
│  │  System action:                                                         │   │
│  │  1. Transaction stays in PENDING state                                  │   │
│  │  2. Background job polls MTN API every 30 seconds                       │   │
│  │  3. If MTN confirms → update transaction + credit wallet                │   │
│  │  4. If still pending after 1 hour → flag for manual review              │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Error Response Format

All API errors follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "INSUFFICIENT_BALANCE",
  "metadata": {
    "current_balance": 25000,
    "requested_amount": 50000
  }
}
```

---

## 8. Security & Authentication

### Authentication Methods

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AUTHENTICATION METHODS                                     │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  USSD (Feature Phones)                                                  │   │
│  │                                                                          │   │
│  │  Method: Phone Number + 4-Digit PIN                                     │   │
│  │                                                                          │   │
│  │  Flow:                                                                  │   │
│  │  1. User dials *123#                                                    │   │
│  │  2. System identifies user by phone number                              │   │
│  │  3. For sensitive operations, asks for PIN                              │   │
│  │  4. PIN verified against SHA-256 hash in database                       │   │
│  │                                                                          │   │
│  │  Security:                                                              │   │
│  │  - PIN is never stored in plain text                                    │   │
│  │  - PIN hashed with salt using SHA-256                                   │   │
│  │  - Session expires after 3 minutes                                      │   │
│  │  - Max 3 PIN attempts per session                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  Web App (Smartphones)                                                  │   │
│  │                                                                          │   │
│  │  Method: Phone Number + Password + JWT Tokens                           │   │
│  │                                                                          │   │
│  │  Flow:                                                                  │   │
│  │  1. User enters phone + password on login page                          │   │
│  │  2. Backend verifies credentials                                        │   │
│  │  3. Returns access token (1 hour) + refresh token (30 days)             │   │
│  │  4. Frontend stores tokens in localStorage                              │   │
│  │  5. Every API call includes: Authorization: Bearer <token>              │   │
│  │                                                                          │   │
│  │  Security:                                                              │   │
│  │  - Password hashed with SHA-256 + salt                                  │   │
│  │  - JWT signed with HMAC-SHA256                                          │   │
│  │  - Access token expires in 1 hour                                       │   │
│  │  - Refresh token expires in 30 days                                     │   │
│  │  - Tokens invalidated on logout                                         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Security Layers

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        SECURITY LAYERS                                           │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 1: Transport Security                                            │   │
│  │                                                                          │   │
│  │  - All API calls use HTTPS (TLS 1.3)                                   │   │
│  │  - USSD goes through Africa's Talking encrypted gateway                 │   │
│  │  - Webhooks verify provider signatures                                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 2: Authentication                                                │   │
│  │                                                                          │   │
│  │  - Phone number is the unique identifier                                │   │
│  │  - PIN/password hashed with SHA-256 + salt                              │   │
│  │  - JWT tokens for session management                                    │   │
│  │  - Tokens expire automatically                                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 3: Authorization                                                 │   │
│  │                                                                          │   │
│  │  - Users can only access their own wallet                               │   │
│  │  - API endpoints validate user ID from JWT                              │   │
│  │  - Cross-user access blocked at database level                          │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 4: Input Validation                                              │   │
│  │                                                                          │   │
│  │  - Phone numbers validated (E.164 format)                               │   │
│  │  - Amounts validated (min/max limits)                                   │   │
│  │  - Lightning invoices validated (BOLT11 format)                         │   │
│  │  - SQL injection prevented (parameterized queries)                      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │  LAYER 5: Transaction Limits                                            │   │
│  │                                                                          │   │
│  │  - Daily limit: $500 USD (configurable)                                │   │
│  │  - Monthly limit: $5,000 USD (configurable)                            │   │
│  │  - Per-transaction limits enforced                                      │   │
│  │  - KYC tiers unlock higher limits                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

### How Mobibit Africa Works in 30 Seconds

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                  │
│  1. USER PICKS UP PHONE                                                         │
│     └── Dials *123# (USSD) or visits mobibitafrica.com (Web)                   │
│                                                                                  │
│  2. USER SELECTS "FUND ACCOUNT"                                                 │
│     └── Enters amount in local currency (e.g., 50,000 UGX)                     │
│                                                                                  │
│  3. USER ENTERS MTN PIN                                                         │
│     └── Payment prompt appears on phone, user enters PIN                        │
│                                                                                  │
│  4. SYSTEM CONVERTS TO BITCOIN                                                  │
│     └── 50,000 UGX → $13.51 USD → 1,351 sats (via CoinGecko rate)             │
│                                                                                  │
│  5. BITCOIN CREDITED TO WALLET                                                  │
│     └── Wallet balance: 0 → 1,351 sats                                         │
│                                                                                  │
│  6. USER CAN NOW:                                                               │
│     ├── Send BTC to anyone via Lightning (< 1 second, ~1 sat fee)              │
│     ├── Receive BTC from anyone worldwide                                       │
│     ├── Spend BTC using virtual Visa card                                       │
│     └── Swap between BTC and USD                                                │
│                                                                                  │
│  TOTAL TIME: ~30 seconds from mobile money to Bitcoin                          │
│  TOTAL FEES: ~2% on conversion + ~1 sat on Lightning                           │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

**Document Version:** 1.0
**Last Updated:** August 28, 2026
**Status:** ✅ Complete
