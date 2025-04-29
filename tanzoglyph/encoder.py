"""
TanzoGlyph Encoder Module
=========================

This module contains functions for encoding structured AI personality profiles
into TanzoGlyph character streams.
"""

import re
import yaml
import json
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

def encode_profile(profile: Dict[str, Any]) -> str:
    """
    Encode a profile dictionary into a TanzoGlyph character stream.
    
    Args:
        profile: A dictionary containing AI personality profile data
        
    Returns:
        A string of Unicode characters representing the encoded profile
        
    Raises:
        ValueError: If the profile structure is invalid or unsupported
    """
    # Initialize sections for different character classes
    traits_glyphs = ""
    archetype_glyphs = ""
    spiritual_arc_glyphs = ""
    mood_glyphs = ""
    scars_glyphs = ""
    projection_glyphs = ""
    
    try:
        # Process traits (Latin A-Z)
        if 'traits' in profile:
            traits_glyphs = encode_traits(profile['traits'])
        
        # Process archetypes (Cyrillic)
        if 'archetypes' in profile:
            archetype_glyphs = encode_archetypes(profile['archetypes'])
        
        # Process spiritual arcs (Greek)
        if 'spiritual_arcs' in profile or 'spiritualArcs' in profile:
            arcs = profile.get('spiritual_arcs') or profile.get('spiritualArcs', {})
            spiritual_arc_glyphs = encode_spiritual_arcs(arcs)
        
        # Process mood profile (Half-width Kana)
        if 'mood' in profile:
            mood_glyphs = encode_mood(profile['mood'])
        
        # Process scars (Braille)
        if 'scars' in profile:
            scars_glyphs = encode_scars(profile['scars'])
        
        # Process projection/style (Block Drawing)
        if 'projection' in profile or 'style' in profile:
            proj_data = profile.get('projection') or profile.get('style', {})
            projection_glyphs = encode_projection(proj_data)
        
        # Combine all sections into a single glyph string
        # Order: Greek, Braille, Latin, Kana, Cyrillic, Block Drawing
        tanzoglyph = (
            spiritual_arc_glyphs +
            scars_glyphs +
            traits_glyphs +
            mood_glyphs +
            archetype_glyphs +
            projection_glyphs
        )
        
        if not tanzoglyph:
            raise ValueError("No encodable elements found in profile")
        
        return tanzoglyph
        
    except Exception as e:
        logger.error(f"Encoding error: {str(e)}")
        raise ValueError(f"Failed to encode profile: {str(e)}")

def encode_traits(traits: Dict[str, Union[float, int, str]]) -> str:
    """
    Encode personality traits using Latin A-Z characters.
    
    Args:
        traits: Dictionary of trait name to value mappings
        
    Returns:
        Latin character string representing encoded traits
    """
    result = ""
    
    for trait_name, trait_value in traits.items():
        # Standardize trait name
        trait_key = trait_name.lower().strip()
        
        # Handle numeric values (typically 0.0-1.0)
        if isinstance(trait_value, (int, float)):
            # Normalize to range 0-1 if needed
            if trait_value > 1.0:
                normalized_value = min(trait_value / 10.0, 1.0)
            else:
                normalized_value = max(0.0, min(trait_value, 1.0))
                
            # Map normalized value to character
            char = traits_map.encode_trait_value(trait_key, normalized_value)
            result += char
        
        # Handle string values (e.g., "high", "medium", "low")
        elif isinstance(trait_value, str):
            char = traits_map.encode_trait_descriptor(trait_key, trait_value.lower().strip())
            result += char
            
    return result

def encode_archetypes(archetypes: Union[List[str], Dict[str, Any]]) -> str:
    """
    Encode archetypes using Cyrillic characters.
    
    Args:
        archetypes: List of archetypal descriptors or dictionary with weights
        
    Returns:
        Cyrillic character string representing encoded archetypes
    """
    result = ""
    
    # Handle list of archetypes
    if isinstance(archetypes, list):
        for archetype in archetypes:
            char = archetypes_map.encode_archetype(archetype)
            result += char
    
    # Handle dictionary of archetypes with weights
    elif isinstance(archetypes, dict):
        for archetype, weight in archetypes.items():
            # Only include archetypes with significant weight
            if isinstance(weight, (int, float)) and weight > 0.2:
                char = archetypes_map.encode_archetype(archetype)
                # Add character multiple times for higher weights
                repetitions = min(3, int(weight * 3))
                result += char * max(1, repetitions)
            elif isinstance(weight, bool) and weight:
                # Boolean True values
                char = archetypes_map.encode_archetype(archetype)
                result += char
    
    return result

