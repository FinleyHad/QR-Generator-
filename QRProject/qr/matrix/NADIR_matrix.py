"""
NADIR - Matrix & Data Placement Module (Person 3)

Your job: Build the 21×21 QR code grid and place Musa's data into it.

This includes:
1. Creating base matrix with finder patterns (the 3 squares)
2. Adding timing patterns (alternating lines)
3. Adding dark module (required by spec)
4. Placing data in specific zig-zag pattern

Reference implementations are in: layout.py, placement.py (read-only)
"""

import numpy as np


def create_matrix() -> np.ndarray:
    """
    Create 21×21 base QR code matrix with all fixed patterns.
    
    A QR code has several fixed elements:
    - Finder Patterns (3x): 7×7 squares at corners
    - Timing Patterns (2x): Alternating black/white lines
    - Format Information Areas: 8-bit format data areas
    - Dark Module: Single black module at (13, 8)
    - Separators: 1-bit white border around finders
    
    Returns:
        21×21 numpy array with fixed patterns
        -1 = unset (ready for data)
        0 = white module
        1 = black module
    
    Example:
        >>> matrix = create_matrix()
        >>> matrix.shape
        (21, 21)
        >>> matrix[6, 6]  # Corner of finder pattern
        1  # Black
        >>> matrix[10, 10]  # Data area
        -1  # Unset, ready for data
    
    Step-by-step:
    1. Create 21×21 array filled with -1
    2. Draw finder patterns at (0,0), (0,14), (14,0)
    3. Add separators around each finder
    4. Add timing patterns at row 6 and column 6
    5. Add dark module at (13, 8)
    6. Mark format info areas
    7. Return matrix
    """
    # TODO: Implement matrix creation
    raise NotImplementedError("create_matrix() not yet implemented")


def place_data(matrix: np.ndarray, data: list) -> np.ndarray:
    """
    Place encoded data into the QR matrix in zig-zag pattern.
    
    Data placement pattern: right-to-left, column pairs, alternating up/down
    
    Args:
        matrix: Base matrix from create_matrix() with -1 for unset areas
        data: Bit list from Musa's ECC module
    
    Returns:
        Matrix with data placed, ready for masking
        0 = white module
        1 = black module
    
    Example:
        >>> matrix = create_matrix()
        >>> data = [0, 1, 0, 1, ...] # from Musa
        >>> placed_matrix = place_data(matrix, data)
        >>> placed_matrix[10, 20]  # Data area
        0 or 1  # Actual data value
    
    Step-by-step:
    1. Start at bottom-right corner (row 20, col 20-21)
    2. Move upward in column pairs, placing bits
    3. When you reach top, move left 2 columns and go down
    4. Skip timing row (row 6) and timing column (col 6)
    5. Skip finder pattern areas
    6. Continue until all data placed
    """
    # TODO: Implement data placement
    raise NotImplementedError("place_data() not yet implemented")


def get_data_capacity() -> int:
    """
    Return total data capacity (version 1, 21×21 matrix).
    
    Returns:
        Maximum number of bits that can be placed in the matrix
    
    For version 1: 128 bits of data capacity
    """
    # TODO: Calculate or return capacity
    raise NotImplementedError("get_data_capacity() not yet implemented")


def validate_matrix(matrix: np.ndarray) -> bool:
    """
    Verify that matrix structure is correct.
    
    Args:
        matrix: 21×21 matrix to validate
    
    Returns:
        True if structure is valid, False otherwise
    
    Checks:
    - Matrix is 21×21
    - All fixed patterns present
    - All data areas filled (no -1 values)
    - Format info areas ready for masking
    """
    # TODO: Implement validation
    raise NotImplementedError("validate_matrix() not yet implemented")


# ============================================================================
# TESTING YOUR WORK
# ============================================================================
#
# Run tests:
#   pytest tests/test_03_matrix_structure.py tests/test_04_data_placement.py -v
#
# Your tests will check:
#   ✓ create_matrix() produces correct 21×21 grid
#   ✓ All fixed patterns (finders, timing, dark module) present
#   ✓ place_data() accepts data from Musa
#   ✓ Data is placed in correct zig-zag pattern
#   ✓ No unset (-1) values remain
#   ✓ Matrix completeness validated
#
# REFERENCE FILES (READ-ONLY):
#   - layout.py: Fixed patterns implementation
#   - placement.py: Data placement algorithm
#
# DEPENDENCIES:
#   Requires MUSA's ECC working (test_02_ecc.py passing)
#
# When you're done:
#   - All 55 tests pass (test_03 + test_04)
#   - Notify FINLEY (Person 4) that matrix is ready
#
# ============================================================================
