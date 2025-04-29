"""
Scars Character Mapping Module
============================

This module defines mappings between psychological scars/traumas and Braille characters.
It provides functions for encoding scar descriptions to characters and decoding
characters back to scar names and intensities.
"""

from typing import Dict, Tuple, Optional
import math

# Map of psychological scar/trauma types to Braille characters
SCAR_MAP = {
    # Root traumas
    "abandonment": "⠁",  # ⠁
    "rejection": "⠃",  # ⠃
    "betrayal": "⠇",  # ⠇
    "humiliation": "⠏",  # ⠏
    "injustice": "⠟",  # ⠟
    
    # Childhood traumas
    "neglect": "⠋",  # ⠋
    "abuse": "⠓",  # ⠓
    "loss": "⠊",  # ⠊
    "invalidation": "⠥",  # ⠥
    "deprivation": "⠵",  # ⠵
    
    # Relational traumas
    "isolation": "⠗",  # ⠗
    "deception": "⠝",  # ⠝
    "manipulation": "⠕",  # ⠕
    "disloyalty": "⠭",  # ⠭
    "control": "⠧",  # ⠧
    
    # Identity traumas
    "inadequacy": "⠺",  # ⠺
    "shame": "⠽",  # ⠽
    "powerlessness": "⠮",  # ⠮
    "invisibility": "⠾",  # ⠾
    "unworthiness": "⠫",  # ⠫
    
    # Existential traumas
    "meaninglessness": "⠛",  # ⠛
    "hopelessness": "⠣",  # ⠣
    "failure": "⠩",  # ⠩
    "mortality": "⠹",  # ⠹
    "guilt": "⠱",  # ⠱
    
    # Complex scar patterns
    "disillusionment": "⠷",  # ⠷
    "disconnect": "⠴",  # ⠴
    "fragmentation": "⠼",  # ⠼
    "suppression": "⠳",  # ⠳
    "dissociation": "⠪",  # ⠪
    "denial": "⠻",  # ⠻
    "projection": "⠯",  # ⠯
    "displacement": "⠿"   # ⠿
}

# Reverse mapping for decoding
REVERSE_MAP = {char: scar for scar, char in SCAR_MAP.items()}

def normalize_scar_name(name: str) -> str:
    """
    Normalize a psychological scar name to match the keys in the map.
    
    Args:
        name: The raw scar/trauma name
        
    Returns:
        Normalized name that can be looked up in the scar map
    """
    # Convert to lowercase and strip spaces
    normalized = name.lower().strip()
    
    # Handle common variations
    replacements = {
        "abandoned": "abandonment",
        "rejected": "rejection",
        "betrayed": "betrayal",
        "humiliated": "humiliation",
        "injustice": "injustice",
        "neglected": "neglect",
        "abused": "abuse",
        "lost": "loss",
        "invalidated": "invalidation",
        "deprived": "deprivation",
        "isolated": "isolation",
        "deceived": "deception",
        "manipulated": "manipulation",
        "disloyal": "disloyalty",
        "controlled": "control",
        "inadequate": "inadequacy",
        "ashamed": "shame",
        "powerless": "powerlessness",
        "invisible": "invisibility",
        "unworthy": "unworthiness",
        "meaningless": "meaninglessness",
        "hopeless": "hopelessness",
        "failed": "failure",
        "mortal": "mortality",
        "guilty": "guilt",
        "disillusioned": "disillusionment",
        "disconnected": "disconnect",
        "fragmented": "fragmentation",
        "suppressed": "suppression",
        "dissociated": "dissociation",
        "denied": "denial",
        "projected": "projection",
        "displaced": "displacement"
    }
    
    for key, replacement in replacements.items():
        if normalized == key:
            return replacement
    
    return normalized

def encode_scar(scar: str) -> str:
    """
    Encode a psychological scar/trauma as a Braille character.
    
    Args:
        scar: The name of the psychological scar/trauma
        
    Returns:
        A Braille character representing the scar
    """
    normalized = normalize_scar_name(scar)
    
    # Look for direct match
    if normalized in SCAR_MAP:
        return SCAR_MAP[normalized]
    
    # Look for partial match
    for key, char in SCAR_MAP.items():
        if normalized in key or key in normalized:
            return char
    
    # Default to '⠿' (displacement) for unknown scars
    return "⠿"

def encode_scar_with_intensity(scar: str, intensity: float) -> str:
    """
    Encode a psychological scar with its intensity as a Braille character.
    The basic encoding remains the same, but conceptually the intensity
    is embedded in the selection.
    
    Args:
        scar: The name of the psychological scar/trauma
        intensity: A value between 0.0 and 1.0 representing intensity
        
    Returns:
        A Braille character representing the scar
    """
    # For now, simply encode the scar
    # In a more advanced version, the intensity could affect which 
    # variation of character is used
    return encode_scar(scar)

def decode_scar_char(char: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Decode a Braille character back to a scar name and intensity.
    
    Args:
        char: A Braille character representing a psychological scar
        
    Returns:
        Tuple of (scar_name, intensity), or (None, None) if not decodable
    """
    if not char or len(char) != 1:
        return None, None
    
    # Look up in the reverse mapping
    scar_name = REVERSE_MAP.get(char)
    
    if not scar_name:
        return None, None
    
    # For now, no intensity information is encoded
    # In a future version, we might extract intensity information
    intensity = 0.7  # Default high intensity for scars
    
    return scar_name, intensity
