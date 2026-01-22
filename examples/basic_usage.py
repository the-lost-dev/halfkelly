#!/usr/bin/env python3
"""
Basic Usage Example

Demonstrates core position sizing functionality with various forex pairs.
"""

import sys
from pathlib import Path

# Add src to path for imports when running directly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from halfkelly import (
    size_position,
    print_trade_summary,
    EURUSD,
    USDJPY,
    XAUUSD,
)


def main():
    print("=" * 60)
    print("HALFKELLY - Position Sizing Examples")
    print("=" * 60)

    # Example 1: EUR/USD Short
    print("\n" + "=" * 60)
    print("Example 1: EUR/USD Short Position")
    print("Account: $10,000 | Risk: 2%")
    print("Entry: 1.17300 | Stop: 1.18218 | Target: 1.15000")
    print("=" * 60)

    trade1 = size_position(
        instrument=EURUSD,
        account_balance=10000,
        risk_percent=2.0,
        entry_price=1.17300,
        stop_loss=1.18218,
        take_profit=1.15000,
        instrument_name="EUR/USD"
    )
    print_trade_summary(trade1)

    # Example 2: EUR/USD Long
    print("=" * 60)
    print("Example 2: EUR/USD Long Position")
    print("Account: $10,000 | Risk: 1%")
    print("Entry: 1.08500 | Stop: 1.08000 | Target: 1.09500")
    print("=" * 60)

    trade2 = size_position(
        instrument=EURUSD,
        account_balance=10000,
        risk_percent=1.0,
        entry_price=1.08500,
        stop_loss=1.08000,
        take_profit=1.09500,
        instrument_name="EUR/USD"
    )
    print_trade_summary(trade2)

    # Example 3: USD/JPY Long
    print("=" * 60)
    print("Example 3: USD/JPY Long Position")
    print("Account: $10,000 | Risk: 1%")
    print("Entry: 150.500 | Stop: 149.500 | Target: 152.500")
    print("=" * 60)

    trade3 = size_position(
        instrument=USDJPY,
        account_balance=10000,
        risk_percent=1.0,
        entry_price=150.500,
        stop_loss=149.500,
        take_profit=152.500,
        instrument_name="USD/JPY"
    )
    print_trade_summary(trade3)

    # Example 4: Gold (XAU/USD) Long
    print("=" * 60)
    print("Example 4: Gold (XAU/USD) Long Position")
    print("Account: $25,000 | Risk: 1.5%")
    print("Entry: 2000.00 | Stop: 1985.00 | Target: 2030.00")
    print("=" * 60)

    trade4 = size_position(
        instrument=XAUUSD,
        account_balance=25000,
        risk_percent=1.5,
        entry_price=2000.00,
        stop_loss=1985.00,
        take_profit=2030.00,
        instrument_name="XAU/USD"
    )
    print_trade_summary(trade4)

    # Example 5: Without take profit
    print("=" * 60)
    print("Example 5: EUR/USD Without Take Profit")
    print("Account: $10,000 | Risk: 1%")
    print("Entry: 1.10000 | Stop: 1.09800 | Target: None")
    print("=" * 60)

    trade5 = size_position(
        instrument=EURUSD,
        account_balance=10000,
        risk_percent=1.0,
        entry_price=1.10000,
        stop_loss=1.09800,
        instrument_name="EUR/USD"
    )
    print_trade_summary(trade5)


if __name__ == "__main__":
    main()
