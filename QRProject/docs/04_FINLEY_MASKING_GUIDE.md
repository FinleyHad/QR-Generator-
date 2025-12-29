# FINLEY - MASKING & FINALIZATION Implementation Guide

## 📖 User Story
*"As a QR code scanner, I need the pattern to avoid large areas of all-black or all-white modules, so my camera can focus properly and read the code reliably under different lighting conditions."*

**Your Job:** Apply checkerboard mask pattern and write format information bits.

**Example:**
```
Before masking:          After masking:
1 0 1 0                  0 1 0 1  (flipped based on checkerboard)
0 1 0 1                  1 0 1 0
1 0 1 0                  0 1 0 1
0 1 0 1                  1 0 1 0
```

---

## **What You Implement**

Two main functions:

### **1. apply_mask0(matrix, reserved) → int**

Apply checkerboard mask pattern 0 to all non-reserved cells.

Mask pattern 0: Flip a cell if `(row + col) % 2 == 0`

```python
# If (row + col) is even, flip the bit
# If (row + col) is odd, keep the bit
```

### **2. finalize_matrix(placed_matrix, ecc_level, mask_id) → np.ndarray**

Takes the masked matrix and adds format information bits, returns final QR code.

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

✅ All 45 tests pass
✅ **Notify Person 5** that masking is ready

**Next:** Person 5 will integrate everything and create the web interface.
