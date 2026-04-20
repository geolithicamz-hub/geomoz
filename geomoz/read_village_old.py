"""
Read village data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils import select_metadata, download_gpkg, validate_code, validate_name


def read_village(
    code_village: Union[str, int] = "all", 
    name_village: str = None,
    year: int = 2017, 
    simplified: bool = True, 
    verbose: bool = False
) -> gpd.GeoDataFrame:
    """
    Download shapefiles of Mozambican villages as geopandas objects.

    Data using Geodetic reference system "WGS 84" and CRS EPSG:4326

    Parameters
    ----------
    code_village : str or int, optional
        The code of a village. 
        If code_village="all", all villages will be loaded (Default).
    name_village : str, optional
        The name of a village. Use this instead of code_village
        to search by name. Case insensitive.
    year : int, optional
        Year of the data, by default 2017
    simplified : bool, optional
        Data 'type', indicating whether the function returns the 'original' dataset
        with high resolution or a dataset with 'simplified' borders (Default)
    verbose : bool, optional
        Print additional information, by default False

    Returns
    -------
    gpd.GeoDataFrame
        Metadata and geopackage of selected villages

    Raises
    ------
    Exception
        If parameters are not found or not well defined

    Examples
    --------
    >>> from geomoz import read_village

    # Read specific village by name
    >>> village = read_village(name_village="Matemo")

    # Read all villages
    >>> villages = read_village(code_village="all")
    """

    if verbose:
        print(f"Loading village data for year {year}")

    # Get metadata
    metadata = select_metadata("village", year=year)

    if code_village is None and name_village is None:
        raise Exception("Either 'code_village' or 'name_village' must be provided")

    # Load specific village by name (priority over code)
    if name_village is not None:
        # Validate and format the name
        validated_name = validate_name(name_village, metadata)
        
        if verbose:
            print(f"Loading data for village: {validated_name}")
        
        # Load the data
        gdf = download_gpkg(metadata, name=validated_name)
        
        if gdf.empty:
            available_names = _get_available_names(metadata)
            raise Exception(
                f"Error: Invalid value for name_village '{name_village}'. "
                f"Available names: {available_names[:10]}... (showing first 10)"
            )
        
        return gdf

    # Load all villages
    elif code_village == "all":
        if verbose:
            print("Loading data for all villages")
        
        return download_gpkg(metadata)

    # Load specific village by code
    else:
        # Validate and format the code
        validated_code = validate_code(code_village, metadata)
        
        if verbose:
            print(f"Loading data for village code: {validated_code}")
        
        # Load the data
        gdf = download_gpkg(metadata, code=validated_code)
        
        if gdf.empty:
            available_codes = _get_available_codes(metadata)
            raise Exception(
                f"Error: Invalid value for code_village '{code_village}'. "
                f"Available codes: {available_codes[:10]}... (showing first 10)"
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
        Available village codes
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
        Available village names
    """
    
    # Load full dataset to get available names
    full_gdf = download_gpkg(metadata)
    name_col = metadata['name_column']
    
    if name_col in full_gdf.columns:
        return sorted(full_gdf[name_col].unique())
    
    return []
