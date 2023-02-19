import pathlib
import typing
import unittest.mock

import numpy
import pytest

import crspectra


@pytest.mark.usefixtures("insert_experiment")
class TestCRSpectra:
    def test_getitem(self, getitem: numpy.ndarray, spectrum: numpy.ndarray) -> None:
        assert numpy.all(getitem == spectrum)

    def test_getitem_key_error(self, spectra: crspectra.CRSpectra) -> None:
        with pytest.raises(KeyError):
            spectra["not_existing_experiment"]

    def test_iter(self, spectra: crspectra.CRSpectra, experiment: str) -> None:
        assert list(spectra.keys()) == [experiment]

    def test_len(self, spectra: crspectra.CRSpectra) -> None:
        assert len(spectra) == 1

    @pytest.fixture
    def spectra(
        self, mock_importlib_resources_path: unittest.mock.MagicMock
    ) -> typing.Iterator[crspectra.CRSpectra]:
        with crspectra.connect() as database:
            mock_importlib_resources_path.assert_called_once_with(
                "crspectra", pathlib.Path("data", "crspectra.db")
            )

            yield database

    @pytest.fixture
    def getitem(self, spectra: crspectra.CRSpectra, experiment: str) -> numpy.ndarray:
        return spectra[experiment]
