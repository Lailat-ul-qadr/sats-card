"""
MTN MoMo Sandbox Setup Script
Run this to create your API User and API Key.

Usage:
  1. Get your subscription key from https://momodeveloper.mtn.co.rw (Profile page)
  2. Replace YOUR_SUBSCRIPTION_KEY below
  3. Run: python backend/setup_mtn.py
"""

import requests
import json
import uuid

# ═══════════════════════════════════════════════════════════════════════
#  REPLACE THIS WITH YOUR SUBSCRIPTION KEY FROM THE DEVELOPER PORTAL
# ═══════════════════════════════════════════════════════════════════════
SUBSCRIPTION_KEY = "YOUR_SUBSCRIPTION_KEY_HERE"
# ═══════════════════════════════════════════════════════════════════════

# Sandbox base URL
BASE_URL = "https://sandbox.momodeveloper.mtn.com"

def create_api_user():
    """Step 1: Create an API User (UUID)"""
    api_user = str(uuid.uuid4())
    
    url = f"{BASE_URL}/v1_0/apiuser"
    headers = {
        "X-Reference-Id": api_user,
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "providerCallbackHost": "webhook.site"
    }
    
    print(f"Creating API User: {api_user}")
    resp = requests.post(url, json=body, headers=headers)
    print(f"  Status: {resp.status_code}")
    
    if resp.status_code == 201:
        print("  ✅ API User created successfully!")
    else:
        print(f"  ❌ Failed: {resp.text}")
        return None
    
    return api_user

def create_api_key(api_user):
    """Step 2: Generate an API Key for the user"""
    url = f"{BASE_URL}/v1_0/apiuser/{api_user}/apikey"
    headers = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"\nGenerating API Key for: {api_user}")
    resp = requests.post(url, headers=headers)
    print(f"  Status: {resp.status_code}")
    
    if resp.status_code == 201:
        json_resp = json.loads(resp.text)
        api_key = json_resp.get("apiKey", "")
        print(f"  ✅ API Key: {api_key}")
        return api_key
    else:
        print(f"  ❌ Failed: {resp.text}")
        return None

def test_token(api_user, api_key):
    """Step 3: Test getting an access token"""
    import base64
    
    url = f"{BASE_URL}/collection/token/"
    
    # Basic auth: base64(api_user:api_key)
    credentials = base64.b64encode(f"{api_user}:{api_key}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY
    }
    
    print(f"\nTesting token generation...")
    resp = requests.post(url, headers=headers)
    print(f"  Status: {resp.status_code}")
    
    if resp.status_code == 200:
        json_resp = json.loads(resp.text)
        token = json_resp.get("access_token", "")
        print(f"  ✅ Access Token: {token[:30]}...")
        print(f"  ✅ Expires in: {json_resp.get('expires_in')} seconds")
        return token
    else:
        print(f"  ❌ Failed: {resp.text}")
        return None

def main():
    print("=" * 60)
    print("  MTN MoMo Sandbox Setup")
    print("=" * 60)
    
    if SUBSCRIPTION_KEY == "YOUR_SUBSCRIPTION_KEY_HERE":
        print("\n❌ ERROR: You need to set your Subscription Key!")
        print("\nTo get your key:")
        print("  1. Go to https://momodeveloper.mtn.co.rw")
        print("  2. Sign up / Login")
        print("  3. Subscribe to 'Collections' API")
        print("  4. Go to Profile → copy Primary Key")
        print("  5. Paste it in SUBSCRIPTION_KEY above")
        return
    
    # Step 1: Create API User
    api_user = create_api_user()
    if not api_user:
        return
    
    # Step 2: Generate API Key
    api_key = create_api_key(api_user)
    if not api_key:
        return
    
    # Step 3: Test token
    token = test_token(api_user, api_key)
    
    # Summary
    print("\n" + "=" * 60)
    print("  YOUR CREDENTIALS")
    print("=" * 60)
    print(f"  Subscription Key: {SUBSCRIPTION_KEY}")
    print(f"  API User UUID:    {api_user}")
    print(f"  API Key:          {api_key}")
    print("=" * 60)
    
    print("\n📋 Copy these and paste them to me to configure the backend!")

if __name__ == "__main__":
    main()
