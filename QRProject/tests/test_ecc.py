import pytest
pytest.importorskip("reedsolo")

from qr.ecc.reed_solomon import add_ecc, DATA_CODEWORDS, ECC_CODEWORDS


def _sample_data():
    return list(range(DATA_CODEWORDS))


def test_add_ecc_length_and_prefix():
    data = _sample_data()
    encoded = add_ecc(data)

    assert isinstance(encoded, list)
    assert len(encoded) == DATA_CODEWORDS + ECC_CODEWORDS
    assert encoded[:DATA_CODEWORDS] == data
    assert all(isinstance(b, int) for b in encoded)
    assert all(0 <= b <= 255 for b in encoded)


def test_add_ecc_validates_length():
    with pytest.raises(ValueError, match="Version 1-L requires 19 data codewords"):
        add_ecc(list(range(DATA_CODEWORDS - 1)))

    with pytest.raises(ValueError, match="Version 1-L requires 19 data codewords"):
        add_ecc(list(range(DATA_CODEWORDS + 1)))


def test_add_ecc_validates_range():
    bad = _sample_data()
    bad[0] = -1
    with pytest.raises(ValueError, match="Codewords must be in range 0–255"):
        add_ecc(bad)

    bad = _sample_data()
    bad[0] = 256
    with pytest.raises(ValueError, match="Codewords must be in range 0–255"):
        add_ecc(bad)


def test_add_ecc_matches_reedsolo():
    # Cross-check that add_ecc produces the same output as direct RSCodec encoding
    from reedsolo import RSCodec

    data = [0x10] * DATA_CODEWORDS
    expected = list(RSCodec(ECC_CODEWORDS).encode(bytes(data)))

    out = add_ecc(data)
    assert out == expected


# The following strings should be verifiable when encoded to DATA_CODEWORDS-length
TEST_STRINGS = [
    "known",
    "We've succeeded!",
    "~¡256_-_aA&ñ",
    "From α to ω...",
    "Sugarplum_Fairy_Nightmare",
]

PAD_BYTES = [0xEC, 0x11]


def _string_to_data_codewords(s: str) -> list[int]:
    """Encode `s` to UTF-8 and fit into exactly DATA_CODEWORDS bytes.

    This function avoids splitting multi-byte UTF-8 characters when truncating.
    If the UTF-8 encoding is shorter than DATA_CODEWORDS, it pads with the
    QR byte pad sequence 0xEC, 0x11.
    """
    raw = b""
    for ch in s:
        chb = ch.encode("utf-8")
        if len(raw) + len(chb) > DATA_CODEWORDS:
            break
        raw += chb

    # Pad if necessary
    pad_i = 0
    while len(raw) < DATA_CODEWORDS:
        raw += bytes([PAD_BYTES[pad_i % 2]])
        pad_i += 1

    assert len(raw) == DATA_CODEWORDS
    return list(raw)


@pytest.mark.parametrize("s", TEST_STRINGS)
def test_strings_produce_expected_ecc(s):
    from reedsolo import RSCodec

    data = _string_to_data_codewords(s)
    assert len(data) == DATA_CODEWORDS

    expected = list(RSCodec(ECC_CODEWORDS).encode(bytes(data)))
    out = add_ecc(data)
    assert out == expected
