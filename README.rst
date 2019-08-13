Cosmic-ray energy spectra
=========================

This Python package provides a database of published cosmic-ray energy spectra,
measured by surface detectors *IceTop* or the *Pierre Auger Observatory*.

A measured cosmic-ray energy spectrum can be requested via:

::

   import crspectra
   database = crspectra.CRSpectra()
   spectrum = database.request("GAMMA")


The following plot was created via this package:

.. figure:: example/crspectra.png

   Cosmic-ray proton and all-particle energy spectra. Only statistical
   uncertainties are shown.
