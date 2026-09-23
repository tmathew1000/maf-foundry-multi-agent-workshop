"""Tests for deterministic workshop tools."""

from support_tools import _return_confirmation


def test_return_confirmation_is_explicitly_simulated() -> None:
    result = _return_confirmation("123", "replacement")

    assert "Simulated return" in result
    assert "RET-123-REPLACEMENT" in result
    assert "No external system was changed" in result

