"""
Legacy utility functions for GeoMoz
Maintained for backward compatibility
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path


def load_metadata() -> pd.DataFrame:
    """
    Load metadata for GeoMoz datasets
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing metadata information
    """
    # Basic metadata for available datasets
    metadata = pd.DataFrame([
        {
            'name': 'province',
            'function': 'read_province',
            'geography': 'Province',
            'filename': 'province_2017.gpkg',
            'year': 2017,
            'code_column': 'CodProv',
            'name_column': 'Provincia',
            'source': 'INE Moçambique',
            'description': 'Provincial boundaries of Mozambique'
        },
        {
            'name': 'district',
            'function': 'read_district',
            'geography': 'District',
            'filename': 'district_2017.gpkg',
            'year': 2017,
            'code_column': 'CodDist',
            'name_column': 'Distrito',
            'source': 'INE Moçambique',
            'description': 'District boundaries of Mozambique'
        },
        {
            'name': 'admin_post',
            'function': 'read_admin_post',
            'geography': 'Administrative Post',
            'filename': 'adminpost_2017.gpkg',
            'year': 2017,
            'code_column': 'CodPosto',
            'name_column': 'Posto',
            'source': 'INE Moçambique',
            'description': 'Administrative post boundaries of Mozambique'
        },
        {
            'name': 'village',
            'function': 'read_village',
            'geography': 'Village',
            'filename': 'village_2017.gpkg',
            'year': 2017,
            'code_column': 'CodPov',
            'name_column': 'Povoacao',
            'source': 'INE Moçambique',
            'description': 'Village boundaries of Mozambique'
        },
        {
            'name': 'geology',
            'function': 'read_geology',
            'geography': 'Geology',
            'filename': 'geology_2006.gpkg',
            'year': 2006,
            'code_column': 'code2006',
            'name_column': 'Legend',
            'source': 'Conselho Nacional de Geologia (DNGM)',
            'description': 'Geological units of Mozambique'
        }
    ])

    return metadata


def select_metadata(data_type: str, year: int = None, simplified: bool = True) -> pd.Series:
    """
    Select metadata for a specific data type
    
    Parameters
    ----------
    data_type : str
        Type of data (province, district, admin_post, village, geology)
    year : int, optional
        Year of the data
    simplified : bool, optional
        Whether to use simplified boundaries
        
    Returns
    -------
    pd.Series
        Metadata for the specified data type
    """
    metadata = load_metadata()
    
    # Filter by data type
    if data_type not in metadata['name'].values:
        raise ValueError(f"Unknown data type: {data_type}")
    
    row = metadata[metadata['name'] == data_type].iloc[0]
    
    # Apply year filter if specified
    if year is not None and row['year'] != year:
        raise ValueError(f"Year {year} not available for {data_type}")
    
    return row


def download_gpkg(metadata: pd.Series, code: str = None) -> 'gpd.GeoDataFrame':
    """
    Download and load geopackage file
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata information
    code : str, optional
        Specific code to filter
        
    Returns
    -------
    geopandas.GeoDataFrame
        Loaded geodataframe
    """
    try:
        import geopandas as gpd
    except ImportError:
        raise ImportError("geopandas is required but not installed")
    
    # Use new data path function
    from .data import get_data_path
    
    # Get data path from Hugging Face
    data_path = get_data_path(metadata['filename'])
    
    # Load the geopackage
    gdf = gpd.read_file(data_path)
    
    # Apply code filter if specified
    if code is not None:
        code_col = metadata['code_column']
        if code_col in gdf.columns:
            gdf = gdf[gdf[code_col] == code]
    
    return gdf


def validate_code(code: str, metadata: pd.Series) -> str:
    """
    Validate and format code
    
    Parameters
    ----------
    code : str
        Code to validate
    metadata : pd.Series
        Metadata information
        
    Returns
    -------
    str
        Validated and formatted code
    """
    if metadata['name'] in ['province', 'district', 'admin_post']:
        return str(code).zfill(2)
    elif metadata['name'] == 'village':
        return str(code).zfill(3)
    else:
        return str(code)


def validate_name(name: str, metadata: pd.Series) -> str:
    """
    Validate name
    
    Parameters
    ----------
    name : str
        Name to validate
    metadata : pd.Series
        Metadata information
        
    Returns
    -------
    str
        Validated name
    """
    return str(name)


def advanced_download_gpkg(metadata: pd.Series, **filters) -> 'gpd.GeoDataFrame':
    """
    Download and filter geopackage file with advanced filters
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata information
    **filters : dict
        Dictionary of column filters
        
    Returns
    -------
    geopandas.GeoDataFrame
        Filtered geodataframe
    """
    try:
        import geopandas as gpd
    except ImportError:
        raise ImportError("geopandas is required but not installed")
    
    # Use new data path function
    from .data import get_data_path
    
    # Get data path from Hugging Face
    data_path = get_data_path(metadata['filename'])
    
    # Load the geopackage
    gdf = gpd.read_file(data_path)
    
    # Apply filters
    for column, value in filters.items():
        if column in gdf.columns and value is not None:
            if isinstance(value, str):
                mask = gdf[column].str.lower() == value.lower()
            else:
                mask = gdf[column] == value
            gdf = gdf[mask]
    
    return gdf
