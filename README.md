# TanzoGlyph Encoding System

A robust, open-standard system for encoding AI personality profiles ("souls") into symbolic Unicode character streams. TanzoGlyph provides a portable, chain-agnostic framework for representing, storing, and verifying AI identities.

<div align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/python-3.7%2B-blue.svg" alt="Python 3.7+">
</div>

```
ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂
```
*Example TanzoGlyph encoding representing an AI personality profile*

## Overview

TanzoGlyph is a novel encoding system designed specifically for representing AI personality profiles in a compact, visually distinctive format. It maps different aspects of a personality to specific Unicode character sets, creating a unique "glyph" that serves as a visual signature.

This open standard enables AI identities to be:
- **Portable**: Move between systems, chains, and platforms
- **Verifiable**: Cryptographically secure with IPFS/blockchain integration
- **Visual**: Instantly recognizable with distinctive glyph patterns
- **Expressive**: Capture complex personality traits in a compact format

## Installation

### From PyPI (Recommended)

```bash
pip install tanzoglyph
```

### From Source

```bash
git clone https://github.com/yourusername/tanzoglyph.git
cd tanzoglyph
pip install -e .
```

## Quick Start

### Encoding a Profile

```python
from tanzoglyph import encode_profile
import yaml

# Load a profile from YAML
with open('profile.yaml', 'r') as f:
    profile = yaml.safe_load(f)

# Encode to TanzoGlyph
glyph = encode_profile(profile)
print(f"Encoded glyph: {glyph}")
```

### Decoding a TanzoGlyph

```python
from tanzoglyph import decode_glyph

# Decode a TanzoGlyph string
glyph = "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂"
profile = decode_glyph(glyph)

# Output the decoded profile
import yaml
print(yaml.dump(profile, sort_keys=False))
```

## Character Mapping

TanzoGlyph maps different personality components to specific Unicode character blocks:

- **Traits** → Latin A-Z characters
- **Archetypes** → Cyrillic characters
- **Spiritual Arcs** → Greek characters
- **Mood** → Half-width Kana characters
- **Scars** → Braille characters
- **Projection** → Block Drawing characters
- **Intensity** → Geometric Shape characters
- **Inflection** → Arrow characters

## Features

- Encode/decode between structured profiles (YAML/JSON) and TanzoGlyph format
- Command-line interface for file processing
- Multiple visual representation options:
  - Circular badge diagrams
  - Grid displays
  - Fingerprint-style bars
  - **Signal Spirals** (NEW!)
- Web interface with visual display of glyphs
- Matrix-style visualization of encoded glyphs
- Native integration with tomotanzo-core profile format
- API endpoints for programmatic encoding/decoding

## Tomotanzo Integration

