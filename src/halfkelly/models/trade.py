"""
Trade result data model.
"""

from dataclasses import dataclass


@dataclass
class TradeResult:
    """
    Result of a position sizing calculation.

    Attributes:
        instrument_name: Name of the instrument (e.g., "EUR/USD").
        direction: Trade direction ("LONG" or "SHORT").
        stop_distance_pips: Distance to stop loss in pips.
        position_size: Calculated position size in lots.
        actual_risk_amount: Actual dollar risk (may be less than intended due to rounding).
        actual_risk_percent: Actual risk as percentage of account balance.
        reward_risk_ratio: Reward-to-risk ratio (optional, only if take_profit provided).
        potential_reward: Potential profit in dollars (optional, only if take_profit provided).

    Example:
        >>> trade = TradeResult(
        ...     instrument_name="EUR/USD",
        ...     direction="LONG",
        ...     stop_distance_pips=50.0,
        ...     position_size=0.20,
        ...     actual_risk_amount=100.00,
        ...     actual_risk_percent=1.0,
        ... )
        >>> trade.position_size
        0.2
    """

    instrument_name: str
    direction: str
    stop_distance_pips: float
    position_size: float
    actual_risk_amount: float
    actual_risk_percent: float
    reward_risk_ratio: float | None = None
    potential_reward: float | None = None
