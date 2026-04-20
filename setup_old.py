from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="geomoz",
    version="0.1.0",
    author="GeoMoz Team",
    author_email="contact@geomoz.org",
    description="Pacote de dados geográficos de Moçambique",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/geomoz/geomoz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    python_requires=">=3.8",
    install_requires=[
        "geopandas>=0.14.0",
        "pandas>=1.5.0",
        "shapely>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "geomoz": ["data/*.gpkg"],
    },
)
