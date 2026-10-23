"""Helper to save Python objects with pickle."""

import pickle
from pathlib import Path
from typing import Any

from prefect import task


@task(name="Save pickle")
def pickle_object(obj: Any, path: Path) -> None:  # noqa: ANN401
    """Save an object to a pickle file.

    Args:
        obj: Object to save (model, encoder, ...).
        path: Destination file.
    """
    with Path(path).open("wb") as file:
        pickle.dump(obj, file)


@task(name="Load pickle")
def load_pickle(path: Path) -> Any:  # noqa: ANN401
    """Load an object from a pickle file.

    Args:
        path: Pickle file to read.

    Returns:
        The unpickled object.
    """
    with Path(path).open("rb") as file:
        return pickle.load(file)
