import ccxt
import pandas as pd
import sys

# --- CONFIGURATION ---
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'
SMA_SHORT = 10
SMA_LONG = 30
STARTING_BALANCE = 1000
STOP_LOSS_PCT = 0.02      # ⚠️ NEW: Sell if we lose 2%
TAKE_PROFIT_PCT = 0.06    # ⚠️ NEW: Sell if we win 6% (Lock in gains)

print(f"⏳ Initializing Optimized Time Machine (SL: {STOP_LOSS_PCT*100}% | TP: {TAKE_PROFIT_PCT*100}%)...")

# 1. Fetch Data
exchange = ccxt.binance()
try:
    bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=1000)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    df['SMA_short'] = df['close'].rolling(window=SMA_SHORT).mean()
    df['SMA_long'] = df['close'].rolling(window=SMA_LONG).mean()
except Exception as e:
    sys.exit(f"❌ Error: {e}")

# 2. Simulation Loop
balance = STARTING_BALANCE
btc_held = 0
in_position = False
trades = 0
buy_price = 0  # Track price we bought at

print("-" * 50)
for i in range(len(df)):
    if pd.isna(df['SMA_long'].iloc[i]): continue
        
    current_price = df['close'].iloc[i]
    short_avg = df['SMA_short'].iloc[i]
    long_avg = df['SMA_long'].iloc[i]
    timestamp = df['timestamp'].iloc[i]

    # --- LOGIC ---

    # CHECK EXIT CONDITIONS FIRST (Safety First!)
    if in_position:
        # A. STOP LOSS HIT? (Bad trade, get out!)
        if current_price < buy_price * (1 - STOP_LOSS_PCT):
            balance = btc_held * current_price
            print(f"🛡️ [STOP LOSS] {timestamp} @ ${current_price:,.2f} | ❌ Loss locked")
            btc_held = 0
            in_position = False
            continue # Skip the rest of the loop

        # B. TAKE PROFIT HIT? (Good trade, cash out!)
        if current_price > buy_price * (1 + TAKE_PROFIT_PCT):
            balance = btc_held * current_price
            print(f"💰 [TAKE PROFIT] {timestamp} @ ${current_price:,.2f} | ✅ Profit locked")
            btc_held = 0
            in_position = False
            continue

        # C. STANDARD SIGNAL EXIT (Death Cross)
        if short_avg < long_avg:
            balance = btc_held * current_price
            btc_held = 0
            in_position = False
            print(f"🔴 [SELL SIGNAL] {timestamp} @ ${current_price:,.2f}")

    # BUY SIGNAL (Golden Cross)
    elif short_avg > long_avg and not in_position:
        btc_held = balance / current_price
        buy_price = current_price # Remember entry price
        balance = 0
        in_position = True
        trades += 1
        print(f"🟢 [BUY]  {timestamp} @ ${current_price:,.2f}")

# 3. Results
final_value = balance if balance > 0 else (btc_held * df['close'].iloc[-1])
profit = final_value - STARTING_BALANCE
return_percent = (profit / STARTING_BALANCE) * 100
buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[30]) / df['close'].iloc[30]) * 100

print("-" * 50)
print(f"📊 OPTIMIZED RESULTS:")
print(f"🏁 Final Balance:    ${final_value:,.2f}")
print(f"📈 Total Return:     {return_percent:.2f}%")
print(f"🦁 Buy & Hold Return: {buy_hold_return:.2f}%")