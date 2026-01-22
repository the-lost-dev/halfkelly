"""
Tests for position sizing calculations.
"""

import pytest

from halfkelly.calculators.position_sizing import (
    calculate_position_size,
    calculate_reward_risk_ratio,
    calculate_risk_amount,
    calculate_risk_per_lot,
    size_position,
    validate_instrument,
)
from halfkelly.instruments.forex import EURUSD, USDJPY

# class TestCalculateStopDistancePips:
#     """Tests for calculate_stop_distance_pips function."""

#     def test_eurusd_short_position(self):
#         """Test stop distance for EUR/USD short."""
#         result = calculate_stop_distance_pips(1.17300, 1.18218, 0.0001)
#         assert abs(result - 91.8) < 0.01

#     def test_eurusd_long_position(self):
#         """Test stop distance for EUR/USD long."""
#         result = calculate_stop_distance_pips(1.08500, 1.08000, 0.0001)
#         assert result == pytest.approx(50.0)

#     def test_usdjpy_long_position(self):
#         """Test stop distance for USD/JPY long."""
#         result = calculate_stop_distance_pips(150.500, 149.500, 0.01)
#         assert result == 100.0

#     def test_returns_positive_for_long(self):
#         """Stop distance should always be positive for long positions."""
#         result = calculate_stop_distance_pips(1.1000, 1.0900, 0.0001)
#         assert result > 0

#     def test_returns_positive_for_short(self):
#         """Stop distance should always be positive for short positions."""
#         result = calculate_stop_distance_pips(1.1000, 1.1100, 0.0001)
#         assert result > 0


class TestCalculateRiskAmount:
    """Tests for calculate_risk_amount function."""

    def test_two_percent_risk(self):
        """Test 2% risk on $10,000 account."""
        result = calculate_risk_amount(10000, 2.0)
        assert result == 200.0

    def test_one_percent_risk(self):
        """Test 1% risk on $10,000 account."""
        result = calculate_risk_amount(10000, 1.0)
        assert result == 100.0

    def test_half_percent_risk(self):
        """Test 0.5% risk on $50,000 account."""
        result = calculate_risk_amount(50000, 0.5)
        assert result == 250.0

    def test_zero_risk(self):
        """Test 0% risk returns 0."""
        result = calculate_risk_amount(10000, 0.0)
        assert result == 0.0


class TestCalculateRiskPerLot:
    """Tests for calculate_risk_per_lot function."""

    def test_eurusd_91_pips(self):
        """Test risk per lot for 91.8 pip stop on EUR/USD."""
        result = calculate_risk_per_lot(91.8, 10.0)
        assert result == 918.0

    def test_eurusd_50_pips(self):
        """Test risk per lot for 50 pip stop on EUR/USD."""
        result = calculate_risk_per_lot(50.0, 10.0)
        assert result == 500.0

    def test_usdjpy_100_pips(self):
        """Test risk per lot for 100 pip stop on USD/JPY."""
        result = calculate_risk_per_lot(100.0, 6.67)
        assert result == 667.0


class TestCalculatePositionSize:
    """Tests for calculate_position_size function."""

    def test_rounds_down(self):
        """Position size should round down, not up."""
        # $200 risk / $918 per lot = 0.2178... should round to 0.21
        result = calculate_position_size(200.0, 918.0, 0.01)
        assert result == 0.21

    def test_exact_division(self):
        """Test when division is exact."""
        # $100 risk / $500 per lot = 0.20 exactly
        result = calculate_position_size(100.0, 500.0, 0.01)
        assert result == 0.20

    def test_respects_lot_increment(self):
        """Position size should be multiple of lot_increment."""
        result = calculate_position_size(200.0, 918.0, 0.01)
        # Check that result is a multiple of 0.01 (within floating point tolerance)
        assert round(result / 0.01) * 0.01 == pytest.approx(result)

    def test_zero_risk_returns_zero(self):
        """Zero risk amount should return zero position size."""
        result = calculate_position_size(0.0, 500.0, 0.01)
        assert result == 0.0


