"""
Read geology data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils import select_metadata, download_gpkg, download_gpkg_advanced, validate_code, validate_name


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

    Parameters
    ----------
    code_geology : str or int, optional
        The code of a geological unit. 
        If code_geology="all", all geological units will be loaded (Default).
    name_geology : str, optional
        The name of a geological unit. Use this instead of code_geology
        to search by name. Case insensitive.
    year : int, optional
        Year of the data, by default 2006
    simplified : bool, optional
        Data 'type', indicating whether the function returns the 'original' dataset
        with high resolution or a dataset with 'simplified' borders (Default)
    verbose : bool, optional
        Print additional information, by default False
    **Geology-specific parameters:**
    code2006, Legend, Legenda, Mapping, EON, ERA, PERIOD, COMPLEX, SUITE, 
    GrstBelt, Supergroup, Group_, Formation, Member, Label, Parent, age, TYPE : str, optional
        Filter by specific geological attributes. Case insensitive.

    Returns
    -------
    gpd.GeoDataFrame
        Metadata and geopackage of selected geological units

    Raises
    ------
    Exception
        If parameters are not found or not well defined

    Examples
    --------
    >>> from geomoz import read_geology

    # Read specific geological unit by code
    >>> geology = read_geology(code_geology='P2Cd')

    # Read by geological suite
    >>> geology = read_geology(SUITE='Malema')

    # Read by formation
    >>> geology = read_geology(Formation='Chidzolomondo')

    # Read all geological units
    >>> geology = read_geology(code_geology='all')
    """

    if verbose:
        print(f"Loading geology data for year {year}")

    # Get metadata
    metadata = select_metadata("geology", year=year)

    # Check if any specific filter is provided
    geology_params = {
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
    
    # Remove None values
    geology_params = {k: v for k, v in geology_params.items() if v is not None}
    
    # Load all geological units
    if code_geology == "all" and not geology_params and name_geology is None:
        if verbose:
            print("Loading data for all geological units")
        
        return download_gpkg(metadata)

    # Load with advanced filtering
    else:
        # Prepare parameters for advanced download
        download_params = {}
        
        # Add code or name filtering
        if name_geology is not None:
            download_params['name'] = name_geology
            if verbose:
                print(f"Loading data for geology: {name_geology}")
        elif code_geology != "all":
            validated_code = validate_code(code_geology, metadata)
            download_params['code'] = validated_code
            if verbose:
                print(f"Loading data for geology code: {validated_code}")
        
        # Add geology-specific parameters
        download_params.update(geology_params)
        
        # Show what's being filtered
        if verbose and geology_params:
            print(f"Filtering by: {', '.join(f'{k}={v}' for k, v in geology_params.items())}")
        
        # Load the data
        gdf = download_gpkg_advanced(metadata, **download_params)
        
        if gdf.empty:
            if code_geology != "all":
                available_codes = _get_available_codes(metadata)
                raise Exception(
                    f"Error: Invalid value for code_geology '{code_geology}'. "
                    f"Available codes: {available_codes[:10]}... (showing first 10)"
                )
            else:
                raise Exception(
                    f"No data found for the specified filters: {geology_params}"
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
        Available geology codes
    """
    
    # Load full dataset to get available codes
    full_gdf = download_gpkg(metadata)
    code_col = metadata['code_column']
    
    if code_col in full_gdf.columns:
        return sorted(full_gdf[code_col].astype(str).unique())
    
    return []
