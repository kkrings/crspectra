"""Database of published cosmic-ray energy spectra

The database contains published cosmic-ray energy spectra from various
experiments, e.g. CREAM, IceTop or the Pierre Auger Observatory.

Examples
--------
Connect to the cosmic-ray energy spectra database.

>>> import crspectra
>>> with crspectra.connect() as database:
...     for experiment in database:
...         spectrum = database[experiment]

Request data from external database.

>>> import crspectra
>>> spectrum = crspectra.from_external("AMS-02")


"""

import logging

from crspectra.connect import connect  # noqa: F401
from crspectra.crspectra import CRSpectra  # noqa: F401
from crspectra.external import from_external  # noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
