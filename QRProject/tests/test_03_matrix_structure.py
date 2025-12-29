"""03. MATRIX STRUCTURE: Create base matrix with finder patterns and reserved areas.

This is the third step in QR code generation. A 21x21 matrix is created with:
- Finder patterns (3 corners) and separators
- Timing patterns (alternating row/col)
- Dark module
- Format information placeholders
"""
import numpy as np
import pytest

from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.format_info import (
    compute_format_bits,
    format_coords_primary_v1,
    format_coords_secondary_v1,
)


# ============================================================================
# Base Matrix Creation
# ============================================================================

@pytest.mark.core
def test_create_base_matrix_size():
    """Test that base matrix is 21x21."""
    matrix = create_base_matrix()
    assert matrix.shape == (21, 21)


@pytest.mark.core
def test_finder_patterns_intact():
    """Test that finder patterns are not corrupted."""
    matrix = create_base_matrix()
    
    # Top-left finder pattern (7x7)
    expected_tl = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    for r in range(7):
        for c in range(7):
            assert matrix[r, c] == expected_tl[r][c], f"Top-left finder corrupted at ({r}, {c})"


# ============================================================================
# Timing Patterns
# ============================================================================

@pytest.mark.core
def test_timing_pattern_horizontal():
    """Test that horizontal timing pattern alternates on row 6."""
    matrix = create_base_matrix()
    
    # Row 6 should have timing pattern in the gap (columns 9-11)
    # Pattern: alternating 1, 0, 1, ...
    for col in range(9, 12):
        expected = 1 if col % 2 == 0 else 0
        assert matrix[6, col] == expected, f"Row 6, col {col}: expected {expected}, got {matrix[6, col]}"


@pytest.mark.core
def test_timing_pattern_vertical():
    """Test that vertical timing pattern alternates on column 6."""
    matrix = create_base_matrix()
    
    # Column 6 should have timing pattern in the gap (rows 9-11)
    # Pattern: alternating 1, 0, 1, ...
    for row in range(9, 12):
        expected = 1 if row % 2 == 0 else 0
        assert matrix[row, 6] == expected, f"Row {row}, col 6: expected {expected}, got {matrix[row, 6]}"


@pytest.mark.core
def test_place_data_preserves_reserved():
    """Test that data placement doesn't overwrite reserved cells."""
    matrix = create_base_matrix()
    data = [0] * 19
    ecc = [0] * 7
    
    result = place_data(matrix, data, ecc)
    
    # Top-left finder should still be intact
    expected_finder = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ]
    for r in range(7):
        for c in range(7):
            assert result[r, c] == expected_finder[r][c]


@pytest.mark.core
def test_is_reserved_dark_module():
    """Test that dark module is protected in place_data."""
    matrix = create_base_matrix()
    data = [1] * 19  # Try to overwrite everything
    ecc = [1] * 7
    
    result = place_data(matrix, data, ecc)
    
    # Dark module at (13, 8) should still be 1
    assert result[13, 8] == 1, "Dark module should not be overwritten"


# ============================================================================
# Format Information
# ============================================================================

@pytest.mark.core
def test_format_bits_length():
    """Test that format bits are exactly 15 bits."""
    bits = compute_format_bits('L', 0)
    assert len(bits) == 15
    assert all(b in [0, 1] for b in bits)


@pytest.mark.core
def test_format_coords_primary_length():
    """Test that primary format coords are exactly 15."""
    coords = format_coords_primary_v1()
    assert len(coords) == 15
    assert all(isinstance(c, tuple) and len(c) == 2 for c in coords)


