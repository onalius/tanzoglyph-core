"""
TanzoGlyph IPFS Tools Module
=========================

This module provides utilities for uploading TanzoGlyph files to IPFS
and generating metadata for blockchain registration.
"""

import os
import sys
import json
import yaml
import logging
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Add the parent directory to the Python path to import tanzoglyph modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tanzoglyph.encoder import create_metadata_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPFSUploader:
    """Base class for IPFS upload integrations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the uploader with optional API key"""
        self.api_key = api_key or os.environ.get('IPFS_API_KEY', '')
        if not self.api_key:
            logger.warning("No IPFS API key provided. Some services may be limited.")
    
    def upload_file(self, file_path: str) -> Dict[str, str]:
        """Upload a file to IPFS"""
        raise NotImplementedError("Subclasses must implement upload_file")
    
    def upload_string(self, content: str, name: str) -> Dict[str, str]:
        """Upload a string as a file to IPFS"""
        raise NotImplementedError("Subclasses must implement upload_string")


class Web3StorageUploader(IPFSUploader):
    """Implementation of IPFS uploads using web3.storage"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with web3.storage API key"""
        super().__init__(api_key)
        self.endpoint = "https://api.web3.storage"
        
        if not self.api_key:
            logger.error("Web3.storage requires an API key. Please provide one.")
            raise ValueError("Missing API key for web3.storage")
    
    def upload_file(self, file_path: str) -> Dict[str, str]:
        """Upload a file to web3.storage
        
        Args:
            file_path: Path to the file to upload
            
        Returns:
            Dictionary with keys: 'cid', 'storage_proof_url', 'status'
        """
        # In a real implementation, we would use the web3.storage API to upload
        # files via their REST API or client library
        
        # This is a placeholder that would be implemented with actual API calls:
        # 1. Read the file
        # 2. Make a POST request to web3.storage's API
        # 3. Parse the response to get the CID
        
        logger.info(f"Uploading {file_path} to web3.storage")
        # Simulate response format for demonstration purposes
        # In the real implementation, this would be the response from the API
        return {
            'cid': f"placeholder-cid-for-{os.path.basename(file_path)}",
            'storage_proof_url': f"https://dweb.link/ipfs/placeholder-cid-for-{os.path.basename(file_path)}",
            'status': 'simulated'
        }
    
    def upload_string(self, content: str, name: str) -> Dict[str, str]:
        """Upload string content as a file to web3.storage
        
        Args:
            content: String content to upload
            name: Filename to use for the upload
            
        Returns:
            Dictionary with keys: 'cid', 'storage_proof_url', 'status'
        """
        # In a real implementation, this would use the actual web3.storage API
        logger.info(f"Uploading string content as {name} to web3.storage")
        
        # Simulate response format
        return {
            'cid': f"placeholder-cid-for-{name}",
            'storage_proof_url': f"https://dweb.link/ipfs/placeholder-cid-for-{name}",
            'status': 'simulated'
        }


class IPFSFactory:
    """Factory for creating IPFS uploaders based on service name"""
    
    @staticmethod
    def create_uploader(service_name: str = 'web3.storage', api_key: Optional[str] = None) -> IPFSUploader:
        """Create an uploader for the specified service
        
        Args:
            service_name: Name of the IPFS service ('web3.storage', 'pinata', etc.)
            api_key: API key for the service
            
        Returns:
            An IPFSUploader instance
            
        Raises:
            ValueError: If the service is not supported
        """
        if service_name.lower() == 'web3.storage':
            return Web3StorageUploader(api_key)
        else:
            raise ValueError(f"Unsupported IPFS service: {service_name}")


def upload_glyph_file(file_path: str, service: str = 'web3.storage', 
                    api_key: Optional[str] = None, 
                    create_metadata: bool = True,
                    output_dir: Optional[str] = None) -> Dict[str, Any]:
    """Upload a glyph file to IPFS and optionally create metadata
    
    Args:
        file_path: Path to the .glyph or .yaml file
        service: IPFS service to use
        api_key: API key for the service
        create_metadata: Whether to create a metadata file
        output_dir: Directory to save metadata file (defaults to same as input file)
        
    Returns:
        Dictionary with upload details
    """
    # Validate file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Create uploader
    uploader = IPFSFactory.create_uploader(service, api_key)
    
    # Upload the file
    result = uploader.upload_file(file_path)
    logger.info(f"File uploaded to IPFS with CID: {result['cid']}")
    
    # Create metadata file if requested
    if create_metadata:
        # Determine output directory
        if not output_dir:
            output_dir = os.path.dirname(file_path)
        
        # Read the glyph file
        with open(file_path, 'r', encoding='utf-8') as f:
            if file_path.lower().endswith(('.yaml', '.yml')):
                content = yaml.safe_load(f)
                if 'glyph_string' in content:
                    glyph_string = content['glyph_string']
                else:
                    # No glyph_string in YAML, so this isn't a valid file
                    raise ValueError(f"YAML file does not contain a glyph_string field")
            elif file_path.lower().endswith('.glyph'):
                glyph_string = f.read().strip()
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
        
        # Create metadata filename
        metadata_path = os.path.join(output_dir, f"{os.path.basename(file_path).split('.')[0]}_metadata.yaml")
        
        # Create metadata file
        metadata = create_metadata_file(
            glyph_string=glyph_string,
            ipfs_cid=result['cid'],
            output_path=metadata_path,
            storage_proof_url=result['storage_proof_url']
        )
        
        logger.info(f"Created metadata file at {metadata_path}")
        
        # Add metadata file info to result
        result['metadata_path'] = metadata_path
        # Store metadata fields individually
        for k, v in metadata.items():
            result[f'metadata_{k}'] = str(v)
    
    return result


def cli():
    """Command-line interface for IPFS tools"""
    parser = argparse.ArgumentParser(description="Upload TanzoGlyph files to IPFS")
    
    parser.add_argument('file', help="Path to the .glyph or .yaml file to upload")
    parser.add_argument('--service', choices=['web3.storage'], default='web3.storage',
                        help="IPFS service to use for upload")
    parser.add_argument('--api-key', help="API key for the IPFS service")
    parser.add_argument('--no-metadata', action='store_true', 
                        help="Skip creation of metadata file")
    parser.add_argument('--output-dir', help="Directory to save metadata file")
    
    args = parser.parse_args()
    
    try:
        result = upload_glyph_file(
            file_path=args.file,
            service=args.service,
            api_key=args.api_key,
            create_metadata=not args.no_metadata,
            output_dir=args.output_dir
        )
        
        # Print result
        print("--- Upload Result ---")
        print(f"CID: {result['cid']}")
        print(f"Storage Proof URL: {result['storage_proof_url']}")
        if 'metadata_path' in result:
            print(f"Metadata file: {result['metadata_path']}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(cli())
