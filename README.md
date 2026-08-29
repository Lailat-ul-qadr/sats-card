<div align="center">

<img src="src/assets/mobi-bit-africa-logo.jpeg" alt="Mobi Bit Africa Logo" width="300" />

<br />

# 🔐 MOBI BIT AFRICA

### ⚡ Secure Bitcoin Access for Africa ⚡

<br />

*"Banking the unbanked, one sat at a time."*

<br />

![License: MIT](https://img.shields.io/badge/License-MIT-4CAF50?style=for-the-badge)
![Security](https://img.shields.io/badge/Security-End--to--End-FF5722?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Bitcoin](https://img.shields.io/badge/Bitcoin-Lightning-FF9900?style=for-the-badge&logo=bitcoin&logoColor=white)

<br />

[The Problem](#-the-problem) ·
[Our Solution](#-our-solution) ·
[Security](#-security-features) ·
[Architecture](#-architecture) ·
[Quick Start](#-quick-start) ·
[API](#-api)

</div>

---

## 🌍 The Problem

<div align="center">

Africa faces **five critical barriers** to Bitcoin adoption and financial freedom:

</div>

<br />

<table>
<tr>
<td width="50" align="center" valign="top"><h1>1️⃣</h1></td>
<td>

### 🔒 Limited Access to Bitcoin
Many Africans cannot easily access Bitcoin because traditional platforms require bank accounts, complicated verification, or technical knowledge. **Mobi Bit Africa** makes access simpler through familiar mobile-money systems.

</td>
</tr>
<tr>
<td width="50" align="center" valign="top"><h1>2️⃣</h1></td>
<td>

### 🏦 Limited Financial Inclusion
Millions of people rely on mobile money rather than traditional banks. Our solution connects people to Bitcoin and digital financial services **without making a traditional bank account the starting point**.

</td>
</tr>
<tr>
<td width="50" align="center" valign="top"><h1>3️⃣</h1></td>
<td>

### 💸 High Cost of Sending Money
Sending money, especially across borders, can be expensive and slow. By using the **Lightning Network**, our solution enables faster and lower-cost digital payments.

</td>
</tr>
<tr>
<td width="50" align="center" valign="top"><h1>4️⃣</h1></td>
<td>

### 💳 Difficulty Using Bitcoin in Everyday Life
Owning Bitcoin is not the same as being able to use it. Mobi Bit Africa connects Bitcoin to a spending experience through a **wallet and virtual-card concept**.

</td>
</tr>
<tr>
<td width="50" align="center" valign="top"><h1>5️⃣</h1></td>
<td>

### ⚙️ Complexity of Cryptocurrency Technology
Bitcoin and Lightning can be difficult for ordinary users to understand. Our solution **hides the technical complexity** and creates a simple experience similar to the mobile-money services Africans already know.

</td>
</tr>
</table>

---

## ✅ Our Solution

<div align="center">

> **Mobi Bit Africa is solving five major problems:** limited access to Bitcoin, financial exclusion, expensive money transfers, difficulty spending Bitcoin, and the complexity of cryptocurrency technology.
>
> **Our goal is to make Bitcoin as simple and accessible as mobile money.**

</div>

<br />

<table>
<tr>
<td align="center" width="25%">

### 💰 Deposit
Fund your card via **MTN MoMo**, **Airtel Money**, or **Orange Money**

</td>
<td align="center" width="8%">

### ➡️

</td>
<td align="center" width="25%">

### ⚡ Convert
Fiat is converted to **BTC** via the Lightning Network

</td>
<td align="center" width="8%">

### ➡️

</td>
<td align="center" width="25%">

### 💳 Spend
Use your **virtual card** anywhere cards are accepted

</td>
</tr>
</table>

---

## 🛡️ Security Features

<div align="center">

| Feature | Implementation |
|:-------:|----------------|
| 🔐 **Encrypted Auth** | JWT tokens with secure httpOnly cookies |
| 🛡️ **Input Validation** | Server-side validation on all endpoints |
| 🔒 **SQL Injection Protection** | SQLAlchemy ORM with parameterized queries |
| 🚫 **Rate Limiting** | API rate limiting to prevent abuse |
| 🔑 **API Key Security** | Environment variables — never committed to code |
| 🌐 **CORS Protection** | Restricted cross-origin resource sharing |
| 📝 **Audit Logging** | Transaction history and payment tracking |
| 💳 **Secure Payments** | Sandbox mode for safe testing, production encryption |

</div>

---

## 🏗️ Architecture

<div align="center">

```
┌─────────────────────────────────────────────────────────────┐
│                    MOBI BIT AFRICA                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Frontend   │───▶│   Backend   │───▶│  Lightning   │     │
│  │  React 18    │    │  FastAPI    │    │    LND       │     │
│  │  Vite 5      │    │  Python     │    │  Network     │     │
│  │  Tailwind    │    │  SQLAlchemy │    │              │     │
│  └─────────────┘    └──────┬──────┘    └─────────────┘     │
│                            │                                │
│         ┌──────────────────┼──────────────────┐             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Database   │    │  Mobile     │    │  External   │     │
│  │  PostgreSQL  │    │  Money APIs │    │  Services   │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

</div>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:-----:|-----------|---------|
| **Frontend** | React 18 · Vite 5 · Tailwind CSS v4 · Framer Motion | User interface and animations |
| **Backend** | Python 3.11+ · FastAPI · SQLAlchemy · Alembic | API and business logic |
| **Database** | PostgreSQL 16 (SQLite for dev) | Data persistence |
| **Lightning** | LND via Docker (Polar Network) | Bitcoin payments |
| **Mobile Money** | Africa's Talking · MTN MoMo · Airtel · Orange | Fiat on-ramp |
| **Security** | JWT · CORS · Rate Limiting · Parameterized Queries | Protection |
| **Deploy** | Docker · Render | Production hosting |

</div>

---

## 📁 Project Structure

```
mobi-bit-africa/
│
├── src/                          # 🔒 Frontend (React)
│   ├── pages/                    # 13 page components
│   ├── components/               # Reusable UI components
│   ├── services/                 # API abstraction layer
│   ├── context/                  # Auth · Wallet · Theme
│   ├── hooks/                    # Custom React hooks
│   ├── utils/                    # Helpers
│   └── assets/                   # Images · logos
│
├── backend/                      # 🔐 Backend (FastAPI)
│   └── app/
│       ├── api/                  # Route handlers
│       ├── core/                 # Config · database
│       ├── models/               # SQLAlchemy models
│       ├── services/             # Business logic
│       ├── adapters/             # MTN · Airtel · Orange · Lightning
│       └── ussd/                 # USSD flow handler
│
├── docker-compose.yml
├── render.yaml
├── LICENSE
└── README.md
```

---

## 🚀 Quick Start

**Prerequisites:** Node.js v18+ · Python 3.11+ · Docker

```bash
# Clone
git clone https://github.com/Lailat-ul-qadr/mobi-bit-africa.git
cd mobi-bit-africa

# Install
npm install
cd backend && pip install -r requirements.txt && cd ..

# Run
docker-compose up -d postgres redis   # database
cd backend && uvicorn app.main:app --reload --port 8000   # API
npm run dev                            # frontend
```

Open **http://localhost:5174** → Login with `demo@satscardapp.com` / `demo@123456`

---

## 📡 API

| Endpoint | Method | Description |
|----------|:------:|-------------|
| `/api/node_info` | `GET` | Lightning node info |
| `/api/balance` | `GET` | Wallet balance |
| `/api/card_balance` | `GET` | Card balance |
| `/api/create_invoice` | `POST` | Create Lightning invoice |
| `/api/check_payment/{id}` | `GET` | Check payment status |
| `/api/deposit/{id}` | `POST` | Deposit to card |
| `/api/card_payment` | `POST` | Pay from card |
| `/api/transactions` | `GET` | Transaction history |

---

## 📱 Mobile Money Integration

<div align="center">

| Provider | Countries | Mode |
|:--------:|-----------|:----:|
| 🟡 **MTN MoMo** | Rwanda · Uganda · Ghana · DRC | Sandbox ✅ |
| 🔴 **Airtel Money** | Rwanda · Kenya · Uganda | Sandbox ✅ |
| 🟠 **Orange Money** | Senegal · Mali · Côte d'Ivoire | Sandbox ✅ |

</div>

> All providers support sandbox mode — no real money moves during testing. See [SETUP.md](SETUP.md) for configuration.

---

## 📋 Changelog

| Version | Date | Changes |
|:-------:|:----:|---------|
| **1.0.0** | Aug 2026 | Initial release — 13 pages, Lightning integration, mobile money adapters |
| **0.9.0** | Aug 2026 | Backend API with FastAPI, Alembic migrations, Polar Network setup |
| **0.8.0** | Aug 2026 | Frontend foundation — React, Tailwind, design system, service layer |

---

## 🙏 Acknowledgments

- **[Bitcoin Lightning Network](https://lightning.network/)** — Enabling instant, low-cost Bitcoin payments
- **[Polar](https://polar.sh/)** — Local Lightning Network development environment
- **[Africa's Talking](https://africastalking.com/)** — Mobile money and USSD API infrastructure
- **[MTN MoMo Developer Portal](https://momodeveloper.mtn.com/)** — Mobile money sandbox and APIs
- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern Python web framework
- **[React](https://react.dev/)** — UI library powering the frontend
- **[Tailwind CSS](https://tailwindcss.com/)** — Utility-first CSS framework

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

### Built with ❤️ by **Mobi Bit Africa**

*Bridging mobile money and Bitcoin across Africa*

<br />

[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)

</div>
