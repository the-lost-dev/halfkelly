# Aperion Documentation

Welcome to the Aperion documentation. Aperion is a Forex Risk Management Engine designed to help traders calculate position sizes and manage risk effectively.

## Table of Contents

- [Getting Started](getting_started.md) - Installation and basic usage
- [API Reference](api_reference.md) - Complete API documentation
- [Instruments](instruments.md) - Supported forex instruments
- [Examples](../examples/) - Example scripts and use cases

## Quick Links

- **Position Sizing**: Learn how to calculate the correct position size for your trades
- **Risk Management**: Understand how to limit your risk per trade
- **Instruments**: See all supported forex pairs and commodities

## Core Concepts

### The Position Sizing Formula

Aperion uses a simple but effective formula for position sizing:

```
Position Size = Risk Amount ÷ Risk Per Lot
```

Where:
- **Risk Amount** = Account Balance × Risk Percentage
- **Risk Per Lot** = Stop Distance (pips) × Pip Value

This ensures you never risk more than your intended percentage on any single trade.

### Rounding Behavior

Position sizes are always rounded **down** to the nearest lot increment. This conservative approach ensures your actual risk never exceeds your intended risk.

## Support

For issues and feature requests, please open an issue on GitHub.
