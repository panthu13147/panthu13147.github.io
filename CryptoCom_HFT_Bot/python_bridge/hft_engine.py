import os
import requests
import time
import hmac
import hashlib
import json
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
BASE_URL = "https://api.crypto.com/v2/"
TRADING_PAIR = "BTC_USD"  # We are watching Bitcoin

# --- HELPER: SIGNATURE (The Security Guard) ---
def get_signature(req, secret_key):
    param_str = ""
    if "params" in req:
        for key in sorted(req["params"].keys()):
            param_str += key + str(req["params"][key])
    sig_payload = req["method"] + str(req["id"]) + req["api_key"] + param_str + str(req["nonce"])
    return hmac.new(
        bytes(str(secret_key), 'utf-8'),
        msg=bytes(sig_payload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

# --- CORE FUNCTION: GET ORDER BOOK ---
def get_order_book():
    """
    Fetches the public list of buyers (Bids) and sellers (Asks).
    HFT Concept: This is your 'Eyes'. You need to see this to know where the price is.
    """
    endpoint = "public/get-book"
    params = {
        "instrument_name": TRADING_PAIR,
        "depth": 10  # We only care about the top 10 offers (Speed > Quantity)
    }
    
    try:
        # Note: Public endpoints don't strictly need keys, but we practice good hygiene.
        response = requests.get(BASE_URL + endpoint, params=params)
        data = response.json()
        
        if data['code'] == 0:
            result = data['result']
            best_bid = result['bids'][0][0] # The highest price someone will pay
            best_ask = result['asks'][0][0] # The lowest price someone will sell for
            spread = float(best_ask) - float(best_bid)
            
            print(f"\n--- 📊 MARKET SCAN: {TRADING_PAIR} ---")
            print(f"🟢 Best BUYER (Bid):  ${best_bid}")
            print(f"🔴 Best SELLER (Ask): ${best_ask}")
            print(f"⚡ SPREAD (Profit Gap): ${spread:.2f}")
            return result
        else:
            print(f"❌ Error fetching book: {data}")
    except Exception as e:
        print(f"❌ Crash: {e}")

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🤖 HFT BOT INITIALIZED...")
    
    # Run loop 3 times just to test
    for i in range(3):
        get_order_book()
        time.sleep(1) # Sleep 1 second (In real HFT, this would be 0.1s or less)