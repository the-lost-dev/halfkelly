"""
Account data model.
"""

from dataclasses import dataclass


@dataclass
class Account:
    """
    Trading account information.

    Attributes:
        account_id: Unique identifier for the account.
        name: Human-readable name (e.g., "Main Trading", "Prop Firm Challenge").
        balance: Account balance in the account's currency.
        currency: Account currency code (e.g., "USD", "EUR", "GBP").

    Example:
        >>> account = Account(
        ...     account_id="acc1",
        ...     name="Main Trading",
        ...     balance=10000.0,
        ...     currency="USD",
        ... )
        >>> account.balance
        10000.0
    """

    account_id: str
    name: str
    balance: float
    currency: str
