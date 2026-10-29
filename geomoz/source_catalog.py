"""Provenance-first registry of *external* Mozambican geospatial datasets.

This module contains references and metadata only. It never downloads,
redistributes, or implies permission to redistribute external datasets.
"""
import json
from copy import deepcopy

_DATASETS = json.loads(r'''[
  {
    "id": "mireme_geology_250k",
    "title": "Seamless Geology 250K",
    "category": "geology",
    "producer": "MIREME/MIS",
    "distributor": "MIREME/MIS",
    "year": null,
    "url": "https://mis.mireme.gov.mz/server/rest/services/Website/Map/MapServer/4",
    "format": "ArcGIS REST Feature Layer",
    "geometry": "Polygon",
    "crs": "EPSG:4130",
    "verification": "service_metadata_verified",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Contains code2006, Legend, ERA, SUITE, Formation. Exact match with existing GeoMoz GeoPackage must be validated."
  },
  {
    "id": "mireme_structures_250k",
    "title": "Geological Structures 250K",
    "category": "geology",
    "producer": "MIREME/MIS",
    "distributor": "MIREME/MIS",
    "year": null,
    "url": "https://mis.mireme.gov.mz/server/rest/services/Website/Map/MapServer/3",
    "format": "ArcGIS REST Feature Layer",
    "geometry": "LineString",
    "crs": "EPSG:4130",
    "verification": "service_metadata_verified",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Structures include faults and shear zones; vector layer ID 3."
  },
  {
    "id": "mireme_mineral_occurrences",
    "title": "Mineral Occurrences",
    "category": "minerals",
    "producer": "MIREME/MIS",
    "distributor": "MIREME/MIS",
    "year": null,
    "url": "https://mis.mireme.gov.mz/server/rest/services/Website/GeoEconomic_Data/MapServer/0",
    "format": "ArcGIS REST Feature Layer",
    "geometry": "Point",
    "crs": "EPSG:4130",
    "verification": "service_metadata_verified",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Mineral occurrence points with commodity-related attributes."
  },
  {
    "id": "data4moz_soils_1995",
    "title": "Tipos de Solo",
    "category": "soils",
    "producer": "INIA",
    "distributor": "DataPortal/Data4Moz",
    "year": 1995,
    "url": "https://dataportal.co.mz/dataset/116",
    "format": "Shapefile",
    "geometry": "Polygon",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Portal reports 2,526 polygons; check attributes and coordinates."
  },
  {
    "id": "data4moz_basins_2015",
    "title": "Bacias Hidrograficas",
    "category": "hydrology",
    "producer": "DNGRH",
    "distributor": "DataPortal/Data4Moz",
    "year": 2015,
    "url": "https://dataportal.co.mz/dataset/118",
    "format": "Shapefile",
    "geometry": "Polygon",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Contains basin area, perimeter, elevation and slope attributes."
  },
  {
    "id": "data4moz_districts_2017",
    "title": "Limite de Distritos",
    "category": "administrative",
    "producer": "CENACARTA",
    "distributor": "DataPortal/Data4Moz",
    "year": 2017,
    "url": "https://dataportal.co.mz/dataset/3",
    "format": "Shapefile",
    "geometry": "Polygon",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Portal reports 162 features vs 161 districts documented in GeoMoz; verify duplicates and counting methodology."
  },
  {
    "id": "data4moz_neighbourhoods_2016",
    "title": "Limite dos Bairros",
    "category": "administrative",
    "producer": "INE",
    "distributor": "DataPortal/Data4Moz",
    "year": 2016,
    "url": "https://dataportal.co.mz/dataset/25",
    "format": "Shapefile",
    "geometry": "Polygon",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Local administrative boundaries; verify geographic completeness."
  },
  {
    "id": "data4moz_roads_2010",
    "title": "Estradas Condicoes",
    "category": "transport",
    "producer": "ANE",
    "distributor": "DataPortal/Data4Moz",
    "year": 2010,
    "url": "https://dataportal.co.mz/dataset/6",
    "format": "Shapefile",
    "geometry": "LineString",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Road class and surface type; historical 2010 snapshot."
  },
  {
    "id": "data4moz_airports_2020",
    "title": "Aeroportos Nacionais",
    "category": "transport",
    "producer": "IACM",
    "distributor": "DataPortal/Data4Moz",
    "year": 2020,
    "url": "https://dataportal.co.mz/dataset/5",
    "format": "Shapefile",
    "geometry": "Point",
    "crs": null,
    "verification": "source_listed_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Airport and aerodrome positions; verify current operational status."
  },
  {
    "id": "data4moz_rainfall_2024",
    "title": "Precipitacao provincial 2024",
    "category": "climate",
    "producer": "INAM (as attributed by DataPortal)",
    "distributor": "DataPortal/Data4Moz",
    "year": 2024,
    "url": "https://dataportal.co.mz/dataset/219",
    "format": "GeoJSON",
    "geometry": "Polygon",
    "crs": null,
    "verification": "source_not_verified_by_portal",
    "redistribution": "permission_unverified",
    "access": "reference_only",
    "note": "Rainfall described for provincial capitals, attached to province polygons; not province-wide observations."
  }
]''')


def list_source_datasets(category=None, distributor=None):
    """List external data references; optionally filter by category/distributor.

    Every record is metadata-only and its redistribution remains unverified.
    Returned dictionaries are independent copies.
    """
    for key, value in (("category", category), ("distributor", distributor)):
        if value is not None and (not isinstance(value, str) or not value.strip()):
            raise ValueError(f"{key} must be a non-empty string or None")
    return [
        deepcopy(item)
        for item in _DATASETS
        if (category is None or item["category"] == category)
        and (distributor is None or item["distributor"] == distributor)
    ]


def get_source_dataset(dataset_id):
    """Return one metadata record. Unknown IDs raise KeyError."""
    if not isinstance(dataset_id, str):
        raise TypeError("dataset_id must be a string")
    for item in _DATASETS:
        if item["id"] == dataset_id:
            return deepcopy(item)
    raise KeyError(f"Unknown external dataset: {dataset_id}")
