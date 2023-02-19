import typing
import unittest.mock

import numpy
import numpy.typing

from crspectra.external import from_external


def test_from_external(
    mock_requests_get: unittest.mock.MagicMock,
    experiment: str,
    spectrum: numpy.typing.NDArray[typing.Any],
) -> None:
    assert numpy.all(from_external(experiment) == spectrum)

    mock_requests_get.assert_called_once_with(
        "http://lpsc.in2p3.fr/crdb/rest.php",
        params={
            "num": "C",
            "energy_type": "EKN",
            "experiment": experiment,
        },
    )
