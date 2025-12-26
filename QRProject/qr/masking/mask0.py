import numpy as np
import logging

logger = logging.getLogger(__name__)

def apply_mask0(matrix: np.ndarray, reserved: np.ndarray) -> int:
    """
    Apply QR mask pattern 0 to data/ECC cells only.
    Mask rule: flip when (r + c) % 2 == 0
    reserved[r, c] == True means do NOT touch that cell.
    Returns number of flipped modules.
    """
    if matrix.shape != reserved.shape:
        raise ValueError("matrix and reserved must have the same shape")

    rows, cols = matrix.shape
    flipped = 0

    logger.info("Applying Mask Pattern 0")

    for r in range(rows):
        for c in range(cols):
            if reserved[r, c]:
                continue
            if (r + c) % 2 == 0:
                matrix[r, c] ^= 1
                flipped += 1

    logger.info("Mask Pattern 0 applied. Number of modules flipped: %d", flipped)
    return flipped
