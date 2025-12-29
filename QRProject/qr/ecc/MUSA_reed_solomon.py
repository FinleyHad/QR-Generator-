"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    MUSA - REED-SOLOMON ERROR CORRECTION                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/ecc/MUSA_reed_solomon.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/ecc/reed_solomon.py         ← Working implementation of add_ecc()

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ add_ecc(data_codewords, ecc_level) → list[int]
     - Takes 19 data bytes from Mustapha
     - Adds Reed-Solomon error correction codes
     - Returns data + ECC (26-36 bytes depending on level)

📝 YOUR IMPLEMENTATION REPLACES:
   - reed_solomon.py lines 31-63 (the add_ecc function)

✅ TESTS TO PASS:
   pytest tests/test_02_ecc.py -v

🔗 WHO USES YOUR CODE:
   ← MUSTAPHA (Person 1) provides the 19 data codewords
   → NADIR (Person 3) uses your data+ECC for matrix placement
   
💡 TIP: Use the reedsolo library (pip install reedsolo). The math is done
        for you - just create RSCodec(ecc_count) and encode the data.
        
═══════════════════════════════════════════════════════════════════════════
"""

# Try to import Reed-Solomon library
try:
    from reedsolo import RSCodec
except ImportError:
    print("ERROR: reedsolo not installed. Run: pip install reedsolo")
    RSCodec = None

# Version 1 QR Code ECC specifications
DATA_CODEWORDS = 19  # Always 19 data bytes for Version 1

# ECC codeword counts for each error correction level
ECC_BY_LEVEL = {
    "L": 7,   # Low - 7% recovery
    "M": 10,  # Medium - 15% recovery (default)
    "Q": 13,  # Quartile - 25% recovery
    "H": 17,  # High - 30% recovery
}

# Backwards-compatible alias for tests
ECC_CODEWORDS = ECC_BY_LEVEL["L"]


def add_ecc(data_codewords: list[int], ecc_level: str = "L") -> list[int]:
    """
    Add Reed-Solomon error correction codes to data codewords.
    
    Args:
        data_codewords: List of exactly 19 integers (0-255) from Mustapha's encoder
        ecc_level: Error correction level - "L", "M", "Q", or "H" (default "L")
    
    Returns:
        list[int]: Complete codeword list = data + ECC codes
        
        Length depends on ECC level:
        - "L": 19 data + 7 ECC = 26 total
        - "M": 19 data + 10 ECC = 29 total
        - "Q": 19 data + 13 ECC = 32 total
        - "H": 19 data + 17 ECC = 36 total
    
    Example:
        >>> data = [65, 66, 67, ...]  # 19 bytes from encoder
        >>> result = add_ecc(data, "M")
        >>> len(result)
        29  # 19 data + 10 ECC
        >>> result[:19]  # First 19 are original data
        [65, 66, 67, ...]
        >>> result[19:]  # Last 10 are ECC codes
        [234, 12, 89, ...]  # Calculated by Reed-Solomon
    
    Process:
    1. Validate inputs (19 codewords, valid level, all 0-255)
    2. Get ECC count for the level from ECC_BY_LEVEL
    3. Create RSCodec with ECC count
    4. Encode data to get data + ECC
    5. Return complete list
    """
    # TODO: Step 1 - Normalize ECC level to uppercase
    ecc_level = ""  # Should be ecc_level.upper()
    
    # TODO: Step 2 - Validate data_codewords length
    # if len(data_codewords) != DATA_CODEWORDS:
    #     raise ValueError(f"Version 1 requires {DATA_CODEWORDS} data codewords")
    
    # TODO: Step 3 - Validate ECC level is valid
    # if ecc_level not in ECC_BY_LEVEL:
    #     raise ValueError(f"Unknown ECC level: {ecc_level}")
    
    # TODO: Step 4 - Validate all codewords are in range 0-255
    # if not all(0 <= b <= 255 for b in data_codewords):
    #     raise ValueError("Codewords must be in range 0–255")
    
    # TODO: Step 5 - Get ECC count for this level
    ecc_count = 0  # Should be ECC_BY_LEVEL[ecc_level]
    
    # TODO: Step 6 - Create Reed-Solomon codec
    # rs = RSCodec(ecc_count)
    
    # TODO: Step 7 - Encode data (returns bytes with data + ECC)
    # encoded = rs.encode(bytes(data_codewords))
    
    # TODO: Step 8 - Extract ECC codes (last ecc_count bytes)
    # ecc = list(encoded[-ecc_count:])
    
    # TODO: Step 9 - Print debug info (optional)
    # print("ECC Level:", ecc_level)
    # print("ECC Codewords:", ecc)
    # print("Final Codeword Count:", len(encoded))
    
    # TODO: Step 10 - Return full list (data + ECC)
    raise NotImplementedError("add_ecc() not yet implemented")
    # When ready, replace the line above with:
    # return list(encoded)


# ============================================================================
# TESTING YOUR CODE
# ============================================================================
# 
# Run: pytest tests/test_02_ecc.py::test_add_ecc_level_L -v
# 
# Expected behavior:
#   Input: 19 data codewords
#   Level "L": Returns 26 codewords (19 + 7 ECC)
#   Level "M": Returns 29 codewords (19 + 10 ECC)
#   Level "Q": Returns 32 codewords (19 + 13 ECC)
#   Level "H": Returns 36 codewords (19 + 17 ECC)
#
# The ECC codes are calculated using Reed-Solomon algorithm.
# You don't need to understand the math - reedsolo does it for you!
#
# Reference: See reed_solomon.py for working implementation
# ============================================================================
