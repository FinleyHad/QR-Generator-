"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    FINLEY - FORMAT INFORMATION                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/masking/FINLEY_format_info.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/masking/format_info.py      ← Working implementation

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ compute_format_bits(ecc_level, mask_id) → list[int]
     - Encode ECC level and mask pattern into 15 bits
     - Apply BCH error correction
     - XOR with format mask
     
   ✓ write_format_bits(matrix, bits) → None
     - Write 15 format bits to two locations in matrix
     - Primary copy: around top-left finder
     - Secondary copy: split between top-right and bottom-left

📝 YOUR IMPLEMENTATION REPLACES:
   - format_info.py lines 27-177 (format bit calculation functions)

✅ TESTS TO PASS:
   pytest tests/test_05_masking.py -v

🔗 WHO USES YOUR CODE:
   ← Called by your own FINLEY_finalize.py
   → Used to encode ECC level and mask pattern
   
💡 TIP: The format bits tell scanners which error correction level and
        mask pattern were used. This is critical for decoding!
        
═══════════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations
import numpy as np
import logging

logger = logging.getLogger(__name__)

# ============================================================
# QR Format Information Constants (from QR specification)
# ============================================================

# Generator polynomial for BCH error correction (fixed by QR spec)
FORMAT_BCH_GENERATOR = 0x537   # Binary: 10100110111

# XOR mask applied to final format bits (prevents pattern confusion)
FORMAT_MASK = 0x5412           # Binary: 101010000010010

# ECC level encoding (2 bits)
ECC_LEVEL_BITS = {
    'L': 0b01,  # 7% recovery
    'M': 0b00,  # 15% recovery
    'Q': 0b11,  # 25% recovery
    'H': 0b10,  # 30% recovery
}


# ============================================================
# Main Functions
# ============================================================

def compute_format_bits(ecc_level: str = "L", mask_id: int = 0) -> list[int]:
    """
    Compute the 15-bit format information string.
    
    Format bits encode:
    - ECC level (2 bits): L=01, M=00, Q=11, H=10
    - Mask pattern (3 bits): 0-7
    - BCH error correction (10 bits)
    
    Process:
    1. Create 5-bit raw value (2 ECC bits + 3 mask bits)
    2. Shift left by 10 to make room for error correction
    3. Calculate BCH remainder for error correction
    4. Combine: (raw << 10) | remainder
    5. XOR with FORMAT_MASK to prevent pattern confusion
    6. Convert to list of 15 bits (MSB first)
    
    Args:
        ecc_level: 'L', 'M', 'Q', or 'H'
        mask_id: 0-7 (we only use 0)
    
    Returns:
        List of 15 bits [1,0,1,0, ...]
    
    Example:
        compute_format_bits('L', 0) → [1,1,1,0,1,1,1,0,0,0,1,0,0,1,0]
    
    TODO: Implement this function
    Steps:
    1. Validate ecc_level is in ECC_LEVEL_BITS
    2. Validate mask_id is 0-7
    3. Get raw_bits using raw_format_bits()
    4. Shift raw_bits left 10: shifted = raw_bits << 10
    5. Calculate remainder using bch_remainder(shifted, FORMAT_BCH_GENERATOR)
    6. Combine: combined = shifted | remainder
    7. XOR with mask: final = combined ^ FORMAT_MASK
    8. Convert to 15-bit list: [(final >> (14-i)) & 1 for i in range(15)]
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement compute_format_bits")


def write_format_bits(matrix: np.ndarray, bits: list[int]) -> None:
    """
    Write the 15 format bits into BOTH format info areas.
    
    Format information appears in TWO places for redundancy:
    - Primary: Around top-left finder pattern
    - Secondary: Split between top-right and bottom-left
    
    Args:
        matrix: 21×21 QR matrix to write into
        bits: List of 15 bits to write
    
    TODO: Implement this function
    Steps:
    1. Validate bits length is 15
    2. Get primary coordinates using format_coords_primary_v1()
    3. Get secondary coordinates using format_coords_secondary_v1()
    4. Loop through primary coords and write bits[i] to matrix[row, col]
    5. Loop through secondary coords and write bits[i] to matrix[row, col]
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement write_format_bits")


