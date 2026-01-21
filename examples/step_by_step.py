#!/usr/bin/env python3
"""
Step-by-Step Calculation Example

Demonstrates using individual functions for detailed position sizing calculations.
"""

import sys
from pathlib import Path

# Add src to path for imports when running directly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from aperion import (
    calculate_stop_distance_pips,
    calculate_risk_amount,
    calculate_risk_per_lot,
    calculate_position_size,
    calculate_reward_risk_ratio,
    EURUSD,
)


def main():
    print("=" * 60)
    print("APERION - Step-by-Step Position Sizing")
    print("=" * 60)

    # Trade parameters
    instrument = EURUSD
    account_balance = 10000
    risk_percent = 2.0
    entry_price = 1.17300
    stop_loss = 1.18218
    take_profit = 1.15000

    print("\nTrade Setup:")
    print(f"  Instrument:      EUR/USD")
    print(f"  Account Balance: ${account_balance:,.2f}")
    print(f"  Risk Percent:    {risk_percent}%")
    print(f"  Entry Price:     {entry_price}")
    print(f"  Stop Loss:       {stop_loss}")
    print(f"  Take Profit:     {take_profit}")

    print("\n" + "-" * 60)
    print("Step 1: Calculate Stop Distance in Pips")
    print("-" * 60)

    stop_pips = calculate_stop_distance_pips(
        entry_price=entry_price,
        stop_loss=stop_loss,
        pip_size=instrument["pip_size"]
    )
    print(f"  Formula: |entry - stop| / pip_size")
    print(f"  Calculation: |{entry_price} - {stop_loss}| / {instrument['pip_size']}")
    print(f"  Result: {stop_pips} pips")

    print("\n" + "-" * 60)
    print("Step 2: Calculate Risk Amount in Dollars")
    print("-" * 60)

    risk_amount = calculate_risk_amount(
        account_balance=account_balance,
        risk_percent=risk_percent
    )
    print(f"  Formula: account_balance × (risk_percent / 100)")
    print(f"  Calculation: ${account_balance:,.2f} × ({risk_percent} / 100)")
    print(f"  Result: ${risk_amount:.2f}")

    print("\n" + "-" * 60)
    print("Step 3: Calculate Risk Per Lot")
    print("-" * 60)

    risk_per_lot = calculate_risk_per_lot(
        stop_pips=stop_pips,
        pip_value=instrument["pip_value"]
    )
    print(f"  Formula: stop_pips × pip_value")
    print(f"  Calculation: {stop_pips} × ${instrument['pip_value']}")
    print(f"  Result: ${risk_per_lot:.2f} per lot")

    print("\n" + "-" * 60)
    print("Step 4: Calculate Position Size")
    print("-" * 60)

    raw_position = risk_amount / risk_per_lot
    position_size = calculate_position_size(
        risk_amount=risk_amount,
        risk_per_lot=risk_per_lot,
        lot_increment=instrument["lot_increment"]
    )
    print(f"  Formula: risk_amount / risk_per_lot (rounded DOWN)")
    print(f"  Calculation: ${risk_amount:.2f} / ${risk_per_lot:.2f}")
    print(f"  Raw Result: {raw_position:.4f} lots")
    print(f"  Rounded Down: {position_size:.2f} lots")

    print("\n" + "-" * 60)
    print("Step 5: Calculate Actual Risk")
    print("-" * 60)

    actual_risk = position_size * risk_per_lot
    actual_risk_percent = (actual_risk / account_balance) * 100
    print(f"  Formula: position_size × risk_per_lot")
    print(f"  Calculation: {position_size:.2f} × ${risk_per_lot:.2f}")
    print(f"  Actual Risk: ${actual_risk:.2f} ({actual_risk_percent:.2f}%)")
    print(f"  Intended Risk: ${risk_amount:.2f} ({risk_percent}%)")
    print(f"  Savings from rounding: ${risk_amount - actual_risk:.2f}")

    print("\n" + "-" * 60)
    print("Step 6: Calculate Reward/Risk Ratio")
    print("-" * 60)

    rr_ratio = calculate_reward_risk_ratio(
        entry=entry_price,
        stop=stop_loss,
        target=take_profit
    )
    potential_reward = actual_risk * rr_ratio
    print(f"  Formula: |target - entry| / |entry - stop|")
    print(f"  Calculation: |{take_profit} - {entry_price}| / |{entry_price} - {stop_loss}|")
    print(f"  R:R Ratio: {rr_ratio:.2f}:1")
    print(f"  Potential Reward: ${potential_reward:.2f}")

    print("\n" + "=" * 60)
    print("Final Trade Summary")
    print("=" * 60)
    print(f"  Direction:        SHORT (stop above entry)")
    print(f"  Position Size:    {position_size:.2f} lots")
    print(f"  Stop Distance:    {stop_pips:.1f} pips")
    print(f"  Risk:             ${actual_risk:.2f} ({actual_risk_percent:.2f}%)")
    print(f"  Reward:           ${potential_reward:.2f}")
    print(f"  R:R Ratio:        {rr_ratio:.2f}:1")
    print("=" * 60)


if __name__ == "__main__":
    main()
