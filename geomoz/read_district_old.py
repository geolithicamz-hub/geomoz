"""
Read district data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils import select_metadata, download_gpkg, validate_code, validate_name


def read_district(
    code_district: Union[str, int] = "all", 
    name_district: str = None,
    year: int = 2017, 
    simplified: bool = True, 
    verbose: bool = False
) -> gpd.GeoDataFrame:
    """
    Download shapefiles of Mozambican districts as geopandas objects.

    Data using Geodetic reference system "WGS 84" and CRS EPSG:4326

    Parameters
    ----------
    code_district : str or int, optional
        The code of a district. 
        If code_district="all", all districts will be loaded (Default).
    name_district : str, optional
        The name of a district (e.g., "Lichinga"). Use this instead of code_district
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
        Metadata and geopackage of selected districts

    Raises
    ------
    Exception
        If parameters are not found or not well defined

    Examples
    --------
    >>> from geomoz import read_district

    # Read specific district by code
    >>> district = read_district(code_district="01")

    # Read specific district by name
    >>> district = read_district(name_district="Lichinga")

    # Read all districts
    >>> districts = read_district(code_district="all")
    """

    if verbose:
        print(f"Loading district data for year {year}")

    # Get metadata
    metadata = select_metadata("district", year=year)

    if code_district is None and name_district is None:
        raise Exception("Either 'code_district' or 'name_district' must be provided")

    # Load specific district by name (priority over code)
    if name_district is not None:
        # Validate and format the name
        validated_name = validate_name(name_district, metadata)
        
        if verbose:
            print(f"Loading data for district: {validated_name}")
        
        # Load the data
        gdf = download_gpkg(metadata, name=validated_name)
        
        if gdf.empty:
            available_names = _get_available_names(metadata)
            raise Exception(
                f"Error: Invalid value for name_district '{name_district}'. "
                f"Available names: {available_names[:10]}... (showing first 10)"
            )
        
        return gdf

    # Load all districts
    elif code_district == "all":
        if verbose:
            print("Loading data for all districts")
        
        return download_gpkg(metadata)

    # Load specific district by code
    else:
        # Validate and format the code
        validated_code = validate_code(code_district, metadata)
        
        if verbose:
            print(f"Loading data for district code: {validated_code}")
        
        # Load the data
        gdf = download_gpkg(metadata, code=validated_code)
        
        if gdf.empty:
            available_codes = _get_available_codes(metadata)
            raise Exception(
                f"Error: Invalid value for code_district '{code_district}'. "
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
        Available district codes
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
        Available district names
    """
    
    # Load full dataset to get available names
    full_gdf = download_gpkg(metadata)
    name_col = metadata['name_column']
    
    if name_col in full_gdf.columns:
        return sorted(full_gdf[name_col].unique())
    
    return []
