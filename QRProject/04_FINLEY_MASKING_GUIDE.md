# FINLEY - MASKING & FINALIZATION Implementation Guide

## � YOUR FILES TO IMPLEMENT

**Edit these skeleton files:**
1. `qr/masking/FINLEY_mask0.py` - Apply mask pattern 0 (checkerboard)
2. `qr/masking/FINLEY_finalize.py` - Finalize matrix and write format info
3. `qr/masking/FINLEY_format_info.py` - Calculate and write format information bits
**Reference files (read-only):**
- `qr/masking/mask0.py` - Working mask pattern implementation
- `qr/masking/finalize.py` - Working finalization function
- `qr/masking/format_info.py` - Format information calculation

---

## �📖 User Story
*"As a QR code scanner, I need the pattern to avoid large areas of all-black or all-white modules, so my camera can focus properly and read the code reliably under different lighting conditions."*

**Your Job:** Apply checkerboard mask pattern and write format information bits.

**Example - Why masking is needed:**
```
PROBLEM: Large blocks of same color are hard for cameras to scan
Before masking:          After masking (pattern 0):
1 1 1 1                  0 1 0 1  ← XOR flips ONLY positions where (row+col) is even
1 1 1 1                  1 0 1 0  ← Creates checkerboard pattern
0 0 0 0                  1 0 1 0  ← Better contrast and edges!
0 0 0 0                  0 1 0 1  ← Breaks up large same-color blocks

Detailed flip logic (showing first 2 rows):
Row 0: Position (0,0): (0+0)%2=0 → FLIP: 1⊕1=0  Position (0,1): (0+1)%2=1 → KEEP: 1⊕0=1
       Position (0,2): (0+2)%2=0 → FLIP: 1⊕1=0  Position (0,3): (0+3)%2=1 → KEEP: 1⊕0=1
       Result: 0 1 0 1

Row 1: Position (1,0): (1+0)%2=1 → KEEP: 1⊕0=1  Position (1,1): (1+1)%2=0 → FLIP: 1⊕1=0
       Position (1,2): (1+2)%2=1 → KEEP: 1⊕0=1  Position (1,3): (1+3)%2=0 → FLIP: 1⊕1=0
       Result: 1 0 1 0

The mask itself is: 1 0 1 0  ← This checkerboard gets XORed with your data
                    0 1 0 1
                    1 0 1 0
                    0 1 0 1
```

**Why this helps:** Cameras and scanners struggle with large areas of solid black or white. The checkerboard XOR pattern creates edges and contrast everywhere, making it easier to detect and read the QR code under different lighting conditions.

---

## **What You Implement**

**You have 3 main functions to implement:**

### **Function 1: apply_mask0(matrix, reserved) in FINLEY_mask0.py**

Apply checkerboard mask pattern 0 to all non-reserved cells.

Mask pattern 0: Flip a cell if `(row + col) % 2 == 0`

```python
# If (row + col) is even, flip the bit
# If (row + col) is odd, keep the bit
```

Returns: Penalty score (int)

---

### **Function 2: finalize_matrix(matrix, ecc_level, mask_id) in FINLEY_finalize.py**

Complete pipeline: apply mask → compute format bits → write format info.

Returns: Final 21×21 QR code ready for rendering

---

### **Function 3: compute_format_bits(ecc_level, mask_id) in FINLEY_format_info.py**

Compute 15-bit format information code with BCH error correction.

Returns: List of 15 bits [0 or 1]

**Note:** There are additional helper functions in these files, but these are the 3 main functions you need to focus on.

---

## **Test Your Work**

```bash
pytest tests/test_05_masking.py -v
```

**Expected:** 45 tests pass

---

## **Reference**

Look at `qr/masking/` for working examples:
- `mask0.py` - Checkerboard pattern
- `finalize.py` - Format bit placement
- `format_info.py` - Format bit coordinates

---

## **When You're Done**

✅ All tests pass
✅ **Notify Person 5** that masking is ready

**Next:** Person 5 will integrate everything and create the web interface.
