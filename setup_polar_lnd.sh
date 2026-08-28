#!/bin/bash

# ============================================
# MOBIBIT AFRICA - POLAR LND SETUP SCRIPT
# ============================================
#
# This script helps you set up a local Lightning Network
# for testing Bitcoin send/receive flows.
#
# Prerequisites:
# - Docker installed and running
# - Polar installed (https://github.com/jamaljsr/polar/releases)
#
# Usage:
#   chmod +x setup_polar_lnd.sh
#   ./setup_polar_lnd.sh
#

set -e

echo "⚡ Mobibit Africa - Polar LND Setup"
echo "===================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "${BLUE}Checking Docker...${NC}"
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running!${NC}"
    echo ""
    echo "Please start Docker:"
    echo "  - Windows/Mac: Open Docker Desktop"
    echo "  - Linux: sudo systemctl start docker"
    echo ""
    exit 1
fi
echo -e "${GREEN}✅ Docker is running${NC}"

# Check if Polar is installed
echo ""
echo -e "${BLUE}Checking Polar...${NC}"
if ! command -v polar &> /dev/null; then
    echo -e "${YELLOW}⚠️  Polar not found in PATH${NC}"
    echo ""
    echo "Please install Polar from:"
    echo "  https://github.com/jamaljsr/polar/releases"
    echo ""
    echo "After installing, you can still use this script."
    echo ""
fi

# Create .env file for backend
echo ""
echo -e "${BLUE}Creating backend .env file...${NC}"

BACKEND_ENV="backend/.env"
if [ ! -f "$BACKEND_ENV" ]; then
    cat > "$BACKEND_ENV" << 'EOF'
# Mobibit Africa Backend Configuration
# Polar LND Testnet Setup

# App
APP_NAME=Mobibit Africa API
APP_VERSION=0.1.0
DEBUG=true
SECRET_KEY=mobibit-test-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database (SQLite for dev)
DATABASE_URL=sqlite+aiosqlite:///./mobibit.db

# ── LND Configuration (Polar Regtest) ─────────────────────────────
# IMPORTANT: Update LND_MACAROON_HEX with your actual macaroon!
LND_HOST=localhost
LND_REST_PORT=8081
LND_MACAROON_HEX=REPLACE_WITH_YOUR_MACAROON_HEX
LND_TLS_CERT_PATH=
LND_NETWORK=regtest

# ── Exchange Rate ───────────────────────────────────────────────
BTC_PRICE_FEED_URL=https://api.coingecko.com/api/v3/simple/price
PRICE_CACHE_TTL_SECONDS=30

# ── SMS Gateway (Mock for testing) ──────────────────────────────
SMS_PROVIDER=africastalking
SMS_API_KEY=
SMS_SENDER_ID=MOBIBIT

# ── USSD ────────────────────────────────────────────────────────
USSD_SESSION_TIMEOUT_SECONDS=180
USSD_SHORT_CODE=*123#
EOF
    echo -e "${GREEN}✅ Created backend/.env${NC}"
else
    echo -e "${YELLOW}⚠️  backend/.env already exists, skipping${NC}"
fi

# Create .env file for frontend
echo ""
echo -e "${BLUE}Creating frontend .env file...${NC}"

FRONTEND_ENV=".env"
if [ ! -f "$FRONTEND_ENV" ]; then
    cat > "$FRONTEND_ENV" << 'EOF'
# Mobibit Africa Frontend Configuration
# Polar LND Testnet Setup

VITE_USE_REAL_API=true
VITE_API_URL=http://localhost:8000/api
EOF
    echo -e "${GREEN}✅ Created frontend .env${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend .env already exists, skipping${NC}"
fi

# Print instructions
echo ""
echo -e "${GREEN}====================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}====================================${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo "1. Open Polar app"
echo "   - Download from: https://github.com/jamaljsr/polar/releases"
echo "   - Or open if already installed"
echo ""
echo "2. Create a new network"
echo "   - Click 'Create New Network'"
echo "   - Name: 'Mobibit Africa Testnet'"
echo "   - Implementation: LND"
echo "   - Number of nodes: 2"
echo "   - Bitcoin node: Bitcoin Core"
echo "   - Click 'Create'"
echo ""
echo "3. Wait for network to start (2-5 minutes)"
echo ""
echo "4. Get LND credentials"
echo "   - Click on LND1 node"
echo "   - Click 'Show' next to Macaroon"
echo "   - Copy the hex string"
echo ""
echo "5. Update backend/.env"
echo "   - Replace REPLACE_WITH_YOUR_MACAROON_HEX with the copied hex"
echo ""
echo "6. Start the backend"
echo "   cd backend"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "7. Start the frontend"
echo "   npm run dev"
echo ""
echo "8. Fund LND node"
echo "   - In Polar, click LND1 → Deposit"
echo "   - Deposit 1 BTC"
echo "   - Click 'Mine Blocks' → Mine 6 blocks"
echo ""
echo "9. Test the flow"
echo "   - Open http://localhost:5174"
echo "   - Sign up / Login"
echo "   - Go to Receive page"
echo "   - Generate invoice"
echo "   - Pay from LND2 in Polar"
echo ""
echo -e "${BLUE}Documentation:${NC}"
echo "   - POLAR_LND_SETUP_GUIDE.md"
echo "   - MOBIBIT_AFRICA_SYSTEM_USAGE.md"
echo ""
echo -e "${GREEN}Happy testing! ⚡${NC}"
