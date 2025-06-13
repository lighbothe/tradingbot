"""Exchange interaction logic using ccxt."""

from __future__ import annotations

import ccxt
import pandas as pd

from typing import Any, Dict, List


class Exchange:
    """Wrapper around ccxt exchange for Bybit futures."""

    def __init__(self, cfg: Dict[str, Any]):
        self.cfg = cfg
        self.symbol = cfg["symbol"]
        exchange_cfg = cfg["exchange"]
        id_ = exchange_cfg["id"]
        params: Dict[str, Any] = {
            "apiKey": exchange_cfg.get("api_key"),
            "secret": exchange_cfg.get("secret"),
            "enableRateLimit": True,
        }
        if exchange_cfg.get("testnet"):
            params["urls"] = {"api": exchange_cfg["testnet_url"]}
        else:
            params["urls"] = {"api": exchange_cfg.get("mainnet_url", "")}
        self.client = getattr(ccxt, id_)(params)
        if exchange_cfg.get("testnet"):
            self.client.set_sandbox_mode(True)
        self.client.options["defaultType"] = "linear"

        # Ensure the configured symbol is supported by the exchange
        markets = self.client.load_markets()
        if self.symbol not in markets:
            raise ValueError(f"Symbol {self.symbol} not supported by {id_}")
        leverage = cfg.get("leverage", 1)
        try:
            self.client.private_linear_post_position_leverage_save({
                "symbol": self.symbol.replace("/", ""),
                "buy_leverage": leverage,
                "sell_leverage": leverage,
            })
        except Exception:
            pass

    def fetch_ohlcv(self, limit: int, timeframe: str) -> pd.DataFrame:
        """Fetch OHLCV data and return DataFrame."""
        data = self.client.fetch_ohlcv(self.symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        return df

    def open_position(self, side: str, size: float, sl: float, tp: float) -> None:
        """Place market order with SL/TP."""
        params = {
            "time_in_force": "GoodTillCancel",
            "reduce_only": False,
            "close_on_trigger": False,
            "category": "linear",
        }
        self.client.create_market_order(self.symbol, side, size, params=params)
        if sl:
            self.client.create_order(
                self.symbol,
                "STOP",
                side="sell" if side == "buy" else "buy",
                amount=size,
                params={"stop_price": sl, "category": "linear"},
            )
        if tp:
            self.client.create_order(
                self.symbol,
                "TAKE_PROFIT",
                side="sell" if side == "buy" else "buy",
                amount=size,
                params={"stop_price": tp, "category": "linear"},
            )

    def position_open(self) -> bool:
        """Check if there is an open position."""
        positions = self.client.fetch_positions([self.symbol])
        for pos in positions:
            if float(pos.get("contracts", 0)) > 0:
                return True
        return False

    def check_positions(self) -> List[Dict[str, Any]]:
        """Return current positions."""
        return self.client.fetch_positions([self.symbol])

    def balance(self) -> float:
        """Return account balance in USDT."""
        balance = self.client.fetch_balance()
        usdt = balance.get("USDT", {})
        return float(usdt.get("free", 0))
