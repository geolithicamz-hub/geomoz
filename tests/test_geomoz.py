"""
Testes básicos da biblioteca GeoMoz.

Os testes estão divididos em dois grupos:

* Testes **offline** — não acessam a rede e validam a API pública,
  os metadados e o carregamento preguiçoso das funções de plot.
* Testes **de rede** (marcados com ``@pytest.mark.network``) — baixam dados
  reais do Hugging Face. Para pulá-los, execute:

      pytest -m "not network"
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import geomoz  # noqa: E402


# ---------------------------------------------------------------------------
# Testes offline (sem rede)
# ---------------------------------------------------------------------------

def test_import_and_version():
    """O pacote deve importar sem dependências opcionais (matplotlib etc.)."""
    assert isinstance(geomoz.__version__, str)
    assert "read_province" in dir(geomoz)


def test_plot_functions_are_lazy():
    """As funções de plot são expostas mas só carregam matplotlib quando usadas."""
    assert "plot_provinces" in dir(geomoz)


def test_list_available_geographies():
    geographies = geomoz.list_available_geographies()
    assert isinstance(geographies, list)
    assert "Province" in geographies
    assert "Geology" in geographies


def test_list_available_years():
    years = geomoz.list_available_years()
    assert 2017 in years
    assert 2006 in years


def test_get_dataset_info():
    info = geomoz.get_dataset_info("Province")
    assert len(info) == 1
    assert info.iloc[0]["function"] == "read_province"


def test_list_geomoz_runs(capsys):
    """list_geomoz() deve imprimir sem lançar exceções."""
    geomoz.list_geomoz()
    out = capsys.readouterr().out
    assert "read_province" in out


# ---------------------------------------------------------------------------
# Testes de rede (baixam dados reais do Hugging Face)
# ---------------------------------------------------------------------------

@pytest.mark.network
def test_read_province_all():
    import geopandas as gpd

    gdf = geomoz.read_province()
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 11  # Moçambique tem 11 províncias
    assert gdf.crs.to_epsg() == 4326


@pytest.mark.network
def test_read_province_by_name():
    gdf = geomoz.read_province(name_province="Nampula")
    assert len(gdf) == 1
    assert gdf.iloc[0]["Provincia"] == "Nampula"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
