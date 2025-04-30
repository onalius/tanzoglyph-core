"""
Inflection Character Mapping Module
===================================

This module defines mappings between intensity inflection patterns and Arrow characters.
It provides functions for encoding inflection states to characters and decoding
characters back to inflection patterns.
"""

from typing import Dict, Optional, Tuple

# Mapping from inflection patterns to Arrow characters
INFLECTION_TO_CHAR: Dict[str, str] = {
    "rising_fast": "⇑",    # UPWARDS DOUBLE ARROW
    "rising": "↑",         # UPWARDS ARROW
    "rising_slow": "↗",    # NORTH EAST ARROW
    "steady": "→",         # RIGHTWARDS ARROW
    "falling_slow": "↘",   # SOUTH EAST ARROW
    "falling": "↓",        # DOWNWARDS ARROW
    "falling_fast": "⇓",   # DOWNWARDS DOUBLE ARROW
    "oscillating": "↔",    # LEFT RIGHT ARROW
    "spiking": "⤊",        # UPWARDS ARROW WITH TIP RIGHTWARDS
    "dipping": "⤋",        # DOWNWARDS ARROW WITH TIP RIGHTWARDS
    "converging": "⇥",     # RIGHTWARDS ARROW TO BAR
    "diverging": "⇤",      # LEFTWARDS ARROW TO BAR
}

# Reverse mapping for decoding
CHAR_TO_INFLECTION: Dict[str, str] = {char: name for name, char in INFLECTION_TO_CHAR.items()}

def normalize_inflection_name(name: str) -> str:
    """
    Normalize an inflection pattern name to match the keys in the map.
    
    Args:
        name: The raw inflection pattern name
        
    Returns:
        Normalized name that can be looked up in the inflection map
    """
    name = name.lower().replace(" ", "_").replace("-", "_")
    return name

def encode_inflection(inflection: str) -> str:
    """
    Encode an inflection pattern as an Arrow character.
    
    Args:
        inflection: The name of the inflection pattern
        
    Returns:
        An Arrow character representing the inflection pattern
    """
    normalized = normalize_inflection_name(inflection)
    if normalized in INFLECTION_TO_CHAR:
        return INFLECTION_TO_CHAR[normalized]
    
    # Default to steady if not recognized
    return INFLECTION_TO_CHAR["steady"]

def decode_inflection_char(char: str) -> Optional[str]:
    """
    Decode an Arrow character back to an inflection pattern name.
    
    Args:
        char: An Arrow character representing an inflection pattern
        
    Returns:
        The inflection pattern name, or None if the character is not recognized
    """
    return CHAR_TO_INFLECTION.get(char)