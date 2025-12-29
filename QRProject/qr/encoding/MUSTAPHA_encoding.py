"""
MUSTAPHA - Encoding Module (Person 1)

Your job: Convert text to bytes for QR code encoding.

Example:
    "A" → byte value 65 → binary 01000001
    "Hello" → bytes [72, 101, 108, 108, 111] → binary string

Your functions will be called by Musa's ECC module (test_02_ecc.py).
Reference implementations are in: byte_mode.py (read-only)
"""

import numpy as np


def byte_mode(text: str) -> bytes:
    """
    Convert text string to bytes using ISO-8859-1 encoding.
    
    Args:
        text: Text string to encode (e.g., "Hello")
    
    Returns:
        bytes object with encoded text
    
    Example:
        >>> byte_mode("A")
        b'A'  # ASCII value 65
        
        >>> byte_mode("Hello")
        b'Hello'  # [72, 101, 108, 108, 111]
    
    Hint: Use Python's built-in .encode() method
    """
    # TODO: Implement byte mode encoding
    raise NotImplementedError("byte_mode() not yet implemented")


def encode_string(text: str) -> list:
    """
    Encode text into bit representation for QR code.
    
    QR codes use structured encoding:
    1. Mode indicator: 0100 (4 bits for byte mode)
    2. Character count: Length as 8-bit number
    3. Data: Each character as 8-bit byte
    
    Args:
        text: Text to encode
    
    Returns:
        List of bits [0, 1, 0, 1, ...] representing the encoded data
    
    Example:
        >>> encode_string("A")
        [0, 1, 0, 0,          # Mode: 0100 (byte mode)
         0, 0, 0, 0, 0, 0, 0, 1,  # Length: 1
         0, 1, 0, 0, 0, 0, 0, 1]  # 'A' = ASCII 65
    
    Step-by-step:
    1. Create mode indicator [0, 1, 0, 0]
    2. Get byte representation of length
    3. Get bytes for each character
    4. Combine into single list
    """
    # TODO: Implement full encoding
    raise NotImplementedError("encode_string() not yet implemented")


def get_encoded_bits(text: str) -> np.ndarray:
    """
    Convert encoded bits to numpy array for matrix placement.
    
    Args:
        text: Text to encode
    
    Returns:
        1D numpy array of 0s and 1s
    
    Example:
        >>> bits = get_encoded_bits("A")
        >>> bits.shape
        (18,)  # 4 mode + 8 length + 8 data
        >>> bits[0:4]
        array([0, 1, 0, 0])  # Mode indicator
    """
    # TODO: Implement conversion to numpy array
    raise NotImplementedError("get_encoded_bits() not yet implemented")


# ============================================================================
# TESTING YOUR WORK
# ============================================================================
#
# Run tests:
#   pytest tests/test_01_encoding.py -v
#
# Your tests will check:
#   ✓ byte_mode() converts text correctly
#   ✓ encode_string() creates proper mode/length/data format
#   ✓ get_encoded_bits() returns numpy array with correct shape
#   ✓ Multiple texts encode correctly
#
# REFERENCE FILES (READ-ONLY):
#   - byte_mode.py: Working implementation
#   - encode.py: Full encoding pipeline
#
# When you're done:
#   - All 21 tests pass
#   - Notify MUSA (Person 2) that encoding is ready
#
# ============================================================================
