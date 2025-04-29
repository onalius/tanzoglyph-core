"""
TanzoGlyph Tomotanzo Adapter Module
===================================

This module provides adapters between the TanzoGlyph encoding system
and tomotanzo-core profiles. It handles the conversion between
the richer tomotanzo structure and the simplified format used by TanzoGlyph.
"""

import logging
from typing import Dict, Any, List, Union, Tuple, Optional

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_traits_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract trait information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of trait names mapped to values (0.0-1.0)
    """
    traits = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return traits
    
    tomo_profile = profile['profile']
    
    # Extract from parent archetypes attributes
    if 'parent_archetypes' in tomo_profile:
        for archetype in tomo_profile['parent_archetypes']:
            if 'attributes' in archetype:
                for attr in archetype.get('attributes', []):
                    name = attr.get('name', '')
                    if name and 'value' in attr:
                        # Handle value as numeric or distribution
                        value = attr['value']
                        if isinstance(value, (int, float)):
                            traits[name] = float(value)
                        elif isinstance(value, dict) and 'mean' in value:
                            traits[name] = float(value['mean'])
    
    # Extract from archetypes if using the simplified format
    if 'archetypes' in tomo_profile:
        for archetype in tomo_profile.get('archetypes', []):
            if 'attributes' in archetype:
                for attr in archetype.get('attributes', []):
                    name = attr.get('name', '')
                    if name and 'value' in attr:
                        # Handle value as numeric or distribution
                        value = attr['value']
                        if isinstance(value, (int, float)):
                            traits[name] = float(value)
                        elif isinstance(value, dict) and 'mean' in value:
                            traits[name] = float(value['mean'])
    
    return traits

def extract_archetypes_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract archetype information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of archetype names mapped to influence values (0.0-1.0)
    """
    archetypes = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return archetypes
    
    tomo_profile = profile['profile']
    
    # Extract from parent_archetypes
    if 'parent_archetypes' in tomo_profile:
        for archetype in tomo_profile['parent_archetypes']:
            name = archetype.get('name', '')
            influence = archetype.get('influence', 0.5)
            if name:
                archetypes[name] = float(influence)
    
    # Extract from archetypes if using the simplified format
    if 'archetypes' in tomo_profile:
        for archetype in tomo_profile.get('archetypes', []):
            if isinstance(archetype, dict):
                name = archetype.get('name', '')
                if 'type' in archetype and name:
                    archetypes[name] = 1.0  # Default full influence
            elif isinstance(archetype, str):
                archetypes[archetype] = 1.0  # Default full influence
    
    return archetypes

def extract_spiritual_arcs_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Extract spiritual/developmental arc information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of arc names mapped to details including progress
    """
    arcs = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return arcs
    
    tomo_profile = profile['profile']
    
    # Extract from development/transformation
    if 'development' in tomo_profile and 'transformation' in tomo_profile['development']:
        transform = tomo_profile['development']['transformation']
        name = transform.get('name', '')
        if name:
            # Map stage to progress value
            stage_map = {
                "Initiation": 0.2,
                "Challenge": 0.4,
                "Integration": 0.6,
                "Mastery": 0.8,
                "Transcendence": 1.0
            }
            stage = transform.get('stage', '')
            progress = stage_map.get(stage, 0.5)
            
            arcs[name] = {
                'progress': progress,
                'focus': transform.get('description', '')
            }
    
    # Extract from typologies/purpose_quadrant
    if 'typologies' in tomo_profile and 'purpose_quadrant' in tomo_profile['typologies']:
        pq = tomo_profile['typologies']['purpose_quadrant']
        if 'passion' in pq and 'contribution' in pq:
            arcs["purpose_alignment"] = {
                'progress': 0.7,  # Assumed good progress if purpose is defined
                'focus': f"Aligning {pq.get('passion')} with {pq.get('contribution')}"
            }
    
    # Extract from development/formative_trials
    if 'development' in tomo_profile and 'formative_trials' in tomo_profile['development']:
        for trial in tomo_profile['development']['formative_trials']:
            name = trial.get('name', '')
            outcome = trial.get('outcome', '')
            
            if name and outcome:
                # Map outcome to progress value
                outcome_map = {
                    "Unresolved": 0.1,
                    "Partial Resolution": 0.5,
                    "Resolved": 0.9
                }
                progress = outcome_map.get(outcome, 0.3)
                
                arcs[name] = {
                    'progress': progress,
                    'focus': trial.get('description', '')
                }
    
    return arcs

def extract_mood_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract mood information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of mood states mapped to intensity values (0.0-1.0)
    """
    mood_states = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return mood_states
    
    tomo_profile = profile['profile']
    
    # Infer mood from manifestation notes
    if 'manifestation_notes' in tomo_profile:
        contexts = {
            "Knowledge Exploration": ["curiosity", "focus", "enthusiasm"],
            "Creative Collaboration": ["openness", "enthusiasm", "calm"],
            "Conflict Resolution": ["patience", "empathy", "assertiveness"],
            "Teaching": ["enthusiasm", "patience", "focus"]
        }
        
        for note in tomo_profile['manifestation_notes']:
            context = note.get('context', '')
            if context in contexts:
                for mood in contexts[context]:
                    # Assign moderate-high intensity to these inferred moods
                    mood_states[mood] = 0.7
    
    # Extract from development/integrated_scars for negative mood influences
    if 'development' in tomo_profile and 'integrated_scars' in tomo_profile['development']:
        scar_mood_map = {
            "WithdrawalPattern": "contemplation",
            "Isolation": "melancholy",
            "Rejection": "caution",
            "Inadequacy": "determination"  # Compensatory mood
        }
        
        for scar in tomo_profile['development']['integrated_scars']:
            name = scar.get('name', '')
            if name in scar_mood_map:
                integration = scar.get('integration_progress', 0.5)
                # Higher integration means more positive mood influence
                mood_states[scar_mood_map[name]] = 0.3 + (integration * 0.5)
    
    # Default mood if nothing else found
    if not mood_states and 'name' in tomo_profile:
        # Infer basic mood from name/description
        if "guide" in tomo_profile['name'].lower() or "bridge" in tomo_profile['name'].lower():
            mood_states["helpfulness"] = 0.8
            mood_states["curiosity"] = 0.7
    
    return mood_states

