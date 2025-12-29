# SULTAN - Integration & Web Implementation Guide

## � YOUR FILES TO IMPLEMENT

**Edit these skeleton files:**
1. `SULTAN_integration.py` - Main integration and PNG rendering functions

**Update imports in these files (after implementing above):**
2. `scripts/webapp.py` - Change imports to use SULTAN_integration
3. `scripts/run_demos.py` - Change imports to use SULTAN_integration  
4. `scripts/save_qr_images.py` - Change imports to use SULTAN_integration

**Reference files (read-only):**
- `qr/generate.py` - Working pipeline orchestration
- `scripts/webapp.py` - Flask endpoints (just update imports)

**HTML templates (already done - no changes needed):**
- `templates/index.html` - Main page (already built)
- `templates/display.html` - Display page (already built)
- `static/style.css` - Styling (already done)

---

## �📖 User Story
*"As a user, I want to visit a website, type in any text, click a button, and instantly see a working QR code that I can download and scan with my phone - all without knowing anything about how QR codes work internally."*

## Overview
Sultan is responsible for integrating all the components (Encoding → ECC → Matrix → Masking) into a complete QR code generation pipeline and implementing the web application interface.

## Your Role in the Pipeline

You work at the **final stage** of the QR code generation process. Your work builds on:
- **Mustapha's** encoded bytes
- **Musa's** ECC codes
- **Nadir's** matrix layout with data placement
- **Finley's** masked and finalized matrix

Your job is to:
1. Create the main integration function that orchestrates all components
2. Implement the web application endpoints
3. Handle end-to-end testing of the complete pipeline

---

## Implementation File
**Location:** `qr/PERSON5_integration.py` (or `SULTAN_integration.py`)

This file should contain:
- `generate_qr_code()` - Main orchestration function
- `render_to_png()` - Convert matrix to PNG image
- `get_version_info()` - Return QR code version info
- Any web utility functions needed

---

## Tests to Pass
Run your tests with:
```bash
pytest tests/test_06_integration.py -v  # End-to-end pipeline
pytest tests/test_07_quality_and_scannability.py -v  # Quality checks
pytest tests/test_08_webapp.py -v  # Web endpoints
```

### Key Test Scenarios
1. **Complete Pipeline Integration**
   - Text input flows through all 4 stages correctly
   - Each stage produces expected intermediate outputs
   - Final matrix is complete and valid

2. **Quality Validation**
   - Matrix is square and complete
   - All required QR code patterns are present (finders, timing, dark module)
   - Data is properly placed in correct order

3. **Web App Endpoints**
   - `/` - Main page loads
   - `/generate-all` - Returns QR codes for all demos
   - `/generate?text=...` - Generates custom QR code
   - `/display/<image_name>` - Displays generated image

---

## Web App Implementation
**Location:** `scripts/webapp.py`

**Good News:** The HTML templates and CSS already exist! You don't need to write HTML.
- `templates/index.html` - Main page with QR generation form (already built)
- `templates/display.html` - Display page for QR codes (already built)
- `static/style.css` - Styling (already done)

Your job is to implement the Flask endpoints that **use** these templates.

### Flask Endpoints to Implement
1. **GET `/`** - Serve main index page
   - Use: `return render_template('index.html')`
   - Display form for custom QR code generation
   - Show list of generated demo QR codes

2. **POST `/generate`** - Generate custom QR code
   - Accept text input from form
   - Call your `generate_qr_code()` function
   - Call your `render_to_png()` function
   - Return JSON with image URL

3. **GET `/generate-all`** - Generate all demo codes
   - Read demo files from `demos/` folder
   - Generate QR for each demo text
   - Return array of all demo QR codes with metadata
   - Include display URLs and image paths

4. **GET `/display/<image_name>`** - Display QR code
   - Use: `return render_template('display.html', image=..., text=..., info=...)`
   - Render QR code image with metadata
   - Show text encoded, version, error correction level

5. **GET `/ping`** - Health check
   - Return "PONG"

---

## Dependencies
```python
import numpy as np
from PIL import Image
import qrcode  # For reference/testing only
from flask import Flask, render_template, request, jsonify
```

### Working Components
- All encoding, ECC, matrix, and masking functions are already implemented
- Your job is to wire them together

---

## Step-by-Step Implementation

### 1. Integration Pipeline Function
```python
def generate_qr_code(text: str) -> np.ndarray:
    """
    Generate QR code matrix from text.
    
    Pipeline:
    1. Encode text to bytes (call Mustapha's function)
    2. Add ECC codes (call Musa's function)
    3. Create matrix structure (call Nadir's function)
    4. Apply masking (call Finley's function)
    5. Return final matrix
    """
    # TODO: Implement orchestration
```

### 2. PNG Rendering Function
```python
def render_to_png(matrix: np.ndarray, filename: str) -> None:
    """
    Convert QR code matrix to PNG image.
    
    - Black = 1, White = 0
    - Each module (bit) becomes a pixel
    - Multiply by scale factor for visibility (e.g., 10x10)
    """
    # TODO: Implement using PIL/Pillow
```

### 3. Flask App Setup
```python
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

@app.route('/')
def index():
    # TODO: Render index.html

@app.route('/generate-all', methods=['GET'])
def generate_all():
    # TODO: Generate all demo codes and return JSON

@app.route('/display/<image_name>')
def display(image_name):
    # TODO: Render display.html with image
```

---

## Testing Your Implementation

### Unit Tests
```bash
pytest tests/test_06_integration.py -v
```
Tests that complete pipeline works end-to-end.

### Integration Tests
```bash
pytest tests/test_07_quality_and_scannability.py -v
```
Tests that generated QR codes are valid and complete.

### Web App Tests
```bash
pytest tests/test_08_webapp.py -v
```
Tests Flask endpoints and responses.

### Manual Testing
```bash
# Start the web app
python scripts/webapp.py

# In another terminal, test endpoints
curl http://localhost:5000/
curl http://localhost:5000/ping
curl http://localhost:5000/generate-all
```

---

## Key Files to Understand
- `qr/generate.py` - See how the full pipeline is expected to work
- `tests/test_06_integration.py` - See exactly what your integration function needs to do
- `tests/test_08_webapp.py` - See what your Flask endpoints need to return
- `scripts/webapp.py` - Main file you'll be working in

---

## Common Issues & Solutions

**Issue:** "ModuleNotFoundError: No module named 'qr'"
- **Solution:** Make sure you're running from the project root directory

**Issue:** "Port 5000 already in use"
- **Solution:** Kill the existing process or use a different port in Flask config

**Issue:** Generated images are too small to see
- **Solution:** Increase the scale factor when converting matrix to PNG (e.g., multiply by 10)

**Issue:** Web app imports aren't working
- **Solution:** Check that all team member's functions are implemented, not just skeletons

---

## Collaboration Notes
- **Coordinate with Finley** on matrix validation before rendering to PNG
- **Coordinate with Mustapha, Musa, Nadir** on function signatures and return types
- **Test all components together** before moving to web implementation
- **Run full test suite** before merging: `pytest tests/ -q`

---

## Success Criteria
✅ All 15 integration tests pass  
✅ All 20+ quality tests pass  
✅ All 5 web app tests pass  
✅ QR codes are scannable by standard readers  
✅ Web app loads and generates codes correctly  
✅ No import errors or missing dependencies  

Good luck! You're the final piece that brings everything together. 🚀
