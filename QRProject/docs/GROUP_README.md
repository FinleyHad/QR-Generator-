# QR CODE GROUP PROJECT - COMPLETE GUIDE

**Goal:** Build a QR code generator together. Each of 5 team members owns one part.

---

## 📋 **Quick Start**

1. **Read this file** (you're doing it now ✓)
2. **Each person reads their guide (in order):**
   - Person 1: `01_MUSTAPHA_ENCODING_GUIDE.md`
   - Person 2: `02_MUSA_ECC_GUIDE.md`
   - Person 3: `03_NADIR_MATRIX_GUIDE.md`
   - Person 4: `04_FINLEY_MASKING_GUIDE.md`
   - Person 5: `05_SULTAN_INTEGRATION_GUIDE.md`

3. **Each person edits their skeleton file:**
   - Person 1: `qr/encoding/PERSON1_encoding.py`
   - Person 2: `qr/ecc/PERSON2_ecc.py`
   - Person 3: `qr/matrix/PERSON3_matrix.py`
   - Person 4: `qr/masking/PERSON4_masking.py`
   - Person 5: `PERSON5_integration.py` (root)

4. **Each person runs their tests:**
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

5. **Final test (everyone):**
   ```bash
   pytest tests/ -v
   ```

---

## 👥 **Team Assignments**

### **Person 1: MUSTAPHA - ENCODING** 
**Files:** `qr/encoding/PERSON1_encoding.py`  
**Guide:** `01_MUSTAPHA_ENCODING_GUIDE.md`  
**Tests:** `tests/test_01_encoding.py` (21 tests)  
**What:** Convert text to bits (e.g., "A" → `0100 00000001 01000001`)  
**Time:** 1-2 hours  

**TODO:**
- [ ] Implement `byte_mode(text)`
- [ ] Implement `encode_string(text)` 
- [ ] Pass 21 tests
- [ ] Notify Person 2 when done

---

### **Person 2: MUSA - ERROR CORRECTION**
**Files:** `qr/ecc/PERSON2_ecc.py`  
**Guide:** `02_MUSA_ECC_GUIDE.md`  
**Tests:** `tests/test_02_ecc.py` (11 tests)  
**What:** Add Reed-Solomon error correction bytes (makes QR scannable)  
**Time:** 1-2 hours  
**Dependency:** Needs Person 1's work first  

**TODO:**
- [ ] Import `reedsolo` library
- [ ] Implement `add_ecc(data, ecc_level)`
- [ ] Pass 11 tests
- [ ] Notify Person 3 when done

---

### **Person 3: NADIR - MATRIX & DATA PLACEMENT**
**Files:** `qr/matrix/PERSON3_matrix.py`  
**Guide:** `03_NADIR_MATRIX_GUIDE.md`  
**Tests:** `tests/test_03_matrix_structure.py` + `tests/test_04_data_placement.py` (55 tests)  
**What:** Build 21×21 QR grid with finder patterns, timing patterns, and place data  
**Time:** 2-3 hours  
**Dependency:** Needs Person 1 & 2's work first  

**TODO:**
- [ ] Create base matrix with finder patterns (7×7)
- [ ] Add timing patterns (alternating row 6 & col 6)
- [ ] Add dark module at (13, 8)
- [ ] Implement data placement in zig-zag pattern
- [ ] Pass 55 tests
- [ ] Notify Person 4 when done

---

### **Person 4: FINLEY - MASKING & FINALIZATION**
**Files:** `qr/masking/PERSON4_masking.py`  
**Guide:** `04_FINLEY_MASKING_GUIDE.md`  
**Tests:** `tests/test_05_masking.py` (45 tests)  
**What:** Apply mask pattern (checkerboard) and write format bits  
**Time:** 2-3 hours  
**Dependency:** Needs Person 1, 2, & 3's work first  

**TODO:**
- [ ] Implement mask pattern 0 (checkerboard)
- [ ] Write format information bits
- [ ] Finalize matrix (0/1 only)
- [ ] Preserve reserved areas
- [ ] Pass 45 tests
- [ ] Notify Person 5 when done

---

### **Person 5: SULTAN - INTEGRATION & WEB**
**Files:** `PERSON5_integration.py`  
**Guide:** `05_SULTAN_INTEGRATION_GUIDE.md`  
**Tests:** `tests/test_06_integration.py` + `tests/test_07_quality_and_scannability.py` + `tests/test_08_webapp.py` (40 tests)  
**What:** Connect everything together, add PNG rendering, Flask web app  
**Time:** 2-3 hours  
**Dependency:** Needs Person 1, 2, 3, & 4's work first  

**TODO:**
- [ ] Implement complete pipeline function
- [ ] Verify matrix completeness
- [ ] Test PNG rendering with scale/border
- [ ] Add Flask web endpoints
- [ ] Pass 40 tests
- [ ] Generate 5 demo QR codes
- [ ] All tests pass together

---

## 🔄 **Workflow & Merge Strategy**

### **Work Order (Sequential)**
```
Person 1 (Days 1-2)
    ↓ (passes test_01_encoding.py)
Person 2 (Days 2-3)
    ↓ (passes test_02_ecc.py)
Person 3 (Days 3-4)
    ↓ (passes test_03 + test_04)
Person 4 (Days 4-5)
    ↓ (passes test_05)
Person 5 (Days 5-6)
    ↓ (passes test_06 + test_07 + test_08)
All together: pytest tests/ -v ✓
```

### **How to Merge**
1. Person 1 finishes → shares working `PERSON1_encoding.py`
2. Person 2 takes Person 1's code, adds their code
3. Person 3 takes Person 1 + 2, adds their code
4. Person 4 takes Person 1 + 2 + 3, adds their code
5. Person 5 takes everyone's code, integrates everything

**Key:** Don't start until the person before you finishes!

---

## 📁 **Project Structure**

```
QRProject/
├── 01_MUSTAPHA_ENCODING_GUIDE.md        ← Person 1 reads this
├── 02_MUSA_ECC_GUIDE.md                 ← Person 2 reads this
├── 03_NADIR_MATRIX_GUIDE.md             ← Person 3 reads this
├── 04_FINLEY_MASKING_GUIDE.md           ← Person 4 reads this
├── 05_SULTAN_INTEGRATION_GUIDE.md       ← Person 5 reads this
├── TEAM_README.md                       ← This file
│
├── qr/
│   ├── encoding/
│   │   ├── byte_mode.py                (reference - read only)
│   │   ├── encode.py                   (reference - read only)
│   │   └── PERSON1_encoding.py         ← PERSON 1 EDITS THIS
│   │
│   ├── ecc/
│   │   ├── reed_solomon.py             (reference - read only)
│   │   └── PERSON2_ecc.py              ← PERSON 2 EDITS THIS
│   │
│   ├── matrix/
│   │   ├── layout.py                   (reference - read only)
│   │   ├── placement.py                (reference - read only)
│   │   └── PERSON3_matrix.py           ← PERSON 3 EDITS THIS
│   │
│   ├── masking/
│   │   ├── mask0.py                    (reference - read only)
│   │   ├── finalize.py                 (reference - read only)
│   │   └── PERSON4_masking.py          ← PERSON 4 EDITS THIS
│   │
│   └── generate.py                     (reference - read only)
│
├── PERSON5_integration.py              ← PERSON 5 EDITS THIS
│
├── tests/
│   ├── test_01_encoding.py             (Person 1 runs this)
│   ├── test_02_ecc.py                  (Person 2 runs this)
│   ├── test_03_matrix_structure.py     (Person 3 runs these)
│   ├── test_04_data_placement.py
│   ├── test_05_masking.py              (Person 4 runs this)
│   ├── test_06_integration.py          (Person 5 runs these)
│   ├── test_07_quality_and_scannability.py
│   └── test_08_webapp.py
│
├── webapp.py                           (final web app)
├── run_demos.py                        (final demo script)
└── save_qr_images.py                   (final image saver)
```

---

## 🎯 **Success Criteria**

✅ **Person 1:** `pytest tests/test_01_encoding.py -v` → 21 passed  
✅ **Person 2:** `pytest tests/test_02_ecc.py -v` → 11 passed  
✅ **Person 3:** `pytest tests/test_03_matrix_structure.py tests/test_04_data_placement.py -v` → 55 passed  
✅ **Person 4:** `pytest tests/test_05_masking.py -v` → 45 passed  
✅ **Person 5:** `pytest tests/test_06_integration.py tests/test_07_quality_and_scannability.py tests/test_08_webapp.py -v` → 40 passed  
✅ **All together:** `pytest tests/ -v` → 172+ passed  
✅ **Final:** Can run `python run_demos.py` and see 5 QR codes  

---

## 🚀 **End Goal: Generate QR Codes**

When everyone finishes:

```bash
# Run demo to generate 5 scannable QR codes
python run_demos.py

# You'll see 5 files created:
# qr_known.png
# qr_succeeded.png
# qr_256.png
# qr_nightmare.png
# qr_fairy.png

# Scan any with your phone's camera! They work! 📱
```

Or run the web app:
```bash
python webapp.py
# Visit http://localhost:5000 in your browser
# Click "Generate All" to see 5 QR codes you can scan
```

---

## 📚 **Reference Docs**

- `REFERENCE_ASCII_BITS.md` - ASCII values and bit operations
- `REFERENCE_CONSTANTS.md` - QR specs and magic numbers
- `REFERENCE_QR_SPECS.md` - Full QR code version 1 specification

---

## ❓ **Help During Implementation**

**For each person:**

1. **Read your guide** carefully (PERSON1/2/3/4/5_GUIDE.md)
2. **Look at test file** to understand what functions should do
3. **Check "Common Issues" section** in your guide
4. **Look at reference implementation** file (read-only) for hints
5. **Ask your AI assistant** (GitHub Copilot) for help with code

**If completely stuck:**
- Check the reference file (qr/encoding/byte_mode.py, etc.)
- The reference is a working implementation you can learn from
- Don't copy it directly - understand it first!

---

## ✨ **Tips for Success**

💡 **Start small:** Get one test passing, then the next  
💡 **Run tests often:** After every function, run pytest  
💡 **Use helper functions:** They save time and reduce bugs  
💡 **Read docstrings:** They tell you exactly what functions should do  
💡 **Test by hand first:** Write out what "A" should become before coding  
💡 **Communicate:** Tell next person when you're done  

---

## 📅 **Timeline (Suggested)**

| Days | Who | What | Status |
|------|-----|------|--------|
| 1-2 | Person 1 | Encoding | 21 tests ✓ |
| 2-3 | Person 2 | ECC | 11 tests ✓ |
| 3-4 | Person 3 | Matrix | 55 tests ✓ |
| 4-5 | Person 4 | Masking | 45 tests ✓ |
| 5-6 | Person 5 | Integration | 40 tests ✓ |
| 6 | Everyone | Final test | 172+ tests ✓ |
| 6 | Everyone | Generate QR codes | 5 scannable PNGs ✓ |

---

## 🎉 **When You're Done**

Run this and see your 5 QR codes:
```bash
python run_demos.py
ls *.png
```

Scan them with your phone! They're real, working QR codes! 📱✨

---

**Good luck! You've got this! 🚀**

---

## 💬 **Questions?**

- Read your PERSON guide
- Check "Common Issues" section
- Look at reference code (read-only)
- Ask your AI assistant
- Text your team on Discord/Slack

**You're building a real QR code generator together. That's awesome!** 🎊
