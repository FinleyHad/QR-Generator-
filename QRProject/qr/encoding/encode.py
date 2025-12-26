from .byte_mode import byte_mode


def encode_string(s: str):
    """Encode a string into the Version 1-L data codewords using byte mode.

    Returns the list of 19 data codewords (ints 0..255).
    """
    codewords, _ = byte_mode(s)
    return codewords