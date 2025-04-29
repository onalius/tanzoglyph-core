"""
Projection Character Mapping Module
=================================

This module defines mappings between projection/style characteristics and Block Drawing characters.
It provides functions for encoding projection values to characters and decoding
characters back to projection attributes and values.
"""

from typing import Dict, Tuple, Optional
import math

# Map of projection/style attributes to Block Drawing characters
PROJECTION_MAP = {
    # Form/presence attributes
    "presence": "█",  # Full block
    "density": "▓",  # Dark shade
    "lightness": "▒",  # Medium shade
    "ethereality": "░",  # Light shade
    
    # Structural attributes
    "stability": "▀",  # Upper half block
    "fluidity": "▄",  # Lower half block
    "symmetry": "▌",  # Left half block
    "asymmetry": "▐",  # Right half block
    
    # Dynamic attributes
    "force": "▬",  # Full block horizontal
    "flow": "▮",  # Full block vertical
    "rhythm": "▭",  # White rectangle
    "harmony": "▯",  # White vertical rectangle
    
    # Geometric attributes
    "linearity": "▁",  # Lower one eighth block
    "circularity": "▂",  # Lower one quarter block
    "angularity": "▃",  # Lower three eighths block
    "integration": "▅",  # Lower five eighths block
    
    # Compositional attributes
    "balance": "▆",  # Lower three quarters block
    "contrast": "▇",  # Lower seven eighths block
    "complexity": "◆",  # Black diamond
    "simplicity": "◇",  # White diamond
    
    # Expressive attributes
    "boldness": "■",  # Black square
    "subtlety": "□",  # White square
    "sharpness": "▲",  # Black up-pointing triangle
    "softness": "△",  # White up-pointing triangle
    
    # Tonal attributes
    "intensity": "▼",  # Black down-pointing triangle
    "mellowness": "▽",  # White down-pointing triangle
    "brightness": "◘",  # Inverse bullet
    "shadow": "◙",  # Inverse white circle
    
    # Interactive attributes
    "openness": "▢",  # White square with rounded corners
    "protection": "▣",  # White square containing black small square
    "extension": "▤",  # Square with horizontal fill
    "reception": "▥",  # Square with vertical fill
    
    # Detail attributes
    "precision": "▦",  # Square with orthogonal crosshatch fill
    "ambiguity": "▧",  # Square with upper left to lower right fill
    "definition": "▨",  # Square with upper right to lower left fill
    "diffusion": "▩"   # Square with diagonal crosshatch fill
}

# Reverse mapping for decoding
REVERSE_MAP = {char: attr for attr, char in PROJECTION_MAP.items()}

def normalize_projection_name(name: str) -> str:
    """
    Normalize a projection/style attribute name to match the keys in the map.
    
    Args:
        name: The raw attribute name
        
    Returns:
        Normalized name that can be looked up in the projection map
    """
    # Convert to lowercase and strip spaces
    normalized = name.lower().strip()
    
    # Handle common variations
    replacements = {
        "weight": "presence",
        "heaviness": "density",
        "light": "lightness",
        "ethereal": "ethereality",
        "solid": "stability",
        "fluid": "fluidity",
        "balanced": "balance",
        "symmetric": "symmetry",
        "asymmetric": "asymmetry",
        "forceful": "force",
        "flowing": "flow",
        "rhythmic": "rhythm",
        "harmonious": "harmony",
        "linear": "linearity",
        "circular": "circularity",
        "angular": "angularity",
        "integrated": "integration",
        "balanced": "balance",
        "contrasting": "contrast",
        "complex": "complexity",
        "simple": "simplicity",
        "bold": "boldness",
        "subtle": "subtlety",
        "sharp": "sharpness",
        "soft": "softness",
        "intense": "intensity",
        "mellow": "mellowness",
        "bright": "brightness",
        "shadowed": "shadow",
        "open": "openness",
        "protective": "protection",
        "extended": "extension",
        "receptive": "reception",
        "precise": "precision",
        "ambiguous": "ambiguity",
        "defined": "definition",
        "diffuse": "diffusion"
    }
    
    for key, replacement in replacements.items():
        if normalized == key:
            return replacement
    
    return normalized

def encode_projection_value(attribute: str, value: float) -> str:
    """
    Encode a projection/style attribute value as a Block Drawing character.
    
    Args:
        attribute: The name of the projection/style attribute
        value: Numeric value between 0.0 and 1.0
        
    Returns:
        A Block Drawing character representing the attribute
    """
    normalized = normalize_projection_name(attribute)
    
    # Look for direct match
    if normalized in PROJECTION_MAP:
        return PROJECTION_MAP[normalized]
    
    # Look for partial match
    for key, char in PROJECTION_MAP.items():
        if normalized in key or key in normalized:
            return char
    
    # Default to '█' (presence) for unknown attributes
    return "█"

def encode_projection_descriptor(attribute: str, descriptor: str) -> str:
    """
    Encode a projection/style attribute with a qualitative descriptor as a Block Drawing character.
    
    Args:
        attribute: The name of the projection/style attribute
        descriptor: Qualitative descriptor (e.g., "high", "low")
        
    Returns:
        A Block Drawing character representing the attribute
    """
    # Convert descriptor to numeric value
    value_map = {
        "none": 0.0,
        "minimal": 0.1,
        "very low": 0.2,
        "low": 0.3,
        "below average": 0.4,
        "medium": 0.5,
        "average": 0.5,
        "above average": 0.6,
        "high": 0.7,
        "very high": 0.8,
        "extreme": 0.9,
        "maximum": 1.0
    }
    
    value = value_map.get(descriptor.lower().strip(), 0.5)
    return encode_projection_value(attribute, value)

def decode_projection_char(char: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Decode a Block Drawing character back to a projection/style attribute and value.
    
    Args:
        char: A Block Drawing character representing a projection/style attribute
        
    Returns:
        Tuple of (attribute_name, value), or (None, None) if not decodable
    """
    if not char or len(char) != 1:
        return None, None
    
    # Look up in the reverse mapping
    attribute = REVERSE_MAP.get(char)
    
    if not attribute:
        return None, None
    
    # For now, a standard value of 0.7 is used
    # In a future version, different character variants could encode different values
    value = 0.7
    
    return attribute, value
