# Aperion

A Forex Risk Management Engine for calculating position sizes and managing trade risk.

## Features

- **Position Sizing**: Calculate optimal position sizes based on account risk parameters
- **Risk Management**: Never risk more than intended with conservative rounding
- **Multiple Instruments**: Pre-configured forex pairs and commodities
- **Pure Functions**: Simple, composable functions with no side effects
- **No Dependencies**: Zero external runtime dependencies

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
from aperion import size_position, EURUSD, print_trade_summary

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

## Core Formula

```
Position Size = Risk Amount ÷ Risk Per Lot

Where:
  Risk Amount = Account Balance × Risk Percentage
  Risk Per Lot = Stop Distance (pips) × Pip Value
```

## Available Instruments

| Instrument | Pip Size | Pip Value |
|------------|----------|-----------|
| EUR/USD    | 0.0001   | $10.00    |
| GBP/USD    | 0.0001   | $10.00    |
| USD/JPY    | 0.01     | $6.67     |
| GBP/JPY    | 0.01     | $6.67     |
| XAU/USD    | 0.01     | $1.00     |

## Project Structure

```
aperion/
├── src/
│   └── aperion/
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
pytest --cov=aperion --cov-report=term-missing
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

## License

MIT
