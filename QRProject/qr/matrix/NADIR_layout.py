"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    NADIR - MATRIX LAYOUT & DATA PLACEMENT                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/matrix/NADIR_layout.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/matrix/layout.py            ← Working create_base_matrix() and place_data()
   - qr/matrix/placement.py         ← Data placement algorithm details

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ create_base_matrix() → numpy array (21×21)
     - Create base matrix with finder patterns, timing, dark module
     - Return matrix with -1 for data areas, 0/1 for fixed patterns
     
   ✓ place_data(matrix, encoded_bits, ecc_codewords) → numpy array
     - Place data and ECC bits in zig-zag pattern
     - Fill all -1 areas with actual data
     - Return complete matrix ready for masking

📝 YOUR IMPLEMENTATION REPLACES:
   - layout.py lines 4-53 (create_base_matrix function)
   - layout.py lines 56-162 (place_data function)

✅ TESTS TO PASS:
   pytest tests/test_03_matrix_structure.py -v
   pytest tests/test_04_data_placement.py -v

🔗 WHO USES YOUR CODE:
   ← MUSA (Person 2) provides data+ECC codewords
   → FINLEY (Person 4) applies masking to your matrix
   
💡 TIP: create_base_matrix() sets up the structure, place_data() fills it.
        Work on structure first, then data placement. Use numpy arrays.
        
═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np


def create_base_matrix():
    """
    Create the Version 1 (21×21) base QR code matrix.
    
    Returns:
        numpy array (21×21) with:
        - -1 for cells ready for data placement
        - 0 for white modules (fixed patterns)
        - 1 for black modules (fixed patterns)
    
    Fixed patterns to add:
    1. Finder patterns (3x): 7×7 squares at corners
       - Top-left (0, 0)
       - Top-right (0, 14)
       - Bottom-left (14, 0)
    
    2. Separators: 1-pixel white border around each finder
    
    3. Timing patterns: Alternating black/white on row 6 and column 6
       - Row 6: alternates by column index (even=1, odd=0)
       - Column 6: alternates by row index (even=1, odd=0)
    
    4. Dark module: Always black at position (13, 8)
    
    5. Format information areas: Reserved for format bits
       - Around finders (will be filled by Finley)
    
    Example:
        >>> matrix = create_base_matrix()
        >>> matrix.shape
        (21, 21)
        >>> matrix[0, 0]  # Top-left of finder pattern
        1
        >>> matrix[6, 0]  # Part of timing pattern
        1  # (row 6, col 0 → even col → 1)
        >>> matrix[10, 10]  # Data area
        -1  # Ready for data
    """
    # TODO: Step 1 - Create 21×21 matrix filled with -1
    size = 21
    matrix = None  # Should be: np.full((size, size), -1, dtype=int)
    
    # TODO: Step 2 - Define finder pattern (7×7)
    # Finder pattern looks like:
    # 1 1 1 1 1 1 1
    # 1 0 0 0 0 0 1
    # 1 0 1 1 1 0 1
    # 1 0 1 1 1 0 1
    # 1 0 1 1 1 0 1
    # 1 0 0 0 0 0 1
    # 1 1 1 1 1 1 1
    
    def place_finder_pattern(row, col):
        """Place a 7×7 finder pattern at (row, col)."""
        # TODO: Define the pattern as a 2D list
        pattern = [
            # [1, 1, 1, 1, 1, 1, 1],
            # [1, 0, 0, 0, 0, 0, 1],
            # ... complete this
        ]
        # TODO: Copy pattern into matrix at position (row, col)
        # for i in range(7):
        #     for j in range(7):
        #         matrix[row + i, col + j] = pattern[i][j]
        pass
    
    # TODO: Step 3 - Place 3 finder patterns
    # place_finder_pattern(0, 0)    # Top-left
    # place_finder_pattern(0, 14)   # Top-right
    # place_finder_pattern(14, 0)   # Bottom-left
    
    # TODO: Step 4 - Add timing patterns on row 6 and column 6
    # Timing pattern alternates: 1-0-1-0-1-0...
    # Only set cells that are still -1 (don't overwrite finder patterns)
    # for i in range(21):
    #     # Row 6: timing pattern
    #     if matrix[6, i] == -1:
    #         matrix[6, i] = 1 if i % 2 == 0 else 0
    #     # Column 6: timing pattern
    #     if matrix[i, 6] == -1:
    #         matrix[i, 6] = 1 if i % 2 == 0 else 0
    
    # TODO: Step 5 - Add dark module at (13, 8)
    # matrix[13, 8] = 1
    
    # TODO: Step 6 - Reserve format information areas (set to -1)
    # Format info goes in specific positions around finders
    # for i in range(9):
    #     if i < 6:
    #         matrix[8, i] = -1        # Horizontal format area
    #         matrix[i, 8] = -1        # Vertical format area
    #     if i < 7:
    #         matrix[8, 14 + i] = -1   # Right side format
    #         matrix[14 + i, 8] = -1   # Bottom format
    
    raise NotImplementedError("create_base_matrix() not yet implemented")
    # When ready, replace the line above with:
    # return matrix


