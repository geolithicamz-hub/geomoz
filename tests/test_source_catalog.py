"""Offline metadata-registry tests; do not contact upstream servers."""
import pytest
from geomoz.source_catalog import get_source_dataset, list_source_datasets


def test_sources_are_unique_and_metadata_only():
    records = list_source_datasets()
    assert len(records) == 10
    assert len({r["id"] for r in records}) == len(records)
    assert all(r["url"].startswith("https://") for r in records)
    assert all(r["access"] == "reference_only" for r in records)
    assert all(r["redistribution"] == "permission_unverified" for r in records)


def test_mireme_crs_and_schema_provenance():
    source = get_source_dataset("mireme_geology_250k")
    assert source["crs"] == "EPSG:4130"
    assert source["producer"] == "MIREME/MIS"
    assert "code2006" in source["note"]


def test_filters_return_defensive_copies():
    results = list_source_datasets(category="soils")
    assert len(results) == 1
    results[0]["title"] = "changed"
    assert get_source_dataset("data4moz_soils_1995")["title"] == "Tipos de Solo"
    assert len(list_source_datasets(distributor="MIREME/MIS")) == 3
    assert list_source_datasets(category="other") == []


def test_invalid_lookups():
    with pytest.raises(KeyError):
        get_source_dataset("not-present")
    with pytest.raises(TypeError):
        get_source_dataset(None)
    with pytest.raises(ValueError):
        list_source_datasets(category="")