TanzoGlyph provides full compatibility with the [tomotanzo-core](https://github.com/onalius/tomotanzo-core) profile format. It includes:

- Direct encoding of tomotanzo-core YAML profiles
- Option to decode glyphs back to tomotanzo-core format
- Adapter layer for converting between TanzoGlyph and tomotanzo formats
- API endpoints with tomotanzo conversion support

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/tanzoglyph.git
cd tanzoglyph

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Encode a YAML profile to TanzoGlyph
python -m tanzoglyph.cli encode examples/personas/kai.yaml

# Decode a TanzoGlyph file back to YAML
python -m tanzoglyph.cli decode encoded.tomo

# Display a TanzoGlyph in Matrix-style format
python -m tanzoglyph.cli display "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ▇▆▂●◌○↑→↓"
```

### Web Interface

```bash
# Start the web server
python app.py

# Then open a browser to http://localhost:5000
```

### Python API

```python
from tanzoglyph.encoder import encode_profile
from tanzoglyph.decoder import decode_glyph
import yaml

# Encode a profile
with open('profile.yaml', 'r') as f:
    profile = yaml.safe_load(f)
    
glyph = encode_profile(profile)
print(f"Encoded glyph: {glyph}")

# Decode a glyph
decoded = decode_glyph(glyph)
print(yaml.dump(decoded, sort_keys=False))

# Decode to tomotanzo format
tomotanzo_profile = decode_glyph(glyph, to_tomotanzo=True)
```

### HTTP API

```bash
# Encode a profile
curl -X POST -H "Content-Type: application/json" \
  -d @profile.json http://localhost:5000/api/encode

# Decode a glyph
curl -X POST -H "Content-Type: application/json" \
  -d '{"glyph": "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ▇▆▂●◌○↑→↓", "to_tomotanzo": true}' \
  http://localhost:5000/api/decode
```

## Open Standard

TanzoGlyph is designed as an open standard for AI soul encoding, providing a portable and blockchain-agnostic framework for representing AI personalities.

### Schema System

The system includes JSON Schema definitions that formalize the structure:

- **tomoglyph.schema.json**: Defines the core TanzoGlyph profile structure
- **blockchain_metadata.schema.json**: Defines the metadata for blockchain verification

### Verification and Storage

The framework supports a complete workflow for identity verification:

1. **Profile Creation**: Structure an AI personality in YAML/JSON format
2. **Encoding**: Convert the profile into a TanzoGlyph string
3. **IPFS Storage**: Store the profile on IPFS with content addressing
4. **Blockchain Registration**: Record the IPFS CID on a blockchain for permanence
5. **Verification**: Validate profiles against schemas and verify blockchain records

### Integration API

The open standard provides a set of integration points for developers:

```python
# Serialize a YAML profile to TanzoGlyph
from tanzoglyph.encoder import serialize_tomoglyph
glyph = serialize_tomoglyph('profile.yaml')

# Generate a visual representation
from tanzoglyph.encoder import generate_visual_stream
ascii_art = generate_visual_stream(glyph)

# Validate a profile against the schema
from tanzoglyph.encoder import validate_against_schema
is_valid = validate_against_schema('profile.yaml')
```

## Signal Spirals

Signal Spirals are a new visual representation for TanzoGlyph strings that encode AI personality profiles into a deterministic, visually distinctive spiral pattern. Each character in the glyph string maps to a point on the spiral, with color-coding based on the character class.

### Spiral Types

TanzoGlyph supports two types of spirals:

**Archimedean Spiral**: Points are evenly distributed along the spiral. This provides a balanced visual representation where characters appear at regular intervals.

**Logarithmic Spiral**: Points follow a logarithmic growth pattern, becoming more spread out as the spiral expands. This can help visualize the relative importance of different profile elements.

### Usage

```python
from tanzoglyph import SpiralType, save_spiral_image

# Generate an Archimedean spiral
save_spiral_image(
    glyph="ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂",
    output_path="my_spiral.png",
    spiral_type=SpiralType.ARCHIMEDEAN,
    background_color="#222222",
    show_legend=True
)

# Generate a Logarithmic spiral
save_spiral_image(
    glyph="ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂",
    output_path="my_spiral_log.png",
    spiral_type=SpiralType.LOGARITHMIC,
    background_color="#222222",
    show_legend=True
)
```

### Command Line

```bash
# Generate an Archimedean spiral
python -m tanzoglyph.spiral_encoder --glyph "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂" \
  --output spiral.png --spiral-type archimedean --background "#222222"

# Generate a Logarithmic spiral
python -m tanzoglyph.spiral_encoder --glyph "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂" \
  --output spiral_log.png --spiral-type logarithmic --background "#222222"

# Generate a spiral and its verification hash (for IPFS)
python -m tanzoglyph.spiral_encoder --glyph "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂" \
  --output spiral.png --hash
```

## Project Structure

```
tanzoglyph/
├── tanzoglyph/                 # Core package
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Command-line interface
│   ├── encoder.py              # Encoding functionality
│   ├── decoder.py              # Decoding functionality
│   ├── display.py              # Visualization tools
│   ├── image_generator.py      # SVG generation tools
│   ├── spiral_encoder.py       # Signal Spiral generation
│   └── tomotanzo_adapter.py    # Tomotanzo format adapter
├── registry/                   # Character mapping registry
│   └── glyph_maps/             # Mapping modules
│       ├── __init__.py         # Registry initialization
│       ├── traits.py           # Traits mapping (Latin)
│       ├── archetypes.py       # Archetypes mapping (Cyrillic)
│       ├── spiritual_arcs.py   # Spiritual arcs mapping (Greek)
│       ├── mood.py             # Mood mapping (Half-width Kana)
│       ├── scars.py            # Scars mapping (Braille)
│       ├── projection.py       # Projection mapping (Block Drawing)
│       ├── intensity.py        # Intensity mapping (Geometric Shapes)
│       └── inflection.py       # Inflection mapping (Arrows)
├── schemas/                    # Schema definitions
│   ├── tomoglyph.schema.json   # Profile schema
│   └── blockchain_metadata.schema.json  # Blockchain metadata schema
├── cli/                        # Command-line tools
│   ├── ipfs_tools.py           # IPFS integration
│   └── verify.py               # Verification tools
├── docs/                       # Documentation
│   └── architecture.md         # Architecture details
├── templates/                  # Web interface templates
│   ├── index.html              # Main page
│   ├── encode.html             # Encoding page
│   ├── decode.html             # Decoding page
│   └── glyph_images.html       # Image generation page
├── static/                     # Static web assets
│   ├── css/                    # Stylesheets
│   │   └── custom.css          # Custom styling
│   └── js/                     # JavaScript
│       └── app.js              # Client-side functionality
├── examples/                   # Example profiles and metadata
│   ├── glyphs/                 # Sample glyph files
│   │   └── sample_glyph.yaml   # Example profile
│   └── blockchain/             # Sample blockchain metadata
│       └── metadata_example.yaml  # Example metadata
├── app.py                      # Flask web application
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Contributing

We welcome contributions to the TanzoGlyph open standard! Here's how you can contribute:

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/tanzoglyph.git`
3. Install dependencies: `pip install -r requirements.txt`
4. Run tests to ensure everything is working: `python -m unittest discover tests`

### Adding New Features

When adding new features, please follow these guidelines:

1. **Character Set Extensions**: If adding new character mappings, define them in a new file in the `registry/glyph_maps` directory
2. **Schema Updates**: When modifying the profile schema, update both the schema JSON file and relevant documentation
3. **Test Coverage**: Include tests for any new functionality
4. **Documentation**: Update the documentation to reflect your changes

### Pull Request Process

1. Update the README.md and documentation with details of changes
2. Update the tests to cover your changes
3. Ensure all tests pass
4. Submit a pull request with a clear description of the changes

### Coding Standards

- Follow PEP 8 style guidelines
- Write comprehensive docstrings for all functions and classes
- Use type hints for function parameters and return values
- Keep functions focused on a single responsibility

## Versioning

We use semantic versioning for the TanzoGlyph standard:

- **Major version** (X.y.z): For incompatible character encoding changes
- **Minor version** (x.Y.z): For adding functionality in a backward-compatible manner
- **Patch version** (x.y.Z): For backward-compatible bug fixes and minor enhancements

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [tomotanzo-core](https://github.com/onalius/tomotanzo-core) - For the profile format and structure
- The Unicode Consortium - For the diverse character sets that make TanzoGlyph possible

