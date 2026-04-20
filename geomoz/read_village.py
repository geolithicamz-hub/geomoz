"""
Read village data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils.data import get_data_path


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
    Data is automatically downloaded from Hugging Face and cached locally.

    Parameters
    ----------
    code_village : str or int, optional
        The code of a village. 
        If code_village="all", all villages will be loaded (Default).
    name_village : str, optional
        The name of a village. Use this instead of code_village
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
        Geodataframe containing village data with columns:
        - CodPov: Village code
        - Povoacao: Village name
        - CodPosto: Administrative post code
        - Posto: Administrative post name
        - CodDist: District code
        - Distrito: District name
        - CodProv: Province code
        - Provincia: Province name
        - geometry: Polygon geometries

    Examples
    --------
    >>> from geomoz import read_village
    >>> 
    >>> # Load all villages
    >>> villages = read_village()
    >>> 
    >>> # Load specific village by code
    >>> village = read_village(code_village="01")
    >>> 
    >>> # Load specific village by name
    >>> village = read_village(name_village="Lichinga")
    >>> 
    >>> # Load with verbose output
    >>> villages = read_village(verbose=True)
    """
    
    # Validate input parameters
    if code_village != "all" and name_village is not None:
        raise ValueError("Cannot specify both code_village and name_village. Use one or the other.")
    
    # Get data path from Hugging Face
    filename = "village_2017.gpkg"
    
    if verbose:
        print(f"Loading village data from Hugging Face: {filename}")
    
    try:
        # Download and load data from Hugging Face
        data_path = get_data_path(filename)
        
        if verbose:
            print(f"Data loaded from: {data_path}")
        
        gdf = gpd.read_file(data_path)
        
    except Exception as e:
        raise RuntimeError(f"Failed to load village data: {str(e)}")
    
    # Apply filters
    if code_village != "all":
        # Filter by code
        if isinstance(code_village, str):
            code_village = code_village.zfill(2)  # Ensure 2-digit format
        
        gdf = gdf[gdf['CodPov'] == str(code_village)]
        
        if verbose:
            print(f"Filtered to village code: {code_village}")
    
    elif name_village is not None:
        # Filter by name (case insensitive)
        mask = gdf['Povoacao'].str.lower() == name_village.lower()
        gdf = gdf[mask]
        
        if verbose:
            print(f"Filtered to village name: {name_village}")
    
    # Validate results
    if len(gdf) == 0:
        if code_village != "all":
            raise ValueError(f"No village found with code: {code_village}")
        elif name_village is not None:
            raise ValueError(f"No village found with name: {name_village}")
    
    return gdf.reset_index(drop=True)
