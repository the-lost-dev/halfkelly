"""
Forex Instrument Configurations

This module defines instrument specifications for forex pairs and commodities.
Each instrument configuration includes:

- pip_size: Minimum price movement (e.g., 0.0001 for EUR/USD, 0.01 for JPY pairs)
- pip_value: Dollar value per pip per standard lot (1.0 lot = 100,000 units)
- lot_increment: Minimum position size increment (typically 0.01 for micro lots)

Note on pip values:
    Pip values can vary based on the quote currency and current exchange rates.
    The values provided here are approximations for USD-denominated accounts.
    For precise calculations, pip values should be updated based on current rates.
"""

# Major Pairs (USD as quote currency)
EURUSD: dict[str, float] = {
    "pip_size": 0.0001,
    "pip_value": 10.0,
    "lot_increment": 0.01,
}

GBPUSD: dict[str, float] = {
    "pip_size": 0.0001,
    "pip_value": 10.0,
    "lot_increment": 0.01,
}

# JPY Pairs (different pip size due to JPY denomination)
USDJPY: dict[str, float] = {
    "pip_size": 0.01,
    "pip_value": 6.67,  # Approximate, varies with USD/JPY rate
    "lot_increment": 0.01,
}

GBPJPY: dict[str, float] = {
    "pip_size": 0.01,
    "pip_value": 6.67,  # Approximate, varies with USD/JPY rate
    "lot_increment": 0.01,
}

# Commodities
XAUUSD: dict[str, float] = {
    "pip_size": 0.01,
    "pip_value": 1.0,  # $1 per pip per lot (100 oz)
    "lot_increment": 0.01,
}

# Registry of all instruments
_INSTRUMENTS: dict[str, dict[str, float]] = {
    "EURUSD": EURUSD,
    "EUR/USD": EURUSD,
    "GBPUSD": GBPUSD,
    "GBP/USD": GBPUSD,
    "USDJPY": USDJPY,
    "USD/JPY": USDJPY,
    "GBPJPY": GBPJPY,
    "GBP/JPY": GBPJPY,
    "XAUUSD": XAUUSD,
    "XAU/USD": XAUUSD,
    "GOLD": XAUUSD,
}


def get_instrument(name: str) -> dict[str, float] | None:
    """
    Get instrument configuration by name.

    Args:
        name: Instrument name (e.g., "EURUSD", "EUR/USD", "GOLD").
              Case-insensitive.

    Returns:
        Instrument configuration dict or None if not found.

    Example:
        >>> inst = get_instrument("EURUSD")
        >>> inst["pip_size"]
        0.0001
        >>> get_instrument("EUR/USD") == get_instrument("EURUSD")
        True
    """
    return _INSTRUMENTS.get(name.upper())


def list_instruments() -> list[str]:
    """
    List all available instrument names.

    Returns:
        List of canonical instrument names (without slash variants).

    Example:
        >>> list_instruments()
        ['EURUSD', 'GBPUSD', 'USDJPY', 'GBPJPY', 'XAUUSD']
    """
    # Return only canonical names (without slashes)
    return [name for name in _INSTRUMENTS.keys() if "/" not in name and name != "GOLD"]
