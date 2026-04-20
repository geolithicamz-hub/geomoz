"""
Utility functions for GeoMoz package
"""

import os
import geopandas as gpd
import pandas as pd
from typing import Optional, Union

# Base directory for data files
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_metadata() -> pd.DataFrame:
    """
    Load metadata for all available datasets
    
    Returns
    -------
    pd.DataFrame
        Metadata with information about available datasets
    """
    
    metadata_data = [
        # Province data
        {
            'function': 'read_province',
            'geography': 'Province',
            'year': 2017,
            'source': 'INE Moçambique',
            'file': 'province_2017.gpkg',
            'code_column': 'CodProv',
            'name_column': 'Provincia'
        },
        # District data
        {
            'function': 'read_district',
            'geography': 'District',
            'year': 2017,
            'source': 'INE Moçambique',
            'file': 'district_2017.gpkg',
            'code_column': 'CodDist',
            'name_column': 'Distrito'
        },
        # Administrative Post data
        {
            'function': 'read_admin_post',
            'geography': 'Administrative Post',
            'year': 2017,
            'source': 'INE Moçambique',
            'file': 'adminpost_2017.gpkg',
            'code_column': 'CodPosto',
            'name_column': 'Posto'
        },
        # Village data
        {
            'function': 'read_village',
            'geography': 'Village',
            'year': 2017,
            'source': 'INE Moçambique',
            'file': 'village_2017.gpkg',
            'code_column': 'CODIGO_CEN',
            'name_column': 'NAME'
        },
        # Geology data
        {
            'function': 'read_geology',
            'geography': 'Geology',
            'year': 2006,
            'source': 'Geological Survey',
            'file': 'geology_2006.gpkg',
            'code_column': 'code2006',
            'name_column': 'Legenda'
        }
    ]
    
    return pd.DataFrame(metadata_data)


def select_metadata(geography: str, year: Optional[int] = None) -> pd.DataFrame:
    """
    Select metadata for a specific geography and year
    
    Parameters
    ----------
    geography : str
        Type of geography (e.g., 'province', 'district')
    year : int, optional
        Year of the data
        
    Returns
    -------
    pd.DataFrame
        Filtered metadata
    """
    
    metadata = load_metadata()
    
    # Filter by geography
    filtered = metadata[metadata['geography'].str.lower() == geography.lower()]
    
    # Filter by year if specified
    if year is not None:
        filtered = filtered[filtered['year'] == year]
    
    if filtered.empty:
        available_geogs = metadata['geography'].unique()
        available_years = metadata['year'].unique()
        raise ValueError(
            f"No data found for geography '{geography}'"
            f"{f' and year {year}' if year else ''}. "
            f"Available geographies: {list(available_geogs)}. "
            f"Available years: {list(available_years)}"
        )
    
    return filtered.iloc[0]  # Return first (and should be only) matching row


def download_gpkg(metadata: pd.Series, code: Optional[Union[str, int]] = None, name: Optional[str] = None) -> gpd.GeoDataFrame:
    """
    Load geopackage file based on metadata
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata row with file information
    code : str or int, optional
        Specific code to filter by
    name : str, optional
        Specific name to filter by
        
    Returns
    -------
    gpd.GeoDataFrame
        Loaded geodataframe
    """
    
    file_path = os.path.join(DATA_DIR, metadata['file'])
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Load the geopackage
    gdf = gpd.read_file(file_path)
    
    # Filter by code if specified
    if code is not None:
        code_col = metadata['code_column']
        
        if code_col not in gdf.columns:
            raise ValueError(f"Code column '{code_col}' not found in dataset")
        
        # Convert code to string for comparison
        code_str = str(code).zfill(2) if isinstance(code, int) else str(code)
        
        # Filter the data
        gdf = gdf[gdf[code_col].astype(str) == code_str]
    
    # Filter by name if specified
    elif name is not None:
        name_col = metadata['name_column']
        
        if name_col not in gdf.columns:
            raise ValueError(f"Name column '{name_col}' not found in dataset")
        
        # Filter by name (case insensitive)
        gdf = gdf[gdf[name_col].str.lower() == name.lower()]
    
    # If neither code nor name is specified, return all data
    # This is the case when we want to load the entire dataset
    
    return gdf.reset_index(drop=True)


def validate_code(code: Union[str, int], metadata: pd.Series) -> str:
    """
    Validate and format code according to metadata
    
    Parameters
    ----------
    code : str or int
        Code to validate
    metadata : pd.Series
        Metadata with code information
        
    Returns
    -------
    str
        Validated and formatted code
    """
    
    if code is None:
        return None
    
    # Convert to string and pad with zeros if it's a number
    if isinstance(code, int):
        return str(code).zfill(2)
    
    return str(code)


def validate_name(name: str, metadata: pd.Series) -> str:
    """
    Validate and format name according to metadata
    
    Parameters
    ----------
    name : str
        Name to validate
    metadata : pd.Series
        Metadata with name information
        
    Returns
    -------
    str
        Validated name
    """
    
    if name is None:
        return None
    
    return str(name).strip()


def download_gpkg_advanced(
    metadata: pd.Series, 
    code: Optional[Union[str, int]] = None, 
    name: Optional[str] = None,
    **kwargs
) -> gpd.GeoDataFrame:
    """
    Load geopackage file based on metadata with advanced filtering options
    
    Parameters
    ----------
    metadata : pd.Series
        Metadata row with file information
    code : str or int, optional
        Specific code to filter by
    name : str, optional
        Specific name to filter by
    **kwargs : optional
        Additional column-value pairs to filter by
        
    Returns
    -------
    gpd.GeoDataFrame
        Loaded geodataframe
    """
    
    file_path = os.path.join(DATA_DIR, metadata['file'])
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    # Load the geopackage
    gdf = gpd.read_file(file_path)
    
    # Filter by code if specified
    if code is not None:
        code_col = metadata['code_column']
        
        if code_col not in gdf.columns:
            raise ValueError(f"Code column '{code_col}' not found in dataset")
        
        # Convert code to string for comparison
        code_str = str(code).zfill(2) if isinstance(code, int) else str(code)
        
        # Filter the data
        gdf = gdf[gdf[code_col].astype(str) == code_str]
    
    # Filter by name if specified
    elif name is not None:
        name_col = metadata['name_column']
        
        if name_col not in gdf.columns:
            raise ValueError(f"Name column '{name_col}' not found in dataset")
        
        # Filter by name (case insensitive)
        gdf = gdf[gdf[name_col].str.lower() == name.lower()]
    
    # Filter by additional kwargs
    for column, value in kwargs.items():
        if column in gdf.columns and value is not None:
            # Case insensitive string comparison
            if gdf[column].dtype == 'object':
                gdf = gdf[gdf[column].str.lower() == str(value).lower()]
            else:
                gdf = gdf[gdf[column] == value]
    
    return gdf.reset_index(drop=True)


def list_available_years(geography: str) -> list:
    """
    List available years for a given geography
    
    Parameters
    ----------
    geography : str
        Type of geography
        
    Returns
    -------
    list
        Available years
    """
    
    metadata = load_metadata()
    filtered = metadata[metadata['geography'].str.lower() == geography.lower()]
    
    return sorted(filtered['year'].unique())
