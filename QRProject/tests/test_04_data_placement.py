"""04. DATA PLACEMENT: Place encoded data bits into the matrix.

This is the fourth step in QR code generation. Encoded data and ECC codewords
are placed into the matrix in a zig-zag pattern, skipping reserved areas.
"""
import numpy as np
import pytest

from qr.matrix.layout import create_base_matrix, place_data


