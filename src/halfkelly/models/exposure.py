"""
Exposure summary data model.
"""

from dataclasses import dataclass

from halfkelly.models.position import Position


@dataclass
class ExposureSummary:
    """
    Summary of risk exposure for an account.

    Attributes:
        total_risk_amount: Sum of all position risks in account currency.
        total_risk_percent: Total risk as percentage of account balance.
        position_count: Number of open positions.
        risk_by_instrument: Dict mapping instrument to total risk.
        risk_by_direction: Dict with "LONG" and "SHORT" risk totals.
        largest_position: Position with highest risk (or None if no positions).

    Example:
        >>> exposure = ExposureSummary(
        ...     total_risk_amount=200.0,
        ...     total_risk_percent=2.0,
        ...     position_count=2,
        ...     risk_by_instrument={"EURUSD": 200.0},
        ...     risk_by_direction={"LONG": 100.0, "SHORT": 100.0},
        ...     largest_position=None,
        ... )
        >>> exposure.total_risk_percent
        2.0
    """

    total_risk_amount: float
    total_risk_percent: float
    position_count: int
    risk_by_instrument: dict[str, float]
    risk_by_direction: dict[str, float]
    largest_position: Position | None
