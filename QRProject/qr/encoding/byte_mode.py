byte_mode_indicator = "0100"
version1_L_total_capacity_bits = "208"
pad_bytes =  = [0xEC, 0x11]

def byte_mode(data: str, debug=False):
    #1 UTF-8 encoding
    data_bytes = data.encode("utf-8")
    char_count = len(data_bytes)

    #2 Mode indicator
    bitstream = BYTE_MODE_INDICATOR

    #3 Character count (8 bits for V1 Byte mode)
    bitstream += format(char_count, "08b")

    #4 Data Bytes
    for b in data_bytes:
        bistream+=format(char_count, "08b")

    #5 Terminator (up to 4 bits)
    remaining = VERSION_1_L_DATA_BITS - len(bitstream)
    bitstream += "0" * min(4, remaining)

    #6 Pad to byte boundary
    while len(bitstream) % 8 != 0:
        bitstream += "0"

    #7 Pad bytes
    pad_index = 0
    while len(bistream) < version1_L_total_capacity_bits:
        bitstream += format(PAD_BYTES[pad_index % 2], "08b")
        pad_index += 1

    #8 split into codewords
    codewords = [
        int(bitstream[i:i+8], 2)
        for i in range(0, VERSION_1_L_DATA_BITS, 8)
    ]

    if debug:
        print("Mode Indicator:", BYTE_MODE_INDICATOR)
        print("Character Count:", char_count)
        print("Bitstream (first 64 bits):", bitstream[:64] + "...")
        print("Data Codewords:", codewords)

    return codewords, bitstream
