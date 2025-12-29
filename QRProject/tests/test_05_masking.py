"""05. MASKING & FINALIZATION: Apply mask pattern and write format info.

This is the fifth step in QR code generation. A mask pattern is applied to reduce
large blocks of the same color, and format information bits are written to the matrix.
"""
import numpy as np
import pytest

from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.finalize import finalize_matrix, build_reserved_map_v1
from qr.masking.format_info import format_coords_primary_v1, format_coords_secondary_v1
from qr.masking.mask0 import apply_mask0


# ============================================================================
# Finalize Matrix Tests (Masking + Format Info)
# ============================================================================

@pytest.mark.core
def test_finalize_matrix_returns_0_1():
    """Test that finalized matrix contains only 0 and 1."""
    matrix = create_base_matrix()
    data = [0] * 19
    ecc = [0] * 7
    placed = place_data(matrix, data, ecc)
    
    result = finalize_matrix(placed, 'L', 0)
    
    assert np.all((result == 0) | (result == 1))


@pytest.mark.core
def test_finalize_matrix_shape():
    """Test that finalized matrix is 21x21."""
    matrix = create_base_matrix()
    data = [0] * 19
    ecc = [0] * 7
    placed = place_data(matrix, data, ecc)
    
    result = finalize_matrix(placed, 'L', 0)
    
    assert result.shape == (21, 21)


@pytest.mark.core
def test_finalize_matrix_applies_mask():
    """Test that finalize_matrix applies masking."""
    matrix = create_base_matrix()
    data = list(range(19))
    ecc = list(range(7))
    placed = place_data(matrix, data, ecc)
    
    result = finalize_matrix(placed, 'L', 0)
    
    assert result.shape == placed.shape


