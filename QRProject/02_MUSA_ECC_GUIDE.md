# MUSA - ERROR CORRECTION (ECC) Implementation Guide

## � YOUR FILES TO IMPLEMENT

**Edit these skeleton files:**
1. `qr/ecc/MUSA_reed_solomon.py` - Reed-Solomon error correction function
2. `qr/ecc/MUSA_ecc.py` - ECC wrapper and utilities

**Reference files (read-only):**
- `qr/ecc/reed_solomon.py` - Working implementation to learn from

---

## �📖 User Story
*"As a QR code user, I want my QR code to still work even if it gets scratched, dirty, or partially covered, so I can scan it in real-world conditions without worrying about minor damage."*

**Your Job:** Add error correction bytes to make the QR code readable even if partially damaged.

**Example:** Mustapha gives you encoded bits, you add ECC bytes so code works even with 30% damage.

---

## 📁 **YOUR FILE TO EDIT**

**Location:** `qr/ecc/MUSA_ecc.py`

This is your skeleton file with TODOs. Fill in the functions here.

---

## **What You Implement**

You need to fill in these 2 functions in `qr/ecc/MUSA_ecc.py`:

### **add_ecc(data: list[int], ecc_level: str) → list[int]**

Takes the encoded bits from Person 1, adds Reed-Solomon error correction bytes, and returns data + ECC.

**Input:**
- `data`: List of bits from Person 1's encode_string() (19 bytes = 152 bits)
- `ecc_level`: One of "L", "M", "Q", "H" (error correction strength)

**Output:**
- List of bits: data + ECC bytes (length depends on level)

**ECC Byte Counts (Version 1):**
- Level L: 7 ECC bytes
- Level M: 10 ECC bytes
- Level Q: 13 ECC bytes
- Level H: 17 ECC bytes

---

## **What is Error Correction?**

Reed-Solomon error correction is a mathematical algorithm that adds extra bytes. If your QR code gets 30% damaged, it can still be read!

**Example:**
```
Original data: [1, 0, 1, 0, ...]
ECC bytes:     [?, ?, ?, ?, ...] ← Algorithm calculates these
─────────────────────────────────
Combined:      [1, 0, 1, 0, ..., ?, ?, ?, ?, ...]

If half is damaged:
               [X, X, X, X, ..., ?, ?, ?, ?, ...]
Scanner can recover the X's using the ? bytes!
```

**Good news:** You don't need to understand the math. You'll use the `reedsolo` library.

---

## **Reference Files**

Two files already have working implementations - use them to learn!

**Read-Only Reference Files:**
- `qr/ecc/reed_solomon.py` - Working ECC implementation
- `qr/ecc/__init__.py` - How ECC fits in the pipeline

You can look at these to understand how things work, but write your own code.

---

## **Step-by-Step Implementation**

### **Step 1: Import reedsolo**

```python
# At the top of PERSON2_ecc.py:
from reedsolo import RSCodec
```

### **Step 2: Implement add_ecc()**

```python
def add_ecc(data: list[int], ecc_level: str) -> list[int]:
    # TODO 1: Validate ecc_level is one of "L", "M", "Q", "H"
    
    # TODO 2: Look up ECC codeword count for the level
    ecc_counts = {"L": 7, "M": 10, "Q": 13, "H": 17}
    
    # TODO 3: Convert bit list to bytes
    # data is a list of 0s and 1s, but RSCodec wants bytes
    # Group bits into 8-bit chunks and convert to integers
    # Example: [0,1,0,0,0,0,0,1] → 0x41 (65)
    
    # TODO 4: Create RSCodec with the ECC count
    
    # TODO 5: Encode the data bytes to add ECC
    
    # TODO 6: Convert result back to bits
    
    # TODO 7: Return the combined result
```

---

## **Detailed Steps**

### **Step 1: Validate ECC Level**

```python
if ecc_level not in ["L", "M", "Q", "H"]:
    raise ValueError(f"Invalid ECC level: {ecc_level}")
```

