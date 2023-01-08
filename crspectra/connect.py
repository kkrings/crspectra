"""Cosmic-ray energy spectra database context manager

"""

import contextlib
import logging
import pathlib
import sqlite3
import typing

import pkg_resources

from crspectra._crspectra import CRSpectra


@contextlib.contextmanager
def connect(filepath: str | None = None) -> typing.Iterator[CRSpectra]:
    """Connect to cosmic-ray energy spectra database

    filepath : str, optional
        Path to SQLite database of cosmic-ray energy spectra;
        if `None`, the internal database is used.

    Yields
    ------
    CRSpectra
        Instance of `CRSpectra` connected to the given database of
        cosmic-ray energy spectra

    Note
    ----
    A `filepath` of other than `None` is mostly intended for unit
    testing.

    """
    database: str
    if filepath is None:
        database = pkg_resources.resource_filename(
            "crspectra", resource_name=str(pathlib.Path("data", "crspectra.db"))
        )
    else:
        database = filepath

    log = logging.getLogger("crspectra.connect")
    log.debug(f"Database: {database}")

    with sqlite3.connect(database) as connection:
        yield CRSpectra(connection)
