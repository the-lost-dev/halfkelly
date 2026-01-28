"""
HalfKelly - Forex Risk Management Engine

A comprehensive toolkit for calculating position sizes, managing risk,
and analyzing forex trades.
"""

__version__ = "0.1.0"
__author__ = "HalfKelly"

from halfkelly.calculators.position_sizing import (
    calculate_position_size,
    calculate_reward_risk_ratio,
    calculate_risk_amount,
    calculate_risk_per_lot,
    calculate_stop_distance_pips,
    size_position,
)
from halfkelly.instruments.forex import (
    EURUSD,
    GBPJPY,
    GBPUSD,
    USDJPY,
    XAUUSD,
    get_instrument,
    list_instruments,
)
from halfkelly.models import (
    Account,
    ExposureSummary,
    Instrument,
    Position,
    TradeResult,
)
from halfkelly.utils.formatting import print_trade_summary

__all__ = [
    # Models
    "Account",
    "ExposureSummary",
    "Instrument",
    "Position",
    "TradeResult",
    # Calculators
    "calculate_stop_distance_pips",
    "calculate_risk_amount",
    "calculate_risk_per_lot",
    "calculate_position_size",
    "calculate_reward_risk_ratio",
    "size_position",
    # Instruments
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "GBPJPY",
    "XAUUSD",
    "get_instrument",
    "list_instruments",
    # Utils
    "print_trade_summary",
]
