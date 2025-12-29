# QR Code Group Project - Team Implementation Guide

**Goal:** Each team member implements one part of the QR code generation pipeline. When all 5 parts are done, you have a complete QR code generator that produces 5 scannable codes from your phone.

---

## **Project Overview**

```
TEXT INPUT
    ↓
[Person 1] ENCODING → "A" becomes bits: 0100 0000 0001 0100 0001
    ↓
[Person 2] ERROR CORRECTION → Add safety bytes
    ↓
[Person 3] MATRIX → Build 21x21 grid with patterns
    ↓
[Person 4] MASKING → Apply checkerboard & format bits
    ↓
[Person 5] INTEGRATION & WEB → Final QR code + PNG + Web interface
    ↓
OUTPUT: Scannable QR codes (run_demos.py or webapp.py)
```

---

## **Team Assignments**

| Person | Role | Main File | Tests to Pass | Time Est. |
|--------|------|-----------|---------------|-----------|
| **1** | Encoding | `PERSON1_encoding.py` | `test_01_encoding.py` (21 tests) | 1-2 hrs |
| **2** | Error Correction | `PERSON2_ecc.py` | `test_02_ecc.py` (11 tests) | 1-2 hrs |
| **3** | Matrix Structure & Data | `PERSON3_matrix.py` | `test_03_matrix_structure.py` + `test_04_data_placement.py` (55 tests) | 2-3 hrs |
| **4** | Masking & Finalization | `PERSON4_masking.py` | `test_05_masking.py` (45 tests) | 2-3 hrs |
| **5** | Integration & Web | `PERSON5_integration.py` | `test_06_integration.py` + `test_07_quality_and_scannability.py` + `test_08_webapp.py` (40 tests) | 2-3 hrs |

---

## **How to Get Started**

### **Step 1: Read Your Personal Guide**
- Person 1: Read `PERSON1_ENCODING_GUIDE.md`
- Person 2: Read `PERSON2_ECC_GUIDE.md`
- Person 3: Read `PERSON3_MATRIX_GUIDE.md`
- Person 4: Read `PERSON4_MASKING_GUIDE.md`
- Person 5: Read `PERSON5_INTEGRATION_GUIDE.md`

### **Step 2: Edit Your Skeleton File**
Each person has a skeleton file with function stubs and detailed TODO comments:
- Person 1: `PERSON1_encoding.py`
- Person 2: `PERSON2_ecc.py`
- Person 3: `PERSON3_matrix.py`
- Person 4: `PERSON4_masking.py`
- Person 5: `PERSON5_integration.py`

### **Step 3: Run Your Tests**
```bash
# Person 1
pytest tests/test_01_encoding.py -v

# Person 2
pytest tests/test_02_ecc.py -v

# Person 3
pytest tests/test_03_matrix_structure.py tests/test_04_data_placement.py -v

# Person 4
pytest tests/test_05_masking.py -v

# Person 5
pytest tests/test_06_integration.py tests/test_07_quality_and_scannability.py tests/test_08_webapp.py -v
```

### **Step 4: Merge & Test Full Pipeline**
Once everyone finishes:
```bash
# Test everything together
pytest tests/ -v

# Generate demo QR codes
python run_demos.py

# Or run web app
python webapp.py
```

---

## **Dependency Order (Important!)**

```
Person 1 → Person 2 → Person 3 → Person 4 → Person 5
```

**You can't start until the person before you finishes.** Person 2 depends on Person 1's output, etc.

### Timeline:
- **Days 1-2:** Person 1 finishes Encoding
- **Days 2-3:** Person 2 finishes ECC (when Person 1 done)
- **Days 3-4:** Person 3 finishes Matrix (when Person 2 done)
- **Days 4-5:** Person 4 finishes Masking (when Person 3 done)
- **Days 5-6:** Person 5 finishes Integration (when Person 4 done)
- **Day 6:** Test everything, generate QR codes

---

## **Merge Strategy**

When each person finishes, they commit/share their code:

1. Person 1 finishes → Person 2 copies their implementation into `qr/encoding/`
2. Person 2 finishes → Person 3 copies both Person 1 & 2 into `qr/`
3. Person 3 finishes → Person 4 copies all previous work
4. Person 4 finishes → Person 5 copies all previous work + integrates web

---

## **Workflow**

### **Each Person's Daily Workflow:**

1. **Read the guide** for your part (5 min)
2. **Look at your tests** - they show exactly what functions should do (10 min)
3. **Open your skeleton file** (`PERSONx_*.py`) (5 min)
4. **Find the first TODO** (the `raise NotImplementedError` parts) (2 min)
5. **Implement that function** using the guide and docstrings (20-30 min)
6. **Run tests** to check if that function works (5 min)
7. **Repeat steps 4-6** for all functions in your file (depends on person, 1-3 hrs total)
8. **When all tests pass**, you're done! Notify next person.

---

## **Reference Files (Read-Only)**

These show working examples - **don't modify these**, use them to understand patterns:
- `qr/encoding/byte_mode.py` - Reference for Person 1
- `qr/ecc/reed_solomon.py` - Reference for Person 2
- `qr/matrix/layout.py` - Reference for Person 3
- `qr/masking/mask0.py` - Reference for Person 4
- `qr/generate.py` - Reference for Person 5

---

## **Quick Reference Docs**

- `REFERENCE_ASCII_BITS.md` - ASCII codes, bit operations
- `REFERENCE_CONSTANTS.md` - ECC levels, matrix sizes, format bits
- `REFERENCE_QR_SPECS.md` - QR code version 1 specifications

---

## **End Goal: Run These Commands**

When ALL team members finish:

```bash
# Generate 5 demo QR codes
python run_demos.py

# Check the output
ls *.png

# Or run the web app and scan from your phone
python webapp.py
# Then visit http://localhost:5000 in your browser
```

**You should see 5 `.png` files that you can scan with your phone's camera!**

---

## **Questions During Implementation?**

Each guide has a "Common Issues" section. If stuck:
1. Check your guide's "Common Issues"
2. Look at the reference implementation file
3. Check the test file to see expected behavior
4. Read the function's docstring again
5. Ask your person's "AI assistant" (GitHub Copilot)

---

## **Success Criteria**

✅ Person 1: `test_01_encoding.py` - 21 passed  
✅ Person 2: `test_02_ecc.py` - 11 passed  
✅ Person 3: `test_03_matrix_structure.py` + `test_04_data_placement.py` - 55 passed  
✅ Person 4: `test_05_masking.py` - 45 passed  
✅ Person 5: Integration tests - 40 passed  
✅ **All together:** `pytest tests/ -v` - 172 passed (or more)  
✅ **Final:** Can scan 5 QR codes from your phone  

---

**Good luck! 🚀**
