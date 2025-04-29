"""
Spiritual Arcs Character Mapping Module
======================================

This module defines mappings between spiritual/developmental arcs and Greek characters.
It provides functions for encoding arc names to characters and decoding
characters back to arc names and progress values.
"""

from typing import Dict, Tuple, Optional
import math

# Map of spiritual/developmental arc types to Greek characters
ARC_MAP = {
    # Foundational arcs
    "awakening": "Α",  # Alpha
    "redemption": "Β",  # Beta
    "transcendence": "Γ",  # Gamma
    "transformation": "Δ",  # Delta
    "enlightenment": "Ε",  # Epsilon
    "liberation": "Ζ",  # Zeta
    "rebirth": "Η",  # Eta
    
    # Growth arcs
    "healing": "Θ",  # Theta
    "mastery": "Ι",  # Iota
    "integration": "Κ",  # Kappa
    "expansion": "Λ",  # Lambda
    "alignment": "Μ",  # Mu
    "refinement": "Ν",  # Nu
    "purification": "Ξ",  # Xi
    
    # Challenge arcs
    "descent": "Ο",  # Omicron
    "shadow_work": "Π",  # Pi
    "confrontation": "Ρ",  # Rho
    "deconstruction": "Σ",  # Sigma
    "initiation": "Τ",  # Tau
    "surrender": "Υ",  # Upsilon
    "sacrifice": "Φ",  # Phi
    
    # Final arcs
    "completion": "Χ",  # Chi
    "unification": "Ψ",  # Psi
    "synthesis": "Ω",  # Omega
    
    # Lowercase variants can be used for alternative versions
    "quest": "α",  # alpha
    "reconciliation": "β",  # beta
    "evolution": "γ",  # gamma
    "renewal": "δ",  # delta
    "realization": "ε",  # epsilon
    "freedom": "ζ",  # zeta
    "restoration": "η",  # eta
    "balance": "θ",  # theta
    "wisdom": "ι",  # iota
    "harmony": "κ",  # kappa
    "growth": "λ",  # lambda
    "purpose": "μ",  # mu
    "clarity": "ν",  # nu
    "release": "ξ",  # xi
    "suffering": "ο",  # omicron
    "reckoning": "π",  # pi
    "challenge": "ρ",  # rho
    "ordeal": "σ",  # sigma
    "calling": "τ",  # tau
    "acceptance": "υ",  # upsilon
    "devotion": "φ",  # phi
    "resolution": "χ",  # chi
    "wholeness": "ψ",  # psi
    "oneness": "ω"   # omega
}

# Reverse mapping for decoding
REVERSE_MAP = {char: arc for arc, char in ARC_MAP.items()}

def normalize_arc_name(name: str) -> str:
    """
    Normalize a spiritual arc name to match the keys in the map.
    
    Args:
        name: The raw arc name
        
    Returns:
        Normalized name that can be looked up in the arc map
    """
    # Convert to lowercase and replace spaces with underscores
    normalized = name.lower().strip().replace(' ', '_')
    
    # Handle common variations
    replacements = {
        "shadow": "shadow_work",
        "illumination": "enlightenment",
        "journey": "quest",
        "emergence": "awakening",
        "spiritual_awakening": "awakening",
        "inner_work": "shadow_work",
        "soul_searching": "quest",
        "revelation": "realization"
    }
    
    for key, replacement in replacements.items():
        if normalized == key or normalized.endswith(f"_{key}"):
            return replacement
    
    return normalized

def encode_arc(arc: str) -> str:
    """
    Encode a spiritual arc name as a Greek character.
    
    Args:
        arc: The name of the spiritual arc
        
    Returns:
        A Greek character representing the arc
    """
    normalized = normalize_arc_name(arc)
    
    # Look for direct match
    if normalized in ARC_MAP:
        return ARC_MAP[normalized]
    
    # Look for partial match
    for key, char in ARC_MAP.items():
        if normalized in key or key in normalized:
            return char
    
    # Default to Omega for unknown arcs
    return "Ω"

def encode_arc_with_progress(arc: str, progress: float) -> str:
    """
    Encode a spiritual arc with its progress as a Greek character.
    The basic encoding remains the same, but conceptually the progress
    is embedded in the selection.
    
    Args:
        arc: The name of the spiritual arc
        progress: A value between 0.0 and 1.0 representing progress on the arc
        
    Returns:
        A Greek character representing the arc
    """
    # For now, simply encode the arc
    # In a more advanced version, the progress could affect which 
    # variation of character is used
    return encode_arc(arc)

def decode_arc_char(char: str) -> Tuple[Optional[str], Optional[float]]:
    """
    Decode a Greek character back to an arc name and progress value.
    
    Args:
        char: A Greek character representing a spiritual arc
        
    Returns:
        Tuple of (arc_name, progress), or (None, None) if not decodable
    """
    if not char or len(char) != 1:
        return None, None
    
    # Look up in the reverse mapping
    arc_name = REVERSE_MAP.get(char)
    
    if not arc_name:
        return None, None
    
    # For now, no progress information is encoded
    # In a future version, we might extract progress information
    progress = 0.5  # Default mid-point
    
    return arc_name, progress
