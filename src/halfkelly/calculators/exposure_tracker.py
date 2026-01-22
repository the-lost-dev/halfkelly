"""
Multi-Position Exposure Tracker

Track and analyze risk exposure across multiple positions and accounts.
Integrates with position_sizing.py for risk calculations.

This module provides:
- Account management (create accounts with different currencies)
- Position tracking (create, add, remove positions)
- Exposure analysis (total risk, risk by instrument/direction, largest position)
"""

from halfkelly.calculators.position_sizing import (
    calculate_risk_per_lot,
    calculate_stop_distance_pips,
)
from halfkelly.instruments.forex import (
    get_instrument,
)

# Currency symbols mapping
_CURRENCY_SYMBOLS: dict[str, str] = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CHF": "CHF",
    "AUD": "A$",
    "CAD": "C$",
    "NZD": "NZ$",
}


def get_currency_symbol(currency_code: str) -> str:
    """
    Get the currency symbol for a currency code.

    Args:
        currency_code: ISO currency code (e.g., "USD", "EUR", "GBP").

    Returns:
        Currency symbol (e.g., "$", "€", "£") or the code itself if unknown.

    Example:
        >>> get_currency_symbol("USD")
        '$'
        >>> get_currency_symbol("EUR")
        '€'
        >>> get_currency_symbol("XYZ")
        'XYZ'
    """
    return _CURRENCY_SYMBOLS.get(currency_code.upper(), currency_code)


def create_account(account_id: str, name: str, balance: float, currency: str) -> dict:
    """
    Create an account data structure.

    Args:
        account_id: Unique identifier for the account.
        name: Human-readable name (e.g., "Main Trading", "Prop Firm Challenge").
        balance: Account balance in the account's currency.
        currency: Account currency code (e.g., "USD", "EUR", "GBP").

    Returns:
        Account dictionary with all fields.

    Example:
        >>> account = create_account("acc1", "Main Trading", 10000, "USD")
        >>> account["balance"]
        10000
        >>> account["currency"]
        'USD'
    """
    return {
        "account_id": account_id,
        "name": name,
        "balance": balance,
        "currency": currency.upper(),
    }


def create_position(
    position_id: str,
    account: dict,
    instrument: str,
    direction: str,
    size: float,
    entry_price: float,
    stop_loss: float,
) -> dict:
    """
    Create a position data structure with calculated risk amount.

    Uses position_sizing module to calculate the risk amount based on
    the position size, entry price, and stop loss.

    Args:
        position_id: Unique identifier for the position.
        account: Account dictionary (from create_account).
        instrument: Instrument name (e.g., "EURUSD", "GBPUSD").
        direction: Trade direction ("LONG" or "SHORT").
        size: Position size in lots.
        entry_price: Entry price for the trade.
        stop_loss: Stop loss price.

    Returns:
        Position dictionary with calculated risk_amount.

    Raises:
        ValueError: If instrument is not found or direction is invalid.

    Example:
        >>> account = create_account("acc1", "Main Trading", 10000, "USD")
        >>> position = create_position(
        ...     "pos1", account, "EURUSD", "SHORT",
        ...     0.08, 1.17300, 1.18218
        ... )
        >>> position["size"]
        0.08
        >>> position["risk_amount"]  # ~$73.44
        73.44
    """
    inst_config = get_instrument(instrument)
    if inst_config is None:
        raise ValueError(f"Unknown instrument: {instrument}")

    direction_upper = direction.upper()
    if direction_upper not in ("LONG", "SHORT"):
        raise ValueError(f"Invalid direction: {direction}. Must be 'LONG' or 'SHORT'.")

    # Calculate risk amount using position_sizing functions
    pip_size = inst_config["pip_size"]
    pip_value = inst_config["pip_value"]

    stop_distance_pips = calculate_stop_distance_pips(entry_price, stop_loss, pip_size)
    risk_per_lot = calculate_risk_per_lot(stop_distance_pips, pip_value)
    risk_amount = size * risk_per_lot

    return {
        "position_id": position_id,
        "account_id": account["account_id"],
        "instrument": instrument.upper(),
        "direction": direction_upper,
        "size": size,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "risk_amount": round(risk_amount, 2),
    }


