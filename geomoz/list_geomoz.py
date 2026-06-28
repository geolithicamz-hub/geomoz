"""
List available datasets in GeoMoz package
"""

import pandas as pd
from .utils import load_metadata


def list_geomoz():
    """
    Print available datasets in GeoMoz package

    Example output
    ------------------------------
    Function: read_province
    Geography available: Province
    Years available: 2017
    Source: INE Moçambique
    ------------------------------
    Function: read_district
    Geography available: District
    Years available: 2017
    Source: INE Moçambique
    ------------------------------
    """

    metadata = load_metadata()

    for i in range(len(metadata)):
        row = metadata.iloc[i]

        print(f"Function: {row['function']}")
        print(f"Geography available: {row['geography']}")
        print(f"Years available: {row['year']}")
        print(f"Source: {row['source']}")
        print("------------------------------")


def list_available_geographies():
    """
    List all available geographies in GeoMoz

    Returns
    -------
    list
        Available geography types
    """

    metadata = load_metadata()
    return sorted(metadata['geography'].unique())


def list_available_years():
    """
    List all available years in GeoMoz

    Returns
    -------
    list
        Available years
    """

    metadata = load_metadata()
    return sorted(metadata['year'].unique())


def get_dataset_info(geography: str, year: int = None) -> pd.DataFrame:
    """
    Get detailed information about a specific dataset

    Parameters
    ----------
    geography : str
        Type of geography
    year : int, optional
        Year of the data

    Returns
    -------
    pd.DataFrame
        Dataset information
    """

    metadata = load_metadata()

    # Filter by geography
    filtered = metadata[metadata['geography'].str.lower() == geography.lower()]

    # Filter by year if specified
    if year is not None:
        filtered = filtered[filtered['year'] == year]

    return filtered
