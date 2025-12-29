"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    MUSTAPHA - BYTE MODE ENCODING                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: qr/encoding/MUSTAPHA_byte_mode.py

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/encoding/byte_mode.py       ← Working implementation of byte_mode()
   - qr/encoding/encode.py          ← Full encoding pipeline

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ byte_mode(data, debug) → (codewords, bitstream)
     - Convert text to QR byte mode format
     - Add mode indicator, character count, data, padding
     - Return 19 codewords and bitstream

📝 YOUR IMPLEMENTATION REPLACES:
   - byte_mode.py line 8-65 (the byte_mode function)

✅ TESTS TO PASS:
   pytest tests/test_01_encoding.py -v

🔗 WHO USES YOUR CODE:
   → MUSA (Person 2) calls your byte_mode() for error correction
   
💡 TIP: Start by reading byte_mode.py to understand the structure, then
        implement it step-by-step in this file following the TODOs below.
        
═══════════════════════════════════════════════════════════════════════════
"""

# QR Code constants for Version 1
BYTE_MODE_INDICATOR = "0100"  # 4 bits indicating byte mode
PAD_BYTES = [0xEC, 0x11]      # Padding bytes to fill remaining space
DATA_CODEWORDS = 19            # Total data bytes for Version 1-L
VERSION_1_L_DATA_BITS = DATA_CODEWORDS * 8  # 152 bits total


def byte_mode(data: str, debug: bool = False) -> tuple[list[int], str]:
    """
    Encode text data in QR Byte Mode for Version 1-L.
    
    Args:
        data: Text string to encode (e.g., "Hello", "A", "test123")
        debug: If True, print debugging info
    
    Returns:
        tuple containing:
        - list[int]: Exactly 19 codewords (bytes, 0-255)
        - str: Full bitstream as string of '0' and '1'
    
    Example:
        >>> codewords, bits = byte_mode("A")
        >>> len(codewords)
        19
        >>> bits[:4]
        '0100'  # Mode indicator
        >>> bits[4:12]
        '00000001'  # Character count = 1
        >>> bits[12:20]
        '01000001'  # ASCII 'A' = 65
    
    Process:
    1. Convert data to UTF-8 bytes
    2. Truncate if necessary to fit DATA_CODEWORDS
    3. Build bitstream:
       - Mode indicator (4 bits)
       - Character count (8 bits)
       - Data bytes (8 bits each)
       - Terminator (up to 4 zero bits)
       - Pad to byte boundary
       - Fill with pad bytes to reach 152 bits
    4. Convert bitstream to 19 codewords
    """
    # TODO: Step 1 - Convert data to UTF-8 bytes
    # data_bytes = data.encode("utf-8")
    
    # TODO: Step 2 - Truncate to fit DATA_CODEWORDS if needed
    # (Don't split multi-byte UTF-8 characters)
    raw = b""  # Your truncated bytes here
    
    # TODO: Step 3 - Start building bitstream with mode indicator
    bitstream = ""  # Start with BYTE_MODE_INDICATOR
    
    # TODO: Step 4 - Add character count (8 bits)
    # char_count = len(raw)
    # bitstream += format(char_count, "08b")
    
    # TODO: Step 5 - Add data bytes (8 bits each)
    # for b in raw:
    #     bitstream += format(b, "08b")
    
    # TODO: Step 6 - Add terminator (up to 4 zero bits)
    # remaining = VERSION_1_L_DATA_BITS - len(bitstream)
    # bitstream += "0" * min(4, remaining)
    
    # TODO: Step 7 - Pad to byte boundary (make length multiple of 8)
    # while len(bitstream) % 8 != 0:
    #     bitstream += "0"
    
    # TODO: Step 8 - Fill remaining space with pad bytes (0xEC, 0x11, alternating)
    # pad_index = 0
    # while len(bitstream) < VERSION_1_L_DATA_BITS:
    #     bitstream += format(PAD_BYTES[pad_index % 2], "08b")
    #     pad_index += 1
    
    # TODO: Step 9 - Convert bitstream to list of codewords (bytes)
    # Split bitstream into 8-bit chunks and convert to integers
    codewords = []  # Should be list of 19 integers (0-255)
    
    if debug:
        print(f"Data: {data!r}")
        print(f"Bitstream length: {len(bitstream)}")
        print(f"Codewords: {len(codewords)}")
    
    raise NotImplementedError("byte_mode() not yet implemented")
    # When ready, replace the line above with:
    # return codewords, bitstream


# ============================================================================
# TESTING YOUR CODE
# ============================================================================
# 
# Run: pytest tests/test_01_encoding.py::test_byte_mode_single_char -v
# 
# Expected behavior:
#   "A" → 19 codewords, 152 bit bitstream
#   First 4 bits: "0100" (mode)
#   Next 8 bits: "00000001" (count = 1)
#   Next 8 bits: "01000001" (ASCII 65)
#   Remaining: terminator + padding
#
# Reference: See byte_mode.py for working implementation
# ============================================================================
