# TanzoGlyph Encoding System

A Python-based system that translates structured AI personality profiles into symbolic Unicode character streams.

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

## Project Structure

```
tanzoglyph/
├── tanzoglyph/                 # Core package
│   ├── __init__.py             # Package initialization
│   ├── cli.py                  # Command-line interface
│   ├── encoder.py              # Encoding functionality
│   ├── decoder.py              # Decoding functionality
│   ├── display.py              # Visualization tools
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
├── templates/                  # Web interface templates
│   ├── index.html              # Main page
│   ├── encode.html             # Encoding page
│   └── decode.html             # Decoding page
├── static/                     # Static web assets
│   ├── css/                    # Stylesheets
│   │   └── custom.css          # Custom styling
│   └── js/                     # JavaScript
│       └── app.js              # Client-side functionality
├── examples/                   # Example profiles
│   └── personas/               # Sample personas
│       └── kai.yaml            # Example profile
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

