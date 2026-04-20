"""
Setup script for GeoMoz package
"""

from setuptools import setup, find_packages
import os

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Requirements for PyPI
requirements = [
    "geopandas>=0.14.0",
    "pandas>=1.5.0", 
    "shapely>=2.0.0",
    "huggingface_hub>=0.10.0",
    "requests>=2.25.0",
    "typing-extensions>=4.0.0"
]

setup(
    name="geomoz",
    version="0.1.0",
    author="Geolithica Team",
    author_email="contact@geolithica.org",
    description="Geospatial data library for Mozambique with automatic Hugging Face integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geolithicamz/geomoz",
    project_urls={
        "Bug Tracker": "https://github.com/geolithicamz/geomoz/issues",
        "Documentation": "https://github.com/geolithicamz/geomoz/blob/main/README.md",
        "Source Code": "https://github.com/geolithicamz/geomoz",
        "Hugging Face": "https://huggingface.co/geolithicamz/geomoz-data"
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Geoscience",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "twine>=4.0.0",
            "wheel>=0.37.0",
            "build>=0.7.0",
        ],
        "complete": [
            "matplotlib>=3.5.0",
            "folium>=0.12.0",
            "contextily>=1.2.0",
            "seaborn>=0.11.0",
        ]
    },
    include_package_data=True,
    package_data={
        'geomoz': ['data/*.md'],
    },
    keywords=[
        "geospatial",
        "mozambique", 
        "gis",
        "geopandas",
        "shapefile",
        "geology",
        "administrative-boundaries",
        "huggingface",
        "spatial-data",
        "africa",
        "geology-mapping",
        "crs",
        "utm",
        "shapefile",
        "gpkg",
        "geopackage",
        "spatial-analysis",
        "mapping",
        "geoscience"
    ],
    zip_safe=False,
)
