import ccxt
import config
import time
import sys
import pandas as pd
import requests
import json
import os
import csv  # <--- NEW: For Excel/Spreadsheet logging
from datetime import datetime

# --- CONFIGURATION ---
SYMBOLS = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'BNB/USDT']
TIMEFRAME = '1m'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_AMOUNT_USDT = 100

# 🛡️ RISK MANAGEMENT
STOP_LOSS_PCT = 0.02
TAKE_PROFIT_PCT = 0.06

# 📲 YOUR DISCORD LINK
WEBHOOK_URL = "https://discord.com/api/webhooks/1456554400003784716/NpNkBdDqJUQAZee35sWANqqEloXFJMra7dA59zgAzru-nTVh9i0zl-JQ6OGzrXyKHOsF"

# 📂 FILES
STATE_FILE = "bot_state.json"
HISTORY_FILE = "trade_history.csv" # <--- NEW: Permanent Ledger

print(f"🤖 Initializing Ledger-Enabled Bot...")

# 1. Connect
try:
    exchange = ccxt.binance({
        'apiKey': config.API_KEY,
        'secret': config.SECRET_KEY,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}
    })
    exchange.set_sandbox_mode(True)
except:
    sys.exit("❌ Error: Keys missing.")

# --- THE BRAIN (SAVE/LOAD) ---
def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            print("⚠️ Memory corrupted.")
    return {}

def save_state(positions):
    with open(STATE_FILE, 'w') as f:
        json.dump(positions, f, indent=4)

# --- THE LEDGER (CSV LOGGING) --- 
def log_trade_to_csv(symbol, entry_price, exit_price, profit_usdt, profit_pct, reason):
    """Writes the trade result to a spreadsheet."""
    file_exists = os.path.isfile(HISTORY_FILE)
    
    with open(HISTORY_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write Header if new file
        if not file_exists:
            writer.writerow(['Date', 'Symbol', 'Entry Price', 'Exit Price', 'Profit ($)', 'Profit (%)', 'Reason'])
            
        # Write Trade Data
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            symbol,
            f"${entry_price:.2f}",
            f"${exit_price:.2f}",
            f"${profit_usdt:.2f}",
            f"{profit_pct:.2f}%",
            reason
        ])
        print(f"📝 Trade logged to {HISTORY_FILE}")

# Initialize State
positions = load_state()
for sym in SYMBOLS:
    if sym not in positions:
        positions[sym] = {'in_position': False, 'entry_price': 0}
save_state(positions)

# --- HELPER FUNCTIONS ---
def send_discord_alert(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except:
        pass

def get_data(symbol):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe=TIMEFRAME, limit=50)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df.iloc[-1]
    except:
        return None

def execute_trade(symbol, side, quantity=None):
    try:
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        coin_name = symbol.split('/')[0]

        if side == 'buy':
            qty = TRADE_AMOUNT_USDT / price
            exchange.create_order(symbol, 'market', 'buy', qty)
            msg = f"🟢 **BUY: {coin_name}** @ ${price:,.2f} | RSI Oversold! 📉"
            print(f"✅ {msg}")
            send_discord_alert(msg)
            return price

        elif side == 'sell':
            balance = exchange.fetch_balance()['total'][coin_name]
            if balance > 0:
                exchange.create_order(symbol, 'market', 'sell', balance)
                return price
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# --- MAIN LOOP ---
print("-" * 40)
print("📡 Scanning 4 Markets (Ledger Active)...")

while True:
    for symbol in SYMBOLS:
        data = get_data(symbol)
        if data is None: continue
            
        rsi = data['RSI']
        price = data['close']
        state = positions[symbol]
        
        if state['in_position'] or rsi < 35 or rsi > 65:
            icon = "🎒" if state['in_position'] else "🔎"
            print(f"{icon} {symbol:<9} | Price: ${price:<10,.2f} | RSI: {rsi:.2f}")

        if state['in_position']:
            entry = state['entry_price']
            pnl_pct = (price - entry) / entry
            sell_reason = None
            
            if pnl_pct <= -STOP_LOSS_PCT:
                sell_reason = "STOP LOSS 🛡️"
            elif pnl_pct >= TAKE_PROFIT_PCT:
                sell_reason = "TAKE PROFIT 💰"
            elif rsi > RSI_OVERBOUGHT:
                sell_reason = "RSI EXIT 🚀"
            
            if sell_reason:
                print(f"   🚨 {sell_reason}")
                sale_price = execute_trade(symbol, 'sell')
                
                if sale_price:
                    # Calc Stats
                    profit_usdt = (TRADE_AMOUNT_USDT / entry) * (sale_price - entry)
                    profit_pct = pnl_pct * 100
                    
                    # 1. Alert
                    emoji = "🤑" if profit_usdt > 0 else "🩸"
                    msg = f"{emoji} **SELL: {symbol}**\n**Profit:** ${profit_usdt:.2f} ({profit_pct:.2f}%)\nReason: {sell_reason}"
                    send_discord_alert(msg)
                    
                    # 2. LOG TO CSV (The New Feature)
                    log_trade_to_csv(symbol, entry, sale_price, profit_usdt, profit_pct, sell_reason)
                    
                    # 3. Reset State
                    positions[symbol]['in_position'] = False
                    positions[symbol]['entry_price'] = 0
                    save_state(positions)

        else:
            if rsi < RSI_OVERSOLD:
                print(f"   📉 BUY SIGNAL!")
                entry = execute_trade(symbol, 'buy')
                if entry:
                    positions[symbol]['in_position'] = True
                    positions[symbol]['entry_price'] = entry
                    save_state(positions)

    time.sleep(10)