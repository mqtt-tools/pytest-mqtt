import pytest

from pytest_mqtt.util import delay
from testing.util import DummyServer


@pytest.fixture(scope="session")
@pytest.mark.early
def no_mqtt_broker(request):
    server = DummyServer("localhost", 1883)
    server.start()
    delay()
    request.addfinalizer(server.shutdown)
    return server


@pytest.fixture(scope="session")
@pytest.mark.late
def mosquitto_mqtt_broker(mosquitto):
    return mosquitto


@pytest.mark.skip(reason="Unable to run together with other test cases")
@pytest.mark.run(order=1)
def test_mosquitto_running(no_mqtt_broker, mosquitto_mqtt_broker):
    assert mosquitto_mqtt_broker == ("localhost", 1883)
    # no_mqtt_broker.shutdown()
