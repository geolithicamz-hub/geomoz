"""
Integration tests that exercise the real documented workflows against the
actual data downloaded from Hugging Face. These guard against regressions in
the exact flows shown in the usage guides.

Run only these with:  pytest -m network tests/test_integration.py
Skip them offline with: pytest -m "not network"
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import geomoz  # noqa: E402
from geomoz.spatial import (  # noqa: E402
    geology_by_province,
    geology_by_district,
    geology_by_admin_post,
)

pytestmark = pytest.mark.network


def test_village_has_normalized_columns():
    """read_village must expose Provincia/Distrito/Posto/Povoacao."""
    villages = geomoz.read_village()
    for col in ("Provincia", "Distrito", "Posto", "Povoacao"):
        assert col in villages.columns, f"missing normalized column {col}"
    nampula = villages[villages["Provincia"] == "Nampula"]
    assert len(nampula) > 0


def test_load_all_layers_by_province():
    """The 'load everything by province' guide flow must work uniformly."""
    name = "Nampula"
    geomoz.read_province(name_province=name)
    districts = geomoz.read_district()
    posts = geomoz.read_admin_post()
    villages = geomoz.read_village()

    assert len(districts[districts["Provincia"] == name]) > 0
    assert len(posts[posts["Provincia"] == name]) > 0
    assert len(villages[villages["Provincia"] == name]) > 0


def test_geology_by_province_name():
    geo = geology_by_province(name_province="Tete")
    assert len(geo) > 0
    assert "ERA" in geo.columns


def test_geology_by_district_name():
    """Regression: previously raised 'Cannot specify both code and name'."""
    geo = geology_by_district(name_district="Cidade de Tete")
    assert len(geo) > 0


def test_geology_by_admin_post_name():
    some_post = geomoz.read_admin_post().iloc[0]["Posto"]
    geo = geology_by_admin_post(name_admin_post=some_post)
    assert geo is not None


def test_era_classification_covers_data():
    """The guide's era-normalization should classify nearly all polygons."""
    geo = geology_by_province(name_province="Tete")

    def classify(value):
        v = str(value).upper()
        if "ARCHEAN" in v:
            return "Arqueano"
        if "PROTEROZOIC" in v:
            return "Proterozoico"
        if "PALEOZOIC" in v or v in ("CAMBRIAN", "ORDOVISIAN"):
            return "Paleozoico"
        if "MESOZOIC" in v or v in ("JURRASSIC", "CRETACEOUS"):
            return "Mesozoico"
        if "CENOZOIC" in v or v in ("TERTIARY", "QUATERNARY"):
            return "Cenozoico"
        return "Outro"

    eras = geo["ERA"].map(classify)
    # at most a tiny fraction should fall through to "Outro"
    assert (eras == "Outro").mean() < 0.05


def test_plot_helpers_render_without_error():
    import matplotlib
    matplotlib.use("Agg")

    ax = geomoz.plot_provinces(show=False)
    assert ax is not None

    from geomoz.plot_utils import quick_map
    ax2 = quick_map(geomoz.read_province(), column="Provincia", show=False)
    assert ax2 is not None
