import typing as t

import pytest


@pytest.fixture(scope="session")
def mqttcliargs(request) -> t.Tuple[str, int]:
    host = request.config.getoption("--mqtt_host", "localhost")
    port = int(request.config.getoption("--mqtt_port", 1883))
    yield host, port
