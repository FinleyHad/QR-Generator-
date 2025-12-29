"""01. ENCODING: Convert text to bits using byte mode.

This is the first step in QR code generation. Text input is converted
to a bitstream following the QR specification for byte mode encoding.
"""
import pytest

from qr.encoding.byte_mode import byte_mode, BYTE_MODE_INDICATOR, PAD_BYTES, DATA_CODEWORDS, VERSION_1_L_DATA_BITS


@pytest.mark.core
def test_byte_mode_mode_indicator():
    """Test that mode indicator is correct (0100 for byte mode)."""
    codewords, bitstream = byte_mode("A")
    assert bitstream.startswith(BYTE_MODE_INDICATOR)
    assert BYTE_MODE_INDICATOR == "0100"


@pytest.mark.core
def test_byte_mode_single_char():
    """Test encoding a single ASCII character."""
    codewords, bitstream = byte_mode("A")
    assert len(codewords) == DATA_CODEWORDS  # 19 for Version 1-L
    assert len(bitstream) == VERSION_1_L_DATA_BITS  # 152 bits
    # First codeword should have mode indicator and char count
    assert codewords[0] >> 4 == int("0100", 2)  # Top 4 bits are mode


@pytest.mark.core
def test_byte_mode_data_bits():
    """Test that data bits match UTF-8 encoding."""
    text = "AB"
    codewords, bitstream = byte_mode(text)
    # Mode: 0100 (4 bits)
    # Char count: 00000010 (8 bits, for "AB" = 2 chars)
    # Data: 01000001 (A=65) + 01000010 (B=66)
    expected_start = "0100" + "00000010" + "01000001" + "01000010"
    assert bitstream.startswith(expected_start)


@pytest.mark.core
def test_byte_mode_padding():
    """Test that bitstream is padded correctly."""
    codewords, bitstream = byte_mode("A")
    assert len(bitstream) % 8 == 0, "Bitstream must be byte-aligned"
    assert len(bitstream) == VERSION_1_L_DATA_BITS


