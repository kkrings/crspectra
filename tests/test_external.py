import unittest.mock

import numpy

import crspectra


def test_from_external(
    mock_requests_get: unittest.mock.MagicMock,
    experiment: str,
    spectrum: numpy.ndarray,
) -> None:
    assert numpy.all(crspectra.from_external(experiment) == spectrum)

    mock_requests_get.assert_called_once_with(
        "http://lpsc.in2p3.fr/crdb/rest.php",
        params={
            "num": "C",
            "energy_type": "EKN",
            "experiment": experiment,
        },
    )
