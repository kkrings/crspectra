import logging

from crspectra._crspectra import CRSpectra  # noqa: F401

logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
