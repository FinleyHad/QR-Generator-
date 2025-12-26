from __future__ import annotations

import numpy as np
import logging

logger = logging.getLogger(__name__)

# ============================================================
# QR Format Information Constants (from QR specification)
# ============================================================

# TODO:
# - Generator polynomial used for BCH error correction of format info
# - Fixed by the QR Code specification
FORMAT_BCH_GENERATOR = 0x537   # 10100110111

# TODO:
# - XOR mask applied to final 15 format bits
# - Prevents format bits from looking like QR patterns
FORMAT_MASK = 0x5412           # 101010000010010


# ============================================================
# Public API
# ============================================================

def compute_format_bits(ecc_level: str = "L", mask_id: int = 0) -> list[int]:
    """
    Compute the 15 format bits (MSB → LSB).

    TODO:
    - Validate ecc_level is one of L, M, Q, H
    - Validate mask_id is in range 0..7
    - Generate 5 raw format bits (ECC bits + mask bits)
    - Shift raw bits left by 10 (append 10 zero bits)
    - Compute BCH remainder using FORMAT_BCH_GENERATOR
    - Combine raw bits + remainder into 15 bits
    - XOR final result with FORMAT_MASK
    - Convert final integer into list of 15 bits (MSB → LSB)
    - Return the list of bits
    """
    raw_bits = raw_format_bits(ecc_level, mask_id)
    shifted = raw_bits << 10
    remainder = bch_remainder(shifted, FORMAT_BCH_GENERATOR)
    combined = shifted | remainder
    final = combined ^ FORMAT_MASK
    return [(final >> (14 - i)) & 1 for i in range(15)]


def write_format_bits(matrix: np.ndarray, bits: list[int]) -> None:
    """
    Write the 15 format bits into BOTH format info areas of a Version 1 QR matrix.

    TODO:
    - Validate bits length is exactly 15
    - Retrieve primary format coordinates
    - Retrieve secondary format coordinates
    - Write bits into primary coordinates in order
    - Write bits into secondary coordinates in order
    - Do NOT apply masking here
    """
    if len(bits) != 15:
        raise ValueError("Format bits must be exactly 15 bits long")
    
    primary_coords = format_coords_primary_v1()
    secondary_coords = format_coords_secondary_v1()
    
    for i, (row, col) in enumerate(primary_coords):
        matrix[row, col] = bits[i]
    
    for i, (row, col) in enumerate(secondary_coords):
        matrix[row, col] = bits[i]


# ============================================================
# Raw Format Bits (ECC Level + Mask Pattern)
# ============================================================

def raw_format_bits(ecc_level: str, mask_id: int) -> int:
    """
    Generate the 5 raw format bits as an integer.

    TODO:
    - Define ECC level → 2-bit mapping (L, M, Q, H)
    - Validate ecc_level exists in mapping
    - Validate mask_id is in range 0..7
    - Combine ECC bits and mask bits:
        (ecc_bits << 3) | mask_id
    - Return 5-bit integer
    """
    ecc_mapping = {"L": 0b01, "M": 0b00, "Q": 0b11, "H": 0b10}
    
    if ecc_level not in ecc_mapping:
        raise ValueError(f"Invalid ECC level: {ecc_level}. Must be L, M, Q, or H")
    
    if not (0 <= mask_id <= 7):
        raise ValueError(f"Invalid mask_id: {mask_id}. Must be in range 0..7")
    
    ecc_bits = ecc_mapping[ecc_level]
    return (ecc_bits << 3) | mask_id


# ============================================================
# BCH Remainder (Polynomial Division in GF(2))
# ============================================================

def bch_remainder(value: int, generator: int) -> int:
    """
    Compute the BCH remainder used for QR format info.

    TODO:
    - Determine degree of generator polynomial
    - While value degree >= generator degree:
        - Align generator with MSB of value
        - XOR generator into value
    - Return the remainder (≤ 10 bits)
    """
    gen_degree = generator.bit_length() - 1
    
    while value.bit_length() - 1 >= gen_degree:
        shift = value.bit_length() - generator.bit_length()
        value ^= (generator << shift)
    
    return value


# ============================================================
# Format Information Coordinates (Version 1)
# ============================================================

def format_coords_primary_v1() -> list[tuple[int, int]]:
    """
    Return ordered list of 15 (row, col) positions
    for the PRIMARY format information area.

    TODO:
    - Add coordinates for row 8, columns 0–5
    - Add coordinates for row 8, columns 7 and 8
    - Add coordinates for column 8, rows 7 down to 0
      (skipping timing pattern at row 6)
    - Ensure exactly 15 coordinates
    - Ensure order matches format bit order (MSB → LSB)
    """
    coords = []
    # Row 8, columns 0-5
    for col in range(6):
        coords.append((8, col))
    # Row 8, columns 7 and 8
    coords.append((8, 7))
    coords.append((8, 8))
    # Column 8, rows 7 down to 0 (skipping row 6 - timing pattern)
    for row in range(7, -1, -1):
        if row != 6:
            coords.append((row, 8))
    
    return coords


def format_coords_secondary_v1() -> list[tuple[int, int]]:
    """
    Return ordered list of 15 (row, col) positions
    for the SECONDARY format information area.

    TODO:
    - Add coordinates for column 8, rows 20 down to 14
    - Add coordinates for row 8, columns 13–20
    - Ensure exactly 15 coordinates
    - Ensure order matches primary format order
    """
    coords = []
    # Column 8, rows 20 down to 14
    for row in range(20, 13, -1):
        coords.append((row, 8))
    # Row 8, columns 13-20
    for col in range(13, 21):
        coords.append((8, col))
    
    return coords