# ============================================================
# Helper Functions
# ============================================================

def raw_format_bits(ecc_level: str, mask_id: int) -> int:
    """
    Create 5-bit raw format value (ECC level + mask pattern).
    
    Format: [2 ECC bits][3 mask bits]
    
    Example:
        ECC L (01) + Mask 0 (000) = 01000 = 8
    
    TODO: Implement this function
    Steps:
    1. Get ECC bits from ECC_LEVEL_BITS dictionary
    2. Validate mask_id is 0-7
    3. Combine: (ecc_bits << 3) | mask_id
    4. Return as integer
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement raw_format_bits")


def bch_remainder(value: int, generator: int) -> int:
    """
    Calculate BCH error correction remainder using polynomial division.
    
    This is like long division in binary - we divide 'value' by 'generator'
    and keep only the remainder.
    
    Args:
        value: The data bits (15-bit number)
        generator: BCH generator polynomial (0x537)
    
    Returns:
        10-bit remainder
    
    TODO: Implement this function
    Steps:
    1. While value has bits beyond 10 bits (value >= 1024):
        a. Find highest set bit position
        b. XOR value with (generator << shift_amount)
    2. Return final value (will be < 1024, i.e., 10 bits)
    
    Hint: Use value.bit_length() to find highest bit position
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement bch_remainder")


def format_coords_primary_v1() -> list[tuple[int, int]]:
    """
    Return the 15 (row, col) coordinates for PRIMARY format info area.
    
    Primary format info wraps around the top-left finder pattern:
    - 8 bits along row 8 (next to finder, skipping timing column 6)
    - 7 bits down column 8 (below finder, including timing row 6)
    
    Order: Read left-to-right, then top-to-bottom
    
    Coordinates (in order):
    Row 8: (8,0), (8,1), (8,2), (8,3), (8,4), (8,5), (8,7), (8,8)
    Col 8: (7,8), (5,8), (4,8), (3,8), (2,8), (1,8), (0,8)
    
    Note: Skip (8,6) and (6,8) because they're timing pattern
    
    TODO: Implement this function
    Return list of 15 (row, col) tuples in correct order
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement format_coords_primary_v1")


def format_coords_secondary_v1() -> list[tuple[int, int]]:
    """
    Return the 15 (row, col) coordinates for SECONDARY format info area.
    
    Secondary format info is split:
    - 7 bits: Top edge, right side (row 0, columns 20 down to 14)
    - 8 bits: Left edge, bottom (column 0, rows 20 down to 13)
    
    Order matches bit sequence 0-14
    
    Coordinates (in order):
    Top: (0,20), (0,19), (0,18), (0,17), (0,16), (0,15), (0,14)
    Left: (20,0), (19,0), (18,0), (17,0), (16,0), (15,0), (14,0), (13,0)
    
    TODO: Implement this function
    Return list of 15 (row, col) tuples in correct order
    """
    # TODO: Your implementation here
    raise NotImplementedError("TODO: Implement format_coords_secondary_v1")


# ═══════════════════════════════════════════════════════════════════════════
# TESTING HELPERS
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Testing FINLEY_format_info.py...")
    
    try:
        bits = compute_format_bits('L', 0)
        print(f"✓ Format bits computed: {len(bits)} bits")
        print(f"  Bits: {''.join(map(str, bits))}")
    except NotImplementedError:
        print("✗ compute_format_bits() not implemented yet")
    
    try:
        coords = format_coords_primary_v1()
        print(f"✓ Primary coordinates: {len(coords)} coords")
    except NotImplementedError:
        print("✗ format_coords_primary_v1() not implemented yet")
    
    try:
        coords = format_coords_secondary_v1()
        print(f"✓ Secondary coordinates: {len(coords)} coords")
    except NotImplementedError:
        print("✗ format_coords_secondary_v1() not implemented yet")
