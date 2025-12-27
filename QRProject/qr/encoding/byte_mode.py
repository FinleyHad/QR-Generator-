BYTE_MODE_INDICATOR = "0100"
PAD_BYTES = [0xEC, 0x11]  # QR spec: cycle 0xEC, 0x11, 0xEC, 0x11, ...
DATA_CODEWORDS = 19
VERSION_1_L_DATA_BITS = DATA_CODEWORDS * 8


def byte_mode(data: str, debug: bool = False) -> tuple[list[int], str]:
    """Encode `data` in QR Byte Mode for Version 1-L.

    Returns a tuple (codewords, bitstream) where `codewords` is a list of
    exactly 19 integers (0..255) and `bitstream` is the full DATA bits string.
    This implementation preserves UTF-8 character boundaries when truncating
    to fit the available byte capacity.
    """
    # 1. UTF-8 bytes
    data_bytes = data.encode("utf-8")

    # Truncate without splitting multi-byte characters
    raw = b""
    for ch in data:
        chb = ch.encode("utf-8")
        if len(raw) + len(chb) > DATA_CODEWORDS:
            break
        raw += chb

    char_count = len(raw)

    # 2. Mode indicator
    bitstream = BYTE_MODE_INDICATOR

    # 3. Character count (8 bits for Version 1 Byte Mode)
    bitstream += format(char_count, "08b")

    # 4. Data bytes
    for b in raw:
        bitstream += format(b, "08b")

    # 5. Terminator (up to 4 bits)
    remaining = VERSION_1_L_DATA_BITS - len(bitstream)
    bitstream += "0" * min(4, remaining)

    # 6. Pad to byte boundary
    while len(bitstream) % 8 != 0:
        bitstream += "0"

    # 7. Pad bytes
    pad_index = 0
    while len(bitstream) < VERSION_1_L_DATA_BITS:
        bitstream += format(PAD_BYTES[pad_index % 2], "08b")
        pad_index += 1

    # 8. Split into codewords
    codewords = [
        int(bitstream[i : i + 8], 2)
        for i in range(0, VERSION_1_L_DATA_BITS, 8)
    ]

    if debug:
        print("Mode Indicator:", BYTE_MODE_INDICATOR)
        print("Character Count:", char_count)
        print("Bitstream (first 64 bits):", bitstream[:64] + "...")
        print("Data Codewords:", codewords)

    return codewords, bitstream
