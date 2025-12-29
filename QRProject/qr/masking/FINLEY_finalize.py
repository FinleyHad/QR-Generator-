"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    FINLEY - FINALIZATION & FORMAT INFO                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/masking/FINLEY_finalize.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/masking/finalize.py         ← Working finalize_matrix()
   - qr/masking/format_info.py      ← Format information calculation

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ finalize_matrix(matrix, ecc_level, mask_id) → numpy array
     - Apply mask pattern (call your FINLEY_mask0.apply_mask0)
     - Calculate format information bits
     - Write format bits to reserved areas
     - Return final 0/1 matrix ready for rendering

📝 YOUR IMPLEMENTATION REPLACES:
   - finalize.py lines 18-108 (the finalize_matrix and helper functions)

✅ TESTS TO PASS:
   pytest tests/test_05_masking.py -v

🔗 WHO USES YOUR CODE:
   ← NADIR (Person 3) provides the matrix with data placed
   → SULTAN (Person 5) uses your finalized matrix for rendering
   
💡 TIP: Import your own apply_mask0 from FINLEY_mask0.py and call it!
        
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import logging
import numpy as np

# TODO: Import your apply_mask0 from FINLEY_mask0
# from qr.masking.FINLEY_mask0 import apply_mask0

# Import format info functions from reference
from qr.masking.format_info import (
    compute_format_bits,
    write_format_bits,
    format_coords_primary_v1,
    format_coords_secondary_v1,
)

logger = logging.getLogger(__name__)

SIZE_V1 = 21


def build_reserved_map_v1() -> np.ndarray:
    """
    Create a 21×21 boolean map showing which cells are RESERVED (fixed patterns).
    
    Reserved cells include:
    - Finder patterns (3 corners): 7×7 squares
    - Separators: 1-pixel white borders around finders
    - Timing patterns: Row 6 and Column 6
    - Dark module: (4*version + 9, 8) = (13, 8) for Version 1
    - Format information areas: Two copies along finder edges
    
    These cells should NOT be masked - they stay as-is.
    
    Returns:
        21×21 boolean array where True = reserved (don't mask)
    
    TODO: Implement this function
    Steps:
    1. Create 21×21 array of False
    2. Mark finder patterns + separators as True
    3. Mark timing patterns (row 6, col 6) as True
    4. Mark dark module at (13, 8) as True
    5. Mark format info areas as True using format_coords functions
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement build_reserved_map_v1")


def finalize_matrix(
    base_matrix: np.ndarray, 
    ecc_level: str = "L", 
    mask_id: int = 0
) -> np.ndarray:
    """
    Finalize a Version 1 QR matrix by applying mask and writing format info.
    
    This is the FINAL step before rendering to PNG. After this, the matrix
    is complete and ready to scan!
    
    Steps:
    1. Make a copy of the input matrix
    2. Build reserved map (which cells to protect from masking)
    3. Apply mask pattern to data/ECC cells only
    4. Calculate format information bits (ECC level + mask pattern)
    5. Write format bits to both format areas
    6. Ensure all values are 0 or 1 (no -1s or other values)
    
    Args:
        base_matrix: 21×21 matrix with data placed (may have -1 for empty)
        ecc_level: Error correction level ('L', 'M', 'Q', 'H')
        mask_id: Mask pattern ID (0-7, we only implement 0)
    
    Returns:
        21×21 numpy array with only 0s and 1s, ready for rendering
    
    Example:
        Input matrix has data bits placed, some -1 for format areas
        Output matrix has mask applied, format bits written, all 0/1
    
    TODO: Implement this function
    Steps:
    1. Validate input is 21×21
    2. Copy matrix and convert to int
    3. Build reserved map using build_reserved_map_v1()
    4. Apply mask using your apply_mask0() from FINLEY_mask0
    5. Compute format bits using compute_format_bits(ecc_level, mask_id)
    6. Write format bits using write_format_bits(matrix, bits)
    7. Convert all non-zero values to 1
    8. Return finalized matrix
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement finalize_matrix")


# ═══════════════════════════════════════════════════════════════════════════
# TESTING HELPERS (You can use these to test your implementation)
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Quick test of your implementation
    print("Testing FINLEY_finalize.py...")
    
    # Create a simple test matrix
    test_matrix = np.random.randint(0, 2, (21, 21))
    
    try:
        reserved = build_reserved_map_v1()
        print(f"✓ Reserved map created: {reserved.shape}")
        print(f"  Reserved cells: {np.sum(reserved)}")
    except NotImplementedError:
        print("✗ build_reserved_map_v1() not implemented yet")
    
    try:
        result = finalize_matrix(test_matrix, "L", 0)
        print(f"✓ Finalize matrix works: {result.shape}")
        print(f"  All values 0/1: {np.all((result == 0) | (result == 1))}")
    except NotImplementedError:
        print("✗ finalize_matrix() not implemented yet")
