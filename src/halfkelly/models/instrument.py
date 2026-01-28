"""
Instrument data model.
"""

from dataclasses import dataclass


@dataclass
class Instrument:
    """
    Instrument configuration for position sizing calculations.

    Attributes:
        pip_size: Minimum price movement (e.g., 0.0001 for EUR/USD, 0.01 for JPY pairs).
        pip_value: Dollar value per pip per standard lot (1.0 lot = 100,000 units).
        lot_increment: Minimum position size increment (typically 0.01 for micro lots).

    Example:
        >>> eurusd = Instrument(pip_size=0.0001, pip_value=10.0, lot_increment=0.01)
        >>> eurusd.pip_size
        0.0001
    """

    pip_size: float
    pip_value: float
    lot_increment: float