class TestCalculateRewardRiskRatio:
    """Tests for calculate_reward_risk_ratio function."""

    def test_two_to_one_long(self):
        """Test 2:1 R:R for long position."""
        result = calculate_reward_risk_ratio(1.08500, 1.08000, 1.09500)
        assert result == pytest.approx(2.0)

    def test_two_to_one_short(self):
        """Test 2:1 R:R for short position."""
        result = calculate_reward_risk_ratio(1.09500, 1.10000, 1.08500)
        assert result == pytest.approx(2.0)

    def test_eurusd_short_example(self):
        """Test the EUR/USD short example from requirements."""
        result = calculate_reward_risk_ratio(1.17300, 1.18218, 1.15000)
        assert abs(result - 2.5) < 0.1


class TestValidateInstrument:
    """Tests for validate_instrument function."""

    def test_valid_instrument(self):
        """Valid instrument should not raise."""
        validate_instrument(EURUSD)  # Should not raise

    def test_missing_pip_size(self):
        """Missing pip_size should raise ValueError."""
        with pytest.raises(ValueError, match="pip_size"):
            validate_instrument({"pip_value": 10.0, "lot_increment": 0.01})

    def test_missing_pip_value(self):
        """Missing pip_value should raise ValueError."""
        with pytest.raises(ValueError, match="pip_value"):
            validate_instrument({"pip_size": 0.0001, "lot_increment": 0.01})

    def test_missing_lot_increment(self):
        """Missing lot_increment should raise ValueError."""
        with pytest.raises(ValueError, match="lot_increment"):
            validate_instrument({"pip_size": 0.0001, "pip_value": 10.0})


class TestSizePosition:
    """Integration tests for size_position function."""

    def test_eurusd_short(self):
        """Test EUR/USD short from requirements."""
        result = size_position(
            instrument=EURUSD,
            account_balance=10000,
            risk_percent=2.0,
            entry_price=1.17300,
            stop_loss=1.18218,
            take_profit=1.15000,
            instrument_name="EUR/USD",
        )

        assert result["direction"] == "SHORT"
        assert result["position_size"] == 0.21
        assert abs(result["actual_risk_amount"] - 193) < 5
        assert abs(result["reward_risk_ratio"] - 2.5) < 0.1

    def test_eurusd_long(self):
        """Test EUR/USD long from requirements."""
        result = size_position(
            instrument=EURUSD,
            account_balance=10000,
            risk_percent=1.0,
            entry_price=1.08500,
            stop_loss=1.08000,
            take_profit=1.09500,
            instrument_name="EUR/USD",
        )

        assert result["direction"] == "LONG"
        assert result["position_size"] == 0.20
        assert result["actual_risk_amount"] == 100.0
        assert result["reward_risk_ratio"] == 2.0

    def test_usdjpy_long(self):
        """Test USD/JPY long from requirements."""
        result = size_position(
            instrument=USDJPY,
            account_balance=10000,
            risk_percent=1.0,
            entry_price=150.500,
            stop_loss=149.500,
            take_profit=152.500,
            instrument_name="USD/JPY",
        )

        assert result["direction"] == "LONG"
        assert result["position_size"] == 0.14
        assert abs(result["actual_risk_amount"] - 93) < 5
        assert result["reward_risk_ratio"] == 2.0

    def test_without_take_profit(self):
        """Test that R:R fields are absent without take_profit."""
        result = size_position(
            instrument=EURUSD,
            account_balance=10000,
            risk_percent=1.0,
            entry_price=1.08500,
            stop_loss=1.08000,
            instrument_name="EUR/USD",
        )

        assert "reward_risk_ratio" not in result
        assert "potential_reward" not in result

    def test_actual_risk_never_exceeds_intended(self):
        """Actual risk should never exceed intended risk due to rounding down."""
        result = size_position(
            instrument=EURUSD,
            account_balance=10000,
            risk_percent=2.0,
            entry_price=1.17300,
            stop_loss=1.18218,
            instrument_name="EUR/USD",
        )

        intended_risk = 10000 * 0.02  # $200
        assert result["actual_risk_amount"] <= intended_risk


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
