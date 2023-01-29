"""External cosmic-ray energy spectra data

"""

import io
import logging
import typing

import numpy
import requests


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

    log = logging.getLogger("crspectra.from_external")
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

    converters: typing.Dict[typing.Union[str, int], typing.Callable[[str], float]] = {
        7: fabs,
        9: fabs,
    }

    response_text = "\n".join(response.text.split("\n")[1:-1])

    result = numpy.loadtxt(
        io.StringIO(response_text),
        dtype,
        converters=converters,
        usecols=(3, 6, 7, 8, 9, 10, 15),
    )

    return result
