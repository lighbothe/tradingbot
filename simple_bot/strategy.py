"""Trading strategy logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import pandas as pd


@dataclass
class Signal:
    """Trading signal dataclass."""

    side: str
    sl_atr: float
    tp_atr: float


def generate_signal(df: pd.DataFrame, cfg: Dict[str, float]) -> Signal:
    """Generate trading signal based on MACD and EMA crossover."""
    ema_fast = df[f"ema_{cfg['ema_fast']}"]
    ema_slow = df[f"ema_{cfg['ema_slow']}"]
    hist = df['MACDh_12_26_9'] if 'MACDh_12_26_9' in df.columns else df['MACDh']
    side = 'NONE'
    if hist.iloc[-1] > 0 and ema_fast.iloc[-1] > ema_slow.iloc[-1]:
        side = 'LONG'
    elif hist.iloc[-1] < 0 and ema_fast.iloc[-1] < ema_slow.iloc[-1]:
        side = 'SHORT'
    return Signal(side=side, sl_atr=cfg['sl_atr'], tp_atr=cfg['tp_atr'])
