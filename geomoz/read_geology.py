"""
Read geology data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils.data import get_data_path


def read_geology(
    code_geology: Union[str, int] = "all", 
    name_geology: str = None,
    year: int = 2006, 
    simplified: bool = True, 
    verbose: bool = False,
    # Geology-specific parameters
    code2006: str = None,
    Legend: str = None,
    Legenda: str = None,
    Mapping: str = None,
    EON: str = None,
    ERA: str = None,
    PERIOD: str = None,
    COMPLEX: str = None,
    SUITE: str = None,
    GrstBelt: str = None,
    Supergroup: str = None,
    Group_: str = None,
    Formation: str = None,
    Member: str = None,
    Label: str = None,
    Parent: str = None,
    age: str = None,
    TYPE: str = None
) -> gpd.GeoDataFrame:
    """
    Download shapefiles of Mozambican geology as geopandas objects.

    Data using Geodetic reference system "WGS 84" and CRS EPSG:4326
    Data is automatically downloaded from Hugging Face and cached locally.

    Parameters
    ----------
    code_geology : str or int, optional
        The code of a geology unit. 
        If code_geology="all", all geology units will be loaded (Default).
    name_geology : str, optional
        The name of a geology unit. Use this instead of code_geology
        to search by name. Case insensitive.
    year : int, optional
        Year of the data. Default is 2006.
    simplified : bool, optional
        Whether to use simplified boundaries. Default is True.
    verbose : bool, optional
        Whether to print progress information. Default is False.
    **geology_filters : optional
        Additional filters for geology attributes:
        - code2006: Geology code from 2006 survey
        - Legend/Legenda: Geological legend description
        - Mapping: Mapping unit
        - EON: Geological eon
        - ERA: Geological era
        - PERIOD: Geological period
        - COMPLEX: Geological complex
        - SUITE: Geological suite
        - GrstBelt: Greenstone belt
        - Supergroup: Geological supergroup
        - Group_: Geological group
        - Formation: Geological formation
        - Member: Geological member
        - Label: Geological label
        - Parent: Parent unit
        - age: Geological age
        - TYPE: Geological type

    Returns
    -------
    gpd.GeoDataFrame
        Geodataframe containing geology data with geological attributes
        and polygon geometries.

    Examples
    --------
    >>> from geomoz import read_geology
    >>> 
    >>> # Load all geology units
    >>> geology = read_geology()
    >>> 
    >>> # Load specific geology by code
    >>> unit = read_geology(code_geology="001")
    >>> 
    >>> # Load specific geology by name
    >>> unit = read_geology(name_geology="Granite")
    >>> 
    >>> # Load with geological filters
    >>> granites = read_geology(SUITE="Granite")
    >>> 
    >>> # Load with verbose output
    >>> geology = read_geology(verbose=True)
    """
    
    # Validate input parameters
    if code_geology != "all" and name_geology is not None:
        raise ValueError("Cannot specify both code_geology and name_geology. Use one or the other.")
    
    # Get data path from Hugging Face
    filename = "geology_2006.gpkg"
    
    if verbose:
        print(f"Loading geology data from Hugging Face: {filename}")
    
    try:
        # Download and load data from Hugging Face
        data_path = get_data_path(filename)
        
        if verbose:
            print(f"Data loaded from: {data_path}")
        
        gdf = gpd.read_file(data_path)
        
    except Exception as e:
        raise RuntimeError(f"Failed to load geology data: {str(e)}")
    
    # Apply filters
    if code_geology != "all":
        # Filter by code
        if isinstance(code_geology, str):
            code_geology = code_geology.zfill(3)  # Ensure 3-digit format
        
        gdf = gdf[gdf['code2006'] == str(code_geology)]
        
        if verbose:
            print(f"Filtered to geology code: {code_geology}")
    
    elif name_geology is not None:
        # Filter by name (case insensitive)
        mask = gdf['Legend'].str.lower() == name_geology.lower()
        gdf = gdf[mask]
        
        if verbose:
            print(f"Filtered to geology name: {name_geology}")
    
    # Apply geological attribute filters
    geology_filters = {
        'code2006': code2006,
        'Legend': Legend,
        'Legenda': Legenda,
        'Mapping': Mapping,
        'EON': EON,
        'ERA': ERA,
        'PERIOD': PERIOD,
        'COMPLEX': COMPLEX,
        'SUITE': SUITE,
        'GrstBelt': GrstBelt,
        'Supergroup': Supergroup,
        'Group_': Group_,
        'Formation': Formation,
        'Member': Member,
        'Label': Label,
        'Parent': Parent,
        'age': age,
        'TYPE': TYPE
    }
    
    for column, value in geology_filters.items():
        if value is not None and column in gdf.columns:
            if verbose:
                print(f"Filtering by {column}: {value}")
            
            if isinstance(value, str):
                mask = gdf[column].str.lower() == value.lower()
            else:
                mask = gdf[column] == value
            
            gdf = gdf[mask]
    
    # Validate results
    if len(gdf) == 0:
        if code_geology != "all":
            raise ValueError(f"No geology found with code: {code_geology}")
        elif name_geology is not None:
            raise ValueError(f"No geology found with name: {name_geology}")
    
    return gdf.reset_index(drop=True)
