#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools


with open("README.rst") as readme:
    long_description = readme.read()

setuptools.setup(
    name="crspectra",
    version="0.1",
    author="Kai Krings",
    author_email="kai.krings@posteo.de",
    description="Database of published cosmic-ray energy spectra",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/kkrings/crspectra",
    license="GPLv3",
    packages=setuptools.find_packages(),
    install_requires=[
        "numpy",
        "requests"
        ],
    package_data={"crspectra": ["data/crspectra.db"]})
