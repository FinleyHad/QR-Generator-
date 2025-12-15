import logging
import sys

def setup_logger(log_file="qr_generation.log"):
    logger = logging.getLogger("qr_generator")
    logger.setLevel(logging.DEBUG)

    # Console handler
    c_handler = logging.StreamHandler(sys.stdout)
    c_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)

    # File handler
    f_handler = logging.FileHandler(log_file)
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger