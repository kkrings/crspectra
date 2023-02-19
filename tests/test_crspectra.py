import pathlib
import typing
import unittest.mock

import numpy
import numpy.typing
import pytest

from crspectra.connect import connect
from crspectra.crspectra import CRSpectra


@pytest.mark.usefixtures("insert_experiment")
class TestCRSpectra:
    def test_getitem(
        self,
        getitem: numpy.typing.NDArray[typing.Any],
        spectrum: numpy.typing.NDArray[typing.Any],
    ) -> None:
        assert numpy.all(getitem == spectrum)

    def test_getitem_key_error(self, spectra: CRSpectra) -> None:
        with pytest.raises(KeyError):
            spectra["not_existing_experiment"]

    def test_iter(self, spectra: CRSpectra, experiment: str) -> None:
        assert list(spectra.keys()) == [experiment]

    def test_len(self, spectra: CRSpectra) -> None:
        assert len(spectra) == 1

    @pytest.fixture
    def spectra(
        self, mock_importlib_resources_path: unittest.mock.MagicMock
    ) -> typing.Iterator[CRSpectra]:
        with connect() as database:
            mock_importlib_resources_path.assert_called_once_with(
                "crspectra", pathlib.Path("data", "crspectra.db")
            )

            yield database

    @pytest.fixture
    def getitem(
        self, spectra: CRSpectra, experiment: str
    ) -> numpy.typing.NDArray[typing.Any]:
        return spectra[experiment]
