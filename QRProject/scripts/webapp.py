"""Minimal Flask app to render QR codes from this project and serve them as PNGs.

Run locally:
    pip install -r requirements.txt
    python webapp.py

Then open http://127.0.0.1:5000/ in your browser.
"""
from io import BytesIO
from urllib.parse import quote_plus

from flask import Flask, request, send_file, render_template, url_for, jsonify
import hashlib
import numpy as np
from PIL import Image

from qr.encoding.encode import encode_string
from qr.matrix.layout import create_base_matrix, place_data
from qr.masking.finalize import finalize_matrix
from qr.utils.logging_config import setup_logger

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

# Configure Flask to use templates and static folders from parent directory
import os
_base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, 
            template_folder=os.path.join(_base_dir, 'templates'),
            static_folder=os.path.join(_base_dir, 'static'))

# Store text by ID for display after scanning
_text_storage = {}

# Logger for step-by-step verification
logger = setup_logger()


def _matrix_summary(name: str, m: np.ndarray) -> str:
    h, w = m.shape
    black = int(np.sum(m))
    return f"{name}: {h}x{w}, black={black}, white={(h*w - black)}"


def _matrix_ascii(m: np.ndarray, rows: int = 21) -> str:
    lines = []
    limit = min(rows, m.shape[0])
    for r in range(limit):
        lines.append(''.join('#' if v else '.' for v in m[r]))
    return '\n'.join(lines)


def _generate_id(text: str) -> str:
    """Generate a short ID for text storage (first 8 chars of MD5 hash)."""
    h = hashlib.md5(text.encode()).hexdigest()[:8]
    return h


def _store_text(text: str) -> str:
    """Store text and return its ID."""
    text_id = _generate_id(text)
    _text_storage[text_id] = text
    return text_id


def matrix_to_png_bytes(matrix: np.ndarray, scale: int = 12, border: int = 8) -> bytes:
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
    return render_template('index.html')


@app.route('/generate-all')
def generate_all():
    """Generate all 5 required test strings encoded as text for Version 1 scanability.

    Version 1 capacity: ~17-19 UTF-8 bytes in Byte Mode.
    Strings that exceed this will show an error.
    Phone scanners will display the text content directly.
    """
    mode = request.args.get('mode', 'text')  # Text-only mode for phone scanability
    test_strings = [
        ("known", "String 1"),
        ("We've succeeded!", "String 2"),
        ("~¡256_-_aA&ñ", "String 3"),
        ("From α to ɷ...", "String 4"),
        ("Sugarplum_Fairy_Nightmare", "String 5"),
    ]
    
    results = []
    for text, label in test_strings:
        result = {
            'label': label,
            'text': text,
            'error': None,
            'png_url': None,
            'display_url': None,
            'encoded': None
        }
        
        try:
            if not text:
                result['error'] = "Text cannot be empty"
            else:
                # Store text and compute display URL
                text_id = _store_text(text)
                result['display_url'] = url_for('display_text', text_id=text_id)

                text_bytes = len(text.encode('utf-8'))
                # Always try text mode for Version 1
                if text_bytes > 19:
                    result['error'] = f"Text too long ({text_bytes} bytes, max 19 for Version 1)"
                else:
                    result['encoded'] = text
                    result['png_url'] = url_for('qr_png', text=result['encoded'])
        except Exception as e:
            result['error'] = f"Error: {str(e)}"
        
        results.append(result)
    
    return jsonify(results)


@app.route('/display/<text_id>')
def display_text(text_id):
    """Display the text that was encoded in the QR code."""
    text = _text_storage.get(text_id, '')
    if not text:
        return render_template('display.html', text='', error='Text not found'), 404
    return render_template('display.html', text=text, error=None)



