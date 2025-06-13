"""Entry point for the trading bot."""

from __future__ import annotations

import argparse
import time

import pandas as pd

from .exchange import Exchange
from .indicators import add_macd, add_ema, add_atr
from .strategy import generate_signal
from .risk import position_size_usd, calc_sl_tp
from .utils import load_cfg, log


def run(cfg_path: str) -> None:
    cfg = load_cfg(cfg_path)
    exchange = Exchange(cfg)
    poll = cfg.get("poll_seconds", 60)
    while True:
        try:
            df = exchange.fetch_ohlcv(limit=cfg["limit"], timeframe=cfg["timeframe"])
            df = add_macd(df, cfg["indicators"]["macd_fast"], cfg["indicators"]["macd_slow"], cfg["indicators"]["macd_signal"])
            df = add_ema(df, cfg["indicators"]["ema_fast"])
            df = add_ema(df, cfg["indicators"]["ema_slow"])
            df = add_atr(df, cfg["indicators"]["atr_period"])
            signal = generate_signal(df, {**cfg["indicators"], **cfg["risk"]})
            log("INFO", f"Signal: {signal.side}")
            if signal.side != "NONE" and not exchange.position_open():
                price = df["close"].iloc[-1]
                balance = exchange.balance()
                size = position_size_usd(balance, price, cfg.get("risk", {}))
                sl, tp = calc_sl_tp(price, signal.side, df, {**cfg["indicators"], **cfg["risk"]})
                log("INFO", f"Open {signal.side} size {size:.4f} SL {sl:.2f} TP {tp:.2f}")
                exchange.open_position("buy" if signal.side == "LONG" else "sell", size, sl, tp)
        except Exception as err:
            log("ERROR", str(err))
        time.sleep(poll)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple trading bot")
    parser.add_argument("--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
