"""Cosmic-ray energy spectra database

"""

import collections.abc
import io
import logging
import sqlite3
import typing

import numpy
import requests


class CRSpectra(collections.abc.Mapping[str, numpy.ndarray]):
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
        table = self._connection.execute(f"SELECT * from '{experiment}'")

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
        return len(tuple(iter(self)))

    @staticmethod
    def from_external(experiment: str, element="C", energy="EKN") -> numpy.ndarray:
        """Request cosmic-ray energy spectrum from external database.

        The database's address is http://lpsc.in2p3.fr/crdb.
        It includes electrons, positrons, anti-protons, and nuclides up
        to Z = 30 for energies below the knee.

        Parameters
        ----------
        experiment : str
            Experiment
        element : str, optional
            Element or isotope
        energy : {"EKN", "EK", "R", "ETOT"}, optional
            Energy axis: kinetic energy per nucleon, total kinetic
            energy, rigidity, or total energy

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
        If ``EKN`` is requested, the returned energy unit is GeV per
        nucleon. If ``R`` is requested, the returned 'energy unit' is GV
        per nucleon.

        """
        params = {
            "num": element,
            "energy_type": energy,
            "experiment": experiment,
        }

        response = requests.get("http://lpsc.in2p3.fr/crdb/rest.php", params=params)

        log = logging.getLogger("crspectra.CRSpectra.from_external")
        log.debug(f"Request: {response.url}")

        response.raise_for_status()

        log.debug(f"Content:\n{response.text}")

        dtype = [
            ("energy", float),
            ("flux", float),
            ("stat", float, (2,)),
            ("sys", float, (2,)),
            ("uplim", bool),
        ]

        def fabs(s: str) -> float:
            return numpy.fabs(float(s))

        converters: dict[str | int, typing.Callable[[str], float]] = {7: fabs, 9: fabs}

        response_text = "\n".join(response.text.split("\n")[1:-1])

        result = numpy.loadtxt(
            io.StringIO(response_text),
            dtype,
            converters=converters,
            usecols=(3, 6, 7, 8, 9, 10, 15),
        )

        return result
