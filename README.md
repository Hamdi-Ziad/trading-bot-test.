# Super Simple Beginner Guide: MT5 RSI Bot (EURUSD)

If you have **never coded before**, follow this exactly from top to bottom.

This bot:
- trades **EURUSD**
- uses **RSI**
- opens 2 orders per signal:
  - Take Profit 1 = **5 pips**
  - Take Profit 2 = **10 pips**

---

## Part A — Install everything (one time)

### 1) Install MetaTrader 5

1. Download and install **MetaTrader 5** from your broker or MetaQuotes.
2. Open MT5.
3. Log in to your trading account (**use demo account first**).

### 2) Install Python

1. Download Python 3.10+ from python.org.
2. During install, check the box: **Add Python to PATH**.
3. Finish install.

### 3) Install Visual Studio Code

1. Download and install **Visual Studio Code** from code.visualstudio.com.
2. Open VS Code.

---

## Part B — Prepare MT5 correctly (very important)

In MT5:

1. Press **Ctrl+M** to open **Market Watch**.
2. Find **EURUSD** in the list.
   - If missing: right-click Market Watch → **Symbols** → search EURUSD → Show.
3. Make sure **Algo Trading / AutoTrading** is enabled (top toolbar button ON).
4. Keep MT5 open.

---

## Part C — Open the bot project in VS Code

1. Open VS Code.
2. Click **File → Open Folder**.
3. Select this project folder (`trading-bot-test`).
4. In VS Code, open terminal:
   - Click **Terminal → New Terminal**.

You should now see a terminal at the bottom.

---

## Part D — Copy/paste these commands exactly

Run each command one by one in the VS Code terminal.

### 1) Create virtual environment
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

### 2) Activate virtual environment

If you are on **Windows PowerShell**:

### B. Activate environment

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

If you are on **Windows CMD**:

**Windows CMD**
```cmd
.venv\Scripts\activate.bat
```

If you are on **Mac/Linux**:

**Linux/macOS**
```bash
source .venv/bin/activate
```

After activation, you usually see `(.venv)` at the start of the terminal line.

### 3) Install required packages
### C. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Part E — Start the bot

With MT5 still open and logged in, run:

```bash
python mt5_rsi_bot.py --lot 0.01
```

(Using `0.01` lot keeps the first test small.)

---

## Part F — What you should see

In terminal logs, you should see lines about:
- current RSI value
- detected signal (buy/sell/none)
- order placed / order failed

If signals do not happen immediately, that is normal — the bot waits for RSI crossover conditions.

---

## Part G — If something goes wrong

### Error: `MT5 initialize() failed`

Do this:
1. Close script (`Ctrl+C` in terminal).
2. Make sure MT5 is open and logged in.
3. Start script again.

### Error: `No module named MetaTrader5`

Do this:
1. Make sure `(.venv)` is visible in terminal.
2. Run again:

```bash
pip install -r requirements.txt
```

### Bot runs but no trades

Check all 3:
1. EURUSD visible in Market Watch.
2. AutoTrading enabled.
3. Wait for valid RSI signal.

---

## Part H — Important safety note

Please use **demo account first** until you are comfortable. Automated trading can lose money.

---

## Files in this project

- `mt5_rsi_bot.py` → bot code
- `requirements.txt` → required Python packages
- `README.md` → this beginner guide
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
