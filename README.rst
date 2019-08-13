Cosmic-ray energy spectra
=========================

This Python package provides a database of published cosmic-ray energy spectra,
measured by surface detectors *IceTop* or the *Pierre Auger Observatory*.

Getting started
---------------

A measured cosmic-ray energy spectrum can be requested via:

.. code-block::

   import crspectra
   database = crspectra.CRSpectra()
   spectrum = database.request("GAMMA")


A structured *NumPy* array is returned containing the requested cosmic-ray
data. The fields are ``energy``, ``flux``, statistical ``stat`` and
systematical ``sys`` uncertainty on the flux, and uncertainty is upper a
limit ``uplim``.

The following plot was created via this package:

.. figure:: example/crspectra.png

   Cosmic-ray proton and all-particle energy spectra. Only statistical
   uncertainties are shown.
