# TanzoGlyph Encoding System

A robust, open-standard system for encoding AI personality profiles ("souls") into symbolic Unicode character streams. TanzoGlyph provides a portable, chain-agnostic framework for representing, storing, and verifying AI identities.

```
ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂
```
*Example TanzoGlyph encoding representing an AI personality profile*

## Overview

TanzoGlyph is a novel encoding system designed specifically for representing AI personality profiles in a compact, visually distinctive format. It maps different aspects of a personality to specific Unicode character sets, creating a unique "glyph" that serves as a visual signature.

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [tomotanzo-core](https://github.com/onalius/tomotanzo-core) - For the profile format and structure
- The Unicode Consortium - For the diverse character sets that make TanzoGlyph possible

