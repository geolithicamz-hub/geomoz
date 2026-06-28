"""
GeoMoz - Pacote de dados geográficos de Moçambique

Similar ao geobr (Brasil), mas focado em dados geográficos de Moçambique.
Fornece acesso fácil a dados de províncias, distritos, e outras divisões administrativas.
"""

__version__ = "0.1.3"
__author__ = "Hélder Gonçalves Félix Traquinho - Chief Executive Officer da Geolithica"

# Import all read functions following geobr pattern
from .read_province import read_province
from .read_district import read_district
from .read_admin_post import read_admin_post
from .read_village import read_village
from .read_geology import read_geology
from .list_geomoz import list_geomoz, list_available_geographies, list_available_years, get_dataset_info

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

# Plotting utilities are imported lazily so that the core package works
# without the optional visualization dependencies (matplotlib, etc.).
# They are exposed via module-level __getattr__ (PEP 562).
_PLOT_FUNCTIONS = {
    "plot_provinces",
    "plot_districts_by_province",
    "plot_administrative_hierarchy",
    "plot_villages_with_names",
    "plot_geology_by_area",
    "create_comparison_plot",
    "quick_map",
}


def __getattr__(name):
    """Lazily import optional plotting helpers (PEP 562).

    Importing ``geomoz`` must not require matplotlib. The plotting helpers
    are only loaded when first accessed, and a clear, actionable error is
    raised if the visualization extras are missing.
    """
    if name in _PLOT_FUNCTIONS:
        try:
            from . import plot_utils
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise ImportError(
                f"'{name}' requires the optional visualization dependencies. "
                "Install them with: pip install 'geomoz[viz]'"
            ) from exc
        return getattr(plot_utils, name)
    raise AttributeError(f"module 'geomoz' has no attribute '{name}'")


def __dir__():
    return sorted(list(globals().keys()) + list(_PLOT_FUNCTIONS))


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

    # Plot utilities (lazily imported)
    "plot_provinces",
    "plot_districts_by_province",
    "plot_administrative_hierarchy",
    "plot_villages_with_names",
    "plot_geology_by_area",
    "create_comparison_plot",
    "quick_map",
]
