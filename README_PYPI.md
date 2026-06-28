# GeoMoz

[![PyPI version](https://img.shields.io/pypi/v/geomoz.svg)](https://pypi.org/project/geomoz/)
[![Python versions](https://img.shields.io/pypi/pyversions/geomoz.svg)](https://pypi.org/project/geomoz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://img.shields.io/pypi/dm/geomoz.svg)](https://pypi.org/project/geomoz/)

**Geospatial data library for Mozambique with automatic Hugging Face integration**

## Installation

### Basic Installation

```bash
pip install geomoz
```

### Complete Installation (with visualization dependencies)

```bash
pip install geomoz[complete]
```

### Development Installation

```bash
pip install geomoz[dev]
```

## Quick Start

```python
import geomoz

# Load provinces (automatic download from Hugging Face)
provinces = geomoz.read_province()
print(f"Loaded {len(provinces)} provinces")

# Load specific province
zambezia = geomoz.read_province(name_province="Zambézia")
print(f"Zambézia: {len(zambezia)} polygons")

# Load geology data
geology = geomoz.read_geology()
print(f"Geology units: {len(geology)}")

# Spatial operations
geo_zambezia = geomoz.geology_by_province(name_province="Zambézia")
area = geomoz.calculate_area(geo_zambezia, unit="km2")
print(f"Total area: {area['area_km2'].sum():.2f} km²")
```

## Main Features

### Data Access
- **Provinces**: 11 administrative provinces (2017)
- **Districts**: 161 administrative districts (2017)
- **Admin Posts**: 459 administrative posts (2017)
- **Villages**: All villages (2017)
- **Geology**: 12,533 geological units (2006)

### Automatic Integration
- **Hugging Face Hub**: Automatic download and caching
- **Smart Cache**: Local storage in `~/.cache/geomoz/`
- **Version Control**: Data versioned and tracked
- **Offline Support**: Works without internet after first download

### CRS Handling
- **Automatic UTM Detection**: Zones 36S (30-36°E) and 37S (36-42°E)
- **Cross-Boundary Support**: Handles areas crossing UTM boundaries
- **Precise Calculations**: Areas in km² using projected CRS
- **Visualization Ready**: Maintains WGS84 for mapping

### Spatial Operations
- **Geology by Administrative Unit**: `geology_by_province()`, `geology_by_district()`
- **Area Calculations**: `calculate_area()` with automatic CRS handling
- **Spatial Joins**: Link administrative boundaries with geological data
- **Flexible Filtering**: Filter by geological attributes (suite, formation, era, etc.)

## Available Functions

### Data Reading Functions
```python
# Administrative boundaries
geomoz.read_province() # All provinces
geomoz.read_district() # All districts
geomoz.read_admin_post() # All admin posts
geomoz.read_village() # All villages

# Geology data
geomoz.read_geology() # All geology
geomoz.read_geology(SUITE="Granite") # Filtered geology
```

### Spatial Analysis Functions
```python
# Geology clipped to administrative boundaries
geomoz.geology_by_province(name_province="Zambézia")
geomoz.geology_by_district(name_district="Lichinga")
geomoz.geology_by_admin_post(name_admin_post="Cidade de Lichinga")

# Area calculations
geomoz.calculate_area(geodata, unit="km2")

# Hierarchical data
geomoz.get_hierarchical_data(name_province="Zambézia", include_villages=True)
```

### Utility Functions
```python
from geomoz.utils.data import get_cache_info, clear_cache

# Cache information
cache_info = get_cache_info()
print(f"Cache size: {cache_info['size_mb']:.2f} MB")

# Clear cache
clear_cache()
```

## Data Sources

All data is automatically downloaded from the **[GeoMoz Dataset](https://huggingface.co/geolithicamz/geomoz-data)** on Hugging Face:

### Available Files
- `province_2017.gpkg` - Administrative provinces (11 units)
- `district_2017.gpkg` - Administrative districts (161 units)
- `adminpost_2017.gpkg` - Administrative posts (459 units)
- `village_2017.gpkg` - Villages (complete coverage)
- `geology_2006.gpkg` - Geological units (12,533 units)

### Data Characteristics
- **Coordinate System**: WGS84 (EPSG:4326)
- **Format**: GeoPackage (.gpkg)
- **Year**: Administrative (2017), Geology (2006)
- **Coverage**: Complete national coverage of Mozambique

## CRS Information

### UTM Zones for Mozambique
- **Zone 36S**: 30°E to 36°E (EPSG:32736) - Southern and central provinces
- **Zone 37S**: 36°E to 42°E (EPSG:32737) - Northern provinces

### Provinces Crossing UTM Boundaries
- **Sofala**: Crosses 36°E meridian
- **Zambézia**: Crosses 36°E meridian
- **Niassa**: Crosses 36°E meridian

The library automatically detects and handles cross-boundary areas!

## Examples

### Basic Usage
```python
import geomoz
import matplotlib.pyplot as plt

# Load and plot provinces
provinces = geomoz.read_province()
provinces.plot(figsize=(10, 8))
plt.title("Mozambique Provinces")
plt.show()
```

### Advanced Analysis
```python
# Geological analysis by province
geo_zambezia = geomoz.geology_by_province(
    name_province="Zambézia",
    SUITE="Granite"
)

# Calculate areas by geological unit
area_by_suite = geo_zambezia.groupby('SUITE').apply(
    lambda x: x.geometry.area.sum() / 1_000_000 # Convert to km²
)

print("Areas by geological suite (km²):")
print(area_by_suite.sort_values(ascending=False))
```

### Complete Mapping Example
```python
import geomoz
import matplotlib.pyplot as plt

# Get data
provinces = geomoz.read_province()
geology = geomoz.geology_by_province(name_province="Zambézia")

# Create map
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Plot provinces
provinces.plot(ax=ax, color='lightgray', alpha=0.5, edgecolor='black')

# Plot geology
geology.plot(ax=ax, column='Legend', cmap='tab20', alpha=0.7, legend=True)

# Configure map
ax.set_title('Geology of Zambézia Province')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.tight_layout()
plt.show()
```

## Development

### Installation from Source
```bash
git clone https://github.com/geolithicamz/geomoz.git
cd geomoz
pip install -e ".[dev]"
```

### Running Tests
```bash
python -m pytest tests/
```

### Building for Distribution
```bash
python build_and_publish.py build # Build only
python build_and_publish.py test # Build and test
python build_and_publish.py pypi # Build and publish to PyPI
```

## Dependencies

### Core Dependencies
- `geopandas>=0.14.0` - Geospatial data handling
- `pandas>=1.5.0` - Data manipulation
- `shapely>=2.0.0` - Geometric operations
- `huggingface_hub>=0.10.0` - Hugging Face integration
- `requests>=2.25.0` - HTTP requests
- `typing-extensions>=4.0.0` - Type hints

### Optional Dependencies
- `matplotlib>=3.5.0` - Plotting and visualization
- `folium>=0.12.0` - Interactive maps
- `contextily>=1.2.0` - Context tiles for maps
- `seaborn>=0.11.0` - Statistical visualization

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage testing
- `black>=22.0.0` - Code formatting
- `flake8>=5.0.0` - Linting
- `twine>=4.0.0` - PyPI publishing
- `wheel>=0.37.0` - Building wheels
- `build>=0.7.0` - Modern build system

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you have any questions or need help using GeoMoz:

- **Documentation**: [GitHub Wiki](https://github.com/geolithicamz/geomoz/wiki)
- **Issues**: [GitHub Issues](https://github.com/geolithicamz/geomoz/issues)
- **Discussions**: [GitHub Discussions](https://github.com/geolithicamz/geomoz/discussions)
- **Email**: contact@geolithica.org

## Acknowledgments

- **Hugging Face**: For hosting the dataset and providing the Hub infrastructure
- **Geopandas**: For the excellent geospatial data handling framework
- **Government of Mozambique**: For making the geospatial data available
- **Geolithica Team**: For the development and maintenance of this library

## Changelog

### Version 1.0.0
- **NEW**: Complete Hugging Face integration
- **NEW**: Automatic UTM zone detection and handling
- **NEW**: Cross-boundary area support
- **NEW**: Smart caching system
- **NEW**: Precise area calculations
- **IMPROVED**: All functions now use automatic download
- **IMPROVED**: Better error handling and user experience
- **IMPROVED**: Comprehensive documentation and examples

---

**GeoMoz** - *Geospatial data for Mozambique, simplified and automated*
