import contextlib
import dataclasses
import pathlib
import sqlite3
import typing
import unittest.mock

import numpy
import numpy.typing
import pytest
import pytest_mock


@pytest.fixture(scope="session")
def experiment() -> str:
    return "some experiment"


@pytest.fixture(scope="session")
def spectrum() -> numpy.typing.NDArray[typing.Any]:
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
    connection: sqlite3.Connection,
    experiment: str,
    spectrum: numpy.typing.NDArray[typing.Any],
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


@contextlib.contextmanager
def as_database_context(database: pathlib.Path) -> typing.Iterator[pathlib.Path]:
    yield database


@pytest.fixture
def mock_importlib_resources_path(
    mocker: pytest_mock.MockerFixture, database: pathlib.Path
) -> unittest.mock.MagicMock:
    path_mock = mocker.patch("importlib.resources.path")
    path_mock.return_value = as_database_context(database)

    return path_mock


@dataclasses.dataclass(frozen=True)
class FakeResponse:
    text: str
    url = ""

    def raise_for_status(self) -> None:
        ...


@pytest.fixture(scope="session")
def response(spectrum: numpy.typing.NDArray[typing.Any]) -> FakeResponse:
    def line(row: numpy.typing.NDArray[typing.Any]) -> str:
        values = ["0.0"] * 16
        values[3] = f"{row['energy']:e}"
        values[6] = f"{row['flux']:e}"
        values[7] = f"-{row['stat'][0]:e}"
        values[8] = f"{row['stat'][1]:e}"
        values[9] = f"-{row['sys'][0]:e}"
        values[10] = f"{row['sys'][1]:e}"
        values[15] = f"{int(row['uplim']):.0f}"

        return " ".join(values)

    text = "\n".join(line(row) for row in spectrum)

    return FakeResponse(text=f"<html><body><p>\n{text}\n</p></body></html>")


@pytest.fixture
def mock_requests_get(
    mocker: pytest_mock.MockerFixture, response: FakeResponse
) -> unittest.mock.MagicMock:
    get_mock = mocker.patch("requests.get")
    get_mock.return_value = response

    return get_mock
