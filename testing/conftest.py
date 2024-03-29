import pytest

from pytest_mqtt.model import MqttSettings


def pytest_addoption(parser) -> None:
    parser.addoption("--mqtt-host", action="store", type=str, default="localhost", help="MQTT host name")
    parser.addoption("--mqtt-port", action="store", type=int, default=1883, help="MQTT port number")


@pytest.fixture(scope="session")
def mqtt_settings(pytestconfig) -> MqttSettings:
    return MqttSettings(
        host=pytestconfig.getoption("--mqtt-host"),
        port=pytestconfig.getoption("--mqtt-port"),
    )
