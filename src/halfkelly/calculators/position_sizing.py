"""
Position Sizing Calculator

Calculate position sizes based on account risk parameters and instrument specifications.
Implements the core risk management formula:

    Position Size = Risk Amount ÷ Risk Per Lot

Where:
    - Risk Amount = Account Balance × Risk Percentage
    - Risk Per Lot = Stop Distance (pips) × Pip Value
"""


def calculate_stop_distance_pips(entry_price: float, stop_loss: float, pip_size: float) -> float:
    """
    Calculate the distance between entry and stop loss in pips.

    Args:
        entry_price: Entry price for the trade.
        stop_loss: Stop loss price.
        pip_size: Minimum price movement (e.g., 0.0001 for EUR/USD, 0.01 for JPY pairs).

    Returns:
        Stop distance in pips (always positive).

    Example:
        >>> calculate_stop_distance_pips(1.17300, 1.18218, 0.0001)
        91.8
        >>> calculate_stop_distance_pips(150.500, 149.500, 0.01)
        100.0
    """
    return abs(entry_price - stop_loss) / pip_size


def calculate_risk_amount(account_balance: float, risk_percent: float) -> float:
    """
    Calculate the dollar amount to risk based on account balance and risk percentage.

    Args:
        account_balance: Total account balance in dollars.
        risk_percent: Percentage of account to risk (e.g., 2.0 for 2%).

    Returns:
        Dollar amount to risk.

    Example:
        >>> calculate_risk_amount(10000, 2.0)
        200.0
        >>> calculate_risk_amount(50000, 0.5)
        250.0
    """
    return account_balance * (risk_percent / 100)


def calculate_risk_per_lot(stop_pips: float, pip_value: float) -> float:
    """
    Calculate the dollar risk per standard lot.

    Args:
        stop_pips: Stop distance in pips.
        pip_value: Dollar value per pip per standard lot.

    Returns:
        Dollar risk per lot.

    Example:
        >>> calculate_risk_per_lot(91.8, 10.0)
        918.0
        >>> calculate_risk_per_lot(50.0, 10.0)
        500.0
    """
    return stop_pips * pip_value


def calculate_position_size(risk_amount: float, risk_per_lot: float, lot_increment: float) -> float:
    """
    Calculate position size rounded down to nearest lot increment.

    Position size is always rounded DOWN to ensure the actual risk
    never exceeds the intended risk amount.

    Args:
        risk_amount: Dollar amount willing to risk.
        risk_per_lot: Dollar risk per standard lot.
        lot_increment: Minimum position size increment (typically 0.01).

    Returns:
        Position size in lots (rounded down to lot_increment).

    Example:
        >>> calculate_position_size(200.0, 918.0, 0.01)
        0.21
        >>> calculate_position_size(100.0, 500.0, 0.01)
        0.2
    """
    raw_size = risk_amount / risk_per_lot
    increments = int(raw_size / lot_increment)
    return increments * lot_increment


def calculate_reward_risk_ratio(entry: float, stop: float, target: float) -> float:
    """
    Calculate the reward-to-risk ratio.

    Args:
        entry: Entry price.
        stop: Stop loss price.
        target: Take profit price.

    Returns:
        Reward-to-risk ratio (e.g., 2.0 means 2:1 R:R).

    Example:
        >>> calculate_reward_risk_ratio(1.17300, 1.18218, 1.15000)
        2.5054466230936817
        >>> calculate_reward_risk_ratio(1.08500, 1.08000, 1.09500)
        2.0
    """
    risk_distance = abs(entry - stop)
    reward_distance = abs(target - entry)
    return reward_distance / risk_distance


def validate_instrument(instrument: dict[str, float]) -> None:
    """
    Validate that instrument dict contains required keys.

    Args:
        instrument: Instrument configuration dictionary.

    Raises:
        ValueError: If required keys are missing.
    """
    required_keys = {"pip_size", "pip_value", "lot_increment"}
    missing = required_keys - set(instrument.keys())
    if missing:
        raise ValueError(f"Instrument missing required keys: {missing}")


def size_position(
    instrument: dict[str, float],
    account_balance: float,
    risk_percent: float,
    entry_price: float,
    stop_loss: float,
    take_profit: float | None = None,
    instrument_name: str = "UNKNOWN",
) -> dict:
    """
    Calculate complete position sizing for a trade.

    This is the main entry point for position sizing. It combines all
    individual calculations and returns a comprehensive trade plan.

    Args:
        instrument: Instrument configuration dict with pip_size, pip_value, lot_increment.
        account_balance: Total account balance in dollars.
        risk_percent: Percentage of account to risk (e.g., 2.0 for 2%).
        entry_price: Entry price for the trade.
        stop_loss: Stop loss price.
        take_profit: Optional take profit price for R:R calculation.
        instrument_name: Name of the instrument for display purposes.

    Returns:
        Dictionary containing:
            - instrument_name: Name of the instrument
            - direction: "LONG" or "SHORT"
            - stop_distance_pips: Distance to stop in pips
            - position_size: Calculated position size in lots
            - actual_risk_amount: Actual dollar risk (may be less due to rounding)
            - actual_risk_percent: Actual risk as percentage of account
            - reward_risk_ratio: R:R ratio (if take_profit provided)
            - potential_reward: Potential profit in dollars (if take_profit provided)

    Example:
        >>> from halfkelly.instruments.forex import EURUSD
        >>> result = size_position(
        ...     instrument=EURUSD,
        ...     account_balance=10000,
        ...     risk_percent=2.0,
        ...     entry_price=1.17300,
        ...     stop_loss=1.18218,
        ...     take_profit=1.15000,
        ...     instrument_name="EUR/USD"
        ... )
        >>> result["position_size"]
        0.21
        >>> result["direction"]
        'SHORT'
    """
    validate_instrument(instrument)

    pip_size = instrument["pip_size"]
    pip_value = instrument["pip_value"]
    lot_increment = instrument["lot_increment"]

    # Determine direction based on stop loss position
    direction = "LONG" if stop_loss < entry_price else "SHORT"

    # Calculate position size components
    stop_distance_pips = calculate_stop_distance_pips(entry_price, stop_loss, pip_size)
    risk_amount = calculate_risk_amount(account_balance, risk_percent)
    risk_per_lot = calculate_risk_per_lot(stop_distance_pips, pip_value)
    position_size = calculate_position_size(risk_amount, risk_per_lot, lot_increment)

    # Calculate actual risk (may be less due to rounding down)
    actual_risk_amount = position_size * risk_per_lot
    actual_risk_percent = (actual_risk_amount / account_balance) * 100

    result = {
        "instrument_name": instrument_name,
        "direction": direction,
        "stop_distance_pips": round(stop_distance_pips, 1),
        "position_size": position_size,
        "actual_risk_amount": round(actual_risk_amount, 2),
        "actual_risk_percent": round(actual_risk_percent, 2),
    }

    # Add reward metrics if take profit provided
    if take_profit is not None:
        rr_ratio = calculate_reward_risk_ratio(entry_price, stop_loss, take_profit)
        potential_reward = actual_risk_amount * rr_ratio
        result["reward_risk_ratio"] = round(rr_ratio, 2)
        result["potential_reward"] = round(potential_reward, 2)

    return result
