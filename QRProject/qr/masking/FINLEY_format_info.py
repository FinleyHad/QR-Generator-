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
    # Generate the 5 raw format bits (ECC level + mask pattern)
    firstFiveBits = raw_format_bits(ecc_level, mask_id)
    # Shift left by 10 to make room for error correction bits    
    shifted = firstFiveBits << 10
    # Calculate BCH remainder for error correction
    compresedBits = bch_remainder(shifted, FORMAT_BCH_GENERATOR)  
    # Combine the shifted bits with the remainder
    fifteenBits = shifted | compresedBits
    # Apply the format mask using XOR
    finalBits = fifteenBits ^ FORMAT_MASK
    # Convert the 15-bit integer to a list of individual bits (MSB first)
    return [(finalBits >> (14 - i)) & 1 for i in range(15)]

def write_format_bits(matrix: np.ndarray, bits: list[int]) -> None:
    ## Validate that we have exactly 15 format bits
    if len(bits) != 15:
        raise ValueError("Format bits must be exactly 15 bits long")
    
    #gets the upper left format coardinates
    primary_coords = format_coords_primary_v1()

    #gets the bottom right format coardinates
    secondary_coords = format_coords_secondary_v1()

    #writes the bits to the primary coardinates
    for i, (row, col) in enumerate(primary_coords):
        matrix[row, col] = bits[i]

    #writes the bits to the secondary coardinates
    for i, (row, col) in enumerate(secondary_coords):
        matrix[row, col] = bits[i]

# ============================================================
# Helper Functions
# ============================================================

def raw_format_bits(ecc_level: str, mask_id: int) -> int:
    ## Define ECC level to check what bits to use
    ecc_mapping = {
        'L': 0b01,
        'M': 0b00,
        'Q': 0b11,
        'H': 0b10,
    }

    ##ECC valadation
    if ecc_level not in ecc_mapping:
        raise ValueError(f"Invalid ECC level: {ecc_level}. Must be one of {list(ecc_mapping.keys())}")
    
    ##Mask validation
    if not (0 <= mask_id <= 7):
        raise ValueError("mask_id must be in range 0-7")
    
    ## Checks which ECC level were using
    ecc_bits = ecc_mapping[ecc_level]

    ## Combines the ECC bits and mask bits into 5 bits and returns it
    return (ecc_bits << 3) | mask_id

def bch_remainder(value: int, generator: int) -> int:
    # Calculate the degree of the generator polynomial
    gen_degree = generator.bit_length() - 1
    
    # Perform polynomial division until value degree is less than generator degree
    while value.bit_length() - 1 >= gen_degree:
        # Calculate how many positions to shift the generator
        shift = value.bit_length() - generator.bit_length()
        # XOR the shifted generator with the current value
        value ^= (generator << shift)
    
    # Return the remainder after division
    return value


def format_coords_primary_v1() -> list[tuple[int, int]]:
    coords = []
    # Row 8, columns 0-5
    for col in range(6):
        coords.append((8, col))

    # Row 8, column 7
    coords.append((8, 7))
    # Row 8, column 8
    coords.append((8, 8))
    # Column 8, rows 7 down to 0 (skipping row 6)
    for row in range(7, -1, -1):
        # Skip row 6 because it contains the timing pattern
        if row != 6:
            coords.append((row, 8))
    return coords


def format_coords_secondary_v1() -> list[tuple[int, int]]:
    # TODO: Your implementation here
    coords = []
    # Top edge, right side (row 0, columns 20 down to 14)
    for col in range(20, 13, -1):
        coords.append((0, col))
    # Left edge, bottom (column 0, rows 20 down to 13)
    for row in range(20, 12, -1):
        coords.append((row, 0))
    return coords
