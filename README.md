Course project for **Programming in Python at the University of Reading**.

This project implements a **Version 1 QR code generator** that converts text strings into scannable **21×21 QR codes** using:

- Byte mode encoding
- Reed–Solomon error correction
- Mask pattern evaluation
- QR matrix construction and data placement

The system also includes a **Flask web interface** that allows users to generate QR codes interactively in a browser.

---

## Key Features

- QR code generation from input text
- Byte-mode data encoding
- Reed–Solomon error correction
- QR matrix generation and masking
- Flask web interface for QR generation
- Automated tests for core functionality

---

## Project Structure


QRProject/
├── qr/ # Core QR code generation modules
│ ├── encoding/ # Data encoding (byte mode)
│ ├── ecc/ # Reed-Solomon error correction
│ ├── matrix/ # Matrix structure and data placement
│ └── masking/ # Mask patterns and format information
├── scripts/
│ └── webapp.py # Flask web interface
├── tests/ # Test suite
├── demos/ # Demo output files
└── docs/ # Documentation


---

## Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

---

## Installation

1. **Navigate to the project directory**

```bash
cd pp_assignment_two

Install dependencies

pip install -r requirements.txt
Running the Web Application

Set the Python path

export PYTHONPATH=QRProject

Windows PowerShell:

$env:PYTHONPATH="QRProject"

Run the web application

python QRProject/scripts/webapp.py

Open the interface

Open your browser and go to:

http://127.0.0.1:5000

Enter text and generate QR codes directly in the web interface.

Running Tests

Run the full test suite:

cd QRProject
pytest tests/ -q

Run specific tests:

pytest tests/test_05_masking.py -v
pytest tests/test_06_integration.py -v
Demo Files

Example QR generation runs are provided in the demos directory.

demo_1.txt – String: "known"

demo_2.txt – String: "We've succeeded!"

demo_3.txt – String: "~i256_~_aA&fi"

demo_4.txt – String: "From a to o..."

demo_5.txt – String: "Sugarplum_Fairy_Nightmare"

Each file logs the steps of:

data encoding

error correction generation

matrix construction

masking evaluation

Notes

The web interface uses the project's encoding, error correction, matrix placement, masking, and format-writing modules to generate the final QR matrix.

If QR generation fails due to missing Reed–Solomon support, install the dependency:

pip install reedsolo

The project currently supports Version 1 QR codes (21×21) but can be extended to larger QR versions.
