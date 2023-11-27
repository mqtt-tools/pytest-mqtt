from pytest_mqtt.capmqtt import MqttClientAdapter
from pytest_mqtt.util import delay


def test_mqtt_client_adapter(mosquitto):
    host, port = mosquitto
    mqtt_client = MqttClientAdapter(host=host, port=port)
    mqtt_client.start()

    assert mqtt_client.client._host == host
    assert mqtt_client.client._port == int(port)

    # Submit MQTT message.
    message_info = mqtt_client.publish("foo", "bar")
    message_info.wait_for_publish(timeout=0.5)
    assert message_info.is_published() is True

    delay()  # Only needed to let the coverage tracker fulfil its job.
    mqtt_client.stop()
