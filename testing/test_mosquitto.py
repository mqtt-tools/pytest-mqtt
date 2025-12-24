import pytest

from pytest_mqtt.util import delay
from testing.util import DummyServer


@pytest.fixture(scope="session")
def no_mqtt_broker(request):
    server = DummyServer("localhost", 1883)
    server.start()
    delay()
    request.addfinalizer(server.shutdown)
    return server


@pytest.fixture(scope="session")
def mosquitto_mqtt_broker(mosquitto):
    return mosquitto


@pytest.mark.run(order=-1)
def test_mosquitto_running(no_mqtt_broker, mosquitto_mqtt_broker):
    assert mosquitto_mqtt_broker == ("127.0.0.1", "1883")
    no_mqtt_broker.shutdown()
