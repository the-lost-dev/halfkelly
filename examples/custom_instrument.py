#!/usr/bin/env python3
"""
Custom Instrument Example

Demonstrates how to create and use custom instrument configurations.
"""

import sys
from pathlib import Path

# Add src to path for imports when running directly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aperion import size_position, print_trade_summary
from aperion.calculators.position_sizing import validate_instrument


def main():
    print("=" * 60)
    print("APERION - Custom Instrument Examples")
    print("=" * 60)

    # Example 1: AUD/USD (USD quote currency - standard pip value)
    print("\n" + "-" * 60)
    print("Example 1: Custom AUD/USD Configuration")
    print("-" * 60)

    AUDUSD = {
        "pip_size": 0.0001,     # Fourth decimal
        "pip_value": 10.0,      # $10 per pip (USD quote)
        "lot_increment": 0.01,  # Micro lots
    }

    # Validate the instrument
    validate_instrument(AUDUSD)
    print("Instrument validated successfully!")

    trade1 = size_position(
        instrument=AUDUSD,
        account_balance=10000,
        risk_percent=1.0,
        entry_price=0.65000,
        stop_loss=0.64500,
        take_profit=0.66000,
        instrument_name="AUD/USD"
    )
    print_trade_summary(trade1)

    # Example 2: EUR/GBP (Cross pair with variable pip value)
    print("-" * 60)
    print("Example 2: Custom EUR/GBP Configuration")
    print("-" * 60)

    # For EUR/GBP, pip value depends on GBP/USD rate
    # At GBP/USD = 1.27: pip_value = 10 * 1.27 = $12.70
    EURGBP = {
        "pip_size": 0.0001,
        "pip_value": 12.70,     # Variable - update based on GBP/USD
        "lot_increment": 0.01,
    }

    validate_instrument(EURGBP)
    print("Instrument validated successfully!")

    trade2 = size_position(
        instrument=EURGBP,
        account_balance=10000,
        risk_percent=1.5,
        entry_price=0.85500,
        stop_loss=0.85800,
        take_profit=0.84900,
        instrument_name="EUR/GBP"
    )
    print_trade_summary(trade2)

    # Example 3: Crypto (BTC/USD with different lot size)
    print("-" * 60)
    print("Example 3: Custom BTC/USD Configuration")
    print("-" * 60)

    # BTC/USD: 1 lot = 1 BTC, pip = $1
    BTCUSD = {
        "pip_size": 1.0,        # $1 movement
        "pip_value": 1.0,       # $1 per pip per BTC
        "lot_increment": 0.001, # Can trade 0.001 BTC increments
    }

    validate_instrument(BTCUSD)
    print("Instrument validated successfully!")

    trade3 = size_position(
        instrument=BTCUSD,
        account_balance=50000,
        risk_percent=2.0,
        entry_price=42000,
        stop_loss=41000,
        take_profit=44000,
        instrument_name="BTC/USD"
    )
    print_trade_summary(trade3)

    # Example 4: Show validation error
    print("-" * 60)
    print("Example 4: Validation Error Handling")
    print("-" * 60)

    invalid_instrument = {
        "pip_size": 0.0001,
        # Missing pip_value and lot_increment
    }

    try:
        validate_instrument(invalid_instrument)
    except ValueError as e:
        print(f"Validation failed (expected): {e}")

    print("\n" + "=" * 60)
    print("Custom Instrument Guidelines:")
    print("=" * 60)
    print("""
    1. pip_size: The minimum price movement for the instrument
       - Most forex pairs: 0.0001 (4th decimal)
       - JPY pairs: 0.01 (2nd decimal)
       - Crypto: Varies by exchange

    2. pip_value: Dollar value per pip per standard lot
       - USD quote pairs: Fixed at $10
       - Other pairs: Calculate based on quote currency rate
       - Formula: 10 * (quote_currency / USD)

    3. lot_increment: Minimum position size you can trade
       - Standard: 1.0 (100,000 units)
       - Mini: 0.1 (10,000 units)
       - Micro: 0.01 (1,000 units)
       - Nano: 0.001 (100 units)
    """)


if __name__ == "__main__":
    main()
