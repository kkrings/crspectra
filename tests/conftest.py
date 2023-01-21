import pathlib
import sqlite3
import typing

import numpy
import pytest
import pytest_mock


@pytest.fixture(scope="session")
def experiment() -> str:
    return "some experiment"


@pytest.fixture(scope="session")
def spectrum() -> numpy.ndarray:
    values = [
        (1e3, 1e-3, (0.5e-4, 0.5e-4), (0.25e-4, 0.25e-4), False),
        (1e4, 1e-4, (0.5e-5, 0.5e-5), (0.25e-5, 0.25e-5), False),
        (1e5, 1e-5, (0.5e-6, 0.5e-6), (0.25e-6, 0.25e-6), False),
    ]

    dtype = [
        ("energy", float),
        ("flux", float),
        ("stat", float, (2,)),
        ("sys", float, (2,)),
        ("uplim", bool),
    ]

    return numpy.array(values, dtype=dtype)


@pytest.fixture(scope="session")
def database(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("database") / "crspectra.db"


@pytest.fixture(scope="session")
def connection(database: pathlib.Path) -> typing.Iterator[sqlite3.Connection]:
    with sqlite3.connect(database) as connection:
        yield connection


@pytest.fixture(scope="session")
def insert_experiment(
    connection: sqlite3.Connection, experiment: str, spectrum: numpy.ndarray
) -> None:
    columns = [
        "energy",
        "flux",
        "stat_low",
        "stat_up",
        "sys_low",
        "sys_up",
        "is_uplim",
    ]

    connection.execute(f"CREATE TABLE '{experiment}'({', '.join(columns)})")

    values = (
        (
            float(row["energy"]),
            float(row["flux"]),
            float(row["stat"][0]),
            float(row["stat"][1]),
            float(row["sys"][0]),
            float(row["sys"][1]),
            int(row["uplim"]),
        )
        for row in spectrum
    )

    connection.executemany(
        f"INSERT INTO '{experiment}' VALUES(?, ?, ?, ?, ?, ?, ?)", values
    )

    connection.commit()


@pytest.fixture
def mock_pkg_resources_resource_filename(
    mocker: pytest_mock.MockerFixture, database: pathlib.Path
) -> None:
    resource_filename = mocker.patch("pkg_resources.resource_filename")
    resource_filename.return_value = str(database)
