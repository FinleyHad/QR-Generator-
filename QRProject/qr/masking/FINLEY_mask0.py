"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    FINLEY - MASKING & FINALIZATION                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/masking/FINLEY_mask0.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/masking/mask0.py            ← Working apply_mask_pattern_0()
   - qr/masking/finalize.py         ← Working finalize_matrix()
   - qr/masking/format_info.py      ← Format information calculation

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ apply_mask_pattern_0(matrix) → numpy array
     - Apply checkerboard mask to data areas only
     - Preserve fixed patterns (finders, timing, format areas)
     
   ✓ write_format_info(matrix, ecc_level, mask_pattern) → numpy array
     - Write 15-bit format code to reserved areas
     - Encode ECC level and mask pattern
     
   ✓ finalize_matrix(matrix, ecc_level) → numpy array
     - Combine masking + format info
     - Return complete QR code (all 0s and 1s)

📝 YOUR IMPLEMENTATION REPLACES:
   - mask0.py lines 4-30 (apply_mask_pattern_0 function)
   - finalize.py lines 1-20 (finalize_matrix function)
   - format_info.py (format bit calculation)

✅ TESTS TO PASS:
   pytest tests/test_05_masking.py -v

🔗 WHO USES YOUR CODE:
   ← NADIR (Person 3) provides matrix with data placed
   → SULTAN (Person 5) renders your finalized matrix to PNG
   
💡 TIP: Masking is XOR on data areas where (row+col)%2==0. Format info
        requires BCH encoding - you can use lookup tables for common values.
        
═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np


def apply_mask_pattern_0(matrix):
    """
    Apply mask pattern 0 (checkerboard) to the data areas of the matrix.
    
    Mask Pattern 0: Invert modules where (row + col) % 2 == 0
    
    Args:
        matrix: 21×21 numpy array from Nadir with data placed
    
    Returns:
        21×21 numpy array with mask applied to data areas only
    
    Important:
    - DO NOT mask fixed patterns (finders, timing, format info areas)
    - Only mask data areas
    - Masking = XOR operation: flip 0→1 and 1→0
    
    Mask pattern creates checkerboard:
        Row 0: cols 0,2,4,6,8,10,12,14,16,18,20 inverted
        Row 1: cols 1,3,5,7,9,11,13,15,17,19 inverted
        Row 2: cols 0,2,4,6,8,10,12,14,16,18,20 inverted
        ...
    
    Example:
        >>> matrix = place_data(...)  # From Nadir
        >>> masked = apply_mask_pattern_0(matrix)
        >>> masked.shape
        (21, 21)
        # Data areas inverted according to pattern
        # Fixed patterns preserved
    """
    # TODO: Step 1 - Copy matrix to avoid modifying original
    # result = matrix.copy()
    
    # TODO: Step 2 - Define which areas are NOT maskable
    # Create a mask of fixed pattern positions
    # is_fixed = np.zeros((21, 21), dtype=bool)
    
    # TODO: Step 3 - Mark finder patterns as fixed (don't mask)
    # Finder patterns at (0,0), (0,14), (14,0), each 7×7
    # Plus 1-pixel separator around each
    # for r in range(9):
    #     for c in range(9):
    #         is_fixed[r, c] = True  # Top-left finder + separator
    # ... (mark other finder patterns too)
    
    # TODO: Step 4 - Mark timing patterns as fixed
    # Row 6 and column 6
    # is_fixed[6, :] = True
    # is_fixed[:, 6] = True
    
    # TODO: Step 5 - Mark format info areas as fixed
    # Format info areas (will be filled later)
    # is_fixed[8, :9] = True  # Horizontal format
    # is_fixed[:9, 8] = True  # Vertical format
    # ... (mark other format areas)
    
    # TODO: Step 6 - Mark dark module as fixed
    # is_fixed[13, 8] = True
    
    # TODO: Step 7 - Apply mask pattern to non-fixed areas
    # For each cell not in is_fixed:
    #   If (row + col) % 2 == 0:
    #     Invert the module (0→1, 1→0)
    
    # for row in range(21):
    #     for col in range(21):
    #         if not is_fixed[row, col]:
    #             if (row + col) % 2 == 0:
    #                 result[row, col] = 1 - result[row, col]  # Flip bit
    
    raise NotImplementedError("apply_mask_pattern_0() not yet implemented")
    # When ready, replace the line above with:
    # return result


