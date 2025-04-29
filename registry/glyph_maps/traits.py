"""
Trait Character Mapping Module
=============================

This module defines mappings between personality traits and Latin A-Z characters.
It provides functions for encoding trait values to characters and decoding
characters back to trait names and values.
"""

from typing import Dict, Tuple, Optional

# Trait categories and their corresponding character ranges
TRAIT_CATEGORIES = {
    # Core personality traits (Big Five / OCEAN)
    "openness": "A",
    "conscientiousness": "B",
    "extraversion": "C", 
    "agreeableness": "D",
    "neuroticism": "E",
    
    # Secondary traits
    "creativity": "F",
    "curiosity": "G",
    "adaptability": "H",
    "resilience": "I",
    "empathy": "J",
    "confidence": "K",
    "patience": "L",
    "ambition": "M",
    "playfulness": "N",
    "discipline": "O",
    
    # Cognitive traits
    "logic": "P",
    "intuition": "Q",
    "perception": "R",
    "memory": "S",
    "focus": "T",
    
    # Communication traits
    "expressiveness": "U",
    "listening": "V",
    "articulation": "W",
    "persuasiveness": "X",
    "humor": "Y",
    "eloquence": "Z"
}

# Map of qualitative descriptors to numeric values
TRAIT_DESCRIPTORS = {
    "none": 0.0,
    "minimal": 0.1,
    "very low": 0.2,
    "low": 0.3,
    "below average": 0.4,
    "average": 0.5,
    "above average": 0.6,
    "high": 0.7,
    "very high": 0.8,
    "exceptional": 0.9,
    "maximum": 1.0
}

def get_trait_letter(trait_name: str) -> str:
    """
    Get the base letter for a trait name.
    
    Args:
        trait_name: The name of the trait
        
    Returns:
        The Latin letter assigned to this trait, or 'X' if not found
    """
    # Normalize trait name
    normalized = trait_name.lower().strip()
    
    # Look for exact match
    if normalized in TRAIT_CATEGORIES:
        return TRAIT_CATEGORIES[normalized]
    
    # Look for partial match
    for category, letter in TRAIT_CATEGORIES.items():
        if normalized in category or category in normalized:
            return letter
    
    # Default to 'X' for unknown traits
    return "X"

def encode_trait_value(trait_name: str, value: float) -> str:
    """
    Encode a trait value as a Latin character.
    
    Args:
        trait_name: The name of the trait
        value: Numeric value between 0.0 and 1.0
        
    Returns:
        A Latin character representing the trait and its value
    """
    base_letter = get_trait_letter(trait_name)
    
    # Determine case based on value (uppercase for higher values)
    if value >= 0.5:
        # Scale 0.5-1.0 to uppercase letter
        return base_letter
    else:
        # Scale 0.0-0.5 to lowercase letter
        return base_letter.lower()

def encode_trait_descriptor(trait_name: str, descriptor: str) -> str:
    """
    Encode a trait with a qualitative descriptor as a Latin character.
    
    Args:
        trait_name: The name of the trait
        descriptor: Qualitative descriptor (e.g., "high", "low")
        
    Returns:
        A Latin character representing the trait and its descriptor
    """
    # Convert descriptor to numeric value
    value = TRAIT_DESCRIPTORS.get(descriptor.lower().strip(), 0.5)
    return encode_trait_value(trait_name, value)

def decode_trait_char(char: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Decode a Latin character back to a trait name and value.
    
    Args:
        char: A Latin character representing a trait
        
    Returns:
        Tuple of (trait_name, value), or (None, None) if not decodable
    """
    if not char or len(char) != 1 or not char.isalpha():
        return None, None
    
    # Get the uppercase version for lookup
    upper_char = char.upper()
    
    # Find the trait category for this letter
    trait_name = None
    for category, letter in TRAIT_CATEGORIES.items():
        if letter == upper_char:
            trait_name = category
            break
    
    if not trait_name:
        return None, None
    
    # Determine value based on case
    value = 0.7 if char.isupper() else 0.3
    
    return trait_name, value
