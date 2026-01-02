import ccxt
import pandas as pd
import sys

# --- CONFIGURATION ---
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70  # Sell Zone
RSI_OVERSOLD = 30    # Buy Zone

print(f"⏳ Initializing RSI Mean Reversion Test for {SYMBOL}...")

# 1. Fetch Data
exchange = ccxt.binance()
try:
    bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=1000)
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    
    # 2. Calculate RSI (The New Brain)
    # We do the math manually to avoid extra library dependencies if possible
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=RSI_PERIOD).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=RSI_PERIOD).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
except Exception as e:
    sys.exit(f"❌ Error: {e}")

# 3. Simulation
balance = 1000
btc_held = 0
in_position = False
trades = 0

print("-" * 50)

for i in range(len(df)):
    if pd.isna(df['RSI'].iloc[i]): continue
        
    price = df['close'].iloc[i]
    rsi = df['RSI'].iloc[i]
    timestamp = df['timestamp'].iloc[i]

    # --- RSI STRATEGY ---
    
    # BUY SIGNAL (Panic Selling -> We Buy)
    if rsi < RSI_OVERSOLD and not in_position:
        btc_held = balance / price
        balance = 0
        in_position = True
        trades += 1
        print(f"🟢 [BUY]  {timestamp} @ ${price:,.2f} | RSI: {rsi:.2f}")

    # SELL SIGNAL (Greed -> We Sell)
    elif rsi > RSI_OVERBOUGHT and in_position:
        balance = btc_held * price
        btc_held = 0
        in_position = False
        print(f"🔴 [SELL] {timestamp} @ ${price:,.2f} | RSI: {rsi:.2f} | Bal: ${balance:,.0f}")

# 4. Results
final_value = balance if balance > 0 else (btc_held * df['close'].iloc[-1])
profit_pct = ((final_value - 1000) / 1000) * 100
buy_hold_return = ((df['close'].iloc[-1] - df['close'].iloc[30]) / df['close'].iloc[30]) * 100

print("-" * 50)
print(f"📊 RSI STRATEGY RESULTS:")
print(f"🏁 Final Balance:    ${final_value:,.2f}")
print(f"📈 Total Return:     {profit_pct:.2f}%")
print(f"🦁 Buy & Hold Return: {buy_hold_return:.2f}%")

if profit_pct > 0:
    print("✅ VERDICT: RSI Works! The market is bouncing.")
else:
    print("❌ VERDICT: Still losing. Market is crashing hard.")