def add_position(portfolio: list[dict], position: dict) -> list[dict]:
    """
    Add a position to the portfolio.

    Args:
        portfolio: List of position dictionaries.
        position: Position dictionary to add.

    Returns:
        Updated portfolio with the new position appended.

    Example:
        >>> portfolio = []
        >>> account = create_account("acc1", "Main Trading", 10000, "USD")
        >>> pos = create_position("pos1", account, "EURUSD", "LONG", 0.1, 1.08500, 1.08000)
        >>> portfolio = add_position(portfolio, pos)
        >>> len(portfolio)
        1
    """
    return portfolio + [position]


def remove_position(portfolio: list[dict], position_id: str) -> list[dict]:
    """
    Remove a position from the portfolio by ID.

    Args:
        portfolio: List of position dictionaries.
        position_id: ID of the position to remove.

    Returns:
        Updated portfolio without the specified position.

    Example:
        >>> portfolio = [{"position_id": "pos1"}, {"position_id": "pos2"}]
        >>> portfolio = remove_position(portfolio, "pos1")
        >>> len(portfolio)
        1
        >>> portfolio[0]["position_id"]
        'pos2'
    """
    return [p for p in portfolio if p["position_id"] != position_id]


def get_positions_by_instrument(portfolio: list[dict], instrument: str) -> list[dict]:
    """
    Filter positions by instrument.

    Args:
        portfolio: List of position dictionaries.
        instrument: Instrument name to filter by (case-insensitive).

    Returns:
        List of positions matching the instrument.

    Example:
        >>> portfolio = [
        ...     {"position_id": "1", "instrument": "EURUSD"},
        ...     {"position_id": "2", "instrument": "GBPUSD"},
        ...     {"position_id": "3", "instrument": "EURUSD"},
        ... ]
        >>> filtered = get_positions_by_instrument(portfolio, "EURUSD")
        >>> len(filtered)
        2
    """
    instrument_upper = instrument.upper()
    return [p for p in portfolio if p["instrument"] == instrument_upper]


def get_positions_by_direction(portfolio: list[dict], direction: str) -> list[dict]:
    """
    Filter positions by direction.

    Args:
        portfolio: List of position dictionaries.
        direction: Direction to filter by ("LONG" or "SHORT", case-insensitive).

    Returns:
        List of positions matching the direction.

    Example:
        >>> portfolio = [
        ...     {"position_id": "1", "direction": "LONG"},
        ...     {"position_id": "2", "direction": "SHORT"},
        ...     {"position_id": "3", "direction": "LONG"},
        ... ]
        >>> filtered = get_positions_by_direction(portfolio, "LONG")
        >>> len(filtered)
        2
    """
    direction_upper = direction.upper()
    return [p for p in portfolio if p["direction"] == direction_upper]


