# MUSTAPHA - ENCODING Implementation Guide

## � YOUR FILES TO IMPLEMENT

**Edit this skeleton file:**
1. `qr/encoding/MUSTAPHA_byte_mode.py` - Main byte mode encoding function

**Reference files (read-only):**
- `qr/encoding/byte_mode.py` - Working implementation to learn from
- `qr/encoding/encode.py` - Full encoding pipeline example

---

## �📖 User Story
*"As a QR code user, I want to type text like 'Hello World', and have it converted into the binary format that QR codes understand, so the text can be encoded into a scannable QR code."*

**Your Job:** Convert text input into a bitstring using byte mode encoding.

**Example:** "A" → [0,1,0,0, 0,0,0,0,0,0,0,1, 0,1,0,0,0,0,0,1]
- First 4 bits: 0100 = byte mode indicator
- Next 8 bits: 00000001 = character count (1)
- Last 8 bits: 01000001 = ASCII code for 'A' (65)

---

## 📁 **YOUR FILE TO EDIT**

**Location:** `qr/encoding/MUSTAPHA_encoding.py`

This is your skeleton file with TODOs. Fill in the functions here.

---

## **What You Implement**

You need to fill in these 3 functions in `qr/encoding/MUSTAPHA_encoding.py`:

### **1. byte_mode(text: str) → bytes**
First function - convert text to bytes using ISO-8859-1 encoding.

**Input:** String (e.g., "A", "hello", "test123")
**Output:** Python bytes object

**Why bytes?** QR codes work with byte values (0-255), not characters.

**Example:**
```python
byte_mode("A")  # Returns b'A'
byte_mode("Hello")  # Returns b'Hello'
```

### **2. encode_string(text: str) → list[int]**
Second function - convert bytes to bit list with QR code structure.

**Input:** String
**Output:** List of bits [0, 1, 0, 1, ...]

**QR Structure:**
- 4 bits: Mode indicator (0100 for byte mode)
- 8 bits: Character count
- 8 bits per character: Actual data
- Optional: Padding bytes

**Example for "A":**
```
Mode:   0100          (4 bits)
Count:  00000001      (8 bits - value 1)
Data:   01000001      (8 bits - ASCII 65)
Result: [0,1,0,0, 0,0,0,0,0,0,0,1, 0,1,0,0,0,0,0,1]
```

### **3. get_encoded_bits(text: str) → numpy.ndarray**
Third function - convert bit list to numpy array for matrix.

**Input:** String
**Output:** 1D numpy array of 0s and 1s

**Why numpy?** The matrix module needs arrays, not lists.

---

## **Reference Files**

Two files already have working implementations - use them to learn!

**Read-Only Reference Files:**
- `qr/encoding/byte_mode.py` - Working byte_mode() implementation
- `qr/encoding/encode.py` - Full working pipeline

You can look at these to understand how things work, but write your own code.

---

## **Step-by-Step Implementation**

### **Step 1: Implement byte_mode()**

```python
def byte_mode(text: str) -> list[int]:
    # TODO 1: Create mode indicator [0,1,0,0]
    
    # TODO 2: Convert character count to 8-bit binary
    
    # TODO 3: Convert each character to 8-bit ASCII
    
    # TODO 4: Combine all bits and return
```

**Helper Code You Can Use:**

```python
# Convert a number to binary bits (8 bits)
def int_to_bits(value: int, num_bits: int) -> list[int]:
    bits = []
    for i in range(num_bits - 1, -1, -1):
        bits.append((value >> i) & 1)
    return bits

# Or using bin():
bits = [int(b) for b in bin(65)[2:].zfill(8)]  # 65 → '01000001'

# Get ASCII value of a character:
ascii_code = ord('A')  # Returns 65
```

### **Step 2: Implement encode_string()**

```python
def encode_string(text: str) -> list[int]:
    # TODO: Just call byte_mode(text) and return result
    pass
```

---

## **Test Your Work**

Run this command to see if your code works:

```bash
pytest tests/test_01_encoding.py -v
```

**What to expect:**
- First run: Lots of red ❌ (functions not implemented)
- After implementing byte_mode: Some green ✅ (but missing padding)
- After implementing padding: All green ✅ (21 tests pass)

