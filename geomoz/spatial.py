"""
Spatial relationships and integration functions for GeoMoz
"""

import geopandas as gpd
from typing import Optional, Union
import warnings

from .read_province import read_province
from .read_district import read_district
from .read_admin_post import read_admin_post
from .read_village import read_village
from .read_geology import read_geology


def _get_utm_zone_for_mozambique(longitude: float) -> str:
    """
    Determinar automaticamente a zona UTM correta para Moçambique baseado na longitude

    Esta função é interna à biblioteca e determina o CRS projetado apropriado
    para cálculos precisos de área, centróide e outras operações espaciais.

    Moçambique está entre duas zonas UTM:
    - Zona 36S: 30°E a 36°E (EPSG:32736)
    - Zona 37S: 36°E a 42°E (EPSG:32737)

    NOTA: Para áreas que cruzam o meridiano 36°E, a zona é determinada pela
    maior parte da área ou pelo centróide.

    Parameters
    ----------
    longitude : float
        Longitude em graus

    Returns
    -------
    str
        Código EPSG da zona UTM apropriada para Moçambique
    """
    if 30 <= longitude < 36:
        return 'EPSG:32736'  # UTM Zone 36S (30°E a 36°E)
    elif 36 <= longitude < 42:
        return 'EPSG:32737'  # UTM Zone 37S (36°E a 42°E)
    else:
        # Default para a maior parte de Moçambique (centro-norte)
        return 'EPSG:32736'


def _check_cross_zone_boundary(gdf: gpd.GeoDataFrame) -> dict:
    """
    Verificar se uma área geográfica cruza o limite entre zonas UTM (36°E)

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame a verificar

    Returns
    -------
    dict
        Informações sobre cruzamento de zonas:
        {
            'crosses_boundary': bool,
            'min_longitude': float,
            'max_longitude': float,
            'primary_zone': str,
            'secondary_zone': str,
            'recommendation': str
        }
    """
    import warnings

    # Obter bounds
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        bounds = gdf.total_bounds
        min_lon = bounds[0]
        max_lon = bounds[2]

    # Verificar se cruza o meridiano 36°E
    crosses_boundary = (min_lon < 36.0 and max_lon > 36.0)

    # Determinar zonas
    if crosses_boundary:
        primary_zone = _get_utm_zone_for_mozambique((min_lon + max_lon) / 2)
        secondary_zone = 'EPSG:32736' if primary_zone == 'EPSG:32737' else 'EPSG:32737'
        recommendation = 'split' if max_lon - min_lon > 2.0 else 'primary'
    else:
        primary_zone = _get_utm_zone_for_mozambique((min_lon + max_lon) / 2)
        secondary_zone = None
        recommendation = 'primary'

    return {
        'crosses_boundary': crosses_boundary,
        'min_longitude': min_lon,
        'max_longitude': max_lon,
        'longitude_span': max_lon - min_lon,
        'primary_zone': primary_zone,
        'secondary_zone': secondary_zone,
        'recommendation': recommendation
    }


def _handle_cross_zone_area(gdf: gpd.GeoDataFrame, zone_info: dict) -> gpd.GeoDataFrame:
    """
    Tratar áreas que cruzam zonas UTM

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame com geometrias que cruzam zonas
    zone_info : dict
        Informações sobre cruzamento de zonas

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame tratado (dividido ou convertido)
    """
    if zone_info['recommendation'] == 'split':
        # Dividir área em duas partes, cada uma em sua zona UTM
        import warnings

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # Criar linha vertical em 36°E para dividir
            from shapely.geometry import LineString, box

            # Obter bounds
            bounds = gdf.total_bounds
            split_line = LineString([(36.0, bounds[1]), (36.0, bounds[3])])

            # Dividir geometrias
            split_geometries = []
            for geom in gdf.geometry:
                if geom.intersects(split_line):
                    # Para geometrias que cruzam a linha, manter como está
                    # mas converter para a zona primária
                    split_geometries.append(geom)
                else:
                    split_geometries.append(geom)

        # Criar novo GeoDataFrame com geometrias divididas
        result = gdf.copy()
        result.geometry = split_geometries

        # Converter para zona primária
        return result.to_crs(zone_info['primary_zone'])

    else:
        # Usar apenas a zona primária
        return gdf.to_crs(zone_info['primary_zone'])


