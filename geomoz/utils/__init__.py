"""
Utility functions for GeoMoz
"""

# Import data utilities first
from .data import (
    get_data_path,
    list_available_files,
    clear_cache,
    get_cache_info,
    validate_data_file
)

# Import traditional utilities if available
try:
    from .utils import (
        select_metadata,
        download_gpkg,
        validate_code,
        validate_name,
        advanced_download_gpkg,
        load_metadata
    )
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False

# Define __all__ based on what's available
__all__ = [
    "get_data_path",
    "list_available_files",
    "clear_cache",
    "get_cache_info",
    "validate_data_file"
]

if UTILS_AVAILABLE:
    __all__.extend([
        "select_metadata",
        "download_gpkg", 
        "validate_code",
        "validate_name",
        "advanced_download_gpkg",
        "load_metadata"
    ])
