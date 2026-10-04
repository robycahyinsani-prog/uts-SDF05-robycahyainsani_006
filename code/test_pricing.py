import pytest
from pricing import calculate_order_total


def test_calculate_order_total_member():
    """Member mendapat diskon 10% lalu pajak 11%."""
    assert calculate_order_total(100, 2, True) == pytest.approx(199.8)


def test_calculate_order_total_non_member():
    """Non-member tidak dapat diskon, tetap kena pajak 11%."""
    assert calculate_order_total(100, 2, False) == pytest.approx(222.0)