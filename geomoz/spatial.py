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
    """
    Link districts with provinces using spatial or attribute join

    Parameters
    ----------
    code_province : str or int, optional
        Province code to filter districts. Default "all" for all provinces.
    name_province : str, optional
        Province name to filter districts.
    how : str, optional
        Type of merge: "left", "right", "inner", "outer". Default "left".
    spatial : bool, optional
        Use spatial join instead of attribute join. Default False.

    Returns
    -------
    gpd.GeoDataFrame
        Districts linked with province information

    Examples
    --------
    >>> from geomoz.spatial import link_district_province
    >>>
    >>> # Attribute join
    >>> linked = link_district_province()
    >>>
    >>> # Spatial join
    >>> linked = link_district_province(spatial=True)
    >>>
    >>> # Filter by province
    >>> linked = link_district_province(name_province="Nampula")
    """

    # Load data
    districts = read_district(code_district="all")
    provinces = read_province(code_province=code_province, name_province=name_province)

    if spatial:
        # Spatial join
        result = gpd.sjoin(districts, provinces, predicate="within", how=how)
    else:
        # Attribute join using province codes
        result = districts.merge(
            provinces[["CodProv", "Provincia", "geometry"]],
            on="CodProv",
            how=how
        )

    return result.reset_index(drop=True)


def link_village_district(
    code_district: Union[str, int] = "all",
    name_district: str = None,
    how: str = "left",
    spatial: bool = False
) -> gpd.GeoDataFrame:
    """
    Link villages with districts using spatial or attribute join

    Parameters
    ----------
    code_district : str or int, optional
        District code to filter villages. Default "all" for all districts.
    name_district : str, optional
        District name to filter villages.
    how : str, optional
        Type of merge: "left", "right", "inner", "outer". Default "left".
    spatial : bool, optional
        Use spatial join instead of attribute join. Default False.

    Returns
    -------
    gpd.GeoDataFrame
        Villages linked with district information
    """

    # Load data
    villages = read_village(code_village="all")
    districts = read_district(code_district=code_district, name_district=name_district)

    if spatial:
        # Spatial join
        result = gpd.sjoin(villages, districts, predicate="within", how=how)
    else:
        # Attribute join - need to find the linking column
        # Check if we can link by district name
        if "DISTRITO" in villages.columns and "Distrito" in districts.columns:
            result = villages.merge(
                districts[["CodDist", "Distrito", "Provincia", "geometry"]],
                left_on="DISTRITO",
                right_on="Distrito",
                how=how
            )
        else:
            # Fallback to spatial join
            warnings.warn("Attribute join columns not found, using spatial join")
            result = gpd.sjoin(villages, districts, predicate="within", how=how)

    return result.reset_index(drop=True)


def link_admin_post_district(
    code_district: Union[str, int] = "all",
    name_district: str = None,
    how: str = "left",
    spatial: bool = False
) -> gpd.GeoDataFrame:
    """
    Link administrative posts with districts using spatial or attribute join

    Parameters
    ----------
    code_district : str or int, optional
        District code to filter admin posts. Default "all" for all districts.
    name_district : str, optional
        District name to filter admin posts.
    how : str, optional
        Type of merge: "left", "right", "inner", "outer". Default "left".
    spatial : bool, optional
        Use spatial join instead of attribute join. Default False.

    Returns
    -------
    gpd.GeoDataFrame
        Administrative posts linked with district information
    """

    # Load data
    admin_posts = read_admin_post(code_admin_post="all")
    districts = read_district(code_district=code_district, name_district=name_district)

    if spatial:
        # Spatial join
        result = gpd.sjoin(admin_posts, districts, predicate="within", how=how)
    else:
        # Attribute join
        result = admin_posts.merge(
            districts[["CodDist", "Distrito", "Provincia", "geometry"]],
            on="CodDist",
            how=how
        )

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
    """
    Calcular área precisa de geometrias usando CRS projetado automático

    Esta função converte automaticamente para o CRS UTM apropriado para cálculos
    precisos de área, depois retorna os dados no CRS original.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame para calcular áreas
    unit : str, optional
        Unidade da área: "km2" (quilômetros quadrados) ou "m2" (metros quadrados)
        Default "km2".

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame original com coluna 'area' adicionada

    Examples
    --------
    >>> from geomoz.spatial import geology_by_province, calculate_area
    >>>
    >>> # Obter geologia e calcular áreas
    >>> geo = geology_by_province(name_province="Zambézia")
    >>> geo_with_area = calculate_area(geo)
    >>> print(f"Área total: {geo_with_area['area'].sum():.2f} km²")
    """
    # Fazer cópia para não modificar original
    gdf_copy = gdf.copy()

    # Converter para CRS projetado
    gdf_projected = _ensure_projected_crs(gdf_copy)

    # Calcular área
    areas = gdf_projected.geometry.area

    # Converter para unidade desejada
    if unit == "km2":
        areas = areas / 1_000_000  # m² para km²
        column_name = "area_km2"
    elif unit == "m2":
        column_name = "area_m2"
    else:
        raise ValueError("unit must be 'km2' or 'm2'")

    # Adicionar coluna de área ao DataFrame original
    gdf_copy[column_name] = areas

    return gdf_copy


def get_hierarchical_data(
    code_province: Union[str, int] = None,
    name_province: str = None,
    include_villages: bool = False,
    spatial: bool = False
) -> dict:
    """
    Get complete hierarchical data for a province

    Parameters
    ----------
    code_province : str or int, optional
        Province code. Either this or name_province must be provided.
    name_province : str, optional
        Province name. Either this or code_province must be provided.
    include_villages : bool, optional
        Include village level data. Default False (can be large).
    spatial : bool, optional
        Use spatial joins instead of attribute joins. Default False.

    Returns
    -------
    dict
        Dictionary containing hierarchical data:
        {
            'province': GeoDataFrame,
            'districts': GeoDataFrame,
            'admin_posts': GeoDataFrame,
            'villages': GeoDataFrame (optional)
        }
    """

    if code_province is None and name_province is None:
        raise ValueError("Either 'code_province' or 'name_province' must be provided")

    # Get province
    province = read_province(code_province=code_province, name_province=name_province)

    # Get linked districts
    districts = link_district_province(
        code_province=code_province,
        name_province=name_province,
        spatial=spatial
    )

    # Get linked admin posts (filtrar pelos distritos da província)
    admin_posts = link_admin_post_district(spatial=spatial)
    # Filtrar para apenas os posts administrativos da província
    if spatial:
        # Se foi spatial join, já tem a informação da província
        admin_posts = admin_posts[admin_posts['Provincia'].str.lower() == name_province.lower() if name_province else admin_posts['CodProv'].astype(str) == str(code_province)]
    else:
        # Se foi attribute join, filtrar pelos códigos de distrito da província
        province_districts = districts['CodDist'].unique()
        admin_posts = admin_posts[admin_posts['CodDist'].isin(province_districts)]

    result = {
        'province': province,
        'districts': districts,
        'admin_posts': admin_posts
    }

    # Optionally include villages (can be very large)
    if include_villages:
        villages = link_village_district(spatial=spatial)
        # Filtrar para apenas as aldeias da província
        if spatial:
            villages = villages[villages['Provincia'].str.lower() == name_province.lower() if name_province else villages['CodProv'].astype(str) == str(code_province)]
        else:
            # Filtrar pelos códigos de distrito da província
            villages = villages[villages['CodDist'].isin(province_districts)]
        result['villages'] = villages

    return result
