Cosmic-ray energy spectra
=========================

This Python package provides a database of published cosmic-ray energy spectra,
measured by surface detectors like *IceTop* or the *Pierre Auger Observatory*;
see references_. Moreover, it gives access to an `external database`_, which
includes electrons, positrons, anti-protons, and nuclide up to ``Z = 30`` for
energies below the cosmic-ray *knee*.

   I have created this database in mid of 2017 when I started writing on my PhD
   thesis. In case you find a publication with newer data, feel free to request
   its addition.

Installation
------------

The easiest way to install this project is by using `pip`:

::

   pip install 'https://github.com/kkrings/crspectra#egg=crspectra'


Getting started
---------------

A measured cosmic-ray energy spectrum can be requested via:

::

   import crspectra
   database = crspectra.CRSpectra()
   spectrum = database.request("Auger")


A structured *NumPy* array is returned containing the requested cosmic-ray
data. The fields are ``energy``, ``flux``, statistical ``stat`` and
systematical ``sys`` uncertainty on the flux, and uncertainty is upper a limit
``uplim``. The energy is given in ``GeV`` and the flux is given in ``GeV^-1
m^-2 s^-1 sr^-1``. The uncertainties describe the lower and upper uncertainty
relative to the flux.

The list of available experiments is obtained via:

::

   experiments = database.experiments


Data from the `external database`_ can be requested via:

::

   spectrum = database.from_external("AMS-02")


The following plot was created using this package; see the `example`_ *Jupyter*
notebook:

.. figure:: example/crspectra.png

   Cosmic-ray proton and all-particle energy spectra. Only statistical
   uncertainties are shown.


.. _references:

References
----------

Please cite the following papers when using this database:

   Auger
      The Pierre Auger Collaboration, Proceedings of the 35th International
      Cosmic Ray Conference, Vol. ICRC2017, Proceedings of Science, 2017,
      p. 486

   CREAM-I/III
      Yoon et al., The Astrophysical Journal 839.1 (2017), p. 5

   GAMMA
      Ter-Antonyan, Physical Review D89.12 (2014), p. 123003

   HAWC
      Alfaro et al., Physical Review D96.12 (2017), p. 12201

   HiRes/MIA
      Abu-Zayyad et al., The Astrophysical Journal 557 (2001), pp. 686-699

   HiRes-I and HiRes-II
      Abbasi et al., Physical Review Letters 100 (2008), p. 101101

   IceTop-73
      Aartsen et al., Physical Review D88.4 (2013), p. 042004

   KASCADE
      Antoni et al., Astroparticle Physics 24 (2005), pp. 1-25

   KASCADE-Grande
      Apel et al., The Astrophysical Journal 36 (2012), pp. 183-194

   Tibet-III
      Amenomori et al., The Astrophysical Journal 678 (2008), pp. 1165-1179


.. Links
.. _external database:
   http://lpsc.in2p3.fr/crdb/
.. _example:
   ./example/crspectra.ipynb
