"""
TanzoGlyph Verification CLI
=========================

This module provides a command-line interface for verifying the authenticity
and validity of TanzoGlyph files.
"""

import os
import sys
import json
import yaml
import logging
import argparse
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# Add the parent directory to the Python path to import tanzoglyph modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tanzoglyph.encoder import validate_against_schema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_hash(content: str) -> str:
    """Calculate the SHA-256 hash of a string
    
    Args:
        content: String content to hash
        
    Returns:
        Hex digest of the hash
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def fetch_from_ipfs(ipfs_cid: str) -> Optional[str]:
    """Fetch content from IPFS by CID
    
    In a real implementation, this would use ipfs-http-client or similar
    to fetch the content. This is a placeholder that would be implemented
    with actual API calls.
    
    Args:
        ipfs_cid: IPFS Content ID
        
    Returns:
        Content as a string, or None if not found
    """
    # This is a placeholder that would be implemented with actual IPFS gateway calls
    logger.info(f"Simulating fetch from IPFS for CID: {ipfs_cid}")
    return f"SIMULATED_CONTENT_FOR_{ipfs_cid}"

def verify_glyph_file(file_path: str, ipfs_check: bool = False) -> Dict[str, Any]:
    """Verify a TanzoGlyph file's validity and authenticity
    
    Args:
        file_path: Path to the file to verify (.glyph, .yaml, or .json)
        ipfs_check: Whether to check against IPFS if metadata contains CID
        
    Returns:
        Dictionary with verification results
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file format is invalid
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    result = {
        'file_path': file_path,
        'valid_format': False,
        'schema_valid': False,
        'file_hash': None,
        'ipfs_check': None,
        'ipfs_match': None
    }
    
    # Read the file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
            result['file_hash'] = calculate_hash(file_content)
            
            # Parse based on file extension
            if file_path.lower().endswith(('.yaml', '.yml', '.json')):
                # Try to validate against schema
                try:
                    validate_against_schema(file_path)
                    result['schema_valid'] = True
                    result['valid_format'] = True
                except Exception as e:
                    logger.warning(f"Schema validation failed: {str(e)}")
                    result['schema_error'] = str(e)
                
                # Check if it contains IPFS metadata
                try:
                    if file_path.lower().endswith(('.yaml', '.yml')):
                        data = yaml.safe_load(file_content)
                    else:  # JSON
                        data = json.loads(file_content)
                    
                    # Check for metadata
                    if 'metadata' in data and 'ipfs_cid' in data['metadata']:
                        ipfs_cid = data['metadata']['ipfs_cid']
                        result['has_ipfs_cid'] = True
                        
                        # Fetch from IPFS if requested
                        if ipfs_check:
                            ipfs_content = fetch_from_ipfs(ipfs_cid)
                            if ipfs_content:
                                result['ipfs_check'] = True
                                ipfs_hash = calculate_hash(ipfs_content)
                                result['ipfs_hash'] = ipfs_hash
                                
                                # Compare content with local file
                                # In a real implementation, we'd need to handle differences in
                                # formatting and structure, not just direct hash comparison
                                result['ipfs_match'] = (ipfs_hash == result['file_hash'])
                    else:
                        result['has_ipfs_cid'] = False
                        
                except Exception as e:
                    logger.warning(f"Error parsing file content: {str(e)}")
                    result['parse_error'] = str(e)
                    
            elif file_path.lower().endswith('.glyph'):
                # Simple glyph file format check
                if len(file_content.strip()) > 0:
                    result['valid_format'] = True
                
                # No schema validation for raw glyph files, but could add
                # character set validation here
            else:
                result['format_error'] = f"Unsupported file format: {file_path}"
    
    except Exception as e:
        logger.error(f"Error reading or processing file: {str(e)}")
        result['error'] = str(e)
    
    return result

def cli():
    """Command-line interface for TanzoGlyph verification"""
    parser = argparse.ArgumentParser(description="Verify TanzoGlyph files")
    
    parser.add_argument('file', help="Path to the TanzoGlyph file to verify")
    parser.add_argument('--ipfs-check', action='store_true', 
                        help="Check against IPFS if metadata contains CID")
    parser.add_argument('--json', action='store_true',
                        help="Output results in JSON format")
    
    args = parser.parse_args()
    
    try:
        result = verify_glyph_file(
            file_path=args.file,
            ipfs_check=args.ipfs_check
        )
        
        # Output results
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\n=== TanzoGlyph Verification Results ===")
            print(f"File: {result['file_path']}")
            print(f"Valid Format: {'✓' if result['valid_format'] else '✗'}")
            print(f"Schema Valid: {'✓' if result['schema_valid'] else '✗' if 'schema_error' in result else 'N/A'}")
            
            if 'schema_error' in result:
                print(f"Schema Error: {result['schema_error']}")
                
            if 'has_ipfs_cid' in result:
                print(f"Has IPFS CID: {'✓' if result['has_ipfs_cid'] else '✗'}")
                
            if result.get('ipfs_check'):
                print(f"IPFS Content Match: {'✓' if result['ipfs_match'] else '✗'}")
                
            if 'error' in result:
                print(f"Error: {result['error']}")
                
            print("\nFile Hash (SHA-256):")
            print(result['file_hash'])
        
        # Return success if valid format, otherwise failure
        return 0 if result['valid_format'] else 1
    
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(cli())
