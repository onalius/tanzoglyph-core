"""
TanzoGlyph Decoder Module
=========================

This module contains functions for decoding TanzoGlyph character streams
back into structured AI personality profiles.
"""

import re
import logging
from typing import Dict, Any, List, Union, Tuple

from registry.glyph_maps import (
    traits as traits_map,
    archetypes as archetypes_map,
    spiritual_arcs as spiritual_arcs_map,
    mood as mood_map,
    scars as scars_map,
    projection as projection_map
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def decode_glyph(glyph: str) -> Dict[str, Any]:
    """
    Decode a TanzoGlyph character stream back into a structured profile.
    
    Args:
        glyph: A string of Unicode characters representing an encoded profile
        
    Returns:
        A dictionary containing the decoded profile data
        
    Raises:
        ValueError: If the glyph string is invalid or cannot be decoded
    """
    if not glyph or not isinstance(glyph, str):
        raise ValueError("Invalid glyph: must be a non-empty string")
    
    # Initialize output profile structure
    profile = {}
    
    try:
        # Extract character sequences by Unicode block
        traits_chars = re.findall(r'[A-Za-z]+', glyph)
        archetype_chars = re.findall(r'[А-Яа-я]+', glyph)  # Cyrillic
        spiritual_arc_chars = re.findall(r'[Α-Ωα-ω]+', glyph)  # Greek
        mood_chars = re.findall(r'[ｦ-ﾝ]+', glyph)  # Half-width Kana
        scars_chars = re.findall(r'[⠀-⣿]+', glyph)  # Braille
        projection_chars = re.findall(r'[▀-▟█-░]+', glyph)  # Block Drawing
        
        # Decode each section if present
        if traits_chars:
            traits = decode_traits(''.join(traits_chars))
            if traits:
                profile['traits'] = traits
                
        if archetype_chars:
            archetypes = decode_archetypes(''.join(archetype_chars))
            if archetypes:
                profile['archetypes'] = archetypes
                
        if spiritual_arc_chars:
            arcs = decode_spiritual_arcs(''.join(spiritual_arc_chars))
            if arcs:
                profile['spiritual_arcs'] = arcs
                
        if mood_chars:
            mood = decode_mood(''.join(mood_chars))
            if mood:
                profile['mood'] = mood
                
        if scars_chars:
            scars = decode_scars(''.join(scars_chars))
            if scars:
                profile['scars'] = scars
                
        if projection_chars:
            projection = decode_projection(''.join(projection_chars))
            if projection:
                profile['projection'] = projection
        
        if not profile:
            raise ValueError("No decodable elements found in glyph")
        
        return profile
        
    except Exception as e:
        logger.error(f"Decoding error: {str(e)}")
        raise ValueError(f"Failed to decode glyph: {str(e)}")

def decode_traits(trait_chars: str) -> Dict[str, float]:
    """
    Decode Latin A-Z characters back into personality traits.
    
    Args:
        trait_chars: String of Latin characters representing traits
        
    Returns:
        Dictionary of trait name to value mappings
    """
    traits = {}
    
    for char in trait_chars:
        trait_name, value = traits_map.decode_trait_char(char)
        if trait_name:
            traits[trait_name] = value
    
    return traits

def decode_archetypes(archetype_chars: str) -> Dict[str, float]:
    """
    Decode Cyrillic characters back into archetypes.
    
    Args:
        archetype_chars: String of Cyrillic characters representing archetypes
        
    Returns:
        Dictionary of archetype names with their weights
    """
    archetypes = {}
    
    # Count occurrences of each character to determine weights
    char_counts = {}
    for char in archetype_chars:
        char_counts[char] = char_counts.get(char, 0) + 1
    
    max_count = max(char_counts.values()) if char_counts else 1
    
    # Decode each unique character and assign normalized weight
    for char, count in char_counts.items():
        archetype = archetypes_map.decode_archetype_char(char)
        if archetype:
            # Normalize weight based on occurrence count
            weight = count / max_count
            archetypes[archetype] = min(1.0, weight)
    
    return archetypes

def decode_spiritual_arcs(arc_chars: str) -> Dict[str, Dict[str, float]]:
    """
    Decode Greek characters back into spiritual/developmental arcs.
    
    Args:
        arc_chars: String of Greek characters representing spiritual arcs
        
    Returns:
        Dictionary of arc names with their details
    """
    arcs = {}
    
    for char in arc_chars:
        arc_name, progress = spiritual_arcs_map.decode_arc_char(char)
        if arc_name:
            arcs[arc_name] = {'progress': progress} if progress is not None else {}
    
    return arcs

def decode_mood(mood_chars: str) -> Dict[str, float]:
    """
    Decode Half-width Kana characters back into mood states.
    
    Args:
        mood_chars: String of Half-width Kana characters representing mood
        
    Returns:
        Dictionary of mood states with their intensities
    """
    mood = {}
    
    for char in mood_chars:
        state, intensity = mood_map.decode_mood_char(char)
        if state:
            mood[state] = intensity if intensity is not None else 1.0
    
    return mood

def decode_scars(scar_chars: str) -> Dict[str, Dict[str, float]]:
    """
    Decode Braille characters back into psychological scars.
    
    Args:
        scar_chars: String of Braille characters representing scars
        
    Returns:
        Dictionary of scar names with their details
    """
    scars = {}
    
    for char in scar_chars:
        scar_name, intensity = scars_map.decode_scar_char(char)
        if scar_name:
            scars[scar_name] = {'intensity': intensity} if intensity is not None else {}
    
    return scars

def decode_projection(projection_chars: str) -> Dict[str, float]:
    """
    Decode Block Drawing characters back into projection/style traits.
    
    Args:
        projection_chars: String of Block Drawing characters representing projection
        
    Returns:
        Dictionary of projection/style traits with their values
    """
    projection = {}
    
    for char in projection_chars:
        attr, value = projection_map.decode_projection_char(char)
        if attr:
            projection[attr] = value
    
    return projection

# Helper function for file operations
def decode_file(file_path: str, output_path: str = None, output_format: str = 'yaml') -> Dict[str, Any]:
    """
    Read a TanzoGlyph file and decode its contents to YAML/JSON.
    
    Args:
        file_path: Path to the input TanzoGlyph file
        output_path: Path to save the decoded output (optional)
        output_format: Output format ('yaml' or 'json')
        
    Returns:
        The decoded profile as a dictionary
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        glyph = f.read().strip()
    
    # Decode the glyph
    profile = decode_glyph(glyph)
    
    # Save to file if output path is specified
    if output_path:
        if output_format.lower() == 'yaml':
            import yaml
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(profile, f, sort_keys=False, default_flow_style=False)
        else:  # json
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
    
    return profile
