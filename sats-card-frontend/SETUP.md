# Sats Card — Setup Guide

## Quick Start (5 minutes)

### 1. Get MTN MoMo Sandbox Credentials

1. Go to **https://momodeveloper.mtn.co.rw** (Rwanda) or **https://momodeveloper.mtn.com** (Uganda)
2. Click **Sign Up** → enter email + password → verify email
3. On the dashboard, find **API Products** → click **Subscribe** on **Collections**
4. Go to **Profile** page → copy your **Primary Key** (this is your subscription key)

### 2. Create Sandbox API User

Run this in your terminal (replace `YOUR_SUBSCRIPTION_KEY`):

```bash
# Generate a UUID for your API user
API_USER_UUID=$(python -c "import uuid; print(uuid.uuid4())")
echo "Your API User UUID: $API_USER_UUID"

# Create the API user on sandbox
curl -X POST "https://sandbox.momodeveloper.mtn.co.rw/v1_0/apiuser" \
  -H "X-Reference-Id: $API_USER_UUID" \
  -H "X-Target-Environment: sandbox" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{"providerCallbackHost": "https://yourdomain.com"}'
```

### 3. Generate API Key

```bash
# Generate API key for your user
curl -X POST "https://sandbox.momodeveloper.mtn.co.rw/v1_0/apiuser/$API_USER_UUID/apikey" \
  -H "X-Target-Environment: sandbox" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY"
```

Save the `apiKey` from the response.

### 4. Configure Environment

```bash
cd backend
cp .env.example .env
```

Edit `.env` with your credentials:

```env
MTN_MOMO_API_USER=your-uuid-from-step-2
MTN_MOMO_API_KEY=your-api-key-from-step-3
MTN_MOMO_SUBSCRIPTION_KEY=your-primary-key-from-step-1
MTN_MOMO_ENVIRONMENT=sandbox
MTN_MOMO_COUNTRY=rw
SECRET_KEY=any-random-string-here
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/satscard
```

### 5. Start Everything

```bash
# Start database (if using Docker)
docker run -d --name satscard-pg -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=satscard postgres:16-alpine

# Start backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Start frontend (new terminal)
npm install
npm run dev
```

### 6. Test the Flow

Open **http://localhost:5174** → Login → Fund Card → Enter amount → Select MTN → Confirm

In sandbox mode, payments are auto-approved — no real money moves.

---

## What Happens in Sandbox

| Step | Real Production | Sandbox |
|------|----------------|---------|
| User enters PIN | Real USSD prompt | Auto-approved |
| Money deducted | Real UGX | Simulated |
| Callback sent | Real webhook | Simulated |
| BTC credited | Real Lightning | Simulated |

---

## Testing with curl

```bash
# 1. Get access token
TOKEN=$(curl -s -X POST "https://sandbox.momodeveloper.mtn.co.rw/collection/token/" \
  -H "Authorization: Basic $(echo -n 'YOUR_API_USER:YOUR_API_KEY' | base64)" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY" | python -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token: $TOKEN"

# 2. Send Request to Pay
TXN_ID=$(python -c "import uuid; print(uuid.uuid4())")

curl -X POST "https://sandbox.momodeveloper.mtn.co.rw/collection/v1_0/requesttopay/$TXN_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Reference-Id: $TXN_ID" \
  -H "X-Target-Environment: sandbox" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "1000",
    "currency": "RWF",
    "externalId": "SC-TEST001",
    "payer": {
      "partyIdType": "MSISDN",
      "partyId": "250771234567"
    },
    "payerMessage": "Pay for Sats Card",
    "payeeNote": "Top-up"
  }'

# 3. Check status
curl -X GET "https://sandbox.momodeveloper.mtn.co.rw/collection/v1_0/requesttopay/$TXN_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Target-Environment: sandbox" \
  -H "Ocp-Apim-Subscription-Key: YOUR_SUBSCRIPTION_KEY"
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong subscription key or API key | Check your keys in Profile page |
| `404 Not Found` | Wrong API URL | Make sure you're using sandbox URL |
| `400 Bad Request` | Missing required field | Check request body format |
| `Reference already exists` | UUID reuse | Generate a new UUID for each request |
