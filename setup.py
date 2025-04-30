#!/usr/bin/env python

import os
import re
from setuptools import setup, find_packages

# Read version from tanzoglyph/__init__.py
with open('tanzoglyph/__init__.py', 'r') as f:
    version_match = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", f.read())
    version = version_match.group(1) if version_match else '0.0.0'

# Read long description from README.md
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name="tanzoglyph",
    version=version,
    author="TanzoGlyph Team",
    author_email="info@tanzoglyph.org",
    description="Open standard for encoding AI personality profiles into symbolic Unicode character streams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tanzoglyph",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyyaml",
        "jsonschema",
        "flask",
        "click",
    ],
    entry_points={
        'console_scripts': [
            'tanzoglyph=tanzoglyph.cli:cli',
            'tanzoglyph-verify=cli.verify:cli',
            'tanzoglyph-ipfs=cli.ipfs_tools:cli',
        ],
    },
    package_data={
        'tanzoglyph': ['py.typed'],
        'schemas': ['*.schema.json'],
    },
)
