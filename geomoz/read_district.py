"""
Read district data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils.data import get_data_path


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
    Data is automatically downloaded from Hugging Face and cached locally.

    Parameters
    ----------
    code_district : str or int, optional
        The code of a district. 
        If code_district="all", all districts will be loaded (Default).
    name_district : str, optional
        The name of a district (e.g., "Lichinga"). Use this instead of code_district
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
        Geodataframe containing district data with columns:
        - CodDist: District code
        - Distrito: District name
        - CodProv: Province code
        - Provincia: Province name
        - geometry: Polygon geometries

    Examples
    --------
    >>> from geomoz import read_district
    >>> 
    >>> # Load all districts
    >>> districts = read_district()
    >>> 
    >>> # Load specific district by code
    >>> lichinga = read_district(code_district="01")
    >>> 
    >>> # Load specific district by name
    >>> lichinga = read_district(name_district="Lichinga")
    >>> 
    >>> # Load with verbose output
    >>> districts = read_district(verbose=True)
    """
    
    # Validate input parameters
    if code_district != "all" and name_district is not None:
        raise ValueError("Cannot specify both code_district and name_district. Use one or the other.")
    
    # Get data path from Hugging Face
    filename = "district_2017.gpkg"
    
    if verbose:
        print(f"Loading district data from Hugging Face: {filename}")
    
    try:
        # Download and load data from Hugging Face
        data_path = get_data_path(filename)
        
        if verbose:
            print(f"Data loaded from: {data_path}")
        
        gdf = gpd.read_file(data_path)
        
    except Exception as e:
        raise RuntimeError(f"Failed to load district data: {str(e)}")
    
    # Apply filters
    if code_district != "all":
        # Filter by code
        if isinstance(code_district, str):
            code_district = code_district.zfill(2)  # Ensure 2-digit format
        
        gdf = gdf[gdf['CodDist'] == str(code_district)]
        
        if verbose:
            print(f"Filtered to district code: {code_district}")
    
    elif name_district is not None:
        # Filter by name (case insensitive)
        mask = gdf['Distrito'].str.lower() == name_district.lower()
        gdf = gdf[mask]
        
        if verbose:
            print(f"Filtered to district name: {name_district}")
    
    # Validate results
    if len(gdf) == 0:
        if code_district != "all":
            raise ValueError(f"No district found with code: {code_district}")
        elif name_district is not None:
            raise ValueError(f"No district found with name: {name_district}")
    
    return gdf.reset_index(drop=True)
