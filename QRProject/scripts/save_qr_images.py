#!/usr/bin/env python
"""Save QR codes for testing."""

import requests

# Get the QR PNG
r = requests.get('http://127.0.0.1:5000/qr.png?text=known')

# Save it
with open('test_qr.png', 'wb') as f:
    f.write(r.content)
    
print("Saved test_qr.png")

# Try with different text lengths
for text in ['hi', 'known', 'test123']:
    r = requests.get(f'http://127.0.0.1:5000/qr.png?text={text}')
    with open(f'qr_{text}.png', 'wb') as f:
        f.write(r.content)
    print(f"Saved qr_{text}.png ({len(text)} chars)")
