"""Cosmic-ray energy spectra database context manager

"""

import contextlib
import importlib.resources
import logging
import pathlib
import sqlite3
import typing

from crspectra.crspectra import CRSpectra


@contextlib.contextmanager
def connect() -> typing.Iterator[CRSpectra]:
    """Connect to cosmic-ray energy spectra database

    Yields
    ------
    CRSpectra
        Instance of `CRSpectra` connected to the given database of
        cosmic-ray energy spectra

    """
    path_to_database = pathlib.Path("data", "crspectra.db")

    with importlib.resources.path("crspectra", path_to_database) as database:
        log = logging.getLogger("crspectra.connect")
        log.debug(f"Database: {database}")

        with sqlite3.connect(database) as connection:
            yield CRSpectra(connection)
