# """
# Tests for instrument configurations.
# """

# import pytest
# import sys
# from pathlib import Path

# # Add src to path for imports
# sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# from aperion.instruments.forex import (
#     EURUSD,
#     GBPUSD,
#     USDJPY,
#     GBPJPY,
#     XAUUSD,
#     get_instrument,
#     list_instruments,
# )


# class TestInstrumentConfigurations:
#     """Tests for instrument configuration dictionaries."""

#     def test_eurusd_config(self):
#         """Test EUR/USD configuration values."""
#         assert EURUSD["pip_size"] == 0.0001
#         assert EURUSD["pip_value"] == 10.0
#         assert EURUSD["lot_increment"] == 0.01

#     def test_gbpusd_config(self):
#         """Test GBP/USD configuration values."""
#         assert GBPUSD["pip_size"] == 0.0001
#         assert GBPUSD["pip_value"] == 10.0
#         assert GBPUSD["lot_increment"] == 0.01

#     def test_usdjpy_config(self):
#         """Test USD/JPY configuration values."""
#         assert USDJPY["pip_size"] == 0.01
#         assert USDJPY["pip_value"] == 6.67
#         assert USDJPY["lot_increment"] == 0.01

#     def test_gbpjpy_config(self):
#         """Test GBP/JPY configuration values."""
#         assert GBPJPY["pip_size"] == 0.01
#         assert GBPJPY["pip_value"] == 6.67
#         assert GBPJPY["lot_increment"] == 0.01

#     def test_xauusd_config(self):
#         """Test XAU/USD (Gold) configuration values."""
#         assert XAUUSD["pip_size"] == 0.01
#         assert XAUUSD["pip_value"] == 1.0
#         assert XAUUSD["lot_increment"] == 0.01

#     def test_all_instruments_have_required_keys(self):
#         """All instruments should have pip_size, pip_value, lot_increment."""
#         instruments = [EURUSD, GBPUSD, USDJPY, GBPJPY, XAUUSD]
#         required_keys = {"pip_size", "pip_value", "lot_increment"}

#         for instrument in instruments:
#             assert required_keys.issubset(instrument.keys())


# class TestGetInstrument:
#     """Tests for get_instrument function."""

#     def test_get_by_canonical_name(self):
#         """Test getting instrument by canonical name (no slash)."""
#         assert get_instrument("EURUSD") == EURUSD
#         assert get_instrument("USDJPY") == USDJPY

#     def test_get_by_slash_name(self):
#         """Test getting instrument by name with slash."""
#         assert get_instrument("EUR/USD") == EURUSD
#         assert get_instrument("USD/JPY") == USDJPY

#     def test_case_insensitive(self):
#         """Test that lookup is case-insensitive."""
#         assert get_instrument("eurusd") == EURUSD
#         assert get_instrument("EurUsd") == EURUSD

#     def test_gold_alias(self):
#         """Test GOLD alias for XAU/USD."""
#         assert get_instrument("GOLD") == XAUUSD

#     def test_unknown_instrument_returns_none(self):
#         """Unknown instrument should return None."""
#         assert get_instrument("UNKNOWN") is None
#         assert get_instrument("BTCUSD") is None


# class TestListInstruments:
#     """Tests for list_instruments function."""

#     def test_returns_list(self):
#         """Should return a list."""
#         result = list_instruments()
#         assert isinstance(result, list)

#     def test_contains_major_pairs(self):
#         """Should contain major forex pairs."""
#         result = list_instruments()
#         assert "EURUSD" in result
#         assert "GBPUSD" in result
#         assert "USDJPY" in result

#     def test_canonical_names_only(self):
#         """Should return canonical names (no slashes)."""
#         result = list_instruments()
#         for name in result:
#             assert "/" not in name

#     def test_no_aliases(self):
#         """Should not include aliases like GOLD."""
#         result = list_instruments()
#         assert "GOLD" not in result


# if __name__ == "__main__":
#     pytest.main([__file__, "-v"])