### **Step 2: Get ECC Byte Count**

```python
ecc_counts = {"L": 7, "M": 10, "Q": 13, "H": 17}
num_ecc = ecc_counts[ecc_level]
```

### **Step 3: Convert Bits to Bytes**

The data from Person 1 is 152 bits = 19 bytes.

```python
# Convert list of bits to list of bytes
data_bytes = []
for i in range(0, len(data), 8):
    byte_bits = data[i:i+8]
    byte_value = 0
    for bit in byte_bits:
        byte_value = (byte_value << 1) | bit
    data_bytes.append(byte_value)

# Now data_bytes = [?, ?, ?, ..., ?]  ← 19 bytes
```

### **Step 4: Create Reed-Solomon Codec**

```python
from reedsolo import RSCodec

# Create codec for the number of ECC bytes we need
codec = RSCodec(num_ecc)
```

### **Step 5: Encode Data to Add ECC**

```python
# The encode() method returns (encoded_data, ecc)
# We want both: data + ecc bytes combined
encoded_bytes = codec.encode(bytes(data_bytes))[0]

# Now encoded_bytes = original 19 bytes + ECC bytes
# Total length = 19 + num_ecc
```

### **Step 6: Convert Bytes Back to Bits**

```python
result = []
for byte_value in encoded_bytes:
    # Convert each byte to 8 bits
    for i in range(7, -1, -1):
        result.append((byte_value >> i) & 1)

return result
```

---

## **Test Your Work**

```bash
pytest tests/test_02_ecc.py -v
```

**What to expect:**
- First run: All red ❌ (function not implemented)
- After implementing: All green ✅ (11 tests pass)

---

## **Tests Explained**

| Test Name | What It Tests | Your Task |
|-----------|---------------|-----------|
| `test_ecc_level_l` | Level L works (7 ECC bytes) | Implement add_ecc with L level |
| `test_ecc_level_m` | Level M works (10 ECC bytes) | Handle M level |
| `test_ecc_level_q` | Level Q works (13 ECC bytes) | Handle Q level |
| `test_ecc_level_h` | Level H works (17 ECC bytes) | Handle H level |
| `test_ecc_invalid_level` | Invalid level raises error | Validate input |
| `test_ecc_deterministic` | Same input = same output | Result must be consistent |

---

## **Common Issues**

### **Issue 1: "reedsolo not found"**

**Solution:** Install it first:
```bash
pip install reedsolo
```

### **Issue 2: "I get wrong number of ECC bytes"**

**Solution:** Make sure you're using the right ecc_counts:
```python
ecc_counts = {"L": 7, "M": 10, "Q": 13, "H": 17}  # Correct!
```

### **Issue 3: "How do I convert bits to bytes?"**

**Solution:** Group 8 bits at a time:
```python
# Bits to bytes
data_bytes = []
for i in range(0, len(bits), 8):
    byte_val = 0
    for bit in bits[i:i+8]:
        byte_val = (byte_val << 1) | bit
    data_bytes.append(byte_val)

# Bytes to bits (reverse)
bits = []
for byte_val in data_bytes:
    for i in range(7, -1, -1):
        bits.append((byte_val >> i) & 1)
```

### **Issue 4: "RSCodec.encode() returns a tuple, not bytes"**

**Solution:** The encode() method returns `(encoded_bytes, ecc_bytes)`. Use the first element:
```python
encoded, ecc = codec.encode(bytes(data_bytes))
# encoded = original data + ECC bytes (what we want)
# ecc = just the ECC bytes (not needed)
```

---

## **When You're Done**

✅ All 11 tests in `test_02_ecc.py` pass  
✅ You can run: `python -c "from PERSON2_ecc import add_ecc; print(len(add_ecc([...], 'L')))"`  
✅ **Notify Person 3** that ECC is ready  

**Next:** Person 3 will take your add_ecc() function and use it to build the QR matrix.
