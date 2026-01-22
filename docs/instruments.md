# Instruments

HalfKelly includes pre-configured instruments for common forex pairs and commodities.

## Instrument Configuration

Each instrument is defined as a dictionary with three required fields:

| Field | Description | Example |
|-------|-------------|---------|
| `pip_size` | Minimum price movement | 0.0001 (EUR/USD), 0.01 (JPY pairs) |
| `pip_value` | Dollar value per pip per standard lot | 10.0 (EUR/USD) |
| `lot_increment` | Minimum position size increment | 0.01 (micro lot) |

## Available Instruments

### Major Pairs (USD Quote Currency)

#### EUR/USD
```python
EURUSD = {
    "pip_size": 0.0001,
    "pip_value": 10.0,
    "lot_increment": 0.01
}
```
- **Pip Size**: Fourth decimal place (0.0001)
- **Pip Value**: $10 per pip per standard lot (100,000 units)
- Standard pip value because USD is the quote currency

#### GBP/USD
```python
GBPUSD = {
    "pip_size": 0.0001,
    "pip_value": 10.0,
    "lot_increment": 0.01
}
```
- Same structure as EUR/USD
- Standard pip value because USD is the quote currency

### JPY Pairs

#### USD/JPY
```python
USDJPY = {
    "pip_size": 0.01,
    "pip_value": 6.67,
    "lot_increment": 0.01
}
```
- **Pip Size**: Second decimal place (0.01) due to JPY denomination
- **Pip Value**: ~$6.67 per pip (varies with USD/JPY exchange rate)

#### GBP/JPY
```python
GBPJPY = {
    "pip_size": 0.01,
    "pip_value": 6.67,
    "lot_increment": 0.01
}
```
- Cross pair with JPY
- Pip value dependent on USD/JPY rate

### Commodities

#### XAU/USD (Gold)
```python
XAUUSD = {
    "pip_size": 0.01,
    "pip_value": 1.0,
    "lot_increment": 0.01
}
```
- **Pip Size**: $0.01 movement
- **Pip Value**: $1 per pip per lot (1 lot = 100 oz)
- Can also be accessed via `get_instrument("GOLD")`

## Understanding Pip Values

### Fixed vs Variable Pip Values

For pairs where USD is the **quote currency** (EUR/USD, GBP/USD):
- Pip value is fixed at $10 per pip per standard lot

For pairs where USD is the **base currency** or cross pairs:
- Pip value varies with exchange rates
- The values in HalfKelly are approximations
- For precise calculations, update pip values based on current rates

### Calculating Variable Pip Values

For USD/JPY and other JPY pairs:
```
Pip Value = (0.01 / USD/JPY rate) × 100,000
```

Example at USD/JPY = 150.00:
```
Pip Value = (0.01 / 150.00) × 100,000 = $6.67
```

## Adding Custom Instruments

You can create custom instrument configurations:

```python
# Custom instrument
AUDUSD = {
    "pip_size": 0.0001,
    "pip_value": 10.0,
    "lot_increment": 0.01
}

# Use with size_position
from halfkelly import size_position

trade = size_position(
    instrument=AUDUSD,
    account_balance=10000,
    risk_percent=1.0,
    entry_price=0.65000,
    stop_loss=0.64500,
    instrument_name="AUD/USD"
)
```

## Instrument Validation

HalfKelly validates that instruments contain required keys:

```python
from halfkelly.calculators.position_sizing import validate_instrument

# This will raise ValueError
invalid_instrument = {"pip_size": 0.0001}
validate_instrument(invalid_instrument)
# ValueError: Instrument missing required keys: {'pip_value', 'lot_increment'}
```

## Lookup Functions

### By Name
```python
from halfkelly import get_instrument

# All of these work:
inst = get_instrument("EURUSD")    # Canonical
inst = get_instrument("EUR/USD")   # With slash
inst = get_instrument("eurusd")    # Lowercase
inst = get_instrument("GOLD")      # Alias
```

### List All
```python
from halfkelly import list_instruments

instruments = list_instruments()
# ['EURUSD', 'GBPUSD', 'USDJPY', 'GBPJPY', 'XAUUSD']
```
