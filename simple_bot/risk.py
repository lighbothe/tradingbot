"""Risk management helpers."""

from __future__ import annotations

from typing import Dict
import pandas as pd


def position_size_usd(balance: float, price: float, cfg: Dict[str, float]) -> float:
    """Calculate position size in contracts.

    Ensures the returned size respects the configured minimum order size.
    Returns ``0.0`` when the calculated size is below the minimum.
    """

    risk_pct = cfg.get("risk_pct", 1) / 100
    size = (balance * risk_pct) / price
    min_size = cfg.get("min_size", 0.001)
    if size < min_size:
        return 0.0
    return size


def calc_sl_tp(price: float, side: str, df: pd.DataFrame, cfg: Dict[str, float]) -> tuple[float, float]:
    """Calculate stop-loss and take-profit based on ATR."""
    atr = df[f"atr_{cfg['atr_period']}"].iloc[-1]
    sl_atr = cfg['sl_atr'] * atr
    tp_atr = cfg['tp_atr'] * atr
    if side == 'LONG':
        sl = price - sl_atr
        tp = price + tp_atr
    else:
        sl = price + sl_atr
        tp = price - tp_atr
    return sl, tp
