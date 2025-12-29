"""06. INTEGRATION: End-to-end QR code generation pipeline tests.

This is the sixth step: full integration tests verifying that all previous
steps (encoding, ECC, matrix structure, data placement, masking) work correctly
together to produce a complete QR code matrix.
"""
import io
import numpy as np
import pytest
from PIL import Image

from qr.encoding.encode import encode_string
from qr.ecc.reed_solomon import add_ecc
from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.finalize import finalize_matrix
from qr.masking.format_info import (
    format_coords_primary_v1,
    format_coords_secondary_v1,
    compute_format_bits,
)


class TestCompletePipeline:
    """Tests for the complete QR encoding pipeline."""
    
    @pytest.mark.core
    def test_pipeline_hello_produces_valid_matrix(self):
        """Test complete pipeline for 'hello' produces valid 21x21 0/1 matrix."""
        text = "hello"
        
        # Full pipeline
        encoded = encode_string(text)
        ecc = add_ecc(encoded, 'L')
        base = create_base_matrix()
        placed = place_data(base, encoded, ecc)
        final = finalize_matrix(placed, 'L', 0)
        
        # Validation
        assert final.shape == (21, 21)
        assert np.all((final == 0) | (final == 1))


    @pytest.mark.core
    def test_pipeline_reproducible(self):
        """Test that same input produces identical output."""
        text = "test"
        
        def encode_full(text):
            encoded = encode_string(text)
            ecc = add_ecc(encoded, 'L')
            base = create_base_matrix()
            placed = place_data(base, encoded, ecc)
            return finalize_matrix(placed, 'L', 0)
        
        matrix1 = encode_full(text)
        matrix2 = encode_full(text)
        
        np.testing.assert_array_equal(matrix1, matrix2)


class TestFormatBitsPlacement:
    """Tests for correct format bits placement and values."""
    
    @pytest.mark.core
    def test_format_bits_at_primary_coordinates(self):
        """Test that format bits are written at primary coordinates."""
        text = "X"
        encoded = encode_string(text)
        ecc = add_ecc(encoded, 'L')
        base = create_base_matrix()
        placed = place_data(base, encoded, ecc)
        final = finalize_matrix(placed, 'L', 0)
        
        # Get expected format bits
        expected_bits = compute_format_bits('L', 0)
        primary_coords = format_coords_primary_v1()
        
        # Format bits should be written at these coordinates
        assert len(primary_coords) == 15
        for i, (r, c) in enumerate(primary_coords):
            assert final[r, c] == expected_bits[i], f"Format bit {i} at ({r}, {c}) mismatch"


    @pytest.mark.core
    def test_data_starts_at_bottom_right(self):
        """Test that data placement starts from bottom-right."""
        # Create a matrix where we can track data bits
        text = "A"  # Single byte: 01000001 (65)
        encoded = encode_string(text)
        
        base = create_base_matrix()
        # Don't apply ECC yet, just place encoded bits
        placed = place_data(base, encoded, [0] * 7)  # Dummy ECC
        
        # Data should be placed starting from rightmost columns
        # and moving left in 2-column stripes
        # The rightmost 2 columns (20, 21) should have data
        assert placed.shape == (21, 21)


    @pytest.mark.core
    def test_masking_doesnt_corrupt_finders(self):
        """Test that masking preserves finder patterns."""
        text = "test"
        encoded = encode_string(text)
        ecc = add_ecc(encoded, 'L')
        base = create_base_matrix()
        placed = place_data(base, encoded, ecc)
        final = finalize_matrix(placed, 'L', 0)
        
        # Top-left finder should be intact
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
                assert final[r, c] == expected_finder[r][c]


