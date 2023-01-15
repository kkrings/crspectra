import numpy
import pytest

import crspectra


@pytest.mark.usefixtures("insert_experiment", "mock_pkg_resources_resource_filename")
def test_getitem(experiment: str, spectrum: numpy.ndarray) -> None:
    reference = spectrum

    with crspectra.connect() as database:
        spectrum = database[experiment]

    assert numpy.all(spectrum == reference)
