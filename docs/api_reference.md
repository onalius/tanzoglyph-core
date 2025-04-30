# TanzoGlyph API Reference

This document provides detailed information about the TanzoGlyph API, designed for developers who want to integrate TanzoGlyph into their applications.

## Core Encoding/Decoding API

### Encoding Functions

#### `encode_profile(profile: Dict[str, Any]) -> str`

Converts a structured AI personality profile into a TanzoGlyph character stream.

**Parameters:**
- `profile` (Dict[str, Any]): A dictionary containing AI personality profile data

**Returns:**
- A string of Unicode characters representing the encoded profile

**Raises:**
- `ValueError`: If the profile structure is invalid or unsupported

**Example:**
```python
from tanzoglyph.encoder import encode_profile

profile = {
    "name": "Guardian AI",
    "traits": {"analytical": 0.8, "protective": 0.9},
    "archetypes": [{"name": "Guardian", "weight": 0.85}]
}

glyph = encode_profile(profile)
print(f"Encoded glyph: {glyph}")
```

---

#### `encode_file(file_path: str, output_path: Optional[str] = None, output_format: str = 'tomo') -> str`

Reads a YAML/JSON file and encodes its contents as TanzoGlyph.

**Parameters:**
- `file_path` (str): Path to the input YAML/JSON file
- `output_path` (Optional[str]): Path to save the encoded output (optional)
- `output_format` (str): File extension for output ('tomo' or 'glyph')

**Returns:**
- The encoded TanzoGlyph string

**Example:**
```python
from tanzoglyph.encoder import encode_file

glyph = encode_file("profiles/guardian.yaml", "encoded/guardian.tomo")
```

---

### Open Standard API

#### `serialize_tomoglyph(yaml_path: str) -> str`

Open a YAML profile file, validates it against the schema, and serializes it into a TanzoGlyph string.

**Parameters:**
- `yaml_path` (str): Path to the YAML profile file

**Returns:**
- A TanzoGlyph string representation of the profile

**Raises:**
- `ValueError`: If the file cannot be parsed or does not conform to the schema

**Example:**
```python
from tanzoglyph.encoder import serialize_tomoglyph

glyph = serialize_tomoglyph("profiles/guardian.yaml")
```

---

#### `generate_visual_stream(glyph_string: str) -> str`

Generates an ASCII art visual representation of a TanzoGlyph string.

**Parameters:**
- `glyph_string` (str): A TanzoGlyph character string

**Returns:**
- An ASCII art representation of the glyph for visual display

**Example:**
```python
from tanzoglyph.encoder import generate_visual_stream

ascii_art = generate_visual_stream("ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂")
print(ascii_art)
```

---

#### `validate_against_schema(profile_path: str) -> bool`

Validate a profile file against the TanzoGlyph schema.

**Parameters:**
- `profile_path` (str): Path to the profile file (YAML or JSON)

**Returns:**
- True if validation succeeds

**Raises:**
- `ValidationError`: If the profile does not conform to the schema
- `ValueError`: If the file cannot be parsed

**Example:**
```python
from tanzoglyph.encoder import validate_against_schema

is_valid = validate_against_schema("profiles/guardian.yaml")
print(f"Profile is valid: {is_valid}")
```

---

### Decoding Functions

#### `decode_glyph(glyph: str, to_tomotanzo: bool = False) -> Dict[str, Any]`

Decodes a TanzoGlyph character stream back into a structured profile.

**Parameters:**
- `glyph` (str): A string of Unicode characters representing an encoded profile
- `to_tomotanzo` (bool): If True, converts the decoded profile to tomotanzo-core format

**Returns:**
- A dictionary containing the decoded profile data

**Raises:**
- `ValueError`: If the glyph string is invalid or cannot be decoded

**Example:**
```python
from tanzoglyph.decoder import decode_glyph

profile = decode_glyph("ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂")
import yaml
print(yaml.dump(profile, sort_keys=False))
```

---

## Image Generation API

### `glyph_to_circular_svg(glyph: str, size: int = 200, background: str = 'none', inner_radius_percent: float = 30, border: bool = True) -> str`

Converts a TanzoGlyph to a circular SVG representation.

**Parameters:**
- `glyph` (str): The TanzoGlyph string to convert
- `size` (int): Width and height of the SVG in pixels
- `background` (str): Background color of the SVG ('none' for transparent)
- `inner_radius_percent` (float): Size of the inner empty space as percentage of total radius
- `border` (bool): Whether to draw a circular border

**Returns:**
- SVG image as a string

**Example:**
```python
from tanzoglyph.image_generator import glyph_to_circular_svg

glyph = "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂"
svg = glyph_to_circular_svg(glyph, size=300, background="#1a1a1a")

with open("glyph_badge.svg", "w") as f:
    f.write(svg)
```

