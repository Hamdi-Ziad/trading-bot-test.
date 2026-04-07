# MT5 RSI Trading Bot (EURUSD) — Complete Setup Guide

Yes — this file is the exact step-by-step guide to set up and run the bot.

This Python bot connects to your **MetaTrader 5** desktop terminal, trades **EURUSD**, and uses RSI signals with:
- **TP1 = 5 pips**
- **TP2 = 10 pips**

---

## 1) What you need first

1. **Windows PC** (recommended for MT5 automation).
2. **MetaTrader 5 desktop terminal** installed and logged in.
3. **Python 3.10+** installed.
4. **Visual Studio Code** installed (or Visual Studio + Python workload).
5. A **demo trading account** (strongly recommended before real money).

---

## 2) MetaTrader 5 terminal setup (important)

Open your MT5 terminal and do all of this first:

1. Login to your broker account.
2. Make sure **EURUSD** is visible in **Market Watch**.
3. Enable **Algo Trading / AutoTrading** (button should be ON/green depending on your MT5 theme).
4. Keep MT5 open while the Python bot is running.

> The Python script uses the currently running MT5 terminal session.

---

## 3) Project setup in VS Code

Open this project folder in VS Code, then run commands in the terminal.

### A. Create virtual environment

```bash
python -m venv .venv
```

### B. Activate environment

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows CMD**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS**
```bash
source .venv/bin/activate
```

### C. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4) Run the bot

Basic run:

```bash
python mt5_rsi_bot.py
```

With custom settings:

```bash
python mt5_rsi_bot.py --lot 0.10 --oversold 30 --overbought 70 --sl-pips 12 --poll-seconds 2
```

---

## 5) Exactly how the strategy works

- Symbol: `EURUSD`
- Timeframe: `M5`
- Indicator: `RSI(14)`
- **Buy** when RSI crosses upward through `30`.
- **Sell** when RSI crosses downward through `70`.
- On each signal, bot sends **2 market orders**:
  - Order A: take profit at **+5 pips**
  - Order B: take profit at **+10 pips**
- A stop-loss is also set (`--sl-pips`, default 12 pips).
- The bot avoids duplicate entries by checking existing positions with its magic number.

---

## 6) Recommended first test (safe)

1. Use a **demo account**.
2. Start MT5 and open EURUSD chart.
3. Run bot with **small lot size**:

```bash
python mt5_rsi_bot.py --lot 0.01
```

4. Watch terminal logs for:
   - RSI values
   - signal detection
   - order placement status / errors

---

## 7) Common issues and fixes

### Problem: `MT5 initialize() failed`
- Fix: Open MT5 first and log in.
- Fix: Make sure MT5 is not blocked by Windows permissions.

### Problem: No trades are opened
- Fix: Confirm `EURUSD` exists in Market Watch.
- Fix: Confirm AutoTrading is enabled.
- Fix: Wait for RSI crossover conditions to happen.

### Problem: Import error for `MetaTrader5`
- Fix: Confirm virtual environment is activated.
- Fix: Re-run `pip install -r requirements.txt`.

---

## 8) Files in this project

- `mt5_rsi_bot.py` → trading bot logic
- `requirements.txt` → Python dependencies
- `README.md` → this setup guide

---

## 9) Risk warning

This is educational automation code. Markets are risky. Always forward-test on demo and apply strict risk management before any live trading.
