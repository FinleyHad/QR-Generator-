import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qr.utils.logging_config import setup_logger
from qr.generate import generate_qr_matrix

strings = [
    "known",
    "We've succeeded!",
    "~i256_~_aA&fi",
    "From a to o...",
    "Sugarplum_Fairy_Nightmare"
]

def run_demos():
    for idx, text in enumerate(strings, start=1):
        logger = setup_logger()
        logger.info(f"=== Processing String {idx}: '{text}' ===")

        try:
            matrix = generate_qr_matrix(text, ecc_level="L", mask_pattern=0)
            logger.info(f"String {idx} processed successfully")
        except Exception as e:
            logger.error(f"String {idx} failed: {e}")

        # Capture logs into file
        with open(f"demos/demo_{idx}.txt", "w") as f:
            # You may redirect log output to file here
            pass  # Placeholder – you'll need to capture logs properly

if __name__ == "__main__":
    run_demos()