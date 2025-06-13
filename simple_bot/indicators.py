"""Indicator helper functions."""

from __future__ import annotations

import pandas as pd
import pandas_ta as ta


def add_macd(df: pd.DataFrame, fast: int, slow: int, signal: int) -> pd.DataFrame:
    """Add MACD indicators to DataFrame."""
    macd = ta.macd(df['close'], fast=fast, slow=slow, signal=signal)
    return pd.concat([df, macd], axis=1)


def add_ema(df: pd.DataFrame, length: int, column: str = 'close') -> pd.DataFrame:
    """Add EMA column."""
    ema = ta.ema(df[column], length=length)
    df[f'ema_{length}'] = ema
    return df


def add_atr(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """Add ATR column."""
    atr = ta.atr(df['high'], df['low'], df['close'], length=length)
    df[f'atr_{length}'] = atr
    return df
