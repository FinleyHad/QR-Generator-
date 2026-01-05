# Individual Contribution - Finley
## Masking Module & Team Leadership

### Team Coordination and Project Scaffolding

As team coordinator, I established the project foundation by creating skeleton files for all four modules before implementation began. Using GitHub Copilot, I explored QR code architecture—understanding how data flows from encoding through error correction to matrix generation and masking. This pre-implementation research allowed me to design clean interfaces between modules and provide each team member with template files containing function signatures, detailed docstrings, and TODO comments. This scaffolding approach ensured seamless integration and gave the team a clear implementation roadmap. I also used Copilot to help structure this documentation and articulate my contributions clearly.

### Masking Module Implementation

I implemented the complete masking module across three files:

- **`mask0.py`** - Applies the checkerboard mask pattern using `(row + col) % 2 == 0`, carefully preserving reserved areas
- **`format_info.py`** - Implements BCH error correction through polynomial division in Galois Field GF(2), shifting the generator polynomial and XORing to produce 10-bit error correction codes from 5-bit data inputs
- **`finalize.py`** - Orchestrates the complete finalization: applying masks, computing format bits with correct ECC levels and mask IDs, writing these bits to both primary and secondary matrix locations, and normalizing output to binary

Beyond my module, I supported teammates with integration debugging—tracing bit-ordering issues in encoding and boundary conditions in Reed-Solomon implementations. I also established the testing framework and ensured our web interface demonstrated all components working together, providing visual validation that our QR codes scan correctly.
