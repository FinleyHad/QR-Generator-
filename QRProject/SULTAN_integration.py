"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    SULTAN - INTEGRATION & WEB APPLICATION                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

📁 YOUR FILE TO EDIT: SULTAN_integration.py (root folder)

📖 REFERENCE FILES (Read-only - look at these for guidance):
   - qr/generate.py                 ← Working generate_qr_code() pipeline
   - scripts/webapp.py              ← Flask web app (update imports)
   - scripts/run_demos.py           ← Demo generation (update imports)
   - scripts/save_qr_images.py      ← Image saving (update imports)

🎯 WHAT YOU NEED TO IMPLEMENT:
   ✓ generate_qr_code(text, ecc_level) → numpy array
     - Orchestrate full pipeline: Mustapha → Musa → Nadir → Finley
     - Call each team member's functions in order
     - Return final 21×21 QR code matrix
     
   ✓ render_to_png(matrix, filename, scale, border)
     - Convert numpy matrix to PNG image
     - Use PIL/Pillow library
     - Add white border (quiet zone)
     
   ✓ get_qr_info(text, ecc_level) → dict
     - Return metadata about QR code

📝 YOUR IMPLEMENTATION REPLACES:
   - qr/generate.py lines 10-50 (generate_qr_code function)
   - qr/generate.py lines 53-80 (render_to_png function)

✅ TESTS TO PASS:
   pytest tests/test_06_integration.py -v
   pytest tests/test_07_quality_and_scannability.py -v
   pytest tests/test_08_webapp.py -v

🔗 WHO USES YOUR CODE:
   ← Calls MUSTAPHA, MUSA, NADIR, FINLEY functions
   → Used by scripts/webapp.py for web interface
   → Used by scripts/run_demos.py to generate demo QR codes
   
💡 AFTER IMPLEMENTATION:
   Update imports in these files to use your functions:
   - scripts/webapp.py: Change imports to SULTAN_integration
   - scripts/run_demos.py: Change imports to SULTAN_integration
   - scripts/save_qr_images.py: Change imports to SULTAN_integration
        
═══════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from pathlib import Path


def generate_qr_code(text: str, ecc_level: str = "M") -> np.ndarray:
    """
    Generate complete QR code matrix from text using the full pipeline.
    
    Pipeline orchestration:
    Text → Encode (Mustapha) → ECC (Musa) → Matrix (Nadir) → Mask (Finley) → QR Code
    
    Args:
        text: Text to encode (e.g., "Hello World", "test123")
        ecc_level: Error correction level ("L", "M", "Q", "H")
    
    Returns:
        21×21 numpy array with final QR code (0s and 1s only)
    
    Example:
        >>> qr = generate_qr_code("Hello")
        >>> qr.shape
        (21, 21)
        >>> np.unique(qr)
        array([0, 1])
    """
    # TODO: Step 1 - Import team member functions
    # from qr.encoding.MUSTAPHA_byte_mode import byte_mode
    # from qr.ecc.MUSA_reed_solomon import add_ecc
    # from qr.matrix.NADIR_layout import create_base_matrix, place_data
    # from qr.masking.FINLEY_mask0 import finalize_matrix
    
    # TODO: Step 2 - Call Mustapha's encoding
    # codewords, bitstream = byte_mode(text)
    
    # TODO: Step 3 - Call Musa's ECC
    # data_with_ecc = add_ecc(codewords, ecc_level)
    
    # TODO: Step 4 - Call Nadir's matrix creation
    # matrix = create_base_matrix()
    
    # TODO: Step 5 - Call Nadir's data placement
    # matrix_with_data = place_data(matrix, codewords, data_with_ecc)
    
    # TODO: Step 6 - Call Finley's finalization (mask + format)
    # final_qr = finalize_matrix(matrix_with_data, ecc_level)
    
    # TODO: Step 7 - Return final QR code matrix
    raise NotImplementedError("generate_qr_code() not yet implemented")
    # When ready, replace the line above with:
    # return final_qr


def render_to_png(matrix: np.ndarray, filename: str, scale: int = 10, border: int = 4):
    """
    Convert QR matrix to PNG image file.
    
    Args:
        matrix: 21×21 QR code matrix from generate_qr_code()
        filename: Output file path (e.g., "output/qr_hello.png")
        scale: Pixels per module (default 10 = each bit becomes 10×10 pixels)
        border: Quiet zone in modules (default 4 = 4-module white border)
    
    Example:
        >>> qr = generate_qr_code("Hello")
        >>> render_to_png(qr, "output/qr_hello.png", scale=10, border=4)
        # Creates 290×290 pixel PNG:
        # (21 modules + 4*2 border) * 10 scale = 29 * 10 = 290
    """
    # TODO: Step 1 - Import PIL/Pillow
    # from PIL import Image
    
    # TODO: Step 2 - Calculate image size
    # size = matrix.shape[0]  # Should be 21
    # total_size = (size + 2 * border) * scale
    
    # TODO: Step 3 - Create white image
    # img = Image.new('RGB', (total_size, total_size), 'white')
    # pixels = img.load()
    
    # TODO: Step 4 - Draw QR code modules
    # for row in range(size):
    #     for col in range(size):
    #         if matrix[row, col] == 1:  # Black module
    #             # Draw scale×scale black square
    #             for dy in range(scale):
    #                 for dx in range(scale):
    #                     x = (col + border) * scale + dx
    #                     y = (row + border) * scale + dy
    #                     pixels[x, y] = (0, 0, 0)  # Black
    
    # TODO: Step 5 - Save image
    # img.save(filename)
    # print(f"QR code saved to {filename}")
    
    raise NotImplementedError("render_to_png() not yet implemented")


def get_qr_info(text: str, ecc_level: str = "M") -> dict:
    """
    Get metadata about a QR code.
    
    Args:
        text: Text that would be encoded
        ecc_level: Error correction level
    
    Returns:
        Dictionary with QR code info
    
    Example:
        >>> info = get_qr_info("Hello", "M")
        >>> info
        {
            "text": "Hello",
            "size": 21,
            "version": 1,
            "ecc_level": "M",
            "char_count": 5,
            "data_bytes": 19,
            "ecc_bytes": 10,
            "total_bytes": 29
        }
    """
    # TODO: Calculate QR code metadata
    raise NotImplementedError("get_qr_info() not yet implemented")


# ============================================================================
# TESTING YOUR CODE
# ============================================================================
# 
# Run: pytest tests/test_06_integration.py -v
# Run: pytest tests/test_07_quality_and_scannability.py -v
# Run: pytest tests/test_08_webapp.py -v
# 
# Expected behavior:
#   generate_qr_code():
#     - Orchestrates full pipeline
#     - Returns 21×21 matrix
#     - All values 0 or 1
#   
#   render_to_png():
#     - Creates PNG file
#     - Correct size with border
#     - Black/white pixels
#   
#   Web app (see scripts/webapp.py):
#     - All endpoints work
#     - Can generate QR codes
#     - Can display results
#
# Manual testing:
#   python scripts/webapp.py
#   Visit http://localhost:5000
#
# Reference: See qr/generate.py for working pipeline implementation
# ============================================================================
