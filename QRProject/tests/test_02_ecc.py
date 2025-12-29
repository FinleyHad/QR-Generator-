"""02. ERROR CORRECTION: Add Reed-Solomon ECC codewords.

This is the second step in QR code generation. Encoded data is combined
with error correction codewords using Reed-Solomon encoding.
"""
import pytest

from qr.ecc.reed_solomon import add_ecc, ECC_BY_LEVEL
@pytest.mark.core


def test_ecc_level_l():
    """Test ECC Level L produces correct codeword count."""
    data = [0] * 19  # Version 1-L has 19 data codewords
    result = add_ecc(data, 'L')
    
    # L level: 19 data + 7 ECC = 26 total
    assert len(result) == 26
    # First 19 should be data (unchanged or permuted)
    assert len([x for x in result if isinstance(x, int)]) == 26


def test_ecc_codewords_are_integers():
    """Test that all returned codewords are integers."""
    data = list(range(19))
    result = add_ecc(data, 'L')
    
    assert all(isinstance(x, int) for x in result)
    assert all(0 <= x <= 255 for x in result)
@pytest.mark.core


def test_ecc_deterministic():
    """Test that same input produces same ECC output."""
    data = list(range(19))
    result1 = add_ecc(data, 'L')
    result2 = add_ecc(data, 'L')
    
    assert result1 == result2
@pytest.mark.core


def test_ecc_different_for_different_data():
    """Test that different data produces different ECC."""
    data1 = [0] * 19
    data2 = [1] + [0] * 18
    
    result1 = add_ecc(data1, 'L')
    result2 = add_ecc(data2, 'L')
    
    assert result1 != result2


