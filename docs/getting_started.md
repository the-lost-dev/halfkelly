# Getting Started

This guide will help you get up and running with Aperion quickly.

## Installation

### From Source

```bash
git clone <repository-url>
cd aperion
pip install -e .
```

### Dependencies

Aperion has no external runtime dependencies. For development:

```bash
pip install -e ".[dev]"
```

## Basic Usage

### Quick Position Sizing

```python
from aperion import size_position, EURUSD, print_trade_summary

# Calculate position size for a EUR/USD trade
trade = size_position(
    instrument=EURUSD,
    account_balance=10000,      # $10,000 account
    risk_percent=2.0,           # Risk 2% per trade
    entry_price=1.08500,        # Entry at 1.08500
    stop_loss=1.08000,          # Stop at 1.08000 (50 pips)
    take_profit=1.09500,        # Target at 1.09500 (100 pips)
    instrument_name="EUR/USD"
)

# Print formatted summary
print_trade_summary(trade)
```

Output:
```
==================================================
  EUR/USD - LONG
==================================================
  Stop Distance:    50.0 pips
  Position Size:    0.20 lots
  Risk Amount:      $100.00
  Risk Percent:     1.00%
  R:R Ratio:        2.00:1
  Potential Reward: $200.00
==================================================
```

### Using Individual Functions

For more control, use the individual calculation functions:

```python
from aperion import (
    calculate_stop_distance_pips,
    calculate_risk_amount,
    calculate_risk_per_lot,
    calculate_position_size,
)
from aperion.instruments import EURUSD

# Step-by-step calculation
entry = 1.08500
stop = 1.08000
account = 10000
risk_pct = 2.0

# 1. Calculate stop distance in pips
stop_pips = calculate_stop_distance_pips(entry, stop, EURUSD["pip_size"])
print(f"Stop distance: {stop_pips} pips")

# 2. Calculate dollar amount to risk
risk_amount = calculate_risk_amount(account, risk_pct)
print(f"Risk amount: ${risk_amount}")

# 3. Calculate risk per lot
risk_per_lot = calculate_risk_per_lot(stop_pips, EURUSD["pip_value"])
print(f"Risk per lot: ${risk_per_lot}")

# 4. Calculate position size
position_size = calculate_position_size(risk_amount, risk_per_lot, EURUSD["lot_increment"])
print(f"Position size: {position_size} lots")
```

### Looking Up Instruments

```python
from aperion import get_instrument, list_instruments

# Get instrument by name (case-insensitive, with or without slash)
eurusd = get_instrument("EUR/USD")
usdjpy = get_instrument("usdjpy")
gold = get_instrument("GOLD")  # Alias for XAUUSD

# List all available instruments
instruments = list_instruments()
print(instruments)  # ['EURUSD', 'GBPUSD', 'USDJPY', 'GBPJPY', 'XAUUSD']
```

## Understanding the Output

The `size_position()` function returns a dictionary with:

| Key | Description |
|-----|-------------|
| `instrument_name` | Name of the instrument |
| `direction` | "LONG" or "SHORT" based on stop position |
| `stop_distance_pips` | Distance from entry to stop in pips |
| `position_size` | Calculated position size in lots |
| `actual_risk_amount` | Actual dollar risk (may be less than intended) |
| `actual_risk_percent` | Actual risk as % of account |
| `reward_risk_ratio` | R:R ratio (only if take_profit provided) |
| `potential_reward` | Potential profit in dollars (only if take_profit provided) |

## Next Steps

- See [API Reference](api_reference.md) for complete function documentation
- Check [Examples](../examples/) for more use cases
- Read [Instruments](instruments.md) to understand instrument configurations
