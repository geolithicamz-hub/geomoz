"""
Read administrative post data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils import select_metadata, download_gpkg, validate_code, validate_name


def read_admin_post(
    code_admin_post: Union[str, int] = "all", 
    name_admin_post: str = None,
    year: int = 2017, 
    simplified: bool = True, 
    verbose: bool = False
) -> gpd.GeoDataFrame:
    """
    Download shapefiles of Mozambican administrative posts as geopandas objects.

    Data using Geodetic reference system "WGS 84" and CRS EPSG:4326

    Parameters
    ----------
    code_admin_post : str or int, optional
        The code of an administrative post. 
        If code_admin_post="all", all administrative posts will be loaded (Default).
    name_admin_post : str, optional
        The name of an administrative post. Use this instead of code_admin_post
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
        Metadata and geopackage of selected administrative posts

    Raises
    ------
    Exception
        If parameters are not found or not well defined

    Examples
    --------
    >>> from geomoz import read_admin_post

    # Read specific administrative post by name
    >>> admin_post = read_admin_post(name_admin_post="PostoName")

    # Read all administrative posts
    >>> admin_posts = read_admin_post(code_admin_post="all")
    """

    if verbose:
        print(f"Loading administrative post data for year {year}")

    # Get metadata
    metadata = select_metadata("administrative post", year=year)

    if code_admin_post is None and name_admin_post is None:
        raise Exception("Either 'code_admin_post' or 'name_admin_post' must be provided")

    # Load specific administrative post by name (priority over code)
    if name_admin_post is not None:
        # Validate and format the name
        validated_name = validate_name(name_admin_post, metadata)
        
        if verbose:
            print(f"Loading data for administrative post: {validated_name}")
        
        # Load the data
        gdf = download_gpkg(metadata, name=validated_name)
        
        if gdf.empty:
            available_names = _get_available_names(metadata)
            raise Exception(
                f"Error: Invalid value for name_admin_post '{name_admin_post}'. "
                f"Available names: {available_names[:10]}... (showing first 10)"
            )
        
        return gdf

    # Load all administrative posts
    elif code_admin_post == "all":
        if verbose:
            print("Loading data for all administrative posts")
        
        return download_gpkg(metadata)

    # Load specific administrative post by code
    else:
        # Validate and format the code
        validated_code = validate_code(code_admin_post, metadata)
        
        if verbose:
            print(f"Loading data for administrative post code: {validated_code}")
        
        # Load the data
        gdf = download_gpkg(metadata, code=validated_code)
        
        if gdf.empty:
            available_codes = _get_available_codes(metadata)
            raise Exception(
                f"Error: Invalid value for code_admin_post '{code_admin_post}'. "
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
        Available administrative post codes
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
        Available administrative post names
    """
    
    # Load full dataset to get available names
    full_gdf = download_gpkg(metadata)
    name_col = metadata['name_column']
    
    if name_col in full_gdf.columns:
        return sorted(full_gdf[name_col].unique())
    
    return []
