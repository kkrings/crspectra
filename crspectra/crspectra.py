"""Cosmic-ray energy spectra database

"""

import sqlite3
import typing

import numpy


class CRSpectra(typing.Mapping[str, numpy.ndarray]):
    """Cosmic-ray energy spectra database

    Parameters
    ----------
    connection : Connection
        Connection to cosmic-ray energy spectra database

    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def __getitem__(self, experiment: str) -> numpy.ndarray:
        """Request cosmic-ray energy spectrum.

        Parameters
        ----------
        experiment : str
            Experiment

        Returns
        -------
        ndarray
            Structured array containing the requested cosmic-ray data.
            The fields are ``energy``, ``flux``, statistical ``stat``
            and systematical ``sys`` uncertainty on the flux, and
            uncertainty is upper a limit ``uplim``. The energy is given
            in GeV and the flux is given in GeV^-1 m^-2 s^-1 sr^-1. The
            uncertainties describe the lower and upper uncertainty
            relative to the flux.

        Note
        ----
        If ``CREAM-I/III (helium)`` data is requested, the returned
        energy unit is GeV per nucleon.

        """
        try:
            table = self._connection.execute(f"SELECT * from '{experiment}'")
        except sqlite3.OperationalError:
            raise KeyError(f"Experiment '{experiment}' not found")

        values = [
            (row[0], row[1], (row[2], row[3]), (row[4], row[5]), bool(row[6]))
            for row in table
        ]

        dtype = [
            ("energy", float),
            ("flux", float),
            ("stat", float, (2,)),
            ("sys", float, (2,)),
            ("uplim", bool),
        ]

        return numpy.array(values, dtype=dtype)

    def __iter__(self) -> typing.Iterator[str]:
        """iterator(str): Available cosmic-ray energy spectra"""
        experiments = self._connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )

        return (name for name, in experiments)

    def __len__(self) -> int:
        """int: Number of available cosmic-ray energy spectra"""
        size = self._connection.execute(
            "SELECT count() FROM sqlite_master WHERE type = 'table'"
        )

        return size.fetchone()[0]