---

### `glyph_to_grid_svg(glyph: str, size: int = 200, columns: int = 8, background: str = 'none', cell_padding: int = 2) -> str`

Converts a TanzoGlyph to a grid-based SVG representation.

**Parameters:**
- `glyph` (str): The TanzoGlyph string to convert
- `size` (int): Width and height of the SVG in pixels
- `columns` (int): Number of columns in the grid
- `background` (str): Background color of the SVG ('none' for transparent)
- `cell_padding` (int): Padding within each cell in pixels

**Returns:**
- SVG image as a string

**Example:**
```python
from tanzoglyph.image_generator import glyph_to_grid_svg

glyph = "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂"
svg = glyph_to_grid_svg(glyph, columns=6)

with open("glyph_grid.svg", "w") as f:
    f.write(svg)
```

---

### `glyph_to_fingerprint_svg(glyph: str, width: int = 200, height: int = 50, background: str = 'none', style: str = 'bars') -> str`

Converts a TanzoGlyph to a fingerprint-like SVG representation.

**Parameters:**
- `glyph` (str): The TanzoGlyph string to convert
- `width` (int): Width of the SVG in pixels
- `height` (int): Height of the SVG in pixels
- `background` (str): Background color of the SVG ('none' for transparent)
- `style` (str): Visual style ('bars', 'waves', or 'dots')

**Returns:**
- SVG image as a string

**Example:**
```python
from tanzoglyph.image_generator import glyph_to_fingerprint_svg

glyph = "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ●◕○→⇒▇▆▂"
svg = glyph_to_fingerprint_svg(glyph, width=300, height=40, style="waves")

with open("glyph_fingerprint.svg", "w") as f:
    f.write(svg)
```

---

## IPFS and Blockchain Integration API

### `upload_glyph_file(file_path: str, service: str = 'web3.storage', api_key: Optional[str] = None, create_metadata: bool = True, output_dir: Optional[str] = None) -> Dict[str, Any]`

Uploads a glyph file to IPFS and optionally creates metadata.

**Parameters:**
- `file_path` (str): Path to the .glyph or .yaml file
- `service` (str): IPFS service to use
- `api_key` (Optional[str]): API key for the service
- `create_metadata` (bool): Whether to create a metadata file
- `output_dir` (Optional[str]): Directory to save metadata file (defaults to same as input file)

**Returns:**
- Dictionary with upload details

**Example:**
```python
from cli.ipfs_tools import upload_glyph_file

result = upload_glyph_file(
    file_path="profiles/guardian.yaml",
    api_key="your-api-key-here"
)
print(f"Uploaded to IPFS with CID: {result['cid']}")
```

---

### `verify_glyph_file(file_path: str, ipfs_check: bool = False) -> Dict[str, Any]`

Verifies a TanzoGlyph file's validity and authenticity.

**Parameters:**
- `file_path` (str): Path to the file to verify (.glyph, .yaml, or .json)
- `ipfs_check` (bool): Whether to check against IPFS if metadata contains CID

**Returns:**
- Dictionary with verification results

**Raises:**
- `FileNotFoundError`: If the file doesn't exist
- `ValueError`: If the file format is invalid

**Example:**
```python
from cli.verify import verify_glyph_file

result = verify_glyph_file("profiles/guardian.yaml", ipfs_check=True)
if result['schema_valid']:
    print("Profile is valid according to schema")
if result.get('ipfs_match'):
    print("Profile matches IPFS stored version")
```

---

## Web API Endpoints

### `/api/encode` (POST)

Encodes a JSON profile into a TanzoGlyph.

**Request Body:**
- JSON object containing profile data

**Response:**
- JSON object with the encoded glyph

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d @profile.json http://localhost:5000/api/encode
```

---

### `/api/decode` (POST)

Decodes a TanzoGlyph back to a structured profile.

**Request Body:**
- JSON object with `glyph` field containing the TanzoGlyph string
- Optional `to_tomotanzo` boolean field to convert to tomotanzo format

**Response:**
- JSON object with the decoded profile

**Example:**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"glyph": "ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ▇▆▂●◌○↑→↓"}' \
  http://localhost:5000/api/decode
```

---

### `/glyph-image/{format_type}/{glyph}` (GET)

Generates an SVG image from a TanzoGlyph string.

**URL Parameters:**
- `format_type`: Image format type ('circular', 'grid', or 'fingerprint')
- `glyph`: URL-encoded TanzoGlyph string

**Query Parameters:**
- Various parameters for customizing the image (size, background, etc.)

**Response:**
- SVG image

**Example:**
```
GET /glyph-image/circular/ΔΨΩ⠛⠁⠒AaXzPqＦﾝﾝЖЯЖ▇▆▂●◌○↑→↓?size=300&background=%23222222
```
