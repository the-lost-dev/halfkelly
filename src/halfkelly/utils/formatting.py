"""
Formatting utilities for trade output and display.
"""

from halfkelly.models.trade import TradeResult


def format_trade_summary(trade: TradeResult) -> str:
    """
    Format a trade summary as a string.

    Args:
        trade: TradeResult returned by size_position().

    Returns:
        Formatted string representation of the trade.

    Example:
        >>> from halfkelly.models.trade import TradeResult
        >>> trade = TradeResult(
        ...     instrument_name="EUR/USD",
        ...     direction="LONG",
        ...     stop_distance_pips=50.0,
        ...     position_size=0.20,
        ...     actual_risk_amount=100.00,
        ...     actual_risk_percent=1.0,
        ... )
        >>> print(format_trade_summary(trade))  # doctest: +NORMALIZE_WHITESPACE
        ==================================================
          EUR/USD - LONG
        ==================================================
          Stop Distance:    50.0 pips
          Position Size:    0.20 lots
          Risk Amount:      $100.00
          Risk Percent:     1.00%
        ==================================================
    """
    lines = [
        "",
        "=" * 50,
        f"  {trade.instrument_name} - {trade.direction}",
        "=" * 50,
        f"  Stop Distance:    {trade.stop_distance_pips} pips",
        f"  Position Size:    {trade.position_size:.2f} lots",
        f"  Risk Amount:      ${trade.actual_risk_amount:.2f}",
        f"  Risk Percent:     {trade.actual_risk_percent:.2f}%",
    ]

    if trade.reward_risk_ratio is not None:
        lines.append(f"  R:R Ratio:        {trade.reward_risk_ratio:.2f}:1")
        lines.append(f"  Potential Reward: ${trade.potential_reward:.2f}")

    lines.append("=" * 50)
    lines.append("")

    return "\n".join(lines)


def print_trade_summary(trade: TradeResult) -> None:
    """
    Print a formatted trade summary to stdout.

    Args:
        trade: TradeResult returned by size_position().

    Example:
        >>> from halfkelly.models.trade import TradeResult
        >>> trade = TradeResult(
        ...     instrument_name="EUR/USD",
        ...     direction="LONG",
        ...     stop_distance_pips=50.0,
        ...     position_size=0.20,
        ...     actual_risk_amount=100.00,
        ...     actual_risk_percent=1.0,
        ...     reward_risk_ratio=2.0,
        ...     potential_reward=200.00,
        ... )
        >>> print_trade_summary(trade)  # doctest: +NORMALIZE_WHITESPACE
        <BLANKLINE>
        ==================================================
          EUR/USD - LONG
        ==================================================
          Stop Distance:    50.0 pips
          Position Size:    0.20 lots
          Risk Amount:      $100.00
          Risk Percent:     1.00%
          R:R Ratio:        2.00:1
          Potential Reward: $200.00
        ==================================================
        <BLANKLINE>
    """
    print(format_trade_summary(trade))
