import os
import requests
import time
import hashlib
import hmac
import socket
from dotenv import load_dotenv

# --- FORCE IPV4 (Fixes Mac/ISP Issues) ---
# This forces Python to use the numbers (106...) instead of the complex letters
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response for response in responses if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

# --- SETUP ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BASE_URL = "https://api.crypto.com/v2/"

def test_connection():
    print("\n--- 🕵️ THE TRUTH TELLER ---")
    
    # CHECK 1: WHAT KEY ARE WE USING?
    if API_KEY:
        print(f"🔑 Key in .env file:   {API_KEY[:6]}...... (Check if this matches website!)")
    else:
        print("❌ CRITICAL: .env file is empty or cannot be read.")
        return

    # CHECK 2: WHAT IP ARE WE USING?
    try:
        my_ip = requests.get("https://api.ipify.org").text
        print(f"🌍 Bot's Current IP:   {my_ip}")
    except:
        print("❌ Could not get IP.")

    # CHECK 3: CONNECT TO CRYPTO.COM
    req = {
        "id": 1,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {"currency": "USD"},
        "nonce": int(time.time() * 1000)
    }

    # Generate Signature
    param_str = ""
    if "params" in req:
        for key in sorted(req["params"].keys()):
            param_str += key + str(req["params"][key])
    sig_payload = req["method"] + str(req["id"]) + req["api_key"] + param_str + str(req["nonce"])
    req["sig"] = hmac.new(bytes(str(SECRET_KEY), 'utf-8'), msg=bytes(sig_payload, 'utf-8'), digestmod=hashlib.sha256).hexdigest()

    print("\nKnocking on Crypto.com's door...")
    try:
        response = requests.post(BASE_URL + "private/get-account-summary", json=req, headers={'Content-Type': 'application/json'})
        data = response.json()
        
        if data['code'] == 0:
            print("\n✅ SUCCESS: CONNECTION ESTABLISHED!")
            print("💰 Account Access: GRANTED")
        else:
            print(f"\n❌ BLOCKED by Crypto.com")
            print(f"⛔ Error Code: {data['code']} ({data['message']})")
            print("\n👉 SOLUTION:")
            print(f"1. Go to Website > API Keys.")
            print(f"2. Find Key starting with: {API_KEY[:6]}...")
            print(f"3. Edit THAT key's IP Whitelist.")
            print(f"4. Add this IP: {my_ip}")
    except Exception as e:
        print(f"❌ Request Failed: {e}")

if __name__ == "__main__":
    test_connection()