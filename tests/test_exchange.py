import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from simple_bot.exchange import Exchange

class DummyClient:
    def __init__(self):
        self.orders = []

    def create_order(self, symbol, order_type, side, amount, params=None):
        order = {
            "symbol": symbol,
            "type": order_type,
            "side": side,
            "amount": amount,
            "params": params or {},
        }
        self.orders.append(order)
        return order

def make_exchange():
    ex = Exchange.__new__(Exchange)
    ex.client = DummyClient()
    ex.symbol = "BTC/USDT"
    return ex

def test_open_position_orders_created():
    ex = make_exchange()
    orders = ex.open_position("buy", 1.0, 100.0, 200.0)
    assert orders["entry"]["type"] == "market"
    assert orders["entry"]["side"] == "buy"

    sl = orders["stop_loss"]
    tp = orders["take_profit"]
    assert sl["params"]["stopLoss"]["triggerPrice"] == 100.0
    assert sl["params"]["tpSlMode"] == "Full"
    assert tp["params"]["takeProfit"]["triggerPrice"] == 200.0
    assert tp["params"]["tpSlMode"] == "Full"
    assert len(ex.client.orders) == 3