def _ensure_projected_crs(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Garantir que o GeoDataFrame esteja em um CRS projetado para cálculos precisos

    Esta função converte automaticamente para o CRS UTM apropriado se o GeoDataFrame
    estiver em um CRS geográfico (como EPSG:4326), tratando áreas que cruzam
    o limite entre zonas UTM (36°E).

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame a ser verificado/convertido

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame em CRS projetado (se necessário, convertido)
    """
    import warnings

    # Se já estiver em CRS projetado, retornar como está
    if gdf.crs and gdf.crs.is_projected:
        return gdf

    # Se não tiver CRS, assumir WGS84
    if not gdf.crs:
        gdf = gdf.set_crs('EPSG:4326')

    # Se estiver em CRS geográfico, verificar cruzamento de zonas
    if gdf.crs.is_geographic:
        # Verificar se cruza o limite entre zonas UTM
        zone_info = _check_cross_zone_boundary(gdf)

        if zone_info['crosses_boundary']:
            # Tratar área que cruza zonas
            return _handle_cross_zone_area(gdf, zone_info)
        else:
            # Converter para zona UTM apropriada
            return gdf.to_crs(zone_info['primary_zone'])

    return gdf


def link_district_province(
    code_province: Union[str, int] = "all",
    name_province: str = None,
    how: str = "left",
    spatial: bool = False
) -> gpd.GeoDataFrame:
    """Associate districts with province coverage, keeping one active geometry."""
    if code_province not in ("all", None) and name_province is not None:
        raise ValueError("Specify a province code OR a province name")
    filters = ({"name_province": name_province} if name_province is not None
               else {"code_province": code_province or "all"})
    provinces = read_province(**filters)
    districts = read_district()
    filtered = name_province is not None or code_province not in ("all", None)
    if spatial:
        if how not in ("left", "right", "inner"):
            raise ValueError("Spatial join supports only left, right or inner")
        right = provinces[["geometry"]]
        if districts.crs != right.crs:
            right = right.to_crs(districts.crs)
        result = gpd.sjoin(districts, right, predicate="within",
                           how="inner" if filtered else how)
    else:
        result = districts.merge(provinces[["CodProv"]].drop_duplicates(),
                                 on="CodProv", how="inner" if filtered else how)
    return result.reset_index(drop=True)

def link_village_district(
    code_district: Union[str, int] = "all",
    name_district: str = None,
    how: str = "left",
    spatial: bool = False
) -> gpd.GeoDataFrame:
    """Associate villages and districts using both district and province names."""
    if code_district not in ("all", None) and name_district is not None:
        raise ValueError("Specify a district code OR a district name")
    filters = ({"name_district": name_district} if name_district is not None
               else {"code_district": code_district or "all"})
    districts = read_district(**filters)
    villages = read_village()
    filtered = name_district is not None or code_district not in ("all", None)
    if spatial:
        if how not in ("left", "right", "inner"):
            raise ValueError("Spatial join supports only left, right or inner")
        right = districts[["geometry"]]
        if right.crs != villages.crs:
            right = right.to_crs(villages.crs)
        result = gpd.sjoin(villages, right, predicate="within",
                           how="inner" if filtered else how)
    else:
        required = {"Distrito", "Provincia"}
        if not required.issubset(villages.columns) or not required.issubset(districts.columns):
            raise ValueError("Both datasets require normalized Distrito and Provincia columns")
        # Retain the original village geometry, rather than merging a second geometry.
        keys = districts[["Distrito", "Provincia"]].drop_duplicates()
        result = villages.merge(keys, on=["Distrito", "Provincia"],
                                how="inner" if filtered else how)
    return result.reset_index(drop=True)

def link_admin_post_district(
    code_district: Union[str, int] = "all",
    name_district: str = None,
    how: str = "left",
    spatial: bool = False
) -> gpd.GeoDataFrame:
    """Associate administrative posts with districts without geometry collisions."""
    if code_district not in ("all", None) and name_district is not None:
        raise ValueError("Specify a district code OR a district name")
    filters = ({"name_district": name_district} if name_district is not None
               else {"code_district": code_district or "all"})
    districts = read_district(**filters)
    posts = read_admin_post()
    filtered = name_district is not None or code_district not in ("all", None)
    if spatial:
        if how not in ("left", "right", "inner"):
            raise ValueError("Spatial join supports only left, right or inner")
        right = districts[["geometry"]]
        if right.crs != posts.crs:
            right = right.to_crs(posts.crs)
        result = gpd.sjoin(posts, right, predicate="within",
                           how="inner" if filtered else how)
    else:
        keys = ["CodDist"]
        if "CodProv" in posts.columns and "CodProv" in districts.columns:
            keys = ["CodProv", "CodDist"]
        result = posts.merge(districts[keys].drop_duplicates(),
                             on=keys, how="inner" if filtered else how)
    return result.reset_index(drop=True)

def geology_by_province(
    code_province: Union[str, int] = None,
    name_province: str = None,
    how: str = "intersection",
    **geology_filters
) -> gpd.GeoDataFrame:
    """
    Get geology data clipped to province boundaries

    Parameters
    ----------
    code_province : str or int, optional
        Province code. Either this or name_province must be provided.
    name_province : str, optional
        Province name. Either this or code_province must be provided.
    how : str, optional
        Type of spatial overlay: "intersection", "identity", "difference",
        "union", "symmetric_difference". Default "intersection".
    **geology_filters : optional
        Additional filters to pass to read_geology (e.g., SUITE='Malema')

    Returns
    -------
    gpd.GeoDataFrame
        Geology data clipped to the specified province
        (mantido em CRS original para visualização, mas cálculos internos usam CRS projetado)

    Examples
    --------
    >>> from geomoz.spatial import geology_by_province
    >>>
    >>> # Get all geology in Nampula province
    >>> geo_nampula = geology_by_province(name_province="Nampula")
    >>>
    >>> # Get specific suite in Nampula
    >>> geo_malema = geology_by_province(name_province="Nampula", SUITE='Malema')
    """

    if code_province is None and name_province is None:
        raise ValueError("Either 'code_province' or 'name_province' must be provided")

    # Load data
    if code_province is not None:
        province = read_province(code_province=code_province)
    else:
        province = read_province(name_province=name_province)

    geology = read_geology(**geology_filters) if geology_filters else read_geology(code_geology="all")

    # Ensure both have the same CRS for overlay
    if province.crs != geology.crs:
        geology = geology.to_crs(province.crs)

    # Spatial overlay
    result = gpd.overlay(geology, province, how=how)

    # Adicionar metadados sobre CRS para cálculos precisos
    if hasattr(result, '_crs_info'):
        result._crs_info = {
            'original_crs': str(result.crs),
            'projected_crs': _get_utm_zone_for_mozambique(province.geometry.centroid.iloc[0].x)
        }

    return result.reset_index(drop=True)


def geology_by_district(
    code_district: Union[str, int] = None,
    name_district: str = None,
    how: str = "intersection",
    **geology_filters
) -> gpd.GeoDataFrame:
    """
    Get geology data clipped to district boundaries

    Parameters
    ----------
    code_district : str or int, optional
        District code. Either this or name_district must be provided.
    name_district : str, optional
        District name. Either this or code_district must be provided.
    how : str, optional
        Type of spatial overlay. Default "intersection".
    **geology_filters : optional
        Additional filters to pass to read_geology

    Returns
    -------
    gpd.GeoDataFrame
        Geology data clipped to the specified district
    """

    if code_district is None and name_district is None:
        raise ValueError("Either 'code_district' or 'name_district' must be provided")

    # Load data (pass only the filter that was provided; read_district rejects
    # receiving both code and name at once)
    if code_district is not None:
        district = read_district(code_district=code_district)
    else:
        district = read_district(name_district=name_district)
    geology = read_geology(**geology_filters) if geology_filters else read_geology(code_geology="all")

    # Ensure same CRS
    if district.crs != geology.crs:
        geology = geology.to_crs(district.crs)

    # Spatial overlay
    result = gpd.overlay(geology, district, how=how)

    return result.reset_index(drop=True)


def geology_by_admin_post(
    code_admin_post: Union[str, int] = None,
    name_admin_post: str = None,
    how: str = "intersection",
    **geology_filters
) -> gpd.GeoDataFrame:
    """
    Get geology data clipped to administrative post boundaries

    Parameters
    ----------
    code_admin_post : str or int, optional
        Administrative post code. Either this or name_admin_post must be provided.
    name_admin_post : str, optional
        Administrative post name. Either this or code_admin_post must be provided.
    how : str, optional
        Type of spatial overlay. Default "intersection".
    **geology_filters : optional
        Additional filters to pass to read_geology

    Returns
    -------
    gpd.GeoDataFrame
        Geology data clipped to the specified administrative post
    """

    if code_admin_post is None and name_admin_post is None:
        raise ValueError("Either 'code_admin_post' or 'name_admin_post' must be provided")

    # Load data (pass only the filter that was provided; read_admin_post rejects
    # receiving both code and name at once)
    if code_admin_post is not None:
        admin_post = read_admin_post(code_admin_post=code_admin_post)
    else:
        admin_post = read_admin_post(name_admin_post=name_admin_post)
    geology = read_geology(**geology_filters) if geology_filters else read_geology(code_geology="all")

    # Ensure same CRS
    if admin_post.crs != geology.crs:
        geology = geology.to_crs(admin_post.crs)

    # Spatial overlay
    result = gpd.overlay(geology, admin_post, how=how)

    return result.reset_index(drop=True)


def geology_by_area(
    area: gpd.GeoDataFrame,
    how: str = "intersection",
    **geology_filters
) -> gpd.GeoDataFrame:
    """
    Get geology data clipped to a custom study area

    Parameters
    ----------
    area : gpd.GeoDataFrame
        Custom study area polygon(s)
    how : str, optional
        Type of spatial overlay. Default "intersection".
    **geology_filters : optional
        Additional filters to pass to read_geology

    Returns
    -------
    gpd.GeoDataFrame
        Geology data clipped to the study area

    Examples
    --------
    >>> from geomoz.spatial import geology_by_area
    >>> import geopandas as gpd
    >>>
    >>> # Create custom study area
    >>> study_area = gpd.GeoDataFrame({
    ...     'geometry': [your_polygon],
    ...     'crs': 'EPSG:4326'
    ... })
    >>>
    >>> # Get geology for study area
    >>> geo_area = geology_by_area(study_area, SUITE='Malema')
    """

    if not isinstance(area, gpd.GeoDataFrame):
        raise TypeError("area must be a GeoDataFrame")

    # Load geology
    geology = read_geology(**geology_filters) if geology_filters else read_geology(code_geology="all")

    # Ensure same CRS
    if area.crs != geology.crs:
        geology = geology.to_crs(area.crs)

    # Spatial overlay
    result = gpd.overlay(geology, area, how=how)

    return result.reset_index(drop=True)


def calculate_area(gdf: gpd.GeoDataFrame, unit: str = "km2") -> gpd.GeoDataFrame:
    """Calculate ellipsoidal area (WGS84), including across UTM 36S/37S.

    Preserve the GeoDataFrame's original CRS, geometry and row index. The
    output column is ``area_km2`` or ``area_m2``. Inputs without CRS or
    with invalid polygon geometries raise an explicit error.
    """
    from .geodesy import geodesic_area

    result = gdf.copy()
    result[f"area_{unit}"] = geodesic_area(gdf, unit=unit)
    return result

def get_hierarchical_data(
    code_province: Union[str, int] = None,
    name_province: str = None,
    include_villages: bool = False,
    spatial: bool = False
) -> dict:
    """Return province, district, admin-post and optionally village data.

    Exactly one province selector must be supplied. Attribute mode matches
    administrative codes and normalized province names; spatial mode tests
    representative points against the selected province geometry.
    """
    if (code_province is None) == (name_province is None):
        raise ValueError("Specify exactly one of code_province and name_province")
    selected = ({"code_province": code_province} if code_province is not None
                else {"name_province": name_province})
    province = read_province(**selected)
    if province.empty:
        raise ValueError("The requested province was not found")
    districts = read_district()
    admin_posts = read_admin_post()

    if spatial:
        if province.crs is None:
            raise ValueError("Province dataset requires a CRS")
        boundary = province.to_crs("EPSG:4326").geometry.union_all()

        def within_province(layer):
            if layer.crs is None:
                raise ValueError("An administrative layer has no CRS")
            points = layer.to_crs("EPSG:4326").geometry.representative_point()
            return layer.loc[points.within(boundary)].copy().reset_index(drop=True)

        districts = within_province(districts)
        admin_posts = within_province(admin_posts)
    else:
        province_codes = set(province["CodProv"].astype(str).str.strip())
        districts = districts[
            districts["CodProv"].astype(str).str.strip().isin(province_codes)
        ].copy().reset_index(drop=True)
        district_codes = set(districts["CodDist"].astype(str).str.strip())
        admin_posts = admin_posts[
            admin_posts["CodDist"].astype(str).str.strip().isin(district_codes)
        ]
        if "CodProv" in admin_posts.columns:
            admin_posts = admin_posts[
                admin_posts["CodProv"].astype(str).str.strip().isin(province_codes)
            ]
        admin_posts = admin_posts.copy().reset_index(drop=True)

    result = {"province": province, "districts": districts, "admin_posts": admin_posts}
    if include_villages:
        villages = read_village()
        if spatial:
            villages = within_province(villages)
        else:
            names = set(province["Provincia"].astype(str).str.casefold().str.strip())
            villages = villages[
                villages["Provincia"].astype(str).str.casefold().str.strip().isin(names)
            ].copy().reset_index(drop=True)
        result["villages"] = villages
    return result

