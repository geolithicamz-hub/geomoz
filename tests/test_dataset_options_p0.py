"""Offline validation of dataset options against fixed published editions."""
import pytest
from geomoz._validation import validate_dataset_options


@pytest.mark.parametrize("year", [2016, 2018, 2024])
def test_unavailable_years_fail(year):
    with pytest.raises(ValueError, match="only supported edition"):
        validate_dataset_options(year, True, available_year=2017)


def test_full_resolution_unavailable():
    with pytest.raises(ValueError, match="simplified=False"):
        validate_dataset_options(2017, False, available_year=2017)


def test_available_options():
    validate_dataset_options(2017, True, 2017)
    validate_dataset_options(2006, True, 2006)
