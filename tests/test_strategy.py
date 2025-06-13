"""Tests for strategy module."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))

from simple_bot.strategy import generate_signal, Signal
from simple_bot.indicators import add_macd, add_ema, add_atr


def test_generate_signal() -> None:
    np.random.seed(0)
    data = np.random.rand(300, 5) * 100
    df = pd.DataFrame(data, columns=["open", "high", "low", "close", "volume"])
    df = add_macd(df, 12, 26, 9)
    df = add_ema(df, 50)
    df = add_ema(df, 200)
    df = add_atr(df, 14)
    cfg = {
        "ema_fast": 50,
        "ema_slow": 200,
        "sl_atr": 1.5,
        "tp_atr": 3.0,
        "atr_period": 14,
    }
    signal = generate_signal(df, cfg)
    assert isinstance(signal, Signal)
    assert signal.side in {"LONG", "SHORT", "NONE"}
