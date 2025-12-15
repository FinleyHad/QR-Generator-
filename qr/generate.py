from qr.utils.logging_config import setup_logger
from qr.encoding.encode import encode_string
from qr.ecc.reed_solomon import add_ecc
from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.mask0 import apply_mask

logger = setup_logger()

def generate_qr_matrix(text, ecc_level="L", mask_pattern=0):
    logger.info(f"Generating QR for: '{text}'")

    # Step 1: Encoding
    encoded_bits = encode_string(text)
    logger.debug(f"Encoded bits: {encoded_bits}")

    # Step 2: Error correction
    ecc_codewords = add_ecc(encoded_bits, ecc_level)
    logger.debug(f"ECC codewords added")

    # Step 3: Matrix assembly
    matrix = create_base_matrix()
    matrix_with_data = place_data(matrix, encoded_bits, ecc_codewords)
    logger.debug("Data placed in matrix")

    # Step 4: Apply mask
    masked_matrix = apply_mask(matrix_with_data, mask_pattern)
    logger.info("QR matrix generation complete")
    return masked_matrix