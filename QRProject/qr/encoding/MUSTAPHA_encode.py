"""
======================================================================================
MUSTAPHA's Encoding Wrapper - STEP 1b (Orchestration)
======================================================================================

YOUR TASK: Implement the encode_string() wrapper function

This file is your implementation of the high-level encoding interface. You will
create a simple wrapper that calls your byte_mode() function and returns just 
the codewords.

REFERENCE FILE: qr/encoding/encode.py
- Shows the exact structure you need to implement
- Very simple: just call byte_mode and return the first element

YOUR FILES:
1. MUSTAPHA_byte_mode.py - The actual byte mode encoding implementation
2. MUSTAPHA_encode.py - This file, a simple wrapper

DEPENDENCIES:
- Your MUSTAPHA_byte_mode.py file must be implemented first
- This function imports and calls byte_mode() from that file

WHAT TO IMPLEMENT:
=================

Function: encode_string(s: str) -> list[int]
----------------------------------------------
A simple wrapper that:
1. Calls byte_mode(s) to get (codewords, bitstream)
2. Returns just the codewords (ignoring bitstream)
3. Should return exactly 19 codewords (ints 0..255)

This provides a clean interface for the rest of the pipeline.

TESTING:
--------
Tests in test_01_encoding.py will verify:
- Returns list of 19 integers
- Each integer is 0..255
- Produces correct output for known strings

IMPLEMENTATION NOTES:
--------------------
- This is a very simple file - just a wrapper function
- Import byte_mode from your MUSTAPHA_byte_mode module
- Use tuple unpacking: codewords, _ = byte_mode(s)
- Return the codewords list

======================================================================================
"""

from .MUSTAPHA_byte_mode import byte_mode


def encode_string(s: str):
    """Encode a string into the Version 1-L data codewords using byte mode.

    Returns the list of 19 data codewords (ints 0..255).
    
    TODO: Implement this function
    1. Call byte_mode(s) to get (codewords, bitstream) tuple
    2. Return just the codewords (first element)
    3. The codewords list should have exactly 19 elements
    """
    raise NotImplementedError("TODO: Implement encode_string() wrapper function")


# ======================================================================================
# TESTING HELPERS
# ======================================================================================

if __name__ == "__main__":
    # Quick test when running this file directly
    try:
        result = encode_string("Hello")
        print(f"Encoded 'Hello' into {len(result)} codewords:")
        print(result)
        print("✓ encode_string() working!")
    except NotImplementedError:
        print("⚠ encode_string() not yet implemented")
