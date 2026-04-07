"""Automated MT5 RSI bot for EURUSD.

Strategy summary:
- Symbol: EURUSD
- Timeframe: M5 (configurable)
- Indicator: RSI (default period 14)
- Entry signals:
  * Buy when RSI crosses up through oversold level (30)
  * Sell when RSI crosses down through overbought level (70)
- Position management:
  * Opens two market orders per signal
  * TP #1: +5 pips
  * TP #2: +10 pips

Disclaimer: This script is for educational use. Test on demo first.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd


@dataclass
class BotConfig:
    symbol: str = "EURUSD"
    timeframe: int = mt5.TIMEFRAME_M5
    rsi_period: int = 14
    oversold: float = 30.0
    overbought: float = 70.0
    lot_size: float = 0.10
    slippage: int = 20
    magic_number: int = 20260406
    stop_loss_pips: float = 12.0
    tp_pips_1: float = 5.0
    tp_pips_2: float = 10.0
    bars_to_fetch: int = 250
    poll_seconds: int = 2


def rsi(series: pd.Series, period: int) -> pd.Series:
    """Calculate RSI using exponential moving averages."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    out = 100 - (100 / (1 + rs))
    return out.fillna(50)


def pip_size(symbol_info: mt5.SymbolInfo) -> float:
    """Return pip size from symbol digits."""
    # For EURUSD in 5-digit pricing, 1 pip = 10 points.
    if symbol_info.digits in (3, 5):
        return symbol_info.point * 10
    return symbol_info.point


def build_request(
    *,
    symbol: str,
    order_type: int,
    volume: float,
    price: float,
    sl: float,
    tp: float,
    deviation: int,
    magic: int,
    comment: str,
) -> dict:
    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }


def send_split_orders(config: BotConfig, direction: str) -> None:
    symbol_info = mt5.symbol_info(config.symbol)
    if symbol_info is None:
        raise RuntimeError(f"Could not get symbol info for {config.symbol}")

    tick = mt5.symbol_info_tick(config.symbol)
    if tick is None:
        raise RuntimeError("Could not get latest tick")

    pips = pip_size(symbol_info)

    if direction == "buy":
        entry = tick.ask
        sl = entry - (config.stop_loss_pips * pips)
        tp_1 = entry + (config.tp_pips_1 * pips)
        tp_2 = entry + (config.tp_pips_2 * pips)
        order_type = mt5.ORDER_TYPE_BUY
    elif direction == "sell":
        entry = tick.bid
        sl = entry + (config.stop_loss_pips * pips)
        tp_1 = entry - (config.tp_pips_1 * pips)
        tp_2 = entry - (config.tp_pips_2 * pips)
        order_type = mt5.ORDER_TYPE_SELL
    else:
        raise ValueError("direction must be 'buy' or 'sell'")

    for idx, tp in enumerate((tp_1, tp_2), start=1):
        req = build_request(
            symbol=config.symbol,
            order_type=order_type,
            volume=config.lot_size,
            price=entry,
            sl=round(sl, symbol_info.digits),
            tp=round(tp, symbol_info.digits),
            deviation=config.slippage,
            magic=config.magic_number,
            comment=f"RSI {direction.upper()} TP{idx}",
        )
        result = mt5.order_send(req)
        if result is None:
            print(f"{datetime.utcnow()} | order_send returned None | request={req}")
            continue
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(
                f"{datetime.utcnow()} | order failed retcode={result.retcode} "
                f"| comment={result.comment} | request={req}"
            )
        else:
            print(
                f"{datetime.utcnow()} | order placed ticket={result.order} "
                f"| direction={direction} | tp_pips={config.tp_pips_1 if idx == 1 else config.tp_pips_2}"
            )


def has_open_position(symbol: str, magic_number: int) -> bool:
    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        return False
    return any(p.magic == magic_number for p in positions)


def get_rsi_frame(config: BotConfig) -> pd.DataFrame:
    rates = mt5.copy_rates_from_pos(config.symbol, config.timeframe, 0, config.bars_to_fetch)
    if rates is None or len(rates) == 0:
        raise RuntimeError("Failed to fetch rates from MT5")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df["rsi"] = rsi(df["close"], config.rsi_period)
    return df


def signal_from_last_two(df: pd.DataFrame, oversold: float, overbought: float) -> str | None:
    prev_rsi = float(df["rsi"].iloc[-2])
    curr_rsi = float(df["rsi"].iloc[-1])

    if prev_rsi < oversold <= curr_rsi:
        return "buy"
    if prev_rsi > overbought >= curr_rsi:
        return "sell"
    return None


def ensure_symbol_selected(symbol: str) -> None:
    info = mt5.symbol_info(symbol)
    if info is None:
        raise RuntimeError(f"Symbol {symbol} not found in Market Watch")
    if not info.visible and not mt5.symbol_select(symbol, True):
        raise RuntimeError(f"Could not enable symbol {symbol} in Market Watch")


def run(config: BotConfig) -> None:
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialize() failed: {mt5.last_error()}")

    try:
        ensure_symbol_selected(config.symbol)
        last_bar_time = None

        print(f"Bot started for {config.symbol}. Waiting for signals...")
        while True:
            df = get_rsi_frame(config)
            current_bar_time = df["time"].iloc[-1]

            # Process only once per bar to avoid duplicate entries.
            if last_bar_time is None or current_bar_time != last_bar_time:
                last_bar_time = current_bar_time
                signal = signal_from_last_two(df, config.oversold, config.overbought)

                print(
                    f"{datetime.utcnow()} | bar={current_bar_time} | RSI={df['rsi'].iloc[-1]:.2f} "
                    f"| signal={signal}"
                )

                if signal and not has_open_position(config.symbol, config.magic_number):
                    send_split_orders(config, signal)
                elif signal:
                    print(f"{datetime.utcnow()} | signal ignored (existing position with magic={config.magic_number})")

            time.sleep(config.poll_seconds)

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        mt5.shutdown()


def parse_args() -> BotConfig:
    parser = argparse.ArgumentParser(description="MT5 EURUSD RSI trading bot")
    parser.add_argument("--lot", type=float, default=0.10, help="Lot size per TP order")
    parser.add_argument("--oversold", type=float, default=30, help="RSI oversold threshold")
    parser.add_argument("--overbought", type=float, default=70, help="RSI overbought threshold")
    parser.add_argument("--sl-pips", type=float, default=12.0, help="Stop-loss in pips")
    parser.add_argument("--poll-seconds", type=int, default=2, help="Polling interval")

    args = parser.parse_args()
    return BotConfig(
        lot_size=args.lot,
        oversold=args.oversold,
        overbought=args.overbought,
        stop_loss_pips=args.sl_pips,
        poll_seconds=args.poll_seconds,
    )


if __name__ == "__main__":
    cfg = parse_args()
    run(cfg)
