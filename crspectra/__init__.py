import logging

from ._crspectra import CRSpectra


logging.getLogger(__name__).addHandler(logging.NullHandler())
del logging
