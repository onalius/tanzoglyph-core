"""
TanzoGlyph Encoding System
==========================

This package provides tools for encoding structured AI personality profiles
into symbolic Unicode character streams called TanzoGlyph, and decoding them
back to their original structured format.

The encoding system maps various profile elements to different Unicode 
character sets:
- traits → Latin A-Z
- archetypes → Cyrillic
- spiritual arcs → Greek
- mood profile → Half-width Kana
- scars → Braille
- projection/style → Block Drawing
- intensity → Geometric Shapes
- inflection → Arrows

This allows for compact, visually distinctive representation of complex
AI personality profiles, providing a portable, chain-agnostic framework 
for representing AI identity and personality structures.
"""

__version__ = '1.0.0'
__author__ = 'TanzoGlyph Team'
__license__ = 'MIT'

# Core functions for public API
from .encoder import (
    encode_profile,
    encode_file,
    serialize_tomoglyph,
    validate_against_schema,
    generate_visual_stream
)

from .decoder import (
    decode_glyph,
    decode_file
)

from .image_generator import (
    glyph_to_circular_svg,
    glyph_to_grid_svg,
    glyph_to_fingerprint_svg,
    save_glyph_svg
)

# For backward compatibility
encode = encode_profile
decode = decode_glyph
