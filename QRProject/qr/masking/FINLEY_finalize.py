from __future__ import annotations
import logging
import numpy as np
from qr.masking.mask0 import apply_mask0
from qr.masking.format_info import (
    compute_format_bits,
    write_format_bits,
    format_coords_primary_v1,
    format_coords_secondary_v1,
)

logger = logging.getLogger(__name__)

SIZE_V1 = 21

## Reversed the map to check if the matrix and parts of the matrix are the correct size
def build_reserved_map_v1() -> np.ndarray:

    reserved = np.zeros((SIZE_V1, SIZE_V1), dtype=bool)##Uses the same size for both rows and columns therfor using SIZE_V1 for both
    ## Helper to mark a cell as reserved
    def mark(r: int, c: int) -> None:
        reserved[r, c] = True
    
    ## Finder patterns (7x7) + 1-cell separators on right/bottom edges (spec)
    ## Top-left
    for r in range(7):
        for c in range(7):
            mark(r, c)
    for c in range(8):
        mark(7, c)  ## bottom separator row
    for r in range(8):
        mark(r, 7)  ## right separator column

    ## Top-right
    for r in range(7):
        for c in range(14, 21):
            mark(r, c)
    for c in range(13, 21):
        mark(7, c)  ## bottom separator row
    for r in range(8):
        mark(r, 13)  ## left separator column

    ## Bottom-left
    for r in range(14, 21):
        for c in range(7):
            mark(r, c)
    for c in range(8):
        mark(13, c)  ## top separator row
    for r in range(13, 21):
        mark(r, 7)  ## right separator column

    ## Timing patterns (entire row 6 and col 6)
    for i in range(SIZE_V1):
        mark(6, i)
        mark(i, 6)

    ## Dark module (Version 1)
    mark(13, 8)

    ## Format info cells (both areas)
    for r, c in format_coords_primary_v1():
        mark(r, c)
    for r, c in format_coords_secondary_v1():
        mark(r, c)

    return reserved

## completes the matrix by applying the mask and writing the format info
def finalize_matrix(
    base_matrix: np.ndarray, 
    ecc_level: str = "L", 
    mask_id: int = 0
) -> np.ndarray:
    # TODO: Your implementation here

    ##Checks for the correct size of the base matrix
    if base_matrix.shape != (SIZE_V1, SIZE_V1):
        raise ValueError(f"Expected {SIZE_V1}x{SIZE_V1}, got {base_matrix.shape}")

    matrix = base_matrix.copy().astype(int)

    reserved = build_reserved_map_v1()
    logger.info("Reserved map built (function + format cells protected).")

    flipped = apply_mask0(matrix, reserved)
    logger.info("Mask 0 applied. Flipped %d modules.", flipped)

    bits = compute_format_bits(ecc_level, mask_id)
    logger.info("Format bits (15): %s", "".join(str(b) for b in bits))

    write_format_bits(matrix, bits)
    logger.info("Format bits written into matrix.")

    ##Ensures that all values in the matrix are either 0 or 1 incase of any errors
    matrix[matrix != 0] = 1
    return matrix
