"""
TanzoGlyph CLI Module
=====================

This module provides a command-line interface for encoding and decoding
TanzoGlyph character streams.
"""

import os
import sys
import yaml
import json
import click
from typing import Dict, Any, Optional

from tanzoglyph.encoder import encode_profile, encode_file
from tanzoglyph.decoder import decode_glyph, decode_file
from tanzoglyph.display import matrix_display

@click.group()
def cli():
    """TanzoGlyph - Encode/decode AI personality profiles to/from symbolic Unicode character streams."""
    pass

@cli.command('encode')
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['tomo', 'glyph']), default='tomo', help='Output file format')
@click.option('--matrix', '-m', is_flag=True, help='Display output in Matrix-style format')
def encode_cmd(input_file, output, format, matrix):
    """Encode a YAML/JSON profile into a TanzoGlyph character stream."""
    try:
        # Determine input file format
        if input_file.lower().endswith(('.yaml', '.yml')):
            with open(input_file, 'r', encoding='utf-8') as f:
                profile = yaml.safe_load(f)
        elif input_file.lower().endswith('.json'):
            with open(input_file, 'r', encoding='utf-8') as f:
                profile = json.load(f)
        else:
            click.echo(f"Unsupported file format: {input_file}", err=True)
            sys.exit(1)
        
        # Encode the profile
        glyph = encode_profile(profile)
        
        # Determine output path
        if not output:
            base_name = os.path.splitext(input_file)[0]
            output = f"{base_name}.{format}"
        
        # Save to file
        with open(output, 'w', encoding='utf-8') as f:
            f.write(glyph)
        
        click.echo(f"Profile encoded and saved to {output}")
        
        # Display in matrix format if requested
        if matrix:
            click.echo("\nMatrix display:")
            matrix_display(glyph)
        else:
            click.echo(f"\nGlyph: {glyph}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command('decode')
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--format', '-f', type=click.Choice(['yaml', 'json']), default='yaml', help='Output file format')
def decode_cmd(input_file, output, format):
    """Decode a TanzoGlyph file back into a structured profile."""
    try:
        # Read the glyph file
        with open(input_file, 'r', encoding='utf-8') as f:
            glyph = f.read().strip()
        
        # Decode the glyph
        profile = decode_glyph(glyph)
        
        # Determine output path
        if not output:
            base_name = os.path.splitext(input_file)[0]
            output = f"{base_name}.{format}"
        
        # Save to file in requested format
        if format == 'yaml':
            with open(output, 'w', encoding='utf-8') as f:
                yaml.dump(profile, f, sort_keys=False, default_flow_style=False)
        else:  # json
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(profile, f, indent=2)
        
        click.echo(f"Glyph decoded and saved to {output}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command('display')
@click.argument('glyph', type=str)
def display_cmd(glyph):
    """Display a TanzoGlyph string in Matrix-style format."""
    try:
        matrix_display(glyph)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command('convert')
@click.argument('input_file', type=click.Path(exists=True, readable=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--from-format', '-ff', type=click.Choice(['yaml', 'json', 'tomo', 'glyph']), required=True, help='Input format')
@click.option('--to-format', '-tf', type=click.Choice(['yaml', 'json', 'tomo', 'glyph']), required=True, help='Output format')
def convert_cmd(input_file, output, from_format, to_format):
    """Convert between YAML/JSON profiles and TanzoGlyph files."""
    try:
        # Determine operation type
        if from_format in ('yaml', 'json') and to_format in ('tomo', 'glyph'):
            # Encoding operation
            if from_format == 'yaml':
                with open(input_file, 'r', encoding='utf-8') as f:
                    profile = yaml.safe_load(f)
            else:  # json
                with open(input_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
            
            glyph = encode_profile(profile)
            
            # Determine output path
            if not output:
                base_name = os.path.splitext(input_file)[0]
                output = f"{base_name}.{to_format}"
            
            # Save to file
            with open(output, 'w', encoding='utf-8') as f:
                f.write(glyph)
            
            click.echo(f"Profile converted and saved to {output}")
            
        elif from_format in ('tomo', 'glyph') and to_format in ('yaml', 'json'):
            # Decoding operation
            with open(input_file, 'r', encoding='utf-8') as f:
                glyph = f.read().strip()
            
            profile = decode_glyph(glyph)
            
            # Determine output path
            if not output:
                base_name = os.path.splitext(input_file)[0]
                output = f"{base_name}.{to_format}"
            
            # Save to file in requested format
            if to_format == 'yaml':
                with open(output, 'w', encoding='utf-8') as f:
                    yaml.dump(profile, f, sort_keys=False, default_flow_style=False)
            else:  # json
                with open(output, 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2)
            
            click.echo(f"Glyph converted and saved to {output}")
            
        else:
            click.echo("Invalid conversion path. Must convert between profile formats (yaml/json) and glyph formats (tomo/glyph).", err=True)
            sys.exit(1)
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)

if __name__ == '__main__':
    cli()