def place_data(matrix, encoded_bits, ecc_codewords):
    """
    Place data and ECC bits into the matrix.
    
    Args:
        matrix: Base matrix from create_base_matrix() (21×21 with -1 for data areas)
        encoded_bits: Bitstring or list of data codewords from Mustapha
        ecc_codewords: ECC codewords from Musa (may include data prefix)
    
    Returns:
        numpy array (21×21) with data placed (no more -1 values except format areas)
    
    Data placement pattern:
    - Start at bottom-right (row 20, col 20-21)
    - Move in column pairs, alternating up/down
    - Skip timing patterns (row 6, col 6)
    - Skip finder patterns and format areas
    - Place bits from right to left, top to bottom within each column pair
    
    Example:
        >>> matrix = create_base_matrix()
        >>> data_bits = "0100" + "00000001" + "01000001" + ...  # From Mustapha
        >>> ecc_bits = [234, 12, 89, ...]  # From Musa
        >>> filled_matrix = place_data(matrix, data_bits, ecc_bits)
        >>> np.all((filled_matrix == 0) | (filled_matrix == 1) | (filled_matrix == -1))
        True
        >>> filled_matrix[20, 20]  # Bottom-right data area
        0 or 1  # Actual data bit
    """
    size = 21
    
    # TODO: Step 1 - Normalize encoded_bits to bitstring
    # Handle both string and list inputs
    # if isinstance(encoded_bits, (list, tuple)):
    #     encoded_bits_str = ''.join(format(b, '08b') if isinstance(b, int) else str(b) 
    #                                 for b in encoded_bits)
    # else:
    #     encoded_bits_str = ''.join(str(b) for b in encoded_bits)
    
    # TODO: Step 2 - Normalize ECC codewords to bitstring
    # If ecc_codewords includes data (longer list), slice off data prefix
    # ecc_input = ecc_codewords
    # if isinstance(ecc_codewords, (list, tuple)) and len(ecc_codewords) > len(encoded_bits):
    #     ecc_input = ecc_codewords[len(encoded_bits):]
    
    # TODO: Step 3 - Combine data and ECC into single bitstring
    # all_bits = encoded_bits_str + ecc_bits_str
    
    # TODO: Step 4 - Place bits in zig-zag pattern
    # Start at bottom-right, move up in column pairs (20-21, 18-19, etc.)
    # When you hit top, move left 2 columns and go down
    # Skip column 6 (timing pattern)
    
    # Pseudocode:
    # bit_index = 0
    # col = 20  # Start at rightmost column pair
    # going_up = True
    # 
    # while col >= 0:
    #     if col == 6:  # Skip timing column
    #         col -= 1
    #         continue
    #     
    #     # Process column pair (col, col-1)
    #     if going_up:
    #         for row in range(20, -1, -1):  # Bottom to top
    #             # Place bits in column pair
    #     else:
    #         for row in range(0, 21):  # Top to bottom
    #             # Place bits in column pair
    #     
    #     col -= 2  # Move left to next column pair
    #     going_up = not going_up  # Alternate direction
    
    raise NotImplementedError("place_data() not yet implemented")
    # When ready, replace the line above with:
    # return matrix


# ============================================================================
# TESTING YOUR CODE
# ============================================================================
# 
# Run: pytest tests/test_03_matrix_structure.py -v
# Run: pytest tests/test_04_data_placement.py -v
# 
# Expected behavior for create_base_matrix():
#   - Returns 21×21 numpy array
#   - Finder patterns at (0,0), (0,14), (14,0)
#   - Timing patterns on row 6 and column 6
#   - Dark module at (13, 8)
#   - Format areas reserved as -1
#   - Data areas marked as -1
#
# Expected behavior for place_data():
#   - Accepts matrix, data bits, and ECC codes
#   - Places all bits in zig-zag pattern
#   - No -1 values remain in data areas
#   - Format areas still -1 (filled by Finley)
#
# Reference: See layout.py and placement.py for working implementations
# ============================================================================