def write_format_info(matrix, ecc_level="M", mask_pattern=0):
    """
    Write format information bits to the QR code.
    
    Format info encodes:
    - Error correction level (2 bits)
    - Mask pattern used (3 bits)
    - BCH error correction for format (10 bits)
    Total: 15 bits
    
    Args:
        matrix: 21×21 masked matrix from apply_mask_pattern_0()
        ecc_level: Error correction level ("L", "M", "Q", "H")
        mask_pattern: Mask pattern number (0-7, we use 0)
    
    Returns:
        21×21 numpy array with format info written
    
    Format bits are written in two locations for redundancy:
    - Near top-left finder: row 8 and column 8
    - Split across top-right and bottom-left finders
    
    Example:
        >>> masked = apply_mask_pattern_0(matrix)
        >>> final = write_format_info(masked, "M", 0)
        >>> final[8, 0]  # Format info position
        0 or 1  # Actual format bit value
    """
    # TODO: Step 1 - Encode error correction level
    # ECC level codes:
    # "L" → 01
    # "M" → 00
    # "Q" → 11
    # "H" → 10
    ecc_bits = ""  # 2 bits
    
    # TODO: Step 2 - Encode mask pattern (3 bits)
    # mask_pattern = 0 → "000"
    mask_bits = ""  # 3 bits
    
    # TODO: Step 3 - Combine ECC and mask bits
    # format_data = ecc_bits + mask_bits  # 5 bits total
    
    # TODO: Step 4 - Calculate BCH error correction (10 bits)
    # This is complex - you can use a lookup table or polynomial division
    # For mask 0 and ECC "M": format bits are specific values
    # You can hard-code common combinations or implement BCH algorithm
    
    # Hint: For "M" level and mask 0, the 15-bit format is:
    # "101010000010010"
    
    # TODO: Step 5 - Apply format mask pattern
    # XOR format bits with "101010000010010" (format mask)
    # final_format = ...
    
    # TODO: Step 6 - Write format bits to matrix
    # Write to row 8 (horizontal) and column 8 (vertical)
    # Also write to other corners for redundancy
    
    # Format positions (example for horizontal):
    # matrix[8, 0] = format_bit_0
    # matrix[8, 1] = format_bit_1
    # ... up to matrix[8, 8]
    
    raise NotImplementedError("write_format_info() not yet implemented")
    # When ready, replace the line above with:
    # return matrix


def finalize_matrix(matrix, ecc_level="M"):
    """
    Complete QR code: apply mask and write format info.
    
    This is the main function that combines everything.
    
    Args:
        matrix: 21×21 matrix from Nadir with data placed
        ecc_level: Error correction level
    
    Returns:
        21×21 finalized QR code matrix (ready for PNG rendering)
        All values are 0 or 1 (no -1)
    
    Example:
        >>> matrix = place_data(...)  # From Nadir
        >>> qr_code = finalize_matrix(matrix, "M")
        >>> qr_code.shape
        (21, 21)
        >>> np.unique(qr_code)
        array([0, 1])  # Only 0s and 1s
    """
    # TODO: Step 1 - Apply mask pattern 0
    # masked = apply_mask_pattern_0(matrix)
    
    # TODO: Step 2 - Write format information
    # final = write_format_info(masked, ecc_level, mask_pattern=0)
    
    # TODO: Step 3 - Replace any remaining -1 with 0 (shouldn't be any in data areas)
    # final[final == -1] = 0
    
    # TODO: Step 4 - Verify matrix is complete (all 0 or 1)
    # assert np.all((final == 0) | (final == 1)), "Matrix has invalid values"
    
    raise NotImplementedError("finalize_matrix() not yet implemented")
    # When ready, replace the line above with:
    # return final


# ============================================================================
# TESTING YOUR CODE
# ============================================================================
# 
# Run: pytest tests/test_05_masking.py -v
# 
# Expected behavior:
#   apply_mask_pattern_0():
#     - Inverts data modules where (row + col) % 2 == 0
#     - Preserves all fixed patterns
#     - Returns 21×21 array
#   
#   write_format_info():
#     - Writes 15-bit format code
#     - Places bits in correct positions
#     - Returns 21×21 array
#   
#   finalize_matrix():
#     - Combines masking + format info
#     - All values are 0 or 1
#     - QR code ready for rendering
#
# Reference: See mask0.py and finalize.py for working implementations
# ============================================================================