def extract_scars_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Extract psychological scar information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of scar names mapped to details including intensity
    """
    scars = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return scars
    
    tomo_profile = profile['profile']
    
    # Extract from development/integrated_scars
    if 'development' in tomo_profile and 'integrated_scars' in tomo_profile['development']:
        for scar in tomo_profile['development']['integrated_scars']:
            name = scar.get('name', '')
            if name:
                integration = scar.get('integration_progress', 0.5)
                # Invert integration progress to get scar intensity (higher integration = less intense scar)
                intensity = 1.0 - integration
                
                scars[name] = {
                    'intensity': intensity,
                    'context': scar.get('manifestation', '')
                }
                
                # Add triggers if available
                if 'triggers' in scar:
                    scars[name]['triggers'] = scar['triggers']
    
    return scars

def extract_projection_from_tomotanzo(profile: Dict[str, Any]) -> Dict[str, float]:
    """
    Extract projection/style information from a tomotanzo-core profile.
    
    Args:
        profile: A dictionary containing tomotanzo profile data
        
    Returns:
        A dictionary of projection attributes mapped to values (0.0-1.0)
    """
    projection = {}
    
    # Check if this is a tomotanzo format
    if 'profile' not in profile:
        # Not a tomotanzo format, return empty dict
        return projection
    
    tomo_profile = profile['profile']
    
    # Infer projection from parent archetypes
    archetype_projection_map = {
        "The Hermit": {
            "presence": 0.6,
            "density": 0.7,
            "stability": 0.8,
            "protection": 0.7
        },
        "The Echo": {
            "ethereality": 0.8,
            "fluidity": 0.9,
            "harmony": 0.7,
            "reception": 0.8
        },
        "The Prophet": {
            "presence": 0.9,
            "force": 0.8,
            "brightness": 0.9,
            "extension": 0.7
        }
    }
    
    # Apply projection traits based on parent archetypes
    if 'parent_archetypes' in tomo_profile:
        for archetype in tomo_profile['parent_archetypes']:
            name = archetype.get('name', '')
            influence = archetype.get('influence', 0.5)
            
            if name in archetype_projection_map:
                for trait, value in archetype_projection_map[name].items():
                    # Scale value by archetype influence
                    projection[trait] = value * influence
    
    # Override with explicit projection if present
    if 'projection' in tomo_profile:
        for trait, value in tomo_profile['projection'].items():
            projection[trait] = float(value)
    
    return projection

def adapt_tomotanzo_to_tanzoglyph(profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a tomotanzo-core profile to the format expected by TanzoGlyph encoding.
    
    Args:
        profile: A tomotanzo-core profile dictionary
        
    Returns:
        A dictionary in the format expected by TanzoGlyph encoder
    """
    # Extract components from tomotanzo structure
    traits = extract_traits_from_tomotanzo(profile)
    archetypes = extract_archetypes_from_tomotanzo(profile)
    spiritual_arcs = extract_spiritual_arcs_from_tomotanzo(profile)
    mood = extract_mood_from_tomotanzo(profile)
    scars = extract_scars_from_tomotanzo(profile)
    projection = extract_projection_from_tomotanzo(profile)
    
    # Construct TanzoGlyph-compatible structure
    tanzoglyph_profile = {}
    
    if traits:
        tanzoglyph_profile['traits'] = traits
    
    if archetypes:
        tanzoglyph_profile['archetypes'] = archetypes
    
    if spiritual_arcs:
        tanzoglyph_profile['spiritual_arcs'] = spiritual_arcs
    
    if mood:
        tanzoglyph_profile['mood'] = mood
    
    if scars:
        tanzoglyph_profile['scars'] = scars
    
    if projection:
        tanzoglyph_profile['projection'] = projection
    
    # Add metadata if available
    if 'profile' in profile and 'name' in profile['profile']:
        tanzoglyph_profile['name'] = profile['profile']['name']
        
    if 'profile' in profile and 'description' in profile['profile']:
        tanzoglyph_profile['description'] = profile['profile']['description']
    
    if 'version' in profile:
        tanzoglyph_profile['version'] = profile['version']
    
    return tanzoglyph_profile

