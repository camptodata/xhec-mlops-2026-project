"""Helpers for the web service."""

import pickle
from pathlib import Path
from typing import Any


def load_object(path: Path) -> Any:  # noqa: ANN401
    """Load an object from a pickle file.

    Args:
        path: Pickle file to read.

    Returns:
        The unpickled object.
    """
    with Path(path).open("rb") as file:
        return pickle.load(file)
