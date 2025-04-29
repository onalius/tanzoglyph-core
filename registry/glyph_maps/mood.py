"""
Mood Character Mapping Module
===========================

This module defines mappings between mood states and Half-width Kana characters.
It provides functions for encoding mood states to characters and decoding
characters back to mood states and intensities.
"""

from typing import Dict, Tuple, Optional
import math

# Map of mood states to Half-width Kana characters
MOOD_MAP = {
    # Positive moods
    "joy": "ｱ",  # ｱ (half-width A)
    "excitement": "ｲ",  # ｲ
    "contentment": "ｳ",  # ｳ
    "peacefulness": "ｴ",  # ｴ
    "amusement": "ｵ",  # ｵ
    "happiness": "ｶ",  # ｶ
    "satisfaction": "ｷ",  # ｷ
    "optimism": "ｸ",  # ｸ
    "enthusiasm": "ｹ",  # ｹ
    "love": "ｺ",  # ｺ
    
    # Neutral moods
    "calm": "ｻ",  # ｻ
    "focus": "ｼ",  # ｼ
    "contemplation": "ｽ",  # ｽ
    "curiosity": "ｾ",  # ｾ
    "mindfulness": "ｿ",  # ｿ
    "neutrality": "ﾀ",  # ﾀ
    "alertness": "ﾁ",  # ﾁ
    "reflection": "ﾂ",  # ﾂ
    "poise": "ﾃ",  # ﾃ
    "patience": "ﾄ",  # ﾄ
    
    # Negative moods
    "anxiety": "ﾅ",  # ﾅ
    "sadness": "ﾆ",  # ﾆ
    "frustration": "ﾇ",  # ﾇ
    "anger": "ﾈ",  # ﾈ
    "grief": "ﾉ",  # ﾉ
    "disappointment": "ﾊ",  # ﾊ
    "fear": "ﾋ",  # ﾋ
    "melancholy": "ﾌ",  # ﾌ
    "confusion": "ﾍ",  # ﾍ
    "boredom": "ﾎ",  # ﾎ
    
    # Complex moods
    "nostalgia": "ﾏ",  # ﾏ
    "longing": "ﾐ",  # ﾐ
    "awe": "ﾑ",  # ﾑ
    "wonder": "ﾒ",  # ﾒ
    "anticipation": "ﾓ",  # ﾓ
    "yearning": "ﾔ",  # ﾔ
    "empathy": "ﾕ",  # ﾕ
    "compassion": "ﾖ",  # ﾖ
    "serenity": "ﾗ",  # ﾗ
    "gratitude": "ﾘ",  # ﾘ
    "inspiration": "ﾙ",  # ﾙ
    "determination": "ﾚ",  # ﾚ
    "pride": "ﾛ",  # ﾛ
    "ambivalence": "ﾜ",  # ﾜ
    "surprise": "ﾝ"   # ﾝ
}

# Reverse mapping for decoding
REVERSE_MAP = {char: mood for mood, char in MOOD_MAP.items()}

def normalize_mood_name(name: str) -> str:
    """
    Normalize a mood state name to match the keys in the map.
    
    Args:
        name: The raw mood state name
        
    Returns:
        Normalized name that can be looked up in the mood map
    """
    # Convert to lowercase and strip spaces
    normalized = name.lower().strip()
    
    # Handle common variations
    replacements = {
        "happy": "happiness",
        "joyful": "joy",
        "excited": "excitement",
        "content": "contentment",
        "peaceful": "peacefulness",
        "amused": "amusement",
        "satisfied": "satisfaction",
        "optimistic": "optimism",
        "enthusiastic": "enthusiasm",
        "loving": "love",
        "anxious": "anxiety",
        "sad": "sadness",
        "frustrated": "frustration",
        "angry": "anger",
        "grieving": "grief",
        "disappointed": "disappointment",
        "fearful": "fear",
        "melancholic": "melancholy",
        "confused": "confusion",
        "bored": "boredom",
        "nostalgic": "nostalgia",
        "awed": "awe",
        "wondering": "wonder",
        "anticipating": "anticipation",
        "yearning": "longing",
        "empathetic": "empathy",
        "compassionate": "compassion",
        "serene": "serenity",
        "grateful": "gratitude",
        "inspired": "inspiration",
        "determined": "determination",
        "proud": "pride",
        "ambivalent": "ambivalence",
        "surprised": "surprise"
    }
    
    for key, replacement in replacements.items():
        if normalized == key:
            return replacement
    
    return normalized

def encode_mood_state(mood: str, intensity: float = 1.0) -> str:
    """
    Encode a mood state as a Half-width Kana character.
    
    Args:
        mood: The name of the mood state
        intensity: Optional intensity value (0.0-1.0), defaults to 1.0
        
    Returns:
        A Half-width Kana character representing the mood state
    """
    normalized = normalize_mood_name(mood)
    
    # Look for direct match
    if normalized in MOOD_MAP:
        return MOOD_MAP[normalized]
    
    # Look for partial match
    for key, char in MOOD_MAP.items():
        if normalized in key or key in normalized:
            return char
    
    # Default to 'ﾝ' (surprise) for unknown moods
    return "ﾝ"

def decode_mood_char(char: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Decode a Half-width Kana character back to a mood state and intensity.
    
    Args:
        char: A Half-width Kana character representing a mood state
        
    Returns:
        Tuple of (mood_state, intensity), or (None, None) if not decodable
    """
    if not char or len(char) != 1:
        return None, None
    
    # Look up in the reverse mapping
    mood_state = REVERSE_MAP.get(char)
    
    if not mood_state:
        return None, None
    
    # For now, no intensity information is encoded
    # In a future version, we might extract intensity information
    intensity = 1.0  # Default full intensity
    
    return mood_state, intensity