def calculate_total_exposure(portfolio: list[dict], account: dict) -> dict:
    """
    Calculate total exposure metrics for an account's positions.

    Args:
        portfolio: List of all position dictionaries.
        account: Account dictionary to calculate exposure for.

    Returns:
        Dictionary containing:
            - total_risk_amount: Sum of all position risks in account currency
            - total_risk_percent: Total risk as percentage of account balance
            - position_count: Number of open positions
            - risk_by_instrument: Dict mapping instrument to total risk
            - risk_by_direction: Dict with "LONG" and "SHORT" risk totals
            - largest_position: Position dict with highest risk (or None if empty)

    Example:
        >>> account = create_account("acc1", "Main Trading", 10000, "USD")
        >>> portfolio = []
        >>> pos1 = create_position("pos1", account, "EURUSD", "SHORT", 0.08, 1.17300, 1.18218)
        >>> pos2 = create_position("pos2", account, "EURUSD", "SHORT", 0.05, 1.17300, 1.18218)
        >>> portfolio = add_position(portfolio, pos1)
        >>> portfolio = add_position(portfolio, pos2)
        >>> exposure = calculate_total_exposure(portfolio, account)
        >>> exposure["position_count"]
        2
        >>> exposure["risk_by_direction"]["SHORT"] > 0
        True
    """
    # Filter positions for this account
    account_positions = [p for p in portfolio if p["account_id"] == account["account_id"]]

    if not account_positions:
        return {
            "total_risk_amount": 0.0,
            "total_risk_percent": 0.0,
            "position_count": 0,
            "risk_by_instrument": {},
            "risk_by_direction": {"LONG": 0.0, "SHORT": 0.0},
            "largest_position": None,
        }

    # Calculate totals
    total_risk_amount = sum(p["risk_amount"] for p in account_positions)
    total_risk_percent = (
        (total_risk_amount / account["balance"]) * 100 if account["balance"] > 0 else 0.0
    )

    # Risk by instrument
    risk_by_instrument: dict[str, float] = {}
    for p in account_positions:
        instrument = p["instrument"]
        risk_by_instrument[instrument] = risk_by_instrument.get(instrument, 0.0) + p["risk_amount"]

    # Risk by direction
    risk_by_direction = {"LONG": 0.0, "SHORT": 0.0}
    for p in account_positions:
        risk_by_direction[p["direction"]] += p["risk_amount"]

    # Largest position
    largest_position = max(account_positions, key=lambda p: p["risk_amount"])

    return {
        "total_risk_amount": round(total_risk_amount, 2),
        "total_risk_percent": round(total_risk_percent, 2),
        "position_count": len(account_positions),
        "risk_by_instrument": {k: round(v, 2) for k, v in risk_by_instrument.items()},
        "risk_by_direction": {k: round(v, 2) for k, v in risk_by_direction.items()},
        "largest_position": largest_position,
    }


