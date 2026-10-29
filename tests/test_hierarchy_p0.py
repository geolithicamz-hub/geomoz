"""Offline synthetic administration-level regressions without network access."""
import geopandas as gpd
import pytest
from shapely.geometry import box, Point
import geomoz.spatial as spatial


@pytest.fixture
def layers(monkeypatch):
    prov = gpd.GeoDataFrame(
        {"CodProv": ["01"], "Provincia": ["Maputo"]},
        geometry=[box(32, -26, 34, -24)], crs=4326)
    districts = gpd.GeoDataFrame(
        {"CodProv": ["01", "02"], "CodDist": ["0101", "0201"],
         "Distrito": ["Boane", "Nampula"], "Provincia": ["Maputo", "Nampula"]},
        geometry=[box(32.1, -25.8, 33, -24.5), box(37, -16, 38, -15)], crs=4326)
    posts = gpd.GeoDataFrame(
        {"CodDist": ["0101", "0201"], "Posto": ["Boane", "Outro"],
         "Provincia": ["Maputo", "Nampula"]},
        geometry=[box(32.2, -25.6, 32.5, -25), box(37.1, -15.8, 37.4, -15.3)], crs=4326)
    villages = gpd.GeoDataFrame(
        {"Provincia": ["Maputo", "Nampula"], "Distrito": ["Boane", "Nampula"],
         "Povoacao": ["Povoacao A", "Povoacao B"]},
        geometry=[Point(32.3, -25.2), Point(37.2, -15.4)], crs=4326)
    def read_province(code_province="all", name_province=None):
        if code_province not in ("all", None):
            return prov.loc[prov.CodProv == str(code_province)].copy()
        if name_province is not None:
            return prov.loc[prov.Provincia == name_province].copy()
        return prov
    def read_district(code_district="all", name_district=None):
        if code_district not in ("all", None):
            return districts.loc[districts.CodDist == str(code_district)].copy()
        if name_district is not None:
            return districts.loc[districts.Distrito == name_district].copy()
        return districts
    monkeypatch.setattr(spatial, "read_province", read_province)
    monkeypatch.setattr(spatial, "read_district", read_district)
    monkeypatch.setattr(spatial, "read_admin_post", lambda **kw: posts)
    monkeypatch.setattr(spatial, "read_village", lambda **kw: villages)


@pytest.mark.parametrize("selector", [{"name_province": "Maputo"}, {"code_province": "01"}])
@pytest.mark.parametrize("spatial_mode", [False, True])
def test_descendants_filtered(layers, selector, spatial_mode):
    result = spatial.get_hierarchical_data(
        **selector, include_villages=True, spatial=spatial_mode)
    assert result["districts"].Distrito.tolist() == ["Boane"]
    assert result["admin_posts"].Posto.tolist() == ["Boane"]
    assert result["villages"].Povoacao.tolist() == ["Povoacao A"]


def test_ambiguous_selector(layers):
    with pytest.raises(ValueError, match="exactly one"):
        spatial.get_hierarchical_data()
    with pytest.raises(ValueError, match="exactly one"):
        spatial.get_hierarchical_data(code_province="01", name_province="Maputo")


def test_join_helpers(layers):
    assert spatial.link_district_province(name_province="Maputo").Distrito.tolist() == ["Boane"]
    assert spatial.link_admin_post_district(name_district="Boane").Posto.tolist() == ["Boane"]
    assert spatial.link_village_district(name_district="Boane").Povoacao.tolist() == ["Povoacao A"]


@pytest.mark.parametrize("spatial_mode", [False, True])
def test_filtered_joins_do_not_leak(layers, spatial_mode):
    assert spatial.link_district_province(name_province="Maputo", spatial=spatial_mode).shape[0] == 1
    assert spatial.link_admin_post_district(name_district="Boane", spatial=spatial_mode).shape[0] == 1
    assert spatial.link_village_district(name_district="Boane", spatial=spatial_mode).shape[0] == 1
