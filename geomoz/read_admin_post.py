"""
Read administrative post data for Mozambique
"""

import geopandas as gpd
from typing import Optional, Union

from .utils.data import get_data_path


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
    Data is automatically downloaded from Hugging Face and cached locally.

    Parameters
    ----------
    code_admin_post : str or int, optional
        The code of an administrative post.
        If code_admin_post="all", all administrative posts will be loaded (Default).
    name_admin_post : str, optional
        The name of an administrative post. Use this instead of code_admin_post
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
        Geodataframe containing administrative post data with columns:
        - CodPosto: Administrative post code
        - Posto: Administrative post name
        - CodDist: District code
        - Distrito: District name
        - CodProv: Province code
        - Provincia: Province name
        - geometry: Polygon geometries

    Examples
    --------
    >>> from geomoz import read_admin_post
    >>>
    >>> # Load all administrative posts
    >>> admin_posts = read_admin_post()
    >>>
    >>> # Load specific administrative post by code
    >>> posto = read_admin_post(code_admin_post="01")
    >>>
    >>> # Load specific administrative post by name
    >>> posto = read_admin_post(name_admin_post="Cidade de Lichinga")
    >>>
    >>> # Load with verbose output
    >>> admin_posts = read_admin_post(verbose=True)
    """

    # Validate input parameters
    if code_admin_post != "all" and name_admin_post is not None:
        raise ValueError("Cannot specify both code_admin_post and name_admin_post. Use one or the other.")

    # Get data path from Hugging Face
    filename = "adminpost_2017.gpkg"

    if verbose:
        print(f"Loading administrative post data from Hugging Face: {filename}")

    try:
        # Download and load data from Hugging Face
        data_path = get_data_path(filename)

        if verbose:
            print(f"Data loaded from: {data_path}")

        gdf = gpd.read_file(data_path)

    except Exception as e:
        raise RuntimeError(f"Failed to load administrative post data: {str(e)}")

    # Apply filters
    if code_admin_post != "all":
        # Filter by code
        if isinstance(code_admin_post, str):
            code_admin_post = code_admin_post.zfill(2)  # Ensure 2-digit format

        gdf = gdf[gdf['CodPosto'] == str(code_admin_post)]

        if verbose:
            print(f"Filtered to administrative post code: {code_admin_post}")

    elif name_admin_post is not None:
        # Filter by name (case insensitive)
        mask = gdf['Posto'].str.lower() == name_admin_post.lower()
        gdf = gdf[mask]

        if verbose:
            print(f"Filtered to administrative post name: {name_admin_post}")

    # Validate results
    if len(gdf) == 0:
        if code_admin_post != "all":
            raise ValueError(f"No administrative post found with code: {code_admin_post}")
        elif name_admin_post is not None:
            raise ValueError(f"No administrative post found with name: {name_admin_post}")

    return gdf.reset_index(drop=True)
