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


def finalize_matrix(base_matrix: np.ndarray, ecc_level: str = "L", mask_id: int = 0) -> np.ndarray:
    """
    Finalize a Version 1 QR matrix:
    - Apply mask pattern 0 to DATA/ECC cells only
    - Compute + write format information bits (ECC L, mask 0)
    - Return final 21x21 numpy array of 0/1
    """
    if base_matrix.shape != (SIZE_V1, SIZE_V1):
        raise ValueError(f"Expected {SIZE_V1}x{SIZE_V1}, got {base_matrix.shape}")

    m = base_matrix.copy().astype(int)

    reserved = build_reserved_map_v1()
    logger.info("Reserved map built (function + format cells protected).")

    # 1) Mask (pattern 0) on data cells only (mask_id currently fixed to 0)
    # Future: support mask_id 1..7 when mask implementations are available
    flipped = apply_mask0(m, reserved)
    logger.info("Mask 0 applied. Flipped %d modules.", flipped)

    # 2) Format bits for selected ECC level + mask id
    bits = compute_format_bits(ecc_level, mask_id)
    logger.info("Format bits (15): %s", "".join(str(b) for b in bits))

    # 3) Write format bits (both copies)
    write_format_bits(m, bits)
    logger.info("Format bits written into matrix.")

    # 4) Safety: enforce 0/1 only
    m[m != 0] = 1
    return m


def build_reserved_map_v1() -> np.ndarray:
    """
    Build boolean map of cells that must NOT be masked:
    - Finder patterns + separators (9x9 blocks in 3 corners)
    - Timing patterns (row 6 and col 6)
    - Dark module (13, 8)
    - Format information cells (both copies)
    """
    reserved = np.zeros((SIZE_V1, SIZE_V1), dtype=bool)

    def mark(r: int, c: int) -> None:
        reserved[r, c] = True

    # Finder patterns (7x7) + 1-cell separators on right/bottom edges (spec)
    # Top-left
    for r in range(7):
        for c in range(7):
            mark(r, c)
    for c in range(8):
        mark(7, c)  # bottom separator row
    for r in range(8):
        mark(r, 7)  # right separator column

    # Top-right
    for r in range(7):
        for c in range(14, 21):
            mark(r, c)
    for c in range(13, 21):
        mark(7, c)  # bottom separator row
    for r in range(8):
        mark(r, 13)  # left separator column

    # Bottom-left
    for r in range(14, 21):
        for c in range(7):
            mark(r, c)
    for c in range(8):
        mark(13, c)  # top separator row
    for r in range(13, 21):
        mark(r, 7)  # right separator column

    # Timing patterns (entire row 6 and col 6)
    for i in range(SIZE_V1):
        mark(6, i)
        mark(i, 6)

    # Dark module (Version 1)
    mark(13, 8)

    # Format info cells (both areas)
    for r, c in format_coords_primary_v1():
        mark(r, c)
    for r, c in format_coords_secondary_v1():
        mark(r, c)

    return reserved
