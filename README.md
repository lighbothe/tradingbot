# Simple Bot

CLI trading bot for Bybit futures (Testnet by default).

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

1. Copy `config.yaml` and edit API keys and parameters.
2. Create `.env` if needed for additional secrets.
3. Adjust the risk settings if desired. `risk_pct` controls the percentage of the
   balance used per trade and `min_size` sets the minimum contract size allowed.

## Running in Testnet

```bash
python -m simple_bot.main --config config.yaml
```

## Switching to Mainnet

Edit `config.yaml`:
```yaml
exchange:
  testnet: false
```

Then run the bot again.
