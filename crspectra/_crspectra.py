"""Published cosmic-ray energy spectra

"""
import io
import logging
import os
import sqlite3

import numpy
import pkg_resources
import requests


class CRSpectra:
    """Cosmic-ray spectra database

    The database contains published cosmic-ray energy spectra from
    various experiments, e.g. CREAM, IceTop or the Pierre Auger
    Observatory.

    """
    def __init__(self):
        filename = pkg_resources.resource_filename(
            "crspectra", os.path.join("data", "crspectra.db"))

        self._database = sqlite3.connect(filename)

    def __del__(self):
        # Close connection to database.
        self._database.close()

    def request(self, experiment):
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
        table = self._database.execute("SELECT * from '{}'".format(experiment))

        values = [
            (row[0], row[1], (row[2], row[3]), (row[4], row[5]), bool(row[6]))
            for row in table
            ]

        dtype = [
            ("energy", numpy.float64),
            ("flux", numpy.float64),
            ("stat", numpy.float64, (2, )),
            ("sys", numpy.float64, (2, )),
            ("uplim", numpy.bool)
            ]

        return numpy.array(values, dtype=dtype)

    @property
    def experiments(self):
        """list(str): Available data
        """
        experiments = self._database.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'")

        return [name for name, in experiments]

    @staticmethod
    def from_external(experiment, element="C", energy="EKN"):
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

        request = requests.get(
            "https://lpsc.in2p3.fr/crdb/_dialog_result.php",
            params=params)

        log = logging.getLogger("crspectra.CRSpectra.from_external")
        log.debug("Request: %s", request.url)

        request.raise_for_status()

        log.debug("Content:\n%s", request.text)

        dtype = [
            ("energy", numpy.float64),
            ("flux", numpy.float64),
            ("stat", numpy.float64, (2, )),
            ("sys", numpy.float64, (2, )),
            ("uplim", numpy.bool)
            ]

        def fabs(s):
            return numpy.fabs(float(s))

        converters = {7: fabs, 9: fabs}

        reqtext = "#" + request.text
        reqtext = reqtext[:reqtext.rindex("\n")+1] + "#" + reqtext[reqtext.rindex("\n")+1:]

        result = numpy.loadtxt(
            io.StringIO(reqtext), dtype, converters=converters,
            usecols=(3, 6, 7, 8, 9, 10, 15))

        return result
