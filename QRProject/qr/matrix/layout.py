import numpy as np

def create_base_matrix():
    """Create the Version 1 (21x21) base matrix as a numpy array.

    Uses -1 as a placeholder for undecided cells which will later be
    replaced with 0 when data placement is complete.
    """
    size = 21
    matrix = np.full((size, size), -1, dtype=int)

    def place_finder_pattern(row, col):
        pattern = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]
        for i in range(7):
            for j in range(7):
                matrix[row + i, col + j] = pattern[i][j]

    place_finder_pattern(0, 0)
    place_finder_pattern(0, 14)
    place_finder_pattern(14, 0)

    # Timing patterns: alternating 1-0-1-0... on row 6 and column 6
    # Run across the ENTIRE row/column except separators (which are -1)
    for i in range(21):
        # Row 6: timing pattern alternating by column index
        if matrix[6, i] == -1:  # Only if not already set as separator
            matrix[6, i] = 1 if i % 2 == 0 else 0
        # Column 6: timing pattern alternating by row index
        if matrix[i, 6] == -1:  # Only if not already set as separator
            matrix[i, 6] = 1 if i % 2 == 0 else 0

    # Dark module (always 1)
    matrix[13, 8] = 1

    for i in range(9):
        if i < 6:
            matrix[8, i] = -1
            matrix[i, 8] = -1
        if i < 7:
            matrix[8, 14 + i] = -1
            matrix[14 + i, 8] = -1

    return matrix


def place_data(matrix, encoded_bits, ecc_codewords):
    """Place data and ECC bits into the matrix.

    Accepts either:
    - encoded_bits: string of '0'/'1' bits OR list of data codewords (ints)
    - ecc_codewords: string/list similar to above (usually list of ints)

    Note: our ``add_ecc`` helper returns *data + ecc* for API compatibility.
    If the ECC list is longer than the data list, we treat the trailing
    portion as ECC only to avoid double-placing data bits.
    """
    size = 21

    # Normalize encoded_bits to a single bitstring
    if isinstance(encoded_bits, (list, tuple)):
        encoded_bits_str = ''.join(format(b, '08b') if isinstance(b, int) else str(b) for b in encoded_bits)
    else:
        encoded_bits_str = ''.join(str(b) for b in encoded_bits)

    # Normalize ecc_codewords to bitstring (slice off data prefix if present)
    ecc_input = ecc_codewords
    if isinstance(ecc_codewords, (list, tuple)) and len(ecc_codewords) > len(encoded_bits):
        # add_ecc returned data+ecc; keep only the ECC tail
        ecc_input = ecc_codewords[len(encoded_bits):]

    if isinstance(ecc_input, (list, tuple)):
        ecc_bits_str = ''.join(format(c, '08b') if isinstance(c, int) else str(c) for c in ecc_input)
    else:
        ecc_bits_str = ''.join(str(b) for b in ecc_input)

    all_bits = encoded_bits_str + ecc_bits_str

    bit_index = 0

    def is_reserved(row, col):
        if row < 9 and col < 9:
            return True
        if row < 9 and col >= 13:
            return True
        if row >= 13 and col < 9:
            return True
        if row == 6 or col == 6:  # Timing patterns (entire row 6 and col 6)
            return True
        if row == 13 and col == 8:  # Dark module
            return True
        # Format information cells (must not be overwritten with data)
        if row == 8 and col <= 8:  # Primary format area: row 8, cols 0-8
            return True
        if row == 8 and col >= 13:  # Secondary format area: row 8, cols 13-20
            return True
        if col == 8 and row <= 8:  # Primary format area: col 8, rows 0-8
            return True
        if col == 8 and row >= 13:  # Secondary format area: col 8, rows 13-20
            return True
        return False

    col = size - 1
    up = True

    while col > 0:
        if col == 6:
            col -= 1
            continue

        if up:
            for row in range(size - 1, -1, -1):
                if not is_reserved(row, col):
                    if bit_index < len(all_bits):
                        matrix[row, col] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row, col] = 0

                if not is_reserved(row, col - 1):
                    if bit_index < len(all_bits):
                        matrix[row, col - 1] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row, col - 1] = 0
        else:
            for row in range(size):
                if not is_reserved(row, col):
                    if bit_index < len(all_bits):
                        matrix[row, col] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row, col] = 0

                if not is_reserved(row, col - 1):
                    if bit_index < len(all_bits):
                        matrix[row, col - 1] = int(all_bits[bit_index])
                        bit_index += 1
                    else:
                        matrix[row, col - 1] = 0

        up = not up
        col -= 2

    # Replace any remaining placeholders (-1) with 0
    try:
        matrix[matrix == -1] = 0
    except Exception:
        # Fallback for non-numpy matrix
        for r in range(size):
            for c in range(size):
                if matrix[r][c] == -1:
                    matrix[r][c] = 0

    return matrix