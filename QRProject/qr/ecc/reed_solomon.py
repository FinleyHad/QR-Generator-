"""Reed–Solomon ECC helper for Version 1 QR codes.

This module attempts to import a compatible RSCodec implementation from a
couple of common packages (prefer `reed_solomon` but fall back to
`reedsolo`). It supports ECC levels for Version 1: L, M, Q, H.
"""

# Try common Reed–Solomon providers and give a clear ImportError if none found.
try:
    from reed_solomon import RSCodec  # some packages provide this name
except Exception:
    try:
        from reedsolo import RSCodec  # widely used package on PyPI
    except Exception as exc:  # pragma: no cover - environment dependent
        raise ImportError(
            "Reed–Solomon dependency not found. Install `reedsolo` or `reed_solomon` "
            "(see requirements.txt)."
        ) from exc

# Version 1 specifics
DATA_CODEWORDS = 19
ECC_BY_LEVEL = {
    "L": 7,
    "M": 10,
    "Q": 13,
    "H": 17,
}
# Backwards-compatible alias expected by tests
ECC_CODEWORDS = ECC_BY_LEVEL["L"]


def add_ecc(data_codewords: list[int], ecc_level: str = "L") -> list[int]:
    """Append ECC codewords for Version 1 QR.

    Parameters
    - data_codewords: list of 19 integers (0..255)
    - ecc_level: one of 'L','M','Q','H' (defaults to 'L')

    Returns the full codeword list (data + ecc) as integers.
    """
    ecc_level = ecc_level.upper()
    if len(data_codewords) != DATA_CODEWORDS:
        raise ValueError(f"Version 1-{ecc_level} requires {DATA_CODEWORDS} data codewords")

    if ecc_level not in ECC_BY_LEVEL:
        raise ValueError(f"Unknown ECC level: {ecc_level}")

    if not all(0 <= b <= 255 for b in data_codewords):
        raise ValueError("Codewords must be in range 0–255")

    ecc_count = ECC_BY_LEVEL[ecc_level]
    rs = RSCodec(ecc_count)
    encoded = rs.encode(bytes(data_codewords))

    ecc = list(encoded[-ecc_count:])

    print("ECC Level:", ecc_level)
    print("ECC Codewords:", ecc)
    print("Final Codeword Count:", len(encoded))

    return list(encoded)