def print_exposure_summary(exposure: dict, account: dict) -> str:
    """
    Generate a readable exposure summary string.

    Args:
        exposure: Exposure dictionary from calculate_total_exposure.
        account: Account dictionary for currency display.

    Returns:
        Formatted string with exposure details.

    Example:
        >>> account = create_account("acc1", "Main Trading", 10000, "USD")
        >>> exposure = {
        ...     "total_risk_amount": 193.20,
        ...     "total_risk_percent": 1.93,
        ...     "position_count": 3,
        ...     "risk_by_instrument": {"EURUSD": 193.20},
        ...     "risk_by_direction": {"LONG": 0.0, "SHORT": 193.20},
        ...     "largest_position": {"position_id": "pos1", "risk_amount": 73.44},
        ... }
        >>> summary = print_exposure_summary(exposure, account)
        >>> "Main Trading" in summary
        True
    """
    symbol = get_currency_symbol(account["currency"])
    lines = [
        f"=== Exposure Summary: {account['name']} ===",
        f"Account Balance: {symbol}{account['balance']:,.2f}",
        "",
        f"Total Risk: {symbol}{exposure['total_risk_amount']:,.2f} ({exposure['total_risk_percent']:.2f}%)",
        f"Open Positions: {exposure['position_count']}",
    ]

    if exposure["risk_by_instrument"]:
        lines.append("")
        lines.append("Risk by Instrument:")
        for instrument, risk in sorted(exposure["risk_by_instrument"].items()):
            lines.append(f"  {instrument}: {symbol}{risk:,.2f}")

    if exposure["risk_by_direction"]:
        lines.append("")
        lines.append("Risk by Direction:")
        for direction in ["LONG", "SHORT"]:
            risk = exposure["risk_by_direction"].get(direction, 0.0)
            lines.append(f"  {direction}: {symbol}{risk:,.2f}")

    if exposure["largest_position"]:
        lines.append("")
        pos = exposure["largest_position"]
        lines.append(
            f"Largest Position: {pos['position_id']} ({pos['instrument']} {pos['direction']})"
        )
        lines.append(f"  Risk: {symbol}{pos['risk_amount']:,.2f}")

    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("Exposure Tracker Tests")
    print("=" * 60)

    # Test 1: USD account, multiple positions same instrument
    print("\n--- Test 1: USD account, multiple EURUSD positions ---")
    account1 = create_account("acc1", "Main Trading", 10000, "USD")
    portfolio1: list[dict] = []

    pos1 = create_position("pos1", account1, "EURUSD", "SHORT", 0.08, 1.17300, 1.18218)
    pos2 = create_position("pos2", account1, "EURUSD", "SHORT", 0.05, 1.17300, 1.18218)
    pos3 = create_position("pos3", account1, "EURUSD", "SHORT", 0.08, 1.17300, 1.18218)

    portfolio1 = add_position(portfolio1, pos1)
    portfolio1 = add_position(portfolio1, pos2)
    portfolio1 = add_position(portfolio1, pos3)

    exposure1 = calculate_total_exposure(portfolio1, account1)
    print(print_exposure_summary(exposure1, account1))

    print("\nExpected: ~$193 total risk (~1.93%)")
    print(f"Actual: ${exposure1['total_risk_amount']} ({exposure1['total_risk_percent']}%)")
    print(f"Risk by instrument: {exposure1['risk_by_instrument']}")
    print(f"Risk by direction: {exposure1['risk_by_direction']}")

    # Test 2: USD account, multiple instruments and directions
    print("\n--- Test 2: USD account, multiple instruments/directions ---")
    account2 = create_account("acc2", "Swing Trading", 10000, "USD")
    portfolio2: list[dict] = []

    pos4 = create_position("pos4", account2, "EURUSD", "LONG", 0.20, 1.08500, 1.08000)
    pos5 = create_position("pos5", account2, "GBPUSD", "LONG", 0.10, 1.26500, 1.26000)
    pos6 = create_position("pos6", account2, "USDJPY", "SHORT", 0.15, 150.500, 151.500)

    portfolio2 = add_position(portfolio2, pos4)
    portfolio2 = add_position(portfolio2, pos5)
    portfolio2 = add_position(portfolio2, pos6)

    exposure2 = calculate_total_exposure(portfolio2, account2)
    print(print_exposure_summary(exposure2, account2))

    # Test 3: EUR account
    print("\n--- Test 3: EUR account ---")
    account3 = create_account("acc3", "EU Broker", 5000, "EUR")
    portfolio3: list[dict] = []

    pos7 = create_position("pos7", account3, "EURUSD", "LONG", 0.10, 1.08500, 1.08000)
    portfolio3 = add_position(portfolio3, pos7)

    exposure3 = calculate_total_exposure(portfolio3, account3)
    print(print_exposure_summary(exposure3, account3))

    # Test 4: Empty portfolio
    print("\n--- Test 4: Empty portfolio ---")
    account4 = create_account("acc4", "Empty Account", 10000, "USD")
    portfolio4: list[dict] = []

    exposure4 = calculate_total_exposure(portfolio4, account4)
    print(print_exposure_summary(exposure4, account4))

    print("\nExpected: All zeros, no errors")
    print(
        f"Actual: total_risk={exposure4['total_risk_amount']}, count={exposure4['position_count']}"
    )

    # Test 5: Remove position
    print("\n--- Test 5: Remove position ---")
    account5 = create_account("acc5", "Remove Test", 10000, "USD")
    portfolio5: list[dict] = []

    pos8 = create_position("pos8", account5, "EURUSD", "LONG", 0.10, 1.08500, 1.08000)
    pos9 = create_position("pos9", account5, "GBPUSD", "LONG", 0.10, 1.26500, 1.26000)

    portfolio5 = add_position(portfolio5, pos8)
    portfolio5 = add_position(portfolio5, pos9)

    print(f"Before removal: {len(portfolio5)} positions")
    exposure_before = calculate_total_exposure(portfolio5, account5)
    print(f"Total risk before: ${exposure_before['total_risk_amount']}")

    portfolio5 = remove_position(portfolio5, "pos8")

    print(f"After removal: {len(portfolio5)} positions")
    exposure_after = calculate_total_exposure(portfolio5, account5)
    print(f"Total risk after: ${exposure_after['total_risk_amount']}")
    print(f"Remaining position: {portfolio5[0]['position_id']} ({portfolio5[0]['instrument']})")

    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
