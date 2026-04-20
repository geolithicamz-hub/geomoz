"""
Read province data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils import validate_code, validate_name, get_data_path


def read_province(
    code_province: Union[str, int] = "all", 
    name_province: str = None,
    year: int = 2017, 
    simplified: bool = True, 
    verbose: bool = False
) -> gpd.GeoDataFrame:
    """
    Download shapefiles of Mozambican provinces as geopandas objects.

    Data using Geodetic reference system "WGS 84" and CRS EPSG:4326
    Data is automatically downloaded from Hugging Face and cached locally.

    Parameters
    ----------
    code_province : str or int, optional
        The code of a province. 
        If code_province="all", all provinces will be loaded (Default).
    name_province : str, optional
        The name of a province (e.g., "Maputo"). Use this instead of code_province
        to search by name. Case insensitive.
    year : int, optional
        Year of the data. Default is 2017.
    simplified : bool, optional
        Whether to use simplified boundaries. Default is True.
    verbose : bool, optional
        Whether to print progress information. Default is False.

    Returns
    -------
    gpd.GeoDataFrame
        Geodataframe containing province data with columns:
        - CodProv: Province code
        - Provincia: Province name
        - geometry: Polygon geometries

    Examples
    --------
    >>> from geomoz import read_province
    >>> 
    >>> # Load all provinces
    >>> provinces = read_province()
    >>> 
    >>> # Load specific province by code
    >>> maputo = read_province(code_province="01")
    >>> 
    >>> # Load specific province by name
    >>> maputo = read_province(name_province="Maputo")
    >>> 
    >>> # Load with verbose output
    >>> provinces = read_province(verbose=True)
    """
    
    # Validate input parameters
    if code_province != "all" and name_province is not None:
        raise ValueError("Cannot specify both code_province and name_province. Use one or the other.")
    
    # Get data path from Hugging Face
    filename = "province_2017.gpkg"
    
    if verbose:
        print(f"Loading province data from Hugging Face: {filename}")
    # Load specific province by code
    else:
        # Validate and format the code
        validated_code = validate_code(code_province, metadata)
        
        if verbose:
            print(f"Loading data for province code: {validated_code}")
        
        # Load the data
        gdf = download_gpkg(metadata, code=validated_code)
        
        if gdf.empty:
            available_codes = _get_available_codes(metadata)
            raise Exception(
                f"Error: Invalid value for code_province '{code_province}'. "
                f"Available codes: {available_codes}"
            )
        
        return gdf


def _get_available_codes(metadata) -> list:
    """
    Helper function to get available codes from the dataset
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata information
        
    Returns
    -------
    list
        Available province codes
    """
    
    # Load full dataset to get available codes
    full_gdf = download_gpkg(metadata)
    code_col = metadata['code_column']
    
    if code_col in full_gdf.columns:
        return sorted(full_gdf[code_col].astype(str).unique())
    
    return []


def _get_available_names(metadata) -> list:
    """
    Helper function to get available names from the dataset
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata information
        
    Returns
    -------
    list
        Available province names
    """
    
    # Load full dataset to get available names
    full_gdf = download_gpkg(metadata)
    name_col = metadata['name_column']
    
    if name_col in full_gdf.columns:
        return sorted(full_gdf[name_col].unique())
    
    return []
