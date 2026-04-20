"""
Read province data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils.data import get_data_path


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
    
    try:
        # Download and load data from Hugging Face
        data_path = get_data_path(filename)
        
        if verbose:
            print(f"Data loaded from: {data_path}")
        
        gdf = gpd.read_file(data_path)
        
    except Exception as e:
        raise RuntimeError(f"Failed to load province data: {str(e)}")
    
    # Apply filters
    if code_province != "all":
        # Filter by code
        if isinstance(code_province, str):
            code_province = code_province.zfill(2)  # Ensure 2-digit format
        
        gdf = gdf[gdf['CodProv'] == str(code_province)]
        
        if verbose:
            print(f"Filtered to province code: {code_province}")
    
    elif name_province is not None:
        # Filter by name (case insensitive)
        mask = gdf['Provincia'].str.lower() == name_province.lower()
        gdf = gdf[mask]
        
        if verbose:
            print(f"Filtered to province name: {name_province}")
    
    # Validate results
    if len(gdf) == 0:
        if code_province != "all":
            raise ValueError(f"No province found with code: {code_province}")
        elif name_province is not None:
            raise ValueError(f"No province found with name: {name_province}")
    
    return gdf.reset_index(drop=True)
