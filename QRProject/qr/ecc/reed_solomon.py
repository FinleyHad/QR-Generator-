from reedsolo import RSCodec

DATA_CODEWORDS = 19
ECC_CODEWORDS = 7


def add_ecc(data_codewords: list[int]) -> list[int]:
    if len(data_codewords) != DATA_CODEWORDS:
        raise ValueError("Version 1-L requires 19 data codewords")

    if not all(0 <= b <= 255 for b in data_codewords):
        raise ValueError("Codewords must be in range 0–255")

    rs = RSCodec(ECC_CODEWORDS)
    encoded = rs.encode(bytes(data_codewords))

    ecc = list(encoded[-ECC_CODEWORDS:])

    print("ECC Level: L")
    print("ECC Codewords:", ecc)
    print("Final Codeword Count:", len(encoded))

    return list(encoded)
