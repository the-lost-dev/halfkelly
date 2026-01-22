# HalfKelly

A complete trading risk management platform that works with any broker, any instrument, any account type. Every feature is optional and configurable. The system adapts to the trader—not the other way around.

**Broker-Agnostic • Multi-Asset • Fully Configurable**

## Vision

A comprehensive trading risk management system designed with flexibility at its core. Whether you trade FX, Crypto, Futures, Stocks, CFDs, or Options—HalfKelly handles it all.

## Core Design Principles

| Principle | Meaning |
|-----------|---------|
| Broker Agnostic | Works with any broker. No vendor lock-in. Manual or API. |
| Instrument Flexible | FX, Crypto, Futures, Stocks, CFDs, Options—anything. |
| Account Universal | Personal, prop firm, demo, managed—all supported. |
| Rules Configurable | User defines all limits. Nothing hardcoded. |
| Modules Optional | Enable only what you need. Disable the rest. |
| Data Portable | Import/export everything. Your data, your control. |

## System Capabilities

### Core Modules (Always Available)

- **Position Sizing Engine** — Universal calculator for any instrument
- **Risk Validation** — Configurable rules, hard/soft limits
- **Portfolio Monitoring** — Exposure, leverage, correlation, concentration
- **Drawdown Tracking** — Daily, rolling, peak-to-trough
- **Trade Journal** — Log, tag, analyze every trade
- **Performance Analytics** — Expectancy, R-multiples, win rate, Sharpe
- **Alerts & Notifications** — Email, Telegram, Discord, webhooks

### Optional Modules (Enable If Needed)

- **Prop Firm Rules** — Compliance tracking for funded accounts
- **Signal Generation** — Technical indicators, custom strategies
- **Automatic Execution** — Broker API integration for order placement
- **Market Analysis** — Price feeds, charts, indicators
- **Multi-Account Sync** — Unified view across brokers/accounts
- **Backtesting Engine** — Test strategies on historical data
- **Regulatory Compliance** — Reporting for tax, audit, regulatory

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from halfkelly import size_position, EURUSD, print_trade_summary

trade = size_position(
    instrument=EURUSD,
    account_balance=10000,
    risk_percent=2.0,
    entry_price=1.08500,
    stop_loss=1.08000,
    take_profit=1.09500,
    instrument_name="EUR/USD"
)

print_trade_summary(trade)
```

Output:
```
==================================================
  EUR/USD - LONG
==================================================
  Stop Distance:    50.0 pips
  Position Size:    0.40 lots
  Risk Amount:      $200.00
  Risk Percent:     2.00%
  R:R Ratio:        2.00:1
  Potential Reward: $400.00
==================================================
```

## System Architecture

### Layered Design

The system is built in layers. Each layer is independent and can be extended without affecting others.

| Layer | Components | Purpose |
|-------|------------|---------|
| Configuration | Accounts, Instruments, Risk Profiles, Rule Sets | User defines everything |
| Risk Engine | Position Sizer, Validator, Exposure Calculator | Universal calculations |
| Portfolio | Multi-Account, Correlation, Concentration | Aggregated risk view |
| Journal | Trade Log, Metrics, Behavioral Analysis | Performance tracking |
| Alerts | Warnings, Breaches, Summaries, Custom Triggers | Notifications |
| Integrations | Broker APIs, Price Feeds, Import/Export, Webhooks | External connections |
| Signals (Opt) | Indicators, Strategies, Screeners | Trade ideas |
| Execution (Opt) | Order Management, Broker Adapters | Automated trading |

### Universal Instrument Model

Instead of hardcoding asset classes, the system uses a universal instrument model. Any tradeable instrument can be defined:

| Attribute | Description | Examples |
|-----------|-------------|----------|
| Symbol | Unique identifier | EURUSD, BTCUSDT, ES, AAPL |
| Asset Class | Category (user-defined) | FX, Crypto, Futures, Stock, CFD |
| Contract Size | Units per lot/contract | 100,000 / 1 / 50 / 100 |
| Tick Size | Min price increment | 0.0001 / 0.01 / 0.25 / 0.01 |
| Tick Value | Value per tick per contract | $10 / $1 / $12.50 / $1 |
| Margin % | Required margin | 3% / 10% / 5% / 50% |
| Quote Currency | For P&L conversion | USD / USDT / USD / USD |
| Trading Hours | Session times (optional) | 24/5 / 24/7 / Exchange hours |

### Configurable Risk Profiles

Users create Risk Profiles with their own rules. Profiles can be assigned to accounts and modified anytime:

| Parameter | Description | Example Values |
|-----------|-------------|----------------|
| Max Risk Per Trade | % of account risked per trade | 0.5% / 1% / 2% |
| Max Open Risk | Total % at risk across open trades | 2% / 5% / 10% |
| Max Leverage | Total exposure / account balance | 2x / 5x / 20x |
| Max Daily Drawdown | Max loss allowed per day | 2% / 5% / None |
| Max Total Drawdown | Max loss from peak | 5% / 10% / 20% |
| Max Concentration | Max % in single instrument | 20% / 50% / 100% |
| Max Correlation Exposure | Max % in correlated instruments | 40% / 70% / 100% |
| Cooling Off Rule | Pause after X% daily loss | After 3% / None |
| Hard Block Mode | Prevent or just warn on breach | true / false |

## Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Language | Python 3.10+ | Rich ecosystem, rapid development |
| Database | SQLite (local) / PostgreSQL (hosted) | Portable or scalable |
| Dashboard | Streamlit → FastAPI + React (v2) | Fast MVP, upgradeable |
| Visualization | Plotly, Lightweight Charts | Interactive, professional |
| Indicators | pandas-ta, TA-Lib | Comprehensive libraries |
| Backtesting | Backtrader, Vectorbt | Flexible frameworks |
| Broker APIs | CCXT, OANDA, IB API | Multi-broker support |
| Price Data | yfinance, CCXT, OANDA | Free and paid options |
| Alerts | Telegram, Discord, Email | User preference |
| Deployment | Docker, Railway, AWS | Portable, scalable |

## Project Structure

```
halfkelly/
├── src/
│   └── halfkelly/
│       ├── __init__.py
│       ├── calculators/
│       │   ├── __init__.py
│       │   └── position_sizing.py
│       ├── instruments/
│       │   ├── __init__.py
│       │   └── forex.py
│       └── utils/
│           ├── __init__.py
│           └── formatting.py
├── tests/
│   ├── __init__.py
│   ├── test_position_sizing.py
│   └── test_instruments.py
├── docs/
│   ├── README.md
│   ├── getting_started.md
│   ├── api_reference.md
│   └── instruments.md
├── examples/
│   ├── basic_usage.py
│   ├── step_by_step.py
│   └── custom_instrument.py
├── pyproject.toml
└── README.md
```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=halfkelly --cov-report=term-missing
```

## Documentation

- [Getting Started](docs/getting_started.md)
- [API Reference](docs/api_reference.md)
- [Instruments](docs/instruments.md)

## Examples

Run the example scripts:

```bash
python examples/basic_usage.py
python examples/step_by_step.py
python examples/custom_instrument.py
```

## Repository

GitHub: https://github.com/the-lost-dev/halfkelly.git

## License

MIT