def encode_spiritual_arcs(arcs: Union[List[str], Dict[str, Any]]) -> str:
    """
    Encode spiritual/developmental arcs using Greek characters.
    
    Args:
        arcs: List of arc descriptors or dictionary with details
        
    Returns:
        Greek character string representing encoded spiritual arcs
    """
    result = ""
    
    # Handle list of arc names
    if isinstance(arcs, list):
        for arc in arcs:
            char = spiritual_arcs_map.encode_arc(arc)
            result += char
    
    # Handle dictionary of arc details
    elif isinstance(arcs, dict):
        for arc_name, arc_data in arcs.items():
            if isinstance(arc_data, dict) and 'progress' in arc_data:
                # If progress is specified, encode with progress level
                progress = float(arc_data['progress'])
                char = spiritual_arcs_map.encode_arc_with_progress(arc_name, progress)
            else:
                # Otherwise just encode the arc name
                char = spiritual_arcs_map.encode_arc(arc_name)
            result += char
    
    return result

def encode_mood(mood: Dict[str, Any]) -> str:
    """
    Encode mood profile using Half-width Kana characters.
    
    Args:
        mood: Dictionary containing mood states and intensities
        
    Returns:
        Half-width Kana character string representing encoded mood
    """
    result = ""
    
    # Handle various mood structures
    if 'current' in mood:
        # Prioritize current mood if available
        current = mood['current']
        if isinstance(current, str):
            result += mood_map.encode_mood_state(current)
        elif isinstance(current, dict):
            for state, intensity in current.items():
                if isinstance(intensity, (int, float)) and intensity > 0.3:
                    char = mood_map.encode_mood_state(state, intensity)
                    result += char
    
    # Handle general mood states
    for state, intensity in mood.items():
        if state not in ('current', 'history', 'tendency'):
            if isinstance(intensity, (int, float)) and intensity > 0.3:
                char = mood_map.encode_mood_state(state, intensity)
                result += char
    
    return result

def encode_scars(scars: Union[List[str], Dict[str, Any]]) -> str:
    """
    Encode psychological scars or trauma using Braille characters.
    
    Args:
        scars: List of scar descriptors or dictionary with details
        
    Returns:
        Braille character string representing encoded scars
    """
    result = ""
    
    # Handle list of scar names
    if isinstance(scars, list):
        for scar in scars:
            char = scars_map.encode_scar(scar)
            result += char
    
    # Handle dictionary of scar details
    elif isinstance(scars, dict):
        for scar_name, scar_data in scars.items():
            if isinstance(scar_data, dict) and 'intensity' in scar_data:
                # If intensity is specified, encode with intensity level
                intensity = float(scar_data['intensity'])
                char = scars_map.encode_scar_with_intensity(scar_name, intensity)
            else:
                # Otherwise just encode the scar name
                char = scars_map.encode_scar(scar_name)
            result += char
    
    return result

def encode_projection(projection: Dict[str, Any]) -> str:
    """
    Encode projection/style characteristics using Block Drawing characters.
    
    Args:
        projection: Dictionary containing style and projection traits
        
    Returns:
        Block Drawing character string representing encoded projection
    """
    result = ""
    
    # Handle various projection/style attributes
    for attr, value in projection.items():
        if isinstance(value, (int, float)):
            # Normalize value to 0-1 range
            normalized = max(0.0, min(value, 1.0))
            char = projection_map.encode_projection_value(attr, normalized)
            result += char
        elif isinstance(value, str):
            char = projection_map.encode_projection_descriptor(attr, value)
            result += char
    
    return result

# Helper function for file operations
def encode_file(file_path: str, output_path: str = None, output_format: str = 'tomo') -> str:
    """
    Read a YAML/JSON file and encode its contents as TanzoGlyph.
    
    Args:
        file_path: Path to the input YAML/JSON file
        output_path: Path to save the encoded output (optional)
        output_format: File extension for output ('tomo' or 'glyph')
        
    Returns:
        The encoded TanzoGlyph string
    """
    # Determine file format from extension
    if file_path.lower().endswith(('.yaml', '.yml')):
        with open(file_path, 'r', encoding='utf-8') as f:
            profile = yaml.safe_load(f)
    elif file_path.lower().endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            profile = json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    
    # Encode the profile
    encoded = encode_profile(profile)
    
    # Save to file if output path is specified
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(encoded)
    # Otherwise generate output filename based on input
    elif output_format:
        output_name = file_path.rsplit('.', 1)[0] + f'.{output_format}'
        with open(output_name, 'w', encoding='utf-8') as f:
            f.write(encoded)
    
    return encoded
