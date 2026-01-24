# 🐙 Multi-Coin Crypto Algo Trader

A robust, persistent, and automated trading bot built in Python that scans multiple cryptocurrency markets simultaneously for high-probability setups.

## 🚀 Key Features
- **Multi-Coin Scanner:** Monitors BTC, ETH, SOL, and BNB simultaneously using a non-blocking loop.
- **RSI Mean Reversion Strategy:** Automatically detects oversold (Buy) and overbought (Sell) conditions.
- **Risk Management:**
  - 🛡️ **Stop Loss:** Automatically cuts losing trades at -2% to preserve capital.
  - 💰 **Take Profit:** Secures gains at +6% based on entry price.
- **Persistence ("The Brain"):** Uses a local JSON database (`bot_state.json`) to remember active trades even if the bot crashes or restarts.
- **Ledger System:** Logs every trade outcome to a CSV file (`trade_history.csv`) for performance analysis.
- **Live Alerts:** Sends real-time trade notifications and profit reports via Discord Webhooks.

## 🛠️ Technology Stack
- **Python 3.9+**
- **CCXT:** For unified connection to the Binance API.
- **Pandas:** For technical analysis and data manipulation.
- **JSON & CSV:** For state persistence and trade logging.
- **Discord API:** For remote monitoring and alerts.

## ⚙️ Logic Overview
The bot operates on a **"Sniper" logic**:
1.  Fetches 1-minute OHLCV candles for all target coins.
2.  Calculates the **RSI (Relative Strength Index)** manually (no heavy libraries required).
3.  **Buys** if RSI < 30 (Oversold Panic).
4.  **Holds** and monitors P&L in real-time.
5.  **Sells** if:
    - RSI > 70 (Overbought).
    - Stop Loss hit (-2%).
    - Take Profit hit (+6%).

## ⚠️ Disclaimer
This software is for educational purposes only. Do not risk money you cannot afford to lose. The authors are not responsible for any financial losses.

---
*Built by [panth shah]*