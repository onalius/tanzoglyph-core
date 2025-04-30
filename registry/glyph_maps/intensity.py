"""
Intensity Character Mapping Module
===================================

This module defines mappings between intensity levels (0.0-1.0) and Geometric Shape characters.
It provides functions for encoding intensity values to characters and decoding
characters back to intensity values.
"""

from typing import Dict, Optional, Tuple

# Mapping from digits to Geometric Shape characters for intensity representation
# Using filled/partial circles to represent intensity from 0.0 to 0.9
DIGIT_TO_CHAR: Dict[int, str] = {
    0: "○",  # WHITE CIRCLE
    1: "◔",  # CIRCLE WITH UPPER RIGHT QUADRANT
    2: "◑",  # CIRCLE WITH RIGHT HALF
    3: "◕",  # CIRCLE WITH ALL BUT UPPER LEFT QUADRANT
    4: "●",  # BLACK CIRCLE
    5: "◆",  # BLACK DIAMOND
    6: "■",  # BLACK SQUARE
    7: "▲",  # BLACK UP-POINTING TRIANGLE
    8: "◉",  # FISHEYE
    9: "◎",  # BULLSEYE
}

# Decimal point for intensity values
DECIMAL_POINT = "◌"  # DOTTED CIRCLE

# Reverse mapping for decoding
CHAR_TO_DIGIT: Dict[str, int] = {char: digit for digit, char in DIGIT_TO_CHAR.items()}

def encode_intensity(value: float) -> str:
    """
    Encode an intensity value (0.0-1.0) as a sequence of Geometric Shape characters.
    
    Args:
        value: Intensity value between 0.0 and 1.0
        
    Returns:
        A string of Geometric Shape characters representing the intensity
    """
    if value < 0.0 or value > 1.0:
        raise ValueError("Intensity value must be between 0.0 and 1.0")
    
    # Convert to a 2-digit representation (0.0 to 1.0 -> 00 to 10)
    # Special case for 1.0
    if value == 1.0:
        return DIGIT_TO_CHAR[1] + DECIMAL_POINT + DIGIT_TO_CHAR[0]
    
    # For values 0.0 to 0.9
    int_value = int(value * 10)
    whole = int_value // 10
    frac = int_value % 10
    
    # Encode as geometric shapes with a "decimal point"
    return DIGIT_TO_CHAR[whole] + DECIMAL_POINT + DIGIT_TO_CHAR[frac]

def decode_intensity(chars: str) -> Optional[float]:
    """
    Decode a sequence of Geometric Shape characters back to an intensity value.
    
    Args:
        chars: A string of Geometric Shape characters
        
    Returns:
        The intensity value between 0.0 and 1.0, or None if not decodable
    """
    if len(chars) != 3 or chars[1] != DECIMAL_POINT:
        return None
    
    whole_char = chars[0]
    frac_char = chars[2]
    
    if whole_char not in CHAR_TO_DIGIT or frac_char not in CHAR_TO_DIGIT:
        return None
    
    whole = CHAR_TO_DIGIT[whole_char]
    frac = CHAR_TO_DIGIT[frac_char]
    
    # Reconstruct the float value
    return whole / 10 + frac / 100