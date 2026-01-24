import os, time, requests, subprocess
from dotenv import load_dotenv

load_dotenv()
# Start C++ Engine
cpp_exe = os.path.abspath("../cpp_core/hft")
engine = subprocess.Popen([cpp_exe], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

def talk_to_engine(price):
    try:
        engine.stdin.write(f"{price}\n")
        engine.stdin.flush()
        return engine.stdout.readline().strip()
    except: return "C++ Engine Error"

def get_price():
    url = "https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT"
    try:
        r = requests.get(url).json()
        return r['result']['data'][0]['a']
    except: return None

print("\n" + "🚀 HFT DASHBOARD: LIVE".center(50, "="))
try:
    while True:
        p = get_price()
        if p:
            response = talk_to_engine(p)
            print(f"[{time.strftime('%H:%M:%S')}] {response}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nStopping..."); engine.terminate()