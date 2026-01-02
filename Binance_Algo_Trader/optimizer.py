import ccxt
import pandas as pd
import sys

# --- CONFIGURATION ---
SYMBOL = 'BTC/USDT'
TIMEFRAME = '1h'

print(f"⏳ Downloading data for {SYMBOL} to Start Grid Search...")

# 1. Fetch Data ONCE (To be fast)
exchange = ccxt.binance()
bars = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=1000)
df_master = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df_master['timestamp'] = pd.to_datetime(df_master['timestamp'], unit='ms')

# 2. Define The Grid (The Combinations to Test)
short_windows = [5, 10, 15]        # Try these Fast lines
long_windows = [20, 40, 60]        # Try these Slow lines
stop_losses = [0.03, 0.05, 0.10]   # Try 3%, 5%, 10% Risk

results = []

print(f"🚀 Testing {len(short_windows) * len(long_windows) * len(stop_losses)} combinations...")
print("-" * 60)
print(f"{'SHORT':<6} {'LONG':<6} {'SL %':<6} | {'RETURN %':<10} | {'TRADES':<6}")
print("-" * 60)

# 3. The Brute Force Loop
for short in short_windows:
    for long in long_windows:
        for sl in stop_losses:
            if short >= long: continue # Skip invalid combos

            # Prepare Data
            df = df_master.copy()
            df['SMA_short'] = df['close'].rolling(window=short).mean()
            df['SMA_long'] = df['close'].rolling(window=long).mean()
            
            # Run Fast Simulation
            balance = 1000
            btc_held = 0
            in_position = False
            trades = 0
            buy_price = 0
            
            for i in range(len(df)):
                if pd.isna(df['SMA_long'].iloc[i]): continue
                
                price = df['close'].iloc[i]
                s_avg = df['SMA_short'].iloc[i]
                l_avg = df['SMA_long'].iloc[i]
                
                # Check Exits
                if in_position:
                    # Stop Loss
                    if price < buy_price * (1 - sl):
                        balance = btc_held * price
                        in_position = False
                        btc_held = 0
                    # Signal Sell
                    elif s_avg < l_avg:
                        balance = btc_held * price
                        in_position = False
                        btc_held = 0
                
                # Check Entry
                elif s_avg > l_avg:
                    btc_held = balance / price
                    buy_price = price
                    balance = 0
                    in_position = True
                    trades += 1

            # Calculate Final Result
            final_val = balance if balance > 0 else (btc_held * df['close'].iloc[-1])
            profit_pct = ((final_val - 1000) / 1000) * 100
            
            # Print row
            print(f"{short:<6} {long:<6} {sl*100:<5.0f}% | {profit_pct:>8.2f}% | {trades:<6}")
            results.append((short, long, sl, profit_pct))

# 4. Find the Winner
best_combo = max(results, key=lambda x: x[3])
print("-" * 60)
print(f"🏆 BEST PARAMETERS FOUND:")
print(f"✅ SMA Short: {best_combo[0]}")
print(f"✅ SMA Long:  {best_combo[1]}")
print(f"✅ Stop Loss: {best_combo[2]*100}%")
print(f"💰 Return:    {best_combo[3]:.2f}%")