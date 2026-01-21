# API Reference

Complete API documentation for Aperion.

## Position Sizing Functions

### `size_position()`

Calculate complete position sizing for a trade.

```python
def size_position(
    instrument: dict[str, float],
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss: float,
    take_profit: Optional[float] = None,
    instrument_name: str = "UNKNOWN"
) -> dict
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `instrument` | `dict` | Instrument config with `pip_size`, `pip_value`, `lot_increment` |
| `account_balance` | `float` | Account balance in dollars |
| `risk_percent` | `float` | Risk percentage (e.g., 2.0 for 2%) |
| `entry_price` | `float` | Trade entry price |
| `stop_loss` | `float` | Stop loss price |
| `take_profit` | `float` | Optional take profit price |
| `instrument_name` | `str` | Display name for the instrument |

**Returns:** Dictionary with trade details (see [Getting Started](getting_started.md#understanding-the-output))

**Example:**
```python
from aperion import size_position, EURUSD

trade = size_position(
    instrument=EURUSD,
    account_balance=10000,
    risk_percent=2.0,
    entry_price=1.17300,
    stop_loss=1.18218,
    take_profit=1.15000,
    instrument_name="EUR/USD"
)
```

---

### `calculate_stop_distance_pips()`

Calculate the distance between entry and stop loss in pips.

```python
def calculate_stop_distance_pips(
    entry_price: float,
    stop_loss: float,
    pip_size: float
) -> float
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `entry_price` | `float` | Entry price for the trade |
| `stop_loss` | `float` | Stop loss price |
| `pip_size` | `float` | Minimum price movement (e.g., 0.0001 for EUR/USD) |

**Returns:** Stop distance in pips (always positive)

**Example:**
```python
from aperion import calculate_stop_distance_pips

pips = calculate_stop_distance_pips(1.17300, 1.18218, 0.0001)
print(pips)  # 91.8
```

---

### `calculate_risk_amount()`

Calculate the dollar amount to risk.

```python
def calculate_risk_amount(
    account_balance: float,
    risk_percent: float
) -> float
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `account_balance` | `float` | Total account balance in dollars |
| `risk_percent` | `float` | Percentage of account to risk |

**Returns:** Dollar amount to risk

**Example:**
```python
from aperion import calculate_risk_amount

risk = calculate_risk_amount(10000, 2.0)
print(risk)  # 200.0
```

---

### `calculate_risk_per_lot()`

Calculate the dollar risk per standard lot.

```python
def calculate_risk_per_lot(
    stop_pips: float,
    pip_value: float
) -> float
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `stop_pips` | `float` | Stop distance in pips |
| `pip_value` | `float` | Dollar value per pip per standard lot |

**Returns:** Dollar risk per lot

**Example:**
```python
from aperion import calculate_risk_per_lot

risk_per_lot = calculate_risk_per_lot(91.8, 10.0)
print(risk_per_lot)  # 918.0
```

---

### `calculate_position_size()`

Calculate position size rounded down to nearest lot increment.

```python
def calculate_position_size(
    risk_amount: float,
    risk_per_lot: float,
    lot_increment: float
) -> float
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `risk_amount` | `float` | Dollar amount willing to risk |
| `risk_per_lot` | `float` | Dollar risk per standard lot |
| `lot_increment` | `float` | Minimum position size increment |

**Returns:** Position size in lots (rounded down)

**Example:**
```python
from aperion import calculate_position_size

lots = calculate_position_size(200.0, 918.0, 0.01)
print(lots)  # 0.21
```

---

### `calculate_reward_risk_ratio()`

Calculate the reward-to-risk ratio.

```python
def calculate_reward_risk_ratio(
    entry: float,
    stop: float,
    target: float
) -> float
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `entry` | `float` | Entry price |
| `stop` | `float` | Stop loss price |
| `target` | `float` | Take profit price |

**Returns:** Reward-to-risk ratio

**Example:**
```python
from aperion import calculate_reward_risk_ratio

rr = calculate_reward_risk_ratio(1.08500, 1.08000, 1.09500)
print(rr)  # 2.0
```

---

## Instrument Functions

### `get_instrument()`

Get instrument configuration by name.

```python
def get_instrument(name: str) -> Optional[dict[str, float]]
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Instrument name (case-insensitive) |

**Returns:** Instrument configuration dict or `None` if not found

**Example:**
```python
from aperion import get_instrument

eurusd = get_instrument("EUR/USD")  # Works with slash
usdjpy = get_instrument("usdjpy")   # Case-insensitive
gold = get_instrument("GOLD")       # Alias for XAUUSD
```

---

### `list_instruments()`

List all available instrument names.

```python
def list_instruments() -> list[str]
```

**Returns:** List of canonical instrument names

**Example:**
```python
from aperion import list_instruments

instruments = list_instruments()
print(instruments)  # ['EURUSD', 'GBPUSD', 'USDJPY', 'GBPJPY', 'XAUUSD']
```

---

## Formatting Functions

### `print_trade_summary()`

Print a formatted trade summary to stdout.

```python
def print_trade_summary(trade: dict) -> None
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `trade` | `dict` | Dictionary returned by `size_position()` |

---

### `format_trade_summary()`

Format a trade summary as a string.

```python
def format_trade_summary(trade: dict) -> str
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `trade` | `dict` | Dictionary returned by `size_position()` |

**Returns:** Formatted string representation
