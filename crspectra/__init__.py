import logging

from crspectra.connect import connect  # noqa: F401
from crspectra.crspectra import CRSpectra  # noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
