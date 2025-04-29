"""
Archetypes Character Mapping Module
==================================

This module defines mappings between personality archetypes and Cyrillic characters.
It provides functions for encoding archetype names to characters and decoding
characters back to archetype names.
"""

from typing import Dict, Optional

# Map of archetypal categories to Cyrillic characters
ARCHETYPE_MAP = {
    # Jungian archetypes
    "hero": "А",  # А (Cyrillic A)
    "mentor": "Б",  # Б
    "threshold_guardian": "В",  # В
    "herald": "Г",  # Г
    "shapeshifter": "Д",  # Д
    "shadow": "Е",  # Е
    "trickster": "Ж",  # Ж
    "ally": "З",  # З
    
    # Common character archetypes
    "creator": "И",  # И
    "explorer": "Й",  # Й
    "caregiver": "К",  # К
    "ruler": "Л",  # Л
    "jester": "М",  # М
    "everyman": "Н",  # Н
    "innocent": "О",  # О
    "sage": "П",  # П
    
    # Additional archetypes
    "warrior": "Р",  # Р
    "magician": "С",  # С
    "lover": "Т",  # Т
    "rebel": "У",  # У
    "orphan": "Ф",  # Ф
    "seeker": "Х",  # Х
    "destroyer": "Ц",  # Ц
    "fool": "Ч",  # Ч
    "mystic": "Ш",  # Ш
    "wanderer": "Щ",  # Щ
    "protector": "Ъ",  # Ъ
    "artist": "Ы",  # Ы
    "judge": "Ь",  # Ь
    "healer": "Э",  # Э
    "teacher": "Ю",  # Ю
    "visionary": "Я"   # Я
}

# Lowercase variations can be used for subtypes or less dominant expressions
SUBTYPE_MAP = {archetype.lower(): char.lower() for archetype, char in ARCHETYPE_MAP.items()}

# Combined map for both main types and subtypes
COMBINED_MAP = {**ARCHETYPE_MAP, **SUBTYPE_MAP}

# Reverse mapping for decoding
REVERSE_MAP = {char: archetype for archetype, char in ARCHETYPE_MAP.items()}
REVERSE_SUBTYPE_MAP = {char.lower(): archetype for archetype, char in ARCHETYPE_MAP.items()}
COMBINED_REVERSE_MAP = {**REVERSE_MAP, **REVERSE_SUBTYPE_MAP}

def normalize_archetype_name(name: str) -> str:
    """
    Normalize an archetype name to match the keys in the map.
    
    Args:
        name: The raw archetype name
        
    Returns:
        Normalized name that can be looked up in the archetype map
    """
    # Convert to lowercase and replace spaces with underscores
    normalized = name.lower().strip().replace(' ', '_')
    
    # Handle common variations
    replacements = {
        "guardian": "threshold_guardian",
        "guide": "mentor",
        "adversary": "shadow",
        "ordinary": "everyman",
        "outlaw": "rebel",
        "regular_person": "everyman"
    }
    
    for key, replacement in replacements.items():
        if normalized == key or normalized.endswith(f"_{key}"):
            return replacement
    
    return normalized

def encode_archetype(archetype: str) -> str:
    """
    Encode an archetype name as a Cyrillic character.
    
    Args:
        archetype: The name of the archetype
        
    Returns:
        A Cyrillic character representing the archetype
    """
    normalized = normalize_archetype_name(archetype)
    
    # Look for direct match
    if normalized in COMBINED_MAP:
        return COMBINED_MAP[normalized]
    
    # Look for partial match
    for key, char in COMBINED_MAP.items():
        if normalized in key or key in normalized:
            return char
    
    # Default to 'Я' (visionary) for unknown archetypes
    return "Я"

def decode_archetype_char(char: str) -> Optional[str]:
    """
    Decode a Cyrillic character back to an archetype name.
    
    Args:
        char: A Cyrillic character representing an archetype
        
    Returns:
        The archetype name, or None if the character is not recognized
    """
    if not char or len(char) != 1:
        return None
    
    # Look up in the reverse mapping
    return COMBINED_REVERSE_MAP.get(char)
