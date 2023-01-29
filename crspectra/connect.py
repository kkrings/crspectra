"""Cosmic-ray energy spectra database context manager

"""

import contextlib
import logging
import os
import sqlite3
import typing

import pkg_resources

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
    database = pkg_resources.resource_filename(
        "crspectra", os.path.join("data", "crspectra.db")
    )

    log = logging.getLogger("crspectra.connect")
    log.debug(f"Database: {database}")

    with sqlite3.connect(database) as connection:
        yield CRSpectra(connection)
