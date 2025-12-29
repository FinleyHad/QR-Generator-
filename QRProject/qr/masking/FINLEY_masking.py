"""
FINLEY - Masking & Finalization Module (Person 4)

Your job: Apply masking pattern to Nadir's matrix and write final format info.

Masking: Applies a checkerboard pattern to break up patterns and improve scannability
Format Info: Writes error correction level and mask pattern used

Reference implementations are in: mask0.py, format_info.py (read-only)
"""

import numpy as np


def apply_mask_pattern_0(matrix: np.ndarray) -> np.ndarray:
    """
    Apply mask pattern 0 (checkerboard) to the QR matrix.
    
    Pattern 0: (row + col) % 2 == 0 → invert module
    This creates a checkerboard effect
    
    Args:
        matrix: 21×21 matrix from Nadir with data placed
    
    Returns:
        21×21 matrix with mask applied
    
    Important:
    - DO NOT mask fixed patterns (finders, timing, dark module, format info areas)
    - Only mask data areas
    - Masking is XOR operation: 0→1, 1→0
    
    Example:
        >>> matrix = np.array([[0, 1], [1, 0]])
        >>> masked = apply_mask_pattern_0(matrix)
        >>> masked  # Checkerboard applied
        array([[1, 1], [1, 1]])  # All inverted
    
    Step-by-step:
    1. Create checkerboard pattern: (row + col) % 2
    2. For each data area cell:
       - If pattern is 0: XOR the module (flip 0↔1)
       - If pattern is 1: leave unchanged
    3. Do NOT apply mask to finder patterns or timing patterns
    4. Return masked matrix
    """
    # TODO: Implement mask pattern 0
    raise NotImplementedError("apply_mask_pattern_0() not yet implemented")


def write_format_info(matrix: np.ndarray, ecc_level: str = "M") -> np.ndarray:
    """
    Write format information bits to reserved areas of QR code.
    
    Format info includes:
    - Error correction level (2 bits)
    - Mask pattern used (3 bits)
    - BCH checksum (3 bits)
    
    Args:
        matrix: 21×21 masked matrix from apply_mask_pattern_0()
        ecc_level: Error correction level ("L", "M", "Q", "H")
    
    Returns:
        21×21 matrix with format info written
    
    Format info is written in two locations (separated by finder patterns):
    - Top-left: horizontal strip (8 bits) + vertical strip (8 bits)
    - Other corners: similar format (for redundancy)
    
    Example:
        >>> masked = apply_mask_pattern_0(matrix)
        >>> final = write_format_info(masked, "M")
        >>> final[8, 0]  # Format info area
        0 or 1  # Actual format bits
    
    Step-by-step:
    1. Determine format code from ECC level and mask pattern
    2. Apply BCH polynomial division for checksum
    3. Write 8 bits across row 8 (format info horizontal)
    4. Write 8 bits down column 8 (format info vertical)
    5. Repeat for other corners if implementing full spec
    6. Return finalized matrix
    """
    # TODO: Implement format info writing
    raise NotImplementedError("write_format_info() not yet implemented")


def finalize_matrix(matrix: np.ndarray, ecc_level: str = "M") -> np.ndarray:
    """
    Complete QR code: apply mask and write format info.
    
    This is the final step before rendering to PNG.
    
    Args:
        matrix: 21×21 matrix from Nadir with all data placed
        ecc_level: Error correction level used
    
    Returns:
        21×21 finalized QR code matrix (0s and 1s only, no -1)
    
    Example:
        >>> matrix = place_data(...)  # From Nadir
        >>> qr_code = finalize_matrix(matrix, "M")
        >>> qr_code.shape
        (21, 21)
        >>> np.unique(qr_code)
        array([0, 1])  # Only 0s and 1s, no -1
    
    Step-by-step:
    1. Apply mask pattern 0
    2. Write format information
    3. Verify matrix is complete (no -1 values)
    4. Return final QR code
    """
    # TODO: Implement finalization
    raise NotImplementedError("finalize_matrix() not yet implemented")


def validate_finalized_matrix(matrix: np.ndarray) -> bool:
    """
    Verify the finalized matrix is complete and valid.
    
    Args:
        matrix: Finalized 21×21 matrix
    
    Returns:
        True if valid, False otherwise
    
    Checks:
    - Matrix is 21×21
    - All values are 0 or 1 (no -1)
    - Fixed patterns preserved
    - Format info written
    """
    # TODO: Implement validation
    raise NotImplementedError("validate_finalized_matrix() not yet implemented")


# ============================================================================
# TESTING YOUR WORK
# ============================================================================
#
# Run tests:
#   pytest tests/test_05_masking.py -v
#
# Your tests will check:
#   ✓ apply_mask_pattern_0() creates correct checkerboard
#   ✓ Fixed patterns NOT masked
#   ✓ write_format_info() writes correct format bits
#   ✓ finalize_matrix() produces complete matrix
#   ✓ No -1 values remain
#   ✓ All masked matrices are valid
#
# REFERENCE FILES (READ-ONLY):
#   - mask0.py: Mask pattern implementation
#   - format_info.py: Format information calculation
#
# DEPENDENCIES:
#   Requires NADIR's matrix working (test_03 + test_04 passing)
#
# When you're done:
#   - All 45 tests pass
#   - Notify SULTAN (Person 5) that masking is ready
#
# ============================================================================
