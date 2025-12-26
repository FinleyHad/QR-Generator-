"""Minimal Flask app to render QR codes from this project and serve them as PNGs.

Run locally:
    pip install -r requirements.txt
    python webapp.py

Then open http://127.0.0.1:5000/ in your browser.
"""
from io import BytesIO
from urllib.parse import quote_plus

from flask import Flask, request, send_file, render_template, url_for
import numpy as np
from PIL import Image

from qr.encoding.encode import encode_string
from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.finalize import finalize_matrix

# The project's QR ecc implementation depends on an external Reed-Solomon package
# (the repo's `qr/ecc/reed_solomon.py` tries to import `RSCodec`). We attempt to
# import the add_ecc function and capture an error message if the dependency is
# missing so we can give a helpful response in the web UI.
try:
    from qr.ecc.reed_solomon import add_ecc
    _ADD_ECC_ERR = None
except Exception as exc:  # pragma: no cover - runtime/environment dependent
    add_ecc = None
    _ADD_ECC_ERR = exc

app = Flask(__name__)


def matrix_to_png_bytes(matrix: np.ndarray, scale: int = 8, border: int = 4) -> bytes:
    """Convert a 0/1 numpy matrix to PNG bytes using Pillow.

    - scale: pixels per QR module
    - border: quiet zone in modules (added on each side)
    """
    if matrix.dtype != np.uint8 and matrix.dtype != np.int64 and matrix.dtype != np.int32:
        matrix = matrix.astype(np.uint8)

    # Add border (quiet zone)
    h, w = matrix.shape
    bordered = np.zeros((h + 2 * border, w + 2 * border), dtype=np.uint8)
    bordered[border:border + h, border:border + w] = matrix

    # Scale up
    scaled = np.kron(bordered, np.ones((scale, scale), dtype=np.uint8))

    # Convert: 1 -> black (0), 0 -> white (255)
    img_arr = (1 - scaled) * 255
    img = Image.fromarray(img_arr.astype('uint8'), mode='L')

    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf


@app.route('/')
def index():
    text = request.args.get('text', '')
    return render_template('index.html', text=text)


@app.route('/qr.png')
def qr_png():
    text = request.args.get('text', '')
    if not text:
        return "", 400

    if add_ecc is None:
        # Helpful error when Reed-Solomon dependency is missing
        msg = (
            "Required Reed-Solomon dependency is missing.\n"
            "Please install required packages (see requirements.txt), for example:\n\n"
            "    pip install reedsolo\n"
            "or\n"
            "    pip install reed_solomon\n\n"
            f"Underlying error: {_ADD_ECC_ERR!r}"
        )
        return (msg, 500, {"Content-Type": "text/plain; charset=utf-8"})

    # 1) encode, 2) ecc, 3) matrix creation, 4) place data
    encoded_bits = encode_string(text)
    ecc_codewords = add_ecc(encoded_bits, 'L')
    base = create_base_matrix()
    placed = place_data(base, encoded_bits, ecc_codewords)

    # finalize (mask + format bits)
    final = finalize_matrix(placed)

    buf = matrix_to_png_bytes(final, scale=8, border=4)
    return send_file(buf, mimetype='image/png')


@app.route('/ping')
def ping():
    return 'pong'


if __name__ == '__main__':
    app.run(debug=True)