@app.route('/qr.png')
def qr_png():
    text = request.args.get('text', '')
    if not text:
        return "", 400

    # Check if we should use reference QR (for testing/scannability)
    use_reference = request.args.get('use_ref', '').lower() in ['1', 'true', 'yes']
    
    if use_reference:
        try:
            import qrcode
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=12, border=8)
            qr.add_data(text)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            return send_file(buf, mimetype='image/png')
        except Exception as e:
            logger.error(f"Failed to use reference QR: {e}")
            # Fall through to our implementation

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
    logger.info("Step 1: encode_string(text)")
    encoded_bits = encode_string(text)
    logger.info(f"Encoded bits length: {len(encoded_bits)}")
    logger.info(f"First 16 bits: {encoded_bits[:16]}")

    logger.info("Step 2: add_ecc(bits, 'L')")
    ecc_codewords = add_ecc(encoded_bits, 'L')
    logger.info(f"ECC codewords count: {len(ecc_codewords)}")
    logger.info(f"ECC sample: {ecc_codewords[:8]}")

    logger.info("Step 3: create_base_matrix()")
    base = create_base_matrix()
    logger.info(_matrix_summary("Base", base))

    logger.info("Step 4: place_data(base, bits, ecc)")
    placed = place_data(base, encoded_bits, ecc_codewords)
    logger.info(_matrix_summary("Placed", placed))

    # finalize (mask + format bits)
    logger.info("Step 5: finalize_matrix(placed, L, mask=0)")
    final = finalize_matrix(placed, ecc_level='L', mask_id=0)
    logger.info(_matrix_summary("Final", final))

    buf = matrix_to_png_bytes(final, scale=12, border=8)
    return send_file(buf, mimetype='image/png')


@app.route('/qr.debug')
def qr_debug():
    """Debug endpoint: return matrix as ASCII art and codeword details."""
    text = request.args.get('text', '')
    if not text:
        return "", 400

    if add_ecc is None:
        return "ECC not available", 500

    encoded_bits = encode_string(text)
    ecc_codewords = add_ecc(encoded_bits, 'L')
    base = create_base_matrix()
    placed = place_data(base, encoded_bits, ecc_codewords)
    final = finalize_matrix(placed, ecc_level='L', mask_id=0)

    # Render as text with step-by-step summaries
    lines = []
    lines.append(f"Text: {text}")
    lines.append(f"Data codewords: {encoded_bits}")
    lines.append(f"ECC codewords: {ecc_codewords}")
    lines.append(f"Total codewords: {len(ecc_codewords)}")
    lines.append(_matrix_summary("Base", base))
    lines.append(_matrix_summary("Placed", placed))
    lines.append(_matrix_summary("Final", final))
    lines.append("")
    lines.append("Base (top 21 rows):")
    lines.append(_matrix_ascii(base))
    lines.append("")
    lines.append("Placed (top 21 rows):")
    lines.append(_matrix_ascii(placed))
    lines.append("")
    lines.append("Final (top 21 rows):")
    lines.append(_matrix_ascii(final))
    
    return '\n'.join(lines), 200, {"Content-Type": "text/plain; charset=utf-8"}


@app.route('/qr.steps')
def qr_steps():
    """Return JSON with step-by-step outputs for verification."""
    text = request.args.get('text', '')
    if not text:
        return jsonify({"error": "text required"}), 400

    if add_ecc is None:
        return jsonify({"error": "ECC not available"}), 500

    encoded_bits = encode_string(text)
    ecc_codewords = add_ecc(encoded_bits, 'L')
    base = create_base_matrix()
    placed = place_data(base, encoded_bits, ecc_codewords)
    final = finalize_matrix(placed, ecc_level='L', mask_id=0)

    result = {
        "text": text,
        "encoded_bits_len": len(encoded_bits),
        "encoded_bits_head": encoded_bits[:32],
        "ecc_count": len(ecc_codewords),
        "ecc_head": ecc_codewords[:10],
        "base": {
            "summary": _matrix_summary("Base", base),
            "ascii": _matrix_ascii(base),
        },
        "placed": {
            "summary": _matrix_summary("Placed", placed),
            "ascii": _matrix_ascii(placed),
        },
        "final": {
            "summary": _matrix_summary("Final", final),
            "ascii": _matrix_ascii(final),
        },
        "png_url": url_for('qr_png', text=text),
    }

    return jsonify(result)


@app.route('/ping')
def ping():
    return 'pong'


if __name__ == '__main__':
    app.run(debug=True)
