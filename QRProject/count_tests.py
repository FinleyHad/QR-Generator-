#!/usr/bin/env python
"""Count tests per file."""
import os
import re

test_dir = "tests"
for file in sorted(os.listdir(test_dir)):
    if file.startswith("test_") and file.endswith(".py"):
        path = os.path.join(test_dir, file)
        with open(path) as f:
            content = f.read()
            test_count = len(re.findall(r'^\s*def test_', content, re.MULTILINE))
            lines = len(content.split('\n'))
            print(f"{file:45} {test_count:3} tests  {lines:4} lines")
