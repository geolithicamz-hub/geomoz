"""
Testes básicos da biblioteca GeoMoz
"""

import pytest
import geopandas as gpd
import os

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import geomoz


def test_list_geometries():
    """Testa se a função list_geometries funciona"""
    geometries = geomoz.list_geometries()
    
    assert isinstance(geometries, dict)
    assert "province_2017" in geometries
    assert geometries["province_2017"]["type"] == "province"
    assert geometries["province_2017"]["year"] == 2017


def test_read_province():
    """Testa se a função read_province funciona"""
    gdf = geomoz.read_province()
    
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 11  # Moçambique tem 11 províncias
    assert "geometry" in gdf.columns
    assert gdf.crs.to_epsg() == 4326


def test_read_province_by_code():
    """Testa se a função read_province funciona com código específico"""
    nampula = geomoz.read_province(code="03")
    
    assert isinstance(nampula, gpd.GeoDataFrame)
    assert len(nampula) == 1
    assert nampula.iloc[0]["Provincia"] == "Nampula"


def test_list_provinces():
    """Testa se a função list_provinces funciona"""
    provinces = geomoz.list_provinces()
    
    assert isinstance(provinces, gpd.GeoDataFrame)
    assert len(provinces) == 11
    assert "CodProv" in provinces.columns
    assert "Provincia" in provinces.columns


def test_province_codes():
    """Testa se os códigos das províncias estão corretos"""
    provinces = geomoz.list_provinces()
    
    expected_codes = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11"]
    actual_codes = provinces["CodProv"].tolist()
    
    assert sorted(actual_codes) == sorted(expected_codes)


if __name__ == "__main__":
    # Executar testes manualmente
    test_list_geometries()
    test_read_province()
    test_read_province_by_code()
    test_list_provinces()
    test_province_codes()
    print("Todos os testes passaram!")
