"""Ellipsoidal WGS84 area measurements with explicit CRS and geometry checks."""
from __future__ import annotations

import geopandas as gpd
import pandas as pd
from pyproj import Geod
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection
from shapely.ops import orient

_GEOD = Geod(ellps="WGS84")


def _area_m2(geometry):
    if geometry is None:
        return float("nan")
    if geometry.is_empty:
        return 0.0
    if not geometry.is_valid:
        raise ValueError("Invalid geometry: repair it before measuring area.")
    if isinstance(geometry, Polygon):
        return abs(_GEOD.geometry_area_perimeter(orient(geometry, sign=1.0))[0])
    if isinstance(geometry, (MultiPolygon, GeometryCollection)):
        return sum(_area_m2(part) for part in geometry.geoms)
    return 0.0


def geodesic_area(gdf: gpd.GeoDataFrame, unit: str = "km2") -> pd.Series:
    """Return areas on WGS84, preserving GeoDataFrame index.

    Point/line/empty geometries produce 0, missing geometry produces NaN.
    Geometries are transformed to EPSG:4326 if required; input is unchanged.
    Not intended for surveying-grade cadastral measurement.
    """
    if not isinstance(gdf, gpd.GeoDataFrame):
        raise TypeError("gdf must be a GeoDataFrame")
    if gdf.crs is None:
        raise ValueError("GeoDataFrame has no CRS; set it explicitly before measurement")
    if unit not in ("km2", "m2"):
        raise ValueError("unit must be 'km2' or 'm2'")
    original = gdf.to_crs("EPSG:4326")
    divisor = 1000000.0 if unit == "km2" else 1.0
    return pd.Series(
        (_area_m2(geom) / divisor for geom in original.geometry),
        index=gdf.index,
        name=f"area_{unit}",
        dtype="float64",
    )
