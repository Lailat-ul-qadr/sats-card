# Sats Card Frontend — Lightning-Powered Bitcoin Card MVP

A **complete, production-grade frontend** for a Bitcoin/Lightning hackathon MVP built in **2 days**. 

**Status:** ✅ DEMO-READY — All 13 pages functional, animated, responsive, with full mock data integration.

---

## 🎯 Project Overview

**Sats Card** solves the problem of Bitcoin adoption in emerging markets:

- **Input:** Mobile money (MTN, Airtel, Orange Money)
- **Process:** Convert fiat to BTC via Lightning Network
- **Output:** Virtual card loaded with sats, ready to spend

This frontend provides a complete user experience for:
- Account creation and login
- Wallet management and balance viewing
- Funding via simulated mobile money
- Sending/receiving Bitcoin via Lightning
- Virtual card spending
- Transaction history tracking
- User profile and settings management

---

## 🚀 Quick Start

### Prerequisites
- Node.js v18+ with npm
- Modern browser (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# Enter the project directory
cd sats-card-frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The app will be available at **http://localhost:5174**

### Demo Credentials
```
Email: demo@satscardapp.com
Password: demo@123456
(Or use any email/password combination)
```

### Production Build

```bash
npm run build
npm run preview
```

---

## 📁 Project Structure

```
src/
├── pages/              # All 13 page components
│   ├── Landing.jsx     # Public landing page
│   ├── Login.jsx       # Authentication
│   ├── Signup.jsx      # Account creation
│   ├── Dashboard.jsx   # Main hub
│   ├── Card.jsx        # Virtual card
│   ├── Fund.jsx        # Mobile money input
│   ├── Send.jsx        # Lightning payments
│   ├── Receive.jsx     # Invoice generation
│   ├── Spend.jsx       # Card spending
│   ├── Transactions.jsx# History
│   ├── Profile.jsx     # User info
│   ├── Settings.jsx    # Preferences
│   └── Help.jsx        # FAQs
│
├── components/         # Reusable UI components
├── services/           # Mock API layer
├── context/            # State management (Auth, Wallet)
├── hooks/              # Custom React hooks
├── data/               # Mock data objects
├── types/              # JSDoc type definitions
├── utils/              # Helper functions
├── App.jsx             # Main routing
└── styles.css          # Global styles
```

---

## ✨ All 13 Pages

### Public Pages
- ✅ **Landing** — Project overview, features, CTA
- ✅ **Login** — Authentication form
- ✅ **Signup** — Account creation

### Authenticated Pages
- ✅ **Dashboard** — Wallet overview, quick actions
- ✅ **Card** — Virtual card display
- ✅ **Fund** — Mobile money conversion
- ✅ **Send** — Lightning payments
- ✅ **Receive** — Invoice generation
- ✅ **Spend** — Card transactions
- ✅ **Transactions** — Complete history with filtering
- ✅ **Profile** — User information, editable
- ✅ **Settings** — Preferences and limits
- ✅ **Help** — FAQs with search

---

## 🎨 Design Features

### Colors & Typography
- **Primary Color:** Muted Green (#6B7F6B)
- **Headings:** Merriweather (serif)
- **Body:** Rubik (sans-serif)
- **Palette:** Cream, clay, gold, organic fintech aesthetic

### Components
- Button (4 variants)
- Input (with validation)
- Card, Badge, Modal
- Alert (4 types)
- Loading, EmptyState, Skeleton

### Animations
- Smooth page transitions
- Framer Motion throughout
- Button hover effects
- Card animations
- Loading spinners

---

## 💰 Features

### Authentication
- [x] Signup with validation
- [x] Login with persistence
- [x] Logout
- [x] Auth guards on protected routes

### Wallet
- [x] Balance display (sats, BTC, USD)
- [x] Virtual card
- [x] Real-time conversions

### Funding
- [x] Mobile money selection (MTN, Airtel, Orange)
- [x] USD → Sats conversion
- [x] Daily limit validation

### Payments
- [x] Send Bitcoin via Lightning
- [x] Receive Bitcoin via Lightning
- [x] Invoice generation
- [x] Transaction tracking

### Spending
- [x] Virtual card spending
- [x] Merchant tracking
- [x] USD ↔ Sats conversion

### Transaction History
- [x] Complete history
- [x] Filtering by type
- [x] Timestamps and status
- [x] Summary statistics

### User Account
- [x] Profile management
- [x] Editable information
- [x] KYC status
- [x] Security settings

### Settings
- [x] Notification preferences
- [x] Transaction limits
- [x] Currency selection
- [x] Language preferences

### Help
- [x] FAQ search
- [x] Category filtering
- [x] Contact form
- [x] Documentation links

---

## 🔐 Authentication Flow

### Routes
```
Public:
  /              (Landing)
  /login         (Login form)
  /signup        (Signup form)

Protected:
  /dashboard     (Main hub)
  /card          (Virtual card)
  /fund          (Fund card)
  /send          (Send Bitcoin)
  /receive       (Receive Bitcoin)
  /spend         (Spend)
  /transactions  (History)
  /profile       (User profile)
  /settings      (Settings)
  /help          (Help)
```

---

## 🛠️ Tech Stack

- **React 18** — UI framework
- **Vite 5** — Ultra-fast build tool
- **React Router 6** — Client-side routing
- **Tailwind CSS v4** — Utility-first styling
- **Framer Motion 11** — Smooth animations
- **Lucide React** — Icon library

---

## 🔗 Service Layer (Ready for Backend)

All API calls go through services in `src/services/index.js`:

```javascript
// Wallet
walletService.getBalance()
walletService.getCardInfo()
walletService.addFunds(amount, currency)

// Transactions
transactionService.getTransactions()
transactionService.createTransaction(tx)

// Payments
paymentService.fundCard(phone, amount, provider)
paymentService.sendBitcoin(address, amount, memo)
paymentService.receiveBitcoin(amount, description)
paymentService.spendCard(merchant, amount, cardLast4)

// Auth
authService.login(email, password)
authService.signup(email, password, phone)
authService.logout()

// User
userService.getProfile()
userService.updateProfile(updates)

// Exchange Rates
exchangeRateService.getExchangeRate(from, to)
exchangeRateService.convertCurrency(amount, from, to)
```

**For Backend Integration:**
1. Replace mock implementations with API calls
2. Update endpoint URLs
3. No component changes needed

---

## 🎬 Complete Demo Flow

1. **Sign Up** → Create account with validation
2. **Login** → Authenticate with credentials
3. **Dashboard** → View balance and recent transactions
4. **View Card** → Beautiful virtual card display
5. **Fund Card** → Select mobile money provider, enter amount
6. **Send Bitcoin** → Input Lightning address, send sats
7. **Receive Bitcoin** → Generate Lightning invoice, copy
8. **Spend** → Simulate card transaction
9. **Transactions** → View and filter transaction history
10. **Profile** → Edit user information
11. **Settings** → Adjust preferences and limits
12. **Help** → Search FAQs and documentation

**All flows are fully functional with mock data simulation.**

---

## 📊 Build Status

✅ **Production Build Successful**
```
vite v5.4.21 building for production...
✓ 461 modules transformed.
✓ built in 5.09s
```

✅ **Dev Server Running**
```
http://localhost:5174
```

---

## 🚀 Development

### Start Dev Server
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Preview Build
```bash
npm run preview
```

---

## 📱 Responsive Design

✅ Mobile (320px+)  
✅ Tablet (768px+)  
✅ Desktop (1024px+)  

All pages tested and optimized for all screen sizes.

---

## 🎯 What's Next?

### Backend Integration
- Connect to Bitcoin Core
- Connect to Lightning Network (LND/CLN)
- Implement actual mobile money APIs
- Create real authentication backend
- Set up database (PostgreSQL)

### Production Features
- Real payment processing
- Actual card issuing
- KYC/AML compliance
- Transaction settlement
- Real-time balance updates

---

## 📝 Key Features

✅ Complete 13-page application  
✅ Full design system with components  
✅ State management (Auth, Wallet, Theme)  
✅ Custom hooks for common patterns  
✅ Service layer for API abstraction  
✅ Real-time currency conversions  
✅ Transaction tracking and history  
✅ Responsive mobile-first design  
✅ Smooth animations throughout  
✅ Form validation on all inputs  
✅ Error handling with user feedback  
✅ Production-ready code structure  

---

## 🎓 Learning

- **React:** https://react.dev
- **Vite:** https://vitejs.dev
- **Tailwind CSS:** https://tailwindcss.com
- **Framer Motion:** https://www.framer.com/motion
- **React Router:** https://reactrouter.com

---

## 📞 Support

See the **Help** page in the app for FAQs and documentation.

---

**Built for Hackathon MVP. Demo-ready. Production-quality. 🚀**
