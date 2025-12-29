# NADIR - MATRIX STRUCTURE & DATA PLACEMENT Implementation Guide

## � YOUR FILES TO IMPLEMENT

**Edit this skeleton file:**
1. `qr/matrix/NADIR_layout.py` - Matrix structure and data placement

**Reference files (read-only):**
- `qr/matrix/layout.py` - Working matrix creation and data placement

---

## �📖 User Story
*"As a QR code scanner, I need to see the three square corners (finder patterns) so I know it's a QR code and can detect its orientation, and I need the data arranged in a specific pattern so I can read it correctly."*

**Your Job:** Build the 21×21 QR code grid and place data into it using zig-zag pattern.

This is the biggest part - you have TWO main tasks:
1. Create base matrix with finder patterns, timing patterns, dark module
2. Place encoded data and ECC into the matrix in zig-zag order

---

## **Part A: Create Base Matrix**

### **What is the base matrix?**

A 21×21 grid with reserved areas already marked:

```
Finder Pattern (7×7)        Timing Pattern (alternating)
┌───────────┐                    │
│ ■■■■■■■ │                    └─ Row 6
│ ■     ■ │                    ┌─ Col 6
│ ■ ■■■ ■ │
│ ■ ■■■ ■ │
│ ■ ■■■ ■ │
│ ■     ■ │
│ ■■■■■■■ │
└───────────┘

Plus:
- Dark module at (13, 8) = always 1
- Format info areas
- Timing patterns at row 6 and col 6
```

### **Function to implement: create_base_matrix() → np.ndarray**

Returns a 21×21 matrix with all reserved areas filled.

---

## **Part B: Place Data**

### **What is data placement?**

Takes the data bits and ECC bits from Person 1 & 2, and places them into the matrix in a specific zig-zag pattern:

```
Start from bottom-right, move up in 2-column stripes:

┌─────────────────────┐
│                     │
│                     │
│     ← ← ↑ ↑         │  Zig-zag pattern
│     ↓ ↓ ← ← ↑ ↑     │
│     ↑ ↑ ↓ ↓ ← ← │
│     ← ← ↑ ↑         │
│                     │
└─────────────────────┘
    ← Skip col 6 (timing pattern)
```

### **Function to implement: place_data(base_matrix, data, ecc) → np.ndarray**

Takes the base matrix and places data/ECC bits in zig-zag order, skipping reserved areas.

---

## **Test Your Work**

```bash
pytest tests/test_03_matrix_structure.py tests/test_04_data_placement.py -v
```

**Expected:** 55 tests pass

---

## **Reference**

Look at `qr/matrix/layout.py` for working examples of:
- `create_base_matrix()`
- `place_data()`
- Finder pattern creation
- Timing pattern creation

Also see `qr/matrix/placement.py` for zig-zag pattern implementation.

---

## **When You're Done**

✅ All tests pass
✅ **Notify Person 4** that matrix is ready

**Next:** Person 4 will apply masking to your matrix.
