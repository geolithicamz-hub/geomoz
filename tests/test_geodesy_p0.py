"""Offline geodesic regressions: UTM boundary, CRS, holes and invalid inputs."""
import geopandas as gpd
import pytest
from pyproj import Geod
from shapely.geometry import Polygon, MultiPolygon, Point
from geomoz.geodesy import geodesic_area
from geomoz.spatial import calculate_area


@pytest.fixture
def crossing():
    return Polygon([(35.5, -20), (36.5, -20), (36.5, -19), (35.5, -19)])


def test_cross_zone_ellipsoidal_area(crossing):
    gdf = gpd.GeoDataFrame(geometry=[crossing], crs="EPSG:4326")
    expected = abs(Geod(ellps="WGS84").geometry_area_perimeter(crossing)[0])
    actual = calculate_area(gdf, unit="m2")
    assert actual.area_m2.iloc[0] == pytest.approx(expected, rel=1e-12)
    assert actual.crs == gdf.crs
    assert actual.geometry.equals(gdf.geometry)
    assert "area_m2" not in gdf.columns


def test_utm_reprojection_invariance(crossing):
    src = gpd.GeoDataFrame(geometry=[crossing], crs="EPSG:4326")
    projected = src.to_crs("EPSG:32736")
    assert geodesic_area(projected).iloc[0] == pytest.approx(
        geodesic_area(src).iloc[0], rel=2e-8)


def test_multipolygon_with_hole():
    donut = Polygon(
        [(32, -20), (33, -20), (33, -19), (32, -19)],
        [[(32.2, -19.8), (32.8, -19.8), (32.8, -19.2), (32.2, -19.2)]],
    )
    piece = Polygon([(35, -16), (36, -16), (36, -15), (35, -15)])
    gdf = gpd.GeoDataFrame(geometry=[donut, MultiPolygon([donut, piece])], crs=4326)
    vals = geodesic_area(gdf, "m2")
    assert vals.iloc[0] > 0
    assert vals.iloc[1] > vals.iloc[0]


def test_crs_required(crossing):
    with pytest.raises(ValueError, match="no CRS"):
        geodesic_area(gpd.GeoDataFrame(geometry=[crossing]))


def test_empty_and_point_geometries():
    gdf = gpd.GeoDataFrame(geometry=[Point(32, -20), Polygon()], crs=4326)
    assert geodesic_area(gdf).tolist() == [0, 0]


def test_empty_gdf_and_invalid_unit():
    gdf = gpd.GeoDataFrame(geometry=[], crs=4326)
    assert "area_km2" in calculate_area(gdf).columns
    with pytest.raises(ValueError, match="unit"):
        calculate_area(gdf, unit="ha")


def test_invalid_polygon_rejected():
    invalid = Polygon([(32, -20), (33, -19), (32, -19), (33, -20)])
    gdf = gpd.GeoDataFrame(geometry=[invalid], crs=4326)
    with pytest.raises(ValueError, match="Invalid geometry"):
        geodesic_area(gdf)