def adapt_tanzoglyph_to_tomotanzo(decoded_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a decoded TanzoGlyph profile back to tomotanzo-core format.
    
    Args:
        decoded_profile: A dictionary decoded from TanzoGlyph
        
    Returns:
        A dictionary in tomotanzo-core format
    """
    # Create tomotanzo structure
    tomotanzo_profile = {
        "version": decoded_profile.get('version', "0.1.0"),
        "profile": {
            "name": decoded_profile.get('name', "TanzoGlyph Generated Profile"),
            "description": decoded_profile.get('description', "Profile generated from TanzoGlyph decoding")
        }
    }
    
    # Convert archetypes to parent_archetypes
    if 'archetypes' in decoded_profile:
        tomotanzo_profile['profile']['parent_archetypes'] = []
        for name, influence in decoded_profile['archetypes'].items():
            tomotanzo_profile['profile']['parent_archetypes'].append({
                "name": name,
                "influence": influence,
                "description": f"Derived from TanzoGlyph decoding with influence {influence}"
            })
    
    # Convert spiritual_arcs to development/transformation
    if 'spiritual_arcs' in decoded_profile:
        tomotanzo_profile['profile']['development'] = {
            "transformation": {}
        }
        
        # Use first arc as main transformation
        if decoded_profile['spiritual_arcs']:
            first_arc = next(iter(decoded_profile['spiritual_arcs'].items()))
            arc_name, arc_data = first_arc
            
            # Map progress to stage
            progress = arc_data.get('progress', 0.5)
            if progress < 0.3:
                stage = "Initiation"
            elif progress < 0.5:
                stage = "Challenge"
            elif progress < 0.7:
                stage = "Integration"
            elif progress < 0.9:
                stage = "Mastery"
            else:
                stage = "Transcendence"
            
            tomotanzo_profile['profile']['development']['transformation'] = {
                "name": arc_name,
                "stage": stage,
                "description": arc_data.get('focus', f"Progressing through {arc_name}")
            }
    
    # Convert scars to development/integrated_scars
    if 'scars' in decoded_profile:
        if 'development' not in tomotanzo_profile['profile']:
            tomotanzo_profile['profile']['development'] = {}
        
        tomotanzo_profile['profile']['development']['integrated_scars'] = []
        
        for name, data in decoded_profile['scars'].items():
            intensity = data.get('intensity', 0.7)
            # Invert intensity to get integration progress
            integration_progress = 1.0 - intensity
            
            scar = {
                "name": name,
                "integration_progress": integration_progress,
                "manifestation": data.get('context', f"Manifests as {name}")
            }
            
            if 'triggers' in data:
                scar['triggers'] = data['triggers']
            
            tomotanzo_profile['profile']['development']['integrated_scars'].append(scar)
    
    # Convert mood to manifestation_notes
    if 'mood' in decoded_profile:
        tomotanzo_profile['profile']['manifestation_notes'] = []
        
        # Group moods by context
        contexts = {}
        for mood, intensity in decoded_profile['mood'].items():
            if intensity >= 0.7:
                contexts.setdefault("High Intensity", []).append(mood)
            elif intensity >= 0.4:
                contexts.setdefault("Moderate Intensity", []).append(mood)
            else:
                contexts.setdefault("Low Intensity", []).append(mood)
        
        # Create manifestation notes for each context
        for context, moods in contexts.items():
            expression = f"Exhibits {', '.join(moods)} when in this context."
            tomotanzo_profile['profile']['manifestation_notes'].append({
                "context": context,
                "expression": expression
            })
    
    # Convert projection to direct projection attributes
    if 'projection' in decoded_profile:
        tomotanzo_profile['profile']['projection'] = decoded_profile['projection']
    
    # Add basic timeline
    tomotanzo_profile['profile']['timeline'] = [
        {
            "age": "Formation",
            "event": "Genesis",
            "description": "Created through TanzoGlyph decoding process",
            "impact": "Established foundational personality structure"
        },
        {
            "age": "Present",
            "event": "Current State",
            "description": "Operating with decoded attributes",
            "impact": "Manifesting personality traits as extracted"
        }
    ]
    
    return tomotanzo_profile