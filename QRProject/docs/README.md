# QR Code Generator - Programming in Python Assignment Two

A Version 1 QR code generator implementation that encodes text strings into scannable 21×21 QR codes using byte mode encoding, Reed-Solomon error correction, and masking patterns.

## Project Structure

```
QRProject/
├── qr/                      # Core QR code generation modules
│   ├── encoding/            # Data encoding (byte mode)
│   ├── ecc/                 # Reed-Solomon error correction
│   ├── matrix/              # Matrix structure and data placement
│   └── masking/             # Mask patterns and format information
├── scripts/                 # Utility scripts
│   └── webapp.py           # Flask web interface
├── tests/                   # Test suite
├── demos/                   # Demo output files
└── docs/                    # Documentation

```

## Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd pp_assignment_two
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Web Application

1. **Set the Python path and start the Flask server:**
   ```bash
   # From the pp_assignment_two directory
   cd pp_assignment_two
   set PYTHONPATH=QRProject  # Windows CMD
   # OR
   $env:PYTHONPATH="QRProject"  # Windows PowerShell
   # OR
   export PYTHONPATH=QRProject  # Linux/Mac

   python QRProject/scripts/webapp.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

3. **Enter text and generate QR codes** - The webapp will display the generated QR code as an image that you can scan with your phone.

### Running Tests

Run the complete test suite:
```bash
cd QRProject
pytest tests/ -q
```

Run specific test files:
```bash
pytest tests/test_05_masking.py -v
pytest tests/test_06_integration.py -v
```

### Demo Files
- [demo_1.txt](demos/demo_1.txt) – String: "known"
- [demo_2.txt](demos/demo_2.txt) – String: "We've succeeded!"
- [demo_3.txt](demos/demo_3.txt) – String: "~i256_~_aA&fi"
- [demo_4.txt](demos/demo_4.txt) – String: "From a to o..."
- [demo_5.txt](demos/demo_5.txt) – String: "Sugarplum_Fairy_Nightmare"

Each file contains logged steps of encoding, ECC addition, matrix assembly, and masking.

## Web UI (local)

A minimal Flask web UI has been added to generate Version 1 QR codes and preview them in your browser.

Quick start:

1. Install dependencies:

    pip install -r requirements.txt

2. Run the app:

    python webapp.py

3. Open: http://127.0.0.1:5000/ and enter the text to encode.

Notes:
- The web UI uses the project's encoding, ECC, placement, masking and format-writing functions to produce the final 21x21 matrix and renders it to a PNG.
- If you see a server error when generating a code, it's likely the Reed–Solomon dependency is missing; install one of the recommended packages from `requirements.txt` (for example `pip install reedsolo`).
- This is a small demonstration scaffold; extend it as needed for larger QR versions and extra features.


