"""
GeoMoz - Pacote de dados geográficos de Moçambique

Similar ao geobr (Brasil), mas focado em dados geográficos de Moçambique.
Fornece acesso fácil a dados de províncias, distritos, e outras divisões administrativas.
"""

__version__ = "0.1.0"
__author__ = "Hélder Gonçalves Félix Traquinho - Chief Executive Officer da Geolithica"

# Import all read functions following geobr pattern
from .read_province import read_province
from .read_district import read_district
from .read_admin_post import read_admin_post
from .read_village import read_village
from .read_geology import read_geology
from .list_geomoz import list_geomoz, list_available_geographies, list_available_years, get_dataset_info

# Import plot utilities
from .plot_utils import (
    plot_provinces,
    plot_districts_by_province,
    plot_administrative_hierarchy,
    plot_villages_with_names,
    plot_geology_by_area,
    create_comparison_plot,
    quick_map
)

# Import spatial functions
from .spatial import (
    link_district_province,
    link_village_district, 
    link_admin_post_district,
    geology_by_province,
    geology_by_district,
    geology_by_admin_post,
    geology_by_area,
    get_hierarchical_data,
    calculate_area
)

# Legacy functions for backward compatibility
from .core import list_geometries, list_provinces

__all__ = [
    # Main read functions
    "read_province",
    "read_district", 
    "read_admin_post",
    "read_village",
    "read_geology",
    
    # List functions
    "list_geomoz",
    "list_available_geographies",
    "list_available_years",
    "get_dataset_info",
    
    # Plot utilities
    "plot_provinces",
    "plot_districts_by_province",
    "plot_administrative_hierarchy",
    "plot_villages_with_names",
    "plot_geology_by_area",
    "create_comparison_plot",
    "quick_map",
    
    # Spatial functions
    "link_district_province",
    "link_village_district",
    "link_admin_post_district", 
    "geology_by_province",
    "geology_by_district",
    "geology_by_admin_post",
    "geology_by_area",
    "get_hierarchical_data",
    "calculate_area",
    
    # Legacy functions
    "list_geometries",
    "list_provinces",
]
