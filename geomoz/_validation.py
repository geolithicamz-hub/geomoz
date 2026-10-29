"""Validate whether requested dataset variants are actually available."""


def validate_dataset_options(year: int, simplified: bool, available_year: int) -> None:
    """Reject silently ignored year/resolution arguments."""
    if year != available_year:
        raise ValueError(
            f"Dataset for year {year} is unavailable; "
            f"the only supported edition is {available_year}."
        )
    if not isinstance(simplified, bool):
        raise TypeError("simplified must be a boolean")
    if not simplified:
        raise ValueError(
            "simplified=False is not available: there is no separate "
            "full-resolution file for this dataset."
        )
