"""
Position data model.
"""

from dataclasses import dataclass


@dataclass
class Position:
    """
    An open trading position.

    Attributes:
        position_id: Unique identifier for the position.
        account_id: ID of the account holding this position.
        instrument: Instrument name (e.g., "EURUSD", "GBPUSD").
        direction: Trade direction ("LONG" or "SHORT").
        size: Position size in lots.
        entry_price: Entry price for the trade.
        stop_loss: Stop loss price.
        risk_amount: Calculated risk amount in account currency.

    Example:
        >>> position = Position(
        ...     position_id="pos1",
        ...     account_id="acc1",
        ...     instrument="EURUSD",
        ...     direction="LONG",
        ...     size=0.10,
        ...     entry_price=1.08500,
        ...     stop_loss=1.08000,
        ...     risk_amount=50.0,
        ... )
        >>> position.size
        0.1
    """

    position_id: str
    account_id: str
    instrument: str
    direction: str
    size: float
    entry_price: float
    stop_loss: float
    risk_amount: float