---

## **Tests Explained (What They Check)**

| Test Name | What It Tests | Your Task |
|-----------|---------------|-----------|
| `test_byte_mode_mode_indicator` | Mode bits are 0100 | Add [0,1,0,0] to start |
| `test_byte_mode_char_count_encoding` | Character count is binary | Use ord() and convert to bits |
| `test_byte_mode_single_char` | Single character works | Include character's ASCII bits |
| `test_byte_mode_multiple_chars` | Multiple chars work | Loop through all characters |
| `test_byte_mode_padding` | Padding bytes added | Add 0xEC and 0x11 bytes if needed |

---

## **Common Issues & Solutions**

### **Issue 1: "I don't know how to convert a number to binary bits"**

**Solution:**
```python
# Method 1: Bit shifting (recommended)
def int_to_bits(value, bits):
    return [(value >> (bits - 1 - i)) & 1 for i in range(bits)]

# Example:
int_to_bits(65, 8)  # Returns [0, 1, 0, 0, 0, 0, 0, 1]

# Method 2: Using bin()
int_to_bits_v2 = [int(b) for b in format(65, '08b')]  # Returns [0, 1, 0, 0, 0, 0, 0, 1]
```

### **Issue 2: "My result is almost right but character count is wrong"**

**Solution:** Character count must be exactly 8 bits:
```python
# Wrong:
count_bits = bin(len(text))[2:]  # "1" for 1 char - TOO SHORT

# Right:
count_bits = format(len(text), '08b')  # "00000001" for 1 char - 8 BITS
```

### **Issue 3: "What is padding? When do I add it?"**

**Solution:** For version 1 QR codes, you need exactly 19 bytes total:
```python
# Calculate how many bits you have so far
bits_so_far = 4 + 8 + (len(text) * 8)

# If less than 19*8 = 152 bits, add padding
if bits_so_far < 152:
    # Add padding bytes: 0xEC (11101100) and 0x11 (00010001) alternating
    padding_needed = (152 - bits_so_far) // 8
    for i in range(padding_needed):
        byte_value = 0xEC if i % 2 == 0 else 0x11
        result.extend(int_to_bits(byte_value, 8))
```

### **Issue 4: "Tests say I need padding but the test text fits without it"**

**Solution:** Some tests use short text (like "A") that don't need padding. That's OK! Only add padding if:
```python
total_bits = 4 + 8 + (len(text) * 8)  # mode + count + data
if total_bits < 152:
    # Add padding
else:
    # No padding needed
```

---

## **Reference: Test Examples**

Looking at `tests/test_01_encoding.py`, here's what each test expects:

```python
# Test 1: Mode indicator
result = byte_mode("A")
assert result[0:4] == [0, 1, 0, 0]  # First 4 bits must be mode

# Test 2: Character count
assert result[4:12] == [0, 0, 0, 0, 0, 0, 0, 1]  # Next 8 bits = 1

# Test 3: Character data
assert result[12:20] == [0, 1, 0, 0, 0, 0, 0, 1]  # ASCII of 'A'

# Test 4: Multiple characters
result = byte_mode("AB")
assert len(result) >= 28  # 4 + 8 + 8 + 8 = 28 bits minimum
```

---

## **Hints**

💡 Use Python's built-in functions:
- `ord(char)` - Get ASCII value
- `len(text)` - Get character count
- `format(value, '08b')` - Convert to 8-bit binary string
- `int(bit, 2)` - Convert binary string to int

💡 Build your result step-by-step:
```python
result = []
result.extend([0, 1, 0, 0])  # Mode
result.extend(char_count_bits)  # Count
for char in text:
    result.extend(char_bits)  # Each character
# Add padding...
return result
```

💡 Test a small example by hand first:
- Write out what "A" should become
- Then code it to match
- Then test it

---

## **When You're Done**

✅ All tests in `test_01_encoding.py` pass  
✅ You can run: `python -c "from PERSON1_encoding import byte_mode; print(byte_mode('A'))"`  
✅ **Notify Person 2** that encoding is ready  

**Next:** Person 2 will take your `byte_mode()` function and use it for error correction.
