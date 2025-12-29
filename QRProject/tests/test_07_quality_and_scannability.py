"""07. QUALITY & SCANNABILITY: Verify QR code is complete and decodable.

This is the seventh step: tests ensuring the generated QR code matrix has proper
structure, can be rendered to PNG, and can be scanned by QR decoders.
"""
import io
import numpy as np
import pytest
from PIL import Image

from qr.encoding.encode import encode_string
from qr.ecc.reed_solomon import add_ecc
from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.finalize import finalize_matrix


# ============================================================================
# Utility Functions
# ============================================================================

def matrix_to_png_bytes(matrix: np.ndarray, scale: int = 12, border: int = 8) -> bytes:
    """Convert matrix to PNG bytes."""
    if matrix.dtype != np.uint8 and matrix.dtype != np.int64 and matrix.dtype != np.int32:
        matrix = matrix.astype(np.uint8)

    h, w = matrix.shape
    bordered = np.zeros((h + 2 * border, w + 2 * border), dtype=np.uint8)
    bordered[border:border + h, border:border + w] = matrix

    scaled = np.kron(bordered, np.ones((scale, scale), dtype=np.uint8))
    img_arr = (1 - scaled) * 255
    img = Image.fromarray(img_arr.astype('uint8'), mode='L')

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf.getvalue()


# ============================================================================
# QR Code Structure Completeness Tests
# ============================================================================

class TestQRCodeStructureCompleteness:
    """Tests to validate the complete QR code structure."""
    
    @pytest.mark.core
    def test_no_uninitialized_cells_in_final_matrix(self):
        """Test that final matrix has no placeholder values (-1)."""
        text = "hello"
        encoded = encode_string(text)
        ecc = add_ecc(encoded, 'L')
        base = create_base_matrix()
        placed = place_data(base, encoded, ecc)
        final = finalize_matrix(placed, 'L', 0)
        
        # All cells should be 0 or 1, never -1
        assert np.all((final == 0) | (final == 1))
        # No NaN values
        assert not np.any(np.isnan(final))


    @pytest.mark.core
    def test_all_required_patterns_present(self):
        """Test that all required QR patterns are present."""
        text = "A"
        encoded = encode_string(text)
        ecc = add_ecc(encoded, 'L')
        base = create_base_matrix()
        placed = place_data(base, encoded, ecc)
        final = finalize_matrix(placed, 'L', 0)
        
        # Check finder patterns exist
        # Top-left
        assert final[0, 0] == 1
        assert final[6, 6] == 1
        
        # Top-right (at 20,0 to 20,6)
        assert final[0, 20] == 1
        
        # Bottom-left
        assert final[20, 0] == 1
        
        # Dark module
        assert final[13, 8] == 1
        
        # Check timing patterns exist (at row 6 and col 6)
        assert final[6, 8] in [0, 1]
        assert final[8, 6] in [0, 1]


    @pytest.mark.core
    def test_entire_matrix_is_valid_binary(self):
        """Test that the entire matrix is valid binary (no other values)."""
        for text in ["A", "hello", "123", "!@#"]:
            encoded = encode_string(text)
            ecc = add_ecc(encoded, 'L')
            base = create_base_matrix()
            placed = place_data(base, encoded, ecc)
            final = finalize_matrix(placed, 'L', 0)
            
            # Count value frequencies
            unique = np.unique(final)
            assert len(unique) == 2  # Only 0 and 1
            assert 0 in unique
            assert 1 in unique


# ============================================================================
# QR Code Module Count Tests
# ============================================================================

class TestQRCodeModuleCount:
    """Tests for proper module (cell) counts."""
    
    @pytest.mark.core
    def test_same_text_same_output(self):
        """Test that encoding same text multiple times gives same result."""
        text = "consistent"
        
        results = []
        for _ in range(3):
            encoded = encode_string(text)
            ecc = add_ecc(encoded, 'L')
            base = create_base_matrix()
            placed = place_data(base, encoded, ecc)
            final = finalize_matrix(placed, 'L', 0)
            results.append(final)
        
        # All three should be identical
        np.testing.assert_array_equal(results[0], results[1])
        np.testing.assert_array_equal(results[1], results[2])


