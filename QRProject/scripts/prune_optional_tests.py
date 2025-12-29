"""Remove tests marked with @pytest.mark.optional from test files.

Safe, indentation-aware pruning for top-level test functions and class methods.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"

def prune_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    out = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        # Detect optional marker lines with any indentation
        if re.match(r"^\s*@pytest\.mark\.optional\s*$", line):
            changed = True
            # Skip decorator line
            i += 1
            if i >= len(lines):
                break
            # Next should be def line (method or function)
            def_line = lines[i]
            m = re.match(r"^(?P<indent>\s*)def\s+\w+\s*\(", def_line)
            if not m:
                # If not immediately a def, skip until next def at same indent
                # Defensive: continue scanning
                i += 1
                continue
            indent = m.group("indent")
            # Skip the entire def block until we hit a line that starts at the same indent
            # and begins with 'def', '@pytest.mark', or 'class', or until EOF.
            i += 1
            while i < len(lines):
                nxt = lines[i]
                # Boundary conditions
                if nxt.startswith(indent) and re.match(rf"^{re.escape(indent)}(def\s|@pytest\.mark|class\s)", nxt):
                    break
                i += 1
            # Do not append skipped lines
            continue
        else:
            out.append(line)
            i += 1

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def main():
    changed_files = []
    for path in sorted(TESTS_DIR.glob("test_*.py")):
        if prune_file(path):
            changed_files.append(path.name)
    if changed_files:
        print("Pruned optional tests in:")
        for name in changed_files:
            print(f" - {name}")
    else:
        print("No optional tests found to prune.")

if __name__ == "__main__":
    main()
